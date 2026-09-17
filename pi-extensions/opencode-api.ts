import { randomBytes } from "node:crypto";
import { AssistantMessageEventStream } from "@earendil-works/pi-ai";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const PROVIDER = "opencode-api";
const BASE_URL = "https://opencode.ai/zen/v1";
const USER_AGENT = process.env.OPENCODE_API_USER_AGENT ?? "opencode/1.18.31";
const FALLBACK_MODELS = [
    "big-pickle",
    "deepseek-v4-flash-free",
    "mimo-v2.5-free",
    "muse-spark-1.3-contributor-free",
    "nemotron-3-ultra-free",
    "nemotron-3.5-lightning-free",
];
const BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
const RESPONSE_MODELS = /^muse-spark/;

function openCodeId(prefix: string) {
    const time = Date.now().toString(16).padStart(12, "0");
    const suffix = Array.from(randomBytes(14), (byte) => BASE62[byte % BASE62.length]).join("");
    return `${prefix}${time}${suffix}`;
}

// Hack: Zen's free tier expects these OpenCode-native identities.
const SESSION_ID = openCodeId("ses_");
const PROJECT_ID = openCodeId("proj_");

function headers(sessionId = SESSION_ID, apiKey = process.env.OPENCODE_API_KEY ?? "public") {
    return {
        "Content-Type": "application/json",
        Accept: "text/event-stream",
        Authorization: `Bearer ${apiKey}`,
        "User-Agent": USER_AGENT,
        "x-opencode-client": "cli",
        "x-opencode-session": sessionId,
        "x-opencode-project": PROJECT_ID,
        "x-opencode-request": openCodeId("msg_"),
    };
}

// Zen requires OpenCode's identity headers, so its native defaults win.
function requestHeaders(options: any, sessionId = SESSION_ID) {
    const result: Record<string, string> = Object.fromEntries(
        Object.entries(options?.headers ?? {}).filter(([, value]) => value != null).map(([key, value]) => [key, String(value)]),
    );
        Object.assign(result, headers(sessionId, options?.apiKey ?? process.env.OPENCODE_API_KEY ?? "public"));
        return result;
}

function modelConfig(id: string) {
    return {
        id,
        name: id,
        reasoning: /deepseek|nemotron|think|reason/i.test(id),
        input: ["text"] as ("text" | "image")[],
        cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
        contextWindow: /nemotron/.test(id) ? 1_000_000 : 131_072,
        maxTokens: 16_384,
        compat: {
            supportsReasoningEffort: false,
            requiresReasoningContentOnAssistantMessages: true,
        },
    };
}

async function discoverModels() {
    const response = await fetch(`${BASE_URL}/models`, {
        headers: headers(),
        signal: AbortSignal.timeout(8_000),
    });
    if (!response.ok) throw new Error(`Zen model discovery failed: HTTP ${response.status}`);

    const data = (await response.json()) as { data?: Array<{ id?: string }> };
    const ids = (data.data ?? [])
    .map((model) => model.id)
    .filter((id): id is string => !!id && (id.endsWith("-free") || id === "big-pickle"));
    return ids.length > 0 ? ids : FALLBACK_MODELS;
}

function textOf(content: unknown) {
    if (typeof content === "string") return content;
    if (!Array.isArray(content)) return "";
    return content
    .filter((part): part is { type: "text"; text?: string } => !!part && typeof part === "object" && part.type === "text")
    .map((part) => part.text ?? "")
    .join("");
}

