import { spawn } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { fileURLToPath } from "node:url";
import { Type } from "@sinclair/typebox";
import { getAgentDir, parseFrontmatter } from "@earendil-works/pi-coding-agent";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

type Agent = { name: string; description: string; prompt: string; model?: string; thinking?: string };
type Result = {
    agent: string; model: string | null; text: string; stopReason: string | null;
    errorMessage: string | null; exitCode: number; stderr: string;
    usage: { input: number; output: number; turns: number };
};

const DESCRIPTION = "Spawn a role-shaped child pi process for one focused task. Roles are markdown files; only the child's final reply returns. Call this tool multiple times in one turn for parallel work.";
const stringValue = (value: unknown) => typeof value === "string" && value.trim() ? value.trim() : undefined;

function loadAgents(dir: string): Agent[] {
    try {
        return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
            if (!entry.name.endsWith(".md") || (!entry.isFile() && !entry.isSymbolicLink())) return [];
            try {
                const file = path.join(dir, entry.name);
                const parsed = parseFrontmatter<Record<string, unknown>>(fs.readFileSync(file, "utf8"));
                const name = stringValue(parsed.frontmatter.name);
                const description = stringValue(parsed.frontmatter.description);
                return name && description ? [{ name, description, prompt: parsed.body.trim(), model: stringValue(parsed.frontmatter.model), thinking: stringValue(parsed.frontmatter.thinking) }] : [];
            } catch { return []; }
        });
    } catch { return []; }
}

function discoverAgents(cwd: string): Agent[] {
    const agents = new Map<string, Agent>();
    for (const agent of loadAgents(path.join(getAgentDir(), "agents"))) agents.set(agent.name, agent);
    for (;;) {
        const dir = path.join(cwd, ".pi", "agents");
        try {
            if (fs.statSync(dir).isDirectory()) {
                for (const agent of loadAgents(dir)) agents.set(agent.name, agent);
                break;
            }
        } catch {}
        const parent = path.dirname(cwd);
        if (parent === cwd) break;
        cwd = parent;
    }
    return [...agents.values()].sort((a, b) => a.name.localeCompare(b.name));
}

function readSettings() {
    try {
        const block = JSON.parse(fs.readFileSync(path.join(getAgentDir(), "settings.json"), "utf8"))["pi-subagent"];
        return {
            model: typeof block?.model === "string" ? block.model : null,
            extensions: Array.isArray(block?.extensions)
                ? block.extensions.filter((value: unknown): value is string => typeof value === "string").map((value) => value.startsWith("~/") || value === "~" ? path.join(os.homedir(), value.slice(1)) : value)
                : [],
        };
    } catch { return { model: null, extensions: [] }; }
}

function parseLine(line: string, result: Result) {
    if (!line.trim()) return;
    try {
        const { type, message } = JSON.parse(line);
        if (type !== "message_end" || message?.role !== "assistant") return;
        const text = typeof message.content === "string" ? message.content : Array.isArray(message.content)
            ? message.content.filter((part: any) => part?.type === "text" && typeof part.text === "string").map((part: any) => part.text).join("\n").trim()
            : "";
            if (text) result.text = text;
            if (message.stopReason) result.stopReason = message.stopReason;
            if (message.errorMessage) result.errorMessage = message.errorMessage;
            if (message.usage) {
                if (typeof message.usage.input === "number") result.usage.input += message.usage.input;
                if (typeof message.usage.output === "number") result.usage.output += message.usage.output;
                result.usage.turns++;
            }
    } catch {}
}

function piCommand() {
    if (!/[\\/]node(?:\.exe)?$/i.test(process.execPath)) {
        return { command: path.basename(process.execPath).replace(/\.exe$/i, "") === "pi" ? process.execPath : "pi", prefix: [] as string[] };
    }
    const prefix = process.execArgv.filter((arg) => arg.startsWith("--experimental-"));
    const node = (script: string) => ({ command: process.execPath, prefix: [...prefix, script] });
    let entry = process.argv[1];
    try { if (entry) entry = fs.realpathSync(entry); } catch {}
    if (entry && /[\\/]@earendil-works[\\/]pi-coding-agent[\\/]/i.test(entry)) return node(entry);
    try {
        const resolved = fileURLToPath(import.meta.resolve("@earendil-works/pi-coding-agent"));
        const cli = path.join(path.dirname(resolved), "cli.js");
        if (fs.existsSync(cli)) return node(cli);
    } catch {}
    return { command: "pi", prefix: [] as string[] };
}

