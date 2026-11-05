import * as fs from "node:fs";
import * as path from "node:path";
import { Type } from "@sinclair/typebox";
import type { ThinkingLevel } from "@earendil-works/pi-agent-core";
import { createAgentSession, getAgentDir, parseFrontmatter, SessionManager } from "@earendil-works/pi-coding-agent";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

type Agent = { name: string; description: string; prompt: string; model?: string; thinking?: string };

const DESCRIPTION = "Run a role-shaped task in a separate Pi session saved as a child of the calling session. Returns the child session's result.";
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
                const slash = agent.model?.indexOf("/") ?? -1;
                if (agent.model && slash <= 0) throw new Error(`Invalid model: ${agent.model}`);
                const model = agent.model
                    ? ctx.modelRegistry.find(agent.model.slice(0, slash), agent.model.slice(slash + 1))
                    : ctx.model;
                if (agent.model && !model) throw new Error(`Unknown model: ${agent.model}`);
                const parentSession = ctx.sessionManager.getSessionFile();
                const { session } = await createAgentSession({
                    cwd: ctx.cwd,
                    model,
                    ...(agent.thinking ? { thinkingLevel: agent.thinking as ThinkingLevel } : {}),
                    sessionManager: SessionManager.create(ctx.cwd, undefined, parentSession ? { parentSession } : undefined),
                });
                const abort = () => { void session.abort(); };
                signal.addEventListener("abort", abort, { once: true });
                if (signal.aborted) abort();
                try {
                    await session.prompt(`${agent.prompt ? `Role instructions:\n${agent.prompt}\n\n` : ""}Task:\n${task}`);
                    const text = session.getLastAssistantText() || "(no output)";
                    return {
                        content: [{ type: "text" as const, text }],
                        details: { sessionId: session.sessionId, sessionFile: session.sessionFile, parentSession },
                    };
                } finally {
                    signal.removeEventListener("abort", abort);
                    session.dispose();
                }
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
        return { systemPrompt: `${event.systemPrompt}\n\n## Available subagent roles\nRoles load from ~/.pi/agent/agents/ or the nearest project .pi/agents/. Each subagent runs in a separate Pi session linked to the session that called it.\n${agents.length ? agents.map((agent) => `- ${agent.name}: ${agent.description}`).join("\n") : "(none discovered)"}` };
    });
}