function normalizeMessages(messages: any[]) {
    return messages.flatMap((message) => {
        if (!message || typeof message !== "object") return [];
        if (message.role === "system" || message.role === "developer") return [{ role: "system", content: textOf(message.content) }];
        if (message.role === "user") {
            if (typeof message.content === "string") return [{ role: "user", content: message.content }];
            const content = (message.content ?? []).flatMap((part: any) => {
                if (part.type === "text") return [{ type: "text", text: part.text }];
                if (part.type === "image") return [{ type: "image_url", image_url: { url: `data:${part.mimeType};base64,${part.data}` } }];
                return [];
            });
            return [{ role: "user", content }];
        }
        if (message.role === "assistant") {
            let content = "";
            let reasoningContent = "";
            const toolCalls: any[] = [];
            for (const part of message.content ?? []) {
                if (part.type === "text") content += part.text;
                if (part.type === "thinking") reasoningContent += part.thinking;
                if (part.type === "toolCall") toolCalls.push({ id: part.id, type: "function", function: { name: part.name, arguments: JSON.stringify(part.arguments ?? {}) } });
            }
            const result: any = { role: "assistant", content: content || null };
            if (reasoningContent || toolCalls.length > 0) result.reasoning_content = reasoningContent;
            if (toolCalls.length > 0) result.tool_calls = toolCalls;
            return [result];
        }
        if (message.role === "toolResult") return [{ role: "tool", tool_call_id: message.toolCallId, content: textOf(message.content) }];
        return [];
    });
}

function normalizeTools(tools: any[]) {
    if (!Array.isArray(tools) || tools.length === 0) return undefined;
    return tools.map((tool) => ({
        type: "function",
        function: { name: tool.name, description: tool.description, parameters: tool.parameters },
    }));
}

function systemPrompt(context: any) {
    const raw = context.systemPrompt;
    return typeof raw === "string"
        ? raw
        : Array.isArray(raw)
            ? raw.map((part: any) => typeof part === "string" ? part : part?.text ?? "").join("")
            : raw?.content ?? raw?.text ?? "";
}

function normalizeResponsesMessages(context: any, prompt: string) {
    const messages: any[] = prompt ? [{ role: "system", content: prompt }] : [];
    for (const message of context.messages ?? []) {
        if (!message || typeof message !== "object") continue;
        if (message.role === "user") {
            const content = typeof message.content === "string"
                ? [{ type: "input_text", text: message.content }]
                : (message.content ?? []).flatMap((part: any) => {
                    if (part.type === "text") return [{ type: "input_text", text: part.text }];
                    if (part.type === "image") return [{ type: "input_image", detail: "auto", image_url: `data:${part.mimeType};base64,${part.data}` }];
                    return [];
                });
                if (content.length > 0) messages.push({ role: "user", content });
        } else if (message.role === "assistant") {
            for (const part of message.content ?? []) {
                if (part.type === "text" && part.text) messages.push({ type: "message", role: "assistant", content: [{ type: "output_text", text: part.text }], status: "completed" });
                if (part.type === "toolCall") {
                    const [callId, itemId] = String(part.id).split("|");
                    messages.push({ type: "function_call", ...(itemId ? { id: itemId } : {}), call_id: callId, name: part.name, arguments: JSON.stringify(part.arguments ?? {}) });
                }
            }
        } else if (message.role === "toolResult") {
            const [callId] = String(message.toolCallId).split("|");
            messages.push({ type: "function_call_output", call_id: callId, output: textOf(message.content) });
        }
    }
    return messages;
}

function createOutput(model: any) {
    return {
        role: "assistant",
        content: [],
        api: model.api,
        provider: model.provider,
        model: model.id,
        usage: {
            input: 0,
            output: 0,
            cacheRead: 0,
            cacheWrite: 0,
            totalTokens: 0,
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0, total: 0 },
        },
        stopReason: "pending",
        timestamp: Date.now(),
    } as any;
}