async function runAgent(cwd: string, agent: Agent, task: string, signal?: AbortSignal): Promise<Result> {
    const config = readSettings();
    const result: Result = {
        agent: agent.name, model: agent.model ?? config.model, text: "", stopReason: null,
        errorMessage: null, exitCode: -1, stderr: "", usage: { input: 0, output: 0, turns: 0 },
    };
    const temp = agent.prompt ? fs.mkdtempSync(path.join(os.tmpdir(), "pi-subagent-")) : null;
    try {
        const prompt = temp && path.join(temp, "system-prompt.md");
        if (prompt) fs.writeFileSync(prompt, agent.prompt, { mode: 0o600 });
        const args = ["--mode", "json", "-p", "--no-session", "--no-extensions"];
        for (const extension of config.extensions) args.push("--extension", extension);
        if (agent.model ?? config.model) args.push("--model", agent.model ?? config.model!);
        if (agent.thinking) args.push("--thinking", agent.thinking);
        if (prompt) args.push("--append-system-prompt", prompt);
        args.push(task);
        const launcher = piCommand();
        result.exitCode = await new Promise<number>((resolve) => {
            const child = spawn(launcher.command, [...launcher.prefix, ...args], { cwd, shell: false, stdio: ["pipe", "pipe", "pipe"] });
            child.stdin.on("error", () => {});
            child.stdin.end();
            let buffer = "";
            let settled = false;
            let abort: (() => void) | undefined;
            const finish = (code: number) => {
                if (settled) return;
                settled = true;
                if (abort && signal) signal.removeEventListener("abort", abort);
                resolve(code);
            };
            child.stdout.on("data", (chunk: Buffer) => {
                const lines = (buffer += chunk.toString()).split(/\r?\n/);
                buffer = lines.pop() ?? "";
                for (const line of lines) parseLine(line, result);
            });
            child.stderr.on("data", (chunk: Buffer) => { result.stderr += chunk.toString(); });
            child.on("close", (code) => { if (buffer.trim()) parseLine(buffer, result); finish(code ?? 0); });
            child.on("error", (error) => { if (!result.stderr) result.stderr = error.message; finish(1); });
            if (signal) {
                abort = () => child.kill("SIGTERM");
                if (signal.aborted) abort();
                else signal.addEventListener("abort", abort, { once: true });
            }
        });
        return result;
    } finally {
        try { if (temp) fs.rmSync(temp, { recursive: true, force: true }); } catch {}
    }
}

function resultFor(agent: string, result: Result) {
    if (result.exitCode !== 0 && !result.text) return {
        content: [{ type: "text" as const, text: `Subagent "${agent}" failed (exit ${result.exitCode}).${result.errorMessage ? `\n\n${result.errorMessage}` : ""}${result.stderr ? `\n\nstderr:\n${result.stderr.trim().slice(-2000)}` : ""}` }],
        details: { result }, isError: true,
    };
    if (!result.text && (result.errorMessage || result.stopReason === "error")) return {
        content: [{ type: "text" as const, text: `Subagent "${agent}" produced no output: ${result.errorMessage ?? "provider reported an error"}${result.model ? ` (model: ${result.model})` : ""}` }],
        details: { result }, isError: true,
    };
    return { content: [{ type: "text" as const, text: result.text || "(empty response)" }], details: { result } };
}

export default function piSubagent(pi: ExtensionAPI) {
    let registered: string | null = null;
    const register = (agents: Agent[]) => {
        const names = agents.map((agent) => agent.name);
        if (names.join(" ") === registered) return;
        pi.registerTool({
            name: "subagent", label: "Subagent",
            description: DESCRIPTION,
            parameters: Type.Object({
                agent: Type.String({ ...(names.length ? { enum: names } : {}), description: `Role markdown file. Available: ${names.join(", ") || "none"}.` }),
                task: Type.String({ description: "Focused task, expected return shape, and context the role needs." }),
            }),
            async execute(_id, params, signal, _update, ctx) {
                const { agent: name, task } = params as { agent: string; task: string };
                const available = discoverAgents(ctx.cwd);
                const agent = available.find((item) => item.name === name);
                if (!agent) {
                    const text = `Unknown subagent "${name}". Available in ${ctx.cwd}: ${available.map((item) => item.name).join(", ") || "(none)"}.`;
                    return { content: [{ type: "text" as const, text }], details: { result: null, errorMessage: text }, isError: true };
                }
                return resultFor(agent.name, await runAgent(ctx.cwd, agent, task, signal));
            },
        });
        registered = names.join(" ");
    };
    const refresh = (cwd: string) => {
        const agents = discoverAgents(cwd);
        try { register(agents); } catch {}
        return agents;
    };
    register(discoverAgents(process.cwd()));
    pi.on("session_start", (_event, ctx) => { refresh(ctx.cwd); });
    pi.on("before_agent_start", (event) => {
        const agents = refresh(event.systemPromptOptions.cwd);
        return { systemPrompt: `${event.systemPrompt}\n\n## Available subagent roles\nRoles load from ~/.pi/agent/agents/ or the nearest project .pi/agents/. Call subagent multiple times in one turn for parallel work.\n${agents.length ? agents.map((agent) => `- ${agent.name}: ${agent.description}`).join("\n") : "(none discovered)"}` };
    });
}