function createBlocks(stream: AssistantMessageEventStream, output: any) {
    const state = { textIndex: -1, thinkingIndex: -1, toolCalls: new Map<number, any>() };
    const closeThinking = () => {
        if (state.thinkingIndex === -1) return;
        const block = output.content[state.thinkingIndex];
        stream.push({ type: "thinking_end", contentIndex: state.thinkingIndex, content: block.thinking, partial: output });
        state.thinkingIndex = -1;
    };
    const closeText = () => {
        if (state.textIndex === -1) return;
        const block = output.content[state.textIndex];
        stream.push({ type: "text_end", contentIndex: state.textIndex, content: block.text, partial: output });
        state.textIndex = -1;
    };
    const textDelta = (delta: string) => {
        closeThinking();
        if (state.textIndex === -1) {
            state.textIndex = output.content.length;
            output.content.push({ type: "text", text: "" });
            stream.push({ type: "text_start", contentIndex: state.textIndex, partial: output });
        }
        output.content[state.textIndex].text += delta;
        stream.push({ type: "text_delta", contentIndex: state.textIndex, delta, partial: output });
    };
    const thinkingDelta = (delta: string) => {
        closeText();
        if (state.thinkingIndex === -1) {
            state.thinkingIndex = output.content.length;
            output.content.push({ type: "thinking", thinking: "" });
            stream.push({ type: "thinking_start", contentIndex: state.thinkingIndex, partial: output });
        }
        output.content[state.thinkingIndex].thinking += delta;
        stream.push({ type: "thinking_delta", contentIndex: state.thinkingIndex, delta, partial: output });
    };
    return { state, closeThinking, closeText, textDelta, thinkingDelta };
}

function finishToolCalls(stream: AssistantMessageEventStream, output: any, calls: Map<number, any>) {
    for (const item of calls.values()) {
        let args = {};
        try {
            args = JSON.parse(item.arguments || "{}");
        } catch {
            throw new Error(`Invalid tool arguments for ${item.name}`);
        }
        output.content[item.contentIndex].arguments = args;
        stream.push({ type: "toolcall_end", contentIndex: item.contentIndex, toolCall: { type: "toolCall", id: item.id, name: item.name, arguments: args }, partial: output });
    }
}

async function request(path: string, body: any, model: any, options: any) {
    const payload = await options?.onPayload?.(body, model);
    const response = await (options?.fetch ?? fetch)(`${BASE_URL}${path}`, {
        method: "POST",
        headers: requestHeaders(options),
        body: JSON.stringify(payload === undefined ? body : payload),
        signal: options?.signal,
    });
    await options?.onResponse?.({ status: response.status, headers: Object.fromEntries(response.headers.entries()) }, model);
    return response;
}

async function readSSE(response: Response, onEvent: (event: any, eventType: string) => void) {
    const reader = response.body!.getReader();
    const decoder = new TextDecoder();
    const newline = String.fromCharCode(10);
    let buffer = "";
    let eventType = "";
    let dataLines: string[] = [];
    const flush = () => {
        if (dataLines.length === 0) return;
        const data = dataLines.join(newline).trim();
        dataLines = [];
        if (data && data !== "[DONE]") onEvent(JSON.parse(data), eventType);
        eventType = "";
    };
    for (;;) {
        const chunk = await reader.read();
        buffer += decoder.decode(chunk.value ?? new Uint8Array(), { stream: !chunk.done });
        let end;
        while ((end = buffer.indexOf(newline)) !== -1) {
            const line = buffer.slice(0, end).trimEnd();
            buffer = buffer.slice(end + 1);
            if (line === "") flush();
            else if (line.startsWith("event:")) eventType = line.slice(6).trim();
            else if (line.startsWith("data:")) dataLines.push(line.slice(5).trimStart());
        }
        if (chunk.done) break;
    }
    const line = buffer.trimEnd();
    if (line.startsWith("event:")) eventType = line.slice(6).trim();
    else if (line.startsWith("data:")) dataLines.push(line.slice(5).trimStart());
    flush();
}

function streamResponses(model: any, context: any, options: any) {
    const stream = new AssistantMessageEventStream();
    const output = createOutput(model);
    const blocks = createBlocks(stream, output);
    (async () => {
        try {
            const tools = normalizeTools(context.tools);
            const body: any = {
                model: model.id,
                input: normalizeResponsesMessages(context, systemPrompt(context)),
                stream: true,
                store: false,
                max_output_tokens: Math.max(16, options?.maxTokens ?? model.maxTokens),
                ...(tools ? { tools: tools.map((tool: any) => ({ type: "function", name: tool.function.name, description: tool.function.description, parameters: tool.function.parameters })) } : {}),
            };
                stream.push({ type: "start", partial: output });
                const response = await request("/responses", body, model, options);
                if (!response.ok) throw new Error(`Zen Responses API request failed: HTTP ${response.status} ${(await response.text()).slice(0, 300)}`);
                if (!response.body) throw new Error("Zen Responses API returned no response body");
                await readSSE(response, (event, eventType) => {
                    const type = event.type ?? eventType;
                    if (type === "response.output_text.delta") blocks.textDelta(event.delta ?? "");
                    else if (type === "response.reasoning_summary_text.delta" || type === "response.reasoning_text.delta") blocks.thinkingDelta(event.delta ?? "");
                    else if (type === "response.output_item.added") {
                        const item = event.item ?? {};
                        if (item.type === "function_call") ensureResponseTool(blocks, stream, output, { ...item, output_index: event.output_index });
                    } else if (type === "response.function_call_arguments.delta") {
                        const item = ensureResponseTool(blocks, stream, output, event);
                        item.arguments += event.delta ?? "";
                        stream.push({ type: "toolcall_delta", contentIndex: item.contentIndex, delta: event.delta ?? "", partial: output });
                    } else if (type === "response.function_call_arguments.done") {
                        const item = ensureResponseTool(blocks, stream, output, event);
                        if (event.arguments && !item.arguments) {
                            item.arguments = event.arguments;
                            stream.push({ type: "toolcall_delta", contentIndex: item.contentIndex, delta: event.arguments, partial: output });
                        }
                    } else if (type === "response.completed") {
                        const usage = event.response?.usage;
                        output.responseId = event.response?.id;
                        if (usage) {
                            const cached = usage.input_tokens_details?.cached_tokens ?? 0;
                            const cacheWrite = usage.input_tokens_details?.cache_write_tokens ?? 0;
                            output.usage.input = Math.max(0, (usage.input_tokens ?? 0) - cached - cacheWrite);
                            output.usage.output = usage.output_tokens ?? 0;
                            output.usage.totalTokens = usage.total_tokens ?? output.usage.input + output.usage.output;
                            output.usage.cacheRead = cached;
                            output.usage.cacheWrite = cacheWrite;
                        }
                        output.stopReason = "stop";
                    } else if (type === "response.incomplete") output.stopReason = "length";
                    else if (type === "error" || type === "response.failed") throw new Error(event.message ?? event.error?.message ?? JSON.stringify(event));
                });
                blocks.closeThinking();
                blocks.closeText();
                finishToolCalls(stream, output, blocks.state.toolCalls);
                if (blocks.state.toolCalls.size > 0) output.stopReason = "toolUse";
                if (output.stopReason === "pending") output.stopReason = "stop";
                stream.push({ type: "done", reason: output.stopReason, message: output });
                stream.end();
        } catch (error) {
            output.stopReason = options?.signal?.aborted ? "aborted" : "error";
            output.errorMessage = error instanceof Error ? error.message : String(error);
            stream.push({ type: "error", reason: output.stopReason, error: output });
            stream.end();
        }
    })();
    return stream;
}

function ensureResponseTool(blocks: any, stream: AssistantMessageEventStream, output: any, event: any) {
    const index = event.output_index ?? event.index ?? 0;
    const item = blocks.state.toolCalls.get(index) ?? { id: event.call_id ?? event.item_id ?? openCodeId(`call_${index}_`), name: event.name ?? "", arguments: "", contentIndex: -1 };
    if (event.call_id) item.id = event.call_id;
    if (event.name) item.name = event.name;
    if (item.contentIndex === -1) {
        blocks.closeThinking();
        blocks.closeText();
        item.contentIndex = output.content.length;
        output.content.push({ type: "toolCall", id: item.id, name: item.name, arguments: {} });
        stream.push({ type: "toolcall_start", contentIndex: item.contentIndex, partial: output });
    }
    blocks.state.toolCalls.set(index, item);
    return item;
}

function streamModel(model: any, context: any, options: any) {
    if (RESPONSE_MODELS.test(model.id)) return streamResponses(model, context, options);

    const stream = new AssistantMessageEventStream();
    const output = createOutput(model);
    const blocks = createBlocks(stream, output);
    (async () => {
        try {
            const tools = normalizeTools(context.tools);
            const prompt = systemPrompt(context);
            const body: any = {
                model: model.id,
                messages: [...(prompt ? [{ role: "system", content: prompt }] : []), ...normalizeMessages(context.messages)],
                stream: true,
                stream_options: { include_usage: true },
                ...(tools ? { tools } : {}),
                max_tokens: options?.maxTokens ?? model.maxTokens,
            };
            stream.push({ type: "start", partial: output });
            const response = await request("/chat/completions", body, model, options);
            if (!response.ok) throw new Error(`Zen API request failed: HTTP ${response.status} ${(await response.text()).slice(0, 300)}`);
            if (!response.body) throw new Error("Zen API returned no response body");
            await readSSE(response, (event) => {
                if (event.error) throw new Error(event.error.message ?? JSON.stringify(event.error));
                const usage = event.usage;
                if (usage) {
                    const cached = usage.prompt_tokens_details?.cached_tokens ?? 0;
                    output.usage.input = Math.max(0, (usage.prompt_tokens ?? 0) - cached);
                    output.usage.output = usage.completion_tokens ?? 0;
                    output.usage.totalTokens = usage.total_tokens ?? output.usage.input + output.usage.output;
                    output.usage.cacheRead = cached;
                }
                const choice = event.choices?.[0];
                const delta = choice?.delta;
                if (delta) {
                    const thinking = delta.reasoning_content ?? delta.reasoning;
                    if (thinking) blocks.thinkingDelta(thinking);
                    if (delta.content) blocks.textDelta(delta.content);
                    for (const call of delta.tool_calls ?? []) {
                        const index = call.index ?? 0;
                        const item = blocks.state.toolCalls.get(index) ?? { id: call.id ?? openCodeId(`call_${index}_`), name: call.function?.name ?? "", arguments: "", contentIndex: -1 };
                        if (call.id) item.id = call.id;
                        if (call.function?.name) item.name = call.function.name;
                        item.arguments += call.function?.arguments ?? "";
                        if (item.contentIndex === -1) {
                            blocks.closeThinking();
                            blocks.closeText();
                            item.contentIndex = output.content.length;
                            output.content.push({ type: "toolCall", id: item.id, name: item.name, arguments: {} });
                            stream.push({ type: "toolcall_start", contentIndex: item.contentIndex, partial: output });
                        }
                        const block = output.content[item.contentIndex];
                        block.id = item.id;
                        block.name = item.name;
                        stream.push({ type: "toolcall_delta", contentIndex: item.contentIndex, delta: call.function?.arguments ?? "", partial: output });
                        blocks.state.toolCalls.set(index, item);
                    }
                }
                if (choice?.finish_reason) output.stopReason = choice.finish_reason === "tool_calls" || choice.finish_reason === "function_call" ? "toolUse" : choice.finish_reason === "length" ? "length" : "stop";
            });
            blocks.closeThinking();
            blocks.closeText();
            finishToolCalls(stream, output, blocks.state.toolCalls);
            if (blocks.state.toolCalls.size > 0) output.stopReason = "toolUse";
            if (output.stopReason === "pending") output.stopReason = "stop";
            stream.push({ type: "done", reason: output.stopReason, message: output });
            stream.end();
        } catch (error) {
            output.stopReason = options?.signal?.aborted ? "aborted" : "error";
            output.errorMessage = error instanceof Error ? error.message : String(error);
            stream.push({ type: "error", reason: output.stopReason, error: output });
            stream.end();
        }
    })();
    return stream;
}

export default async function opencodeApi(pi: ExtensionAPI) {
    let modelIds = FALLBACK_MODELS;
    try {
        modelIds = await discoverModels();
    } catch {
        // Use the fallback catalog when Zen discovery is unavailable.
    }

    pi.registerProvider(PROVIDER, {
        name: "OpenCode Zen Free (native)",
        baseUrl: BASE_URL,
        apiKey: "public",
        api: "openai-completions",
        models: modelIds.map(modelConfig),
        streamSimple: streamModel,
    });
}
