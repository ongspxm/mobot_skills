import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { generateDiffString, type ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { StringEnum } from "@earendil-works/pi-ai";
import { Type, type Static } from "typebox";

const MAX_BYTES = 50 * 1024;
const MAX_LINES = 2000;
const ALPHABET = "ZPMQVRWSNKTXJBYH";
const encoder = new TextEncoder();
const significant = /[\p{L}\p{N}]/u;
const P1 = 0x9e3779b1;
const P2 = 0x85ebca77;
const P3 = 0xc2b2ae3d;
const P4 = 0x27d4eb2f;
const P5 = 0x165667b1;

function rotl(value: number, bits: number) {
	return (value << bits) | (value >>> (32 - bits));
}

function xxhash(text: string, seed = 0) {
	const bytes = encoder.encode(text);
	const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
	let pos = 0;
	let hash: number;
	if (bytes.length >= 16) {
		let a = (seed + P1 + P2) >>> 0;
		let b = (seed + P2) >>> 0;
		let c = seed >>> 0;
		let d = (seed - P1) >>> 0;
		while (pos <= bytes.length - 16) {
			a = Math.imul(rotl((a + Math.imul(view.getUint32(pos, true), P2)) >>> 0, 13), P1) >>> 0;
			pos += 4;
			b = Math.imul(rotl((b + Math.imul(view.getUint32(pos, true), P2)) >>> 0, 13), P1) >>> 0;
			pos += 4;
			c = Math.imul(rotl((c + Math.imul(view.getUint32(pos, true), P2)) >>> 0, 13), P1) >>> 0;
			pos += 4;
			d = Math.imul(rotl((d + Math.imul(view.getUint32(pos, true), P2)) >>> 0, 13), P1) >>> 0;
			pos += 4;
		}
		hash = (rotl(a, 1) + rotl(b, 7) + rotl(c, 12) + rotl(d, 18)) >>> 0;
	} else {
		hash = (seed + P5) >>> 0;
	}
	hash = (hash + bytes.length) >>> 0;
	while (pos <= bytes.length - 4) {
		hash = Math.imul(rotl((hash ^ Math.imul(view.getUint32(pos, true), P3)) >>> 0, 17), P4) >>> 0;
		pos += 4;
	}
	while (pos < bytes.length) {
		hash = Math.imul(rotl((hash ^ Math.imul(bytes[pos++], P5)) >>> 0, 11), P1) >>> 0;
	}
	hash ^= hash >>> 15;
	hash = Math.imul(hash, P2) >>> 0;
	hash ^= hash >>> 13;
	hash = Math.imul(hash, P3) >>> 0;
	return (hash ^ (hash >>> 16)) >>> 0;
}

function lineHash(lineNumber: number, text: string) {
	if (text.endsWith("\r")) text = text.slice(0, -1);
	text = text.replace(/\s+/g, "");
	const hash = xxhash(text, significant.test(text) ? 0 : lineNumber);
	return ALPHABET[(hash >>> 4) & 15] + ALPHABET[hash & 15];
}

function tag(line: number, text: string) {
	return `${line}#${lineHash(line, text)}`;
}

function format(text: string, start = 1) {
	return text.split("\n").map((line, index) => `${tag(start + index, line)}:${line}`).join("\n");
}

type Anchor = { line: number; hash: string };
type Edit =
	| { op: "replace"; pos: Anchor; end?: undefined; lines: string[]; current: string }
	| { op: "replace"; pos: Anchor; end: Anchor; lines: string[] }
	| { op: "append" | "prepend"; pos?: Anchor; lines: string[] };

function parseTag(value: string): Anchor {
	const match = value.match(/^\s*[>+-]*\s*(\d+)\s*#\s*([ZPMQVRWSNKTXJBYH]{2})/);
	if (!match) throw new Error(`Invalid line reference "${value}". Expected "LINE#ID".`);
	const line = Number(match[1]);
	if (line < 1) throw new Error(`Line number must be >= 1, got ${line}.`);
	return { line, hash: match[2] };
}

function mismatchMessage(mismatches: { line: number; expected: string }[], lines: string[]) {
	const changed = new Set(mismatches.map((item) => item.line));
	const shown = new Set<number>();
	for (const { line } of mismatches) for (let n = Math.max(1, line - 2); n <= Math.min(lines.length, line + 2); n++) shown.add(n);
	const ordered = [...shown].sort((a, b) => a - b);
	const output = [`${mismatches.length} line${mismatches.length > 1 ? "s have" : " has"} changed since last read. Use the updated LINE#ID references below.`];
	let previous = 0;
	for (const line of ordered) {
		if (previous && line > previous + 1) output.push("    ...");
		const prefix = `${line}#${lineHash(line, lines[line - 1])}`;
		output.push(`${changed.has(line) ? ">>>" : "   "} ${prefix}:${lines[line - 1]}`);
		previous = line;
	}
	return output.join("\n");
}

function apply(text: string, edits: Edit[]) {
	if (!edits.length) return { text, changed: undefined as number | undefined, warnings: [] as string[] };
	const source = text.split("\n");
	const lines = [...source];
	const mismatches: { line: number; expected: string }[] = [];
	const warnings: string[] = [];
	const currentMismatches: { line: number; expected: string; actual: string }[] = [];
	const check = (anchor: Anchor) => {
		if (anchor.line < 1 || anchor.line > lines.length) throw new Error(`Line ${anchor.line} does not exist (file has ${lines.length} lines)`);
		const actual = lineHash(anchor.line, lines[anchor.line - 1]);
		if (actual === anchor.hash) return true;
		mismatches.push({ line: anchor.line, expected: anchor.hash });
		return false;
	};
	for (const edit of edits) {
		if (edit.op === "replace") {
			const startValid = check(edit.pos);
			const endValid = edit.end ? check(edit.end) : true;
			if (edit.end && edit.pos.line > edit.end.line) throw new Error("Range start must not be after range end");
			if (startValid && endValid && !edit.end && lines[edit.pos.line - 1] !== edit.current) {
				currentMismatches.push({ line: edit.pos.line, expected: edit.current, actual: lines[edit.pos.line - 1] });
			}
		} else {
			if (edit.pos) check(edit.pos);
			if (!edit.lines.length) edit.lines = [""];
		}
	}
	if (mismatches.length) throw new Error(mismatchMessage(mismatches, lines));
	if (currentMismatches.length) {
		throw new Error(`Current content mismatch: ${currentMismatches.map((item) => `line ${item.line}: expected ${JSON.stringify(item.expected)}, got ${JSON.stringify(item.actual)}`).join("; ")}`);
	}
	for (const edit of edits) {
		const corrected = edit.lines.map((line) => line.replace(/^(\\t)+/, (value) => "\t".repeat(value.length / 2)));
		if (corrected.some((line, index) => line !== edit.lines[index])) {
			edit.lines = corrected;
			warnings.push("Auto-corrected escaped tab indentation");
		}
	}
	const seen = new Set<string>();
	const unique = edits.filter((edit) => {
		const location = edit.op === "replace" ? edit.end ? `r:${edit.pos.line}:${edit.end.line}` : `s:${edit.pos.line}` : `${edit.op[0]}:${edit.pos?.line ?? "edge"}`;
		const key = `${location}:${edit.lines.join("\n")}`;
		if (seen.has(key)) return false;
		seen.add(key);
		return true;
	});
	const ordered = unique.map((edit, index) => ({
		edit, index,
		line: edit.op === "replace" ? (edit.end?.line ?? edit.pos.line) : edit.pos?.line ?? (edit.op === "append" ? lines.length + 1 : 0),
		rank: edit.op === "replace" ? 0 : edit.op === "append" ? 1 : 2,
	})).sort((a, b) => b.line - a.line || a.rank - b.rank || a.index - b.index);
	let first: number | undefined;
	for (const { edit } of ordered) {
		const mark = (line: number) => { first = first === undefined ? line : Math.min(first, line); };
		if (edit.op === "replace") {
			const end = edit.end?.line ?? edit.pos.line;
			let replacement = edit.lines;
			if (edit.end) {
				const matching = (payload: (n: number) => number, original: (n: number) => number, max: number) => {
					for (let n = max; n > 0; n--) {
						let same = true;
						for (let i = 0; i < n; i++) if (replacement[payload(n) + i]?.trimEnd() !== source[original(n) + i]?.trimEnd()) same = false;
						if (same && replacement.slice(payload(n), payload(n) + n).some(Boolean)) return n;
					}
					return 0;
				};
				let leading = matching(() => 0, (n) => edit.pos.line - 1 - n, Math.min(replacement.length, edit.pos.line - 1));
				let trailing = matching((n) => replacement.length - n, () => edit.end!.line, Math.min(replacement.length, lines.length - edit.end.line));
				while (leading + trailing > 0 && replacement.length - leading - trailing < 1) trailing >= leading ? trailing-- : leading--;
				if (leading || trailing) {
					replacement = replacement.slice(leading, replacement.length - trailing || undefined);
					warnings.push("Auto-corrected range replacement context");
				}
			}
			if (!edit.end && lines[edit.pos.line - 1] === replacement[0] && replacement.length === 1) continue;
			lines.splice(edit.pos.line - 1, end - edit.pos.line + 1, ...replacement);
			mark(edit.pos.line);
		} else if (edit.op === "append") {
			if (edit.pos) lines.splice(edit.pos.line, 0, ...edit.lines), mark(edit.pos.line + 1);
			else if (lines.length === 1 && lines[0] === "") lines.splice(0, 1, ...edit.lines), mark(1);
			else lines.push(...edit.lines), mark(lines.length - edit.lines.length + 1);
		} else if (edit.pos) lines.splice(edit.pos.line - 1, 0, ...edit.lines), mark(edit.pos.line);
		else if (lines.length === 1 && lines[0] === "") lines.splice(0, 1, ...edit.lines), mark(1);
		else lines.unshift(...edit.lines), mark(1);
	}
	return { text: lines.join("\n"), changed: first, warnings };
}

const readSchema = Type.Object({
	path: Type.String({ description: "File path, relative or absolute" }),
	offset: Type.Optional(Type.Number({ description: "First line, 1-indexed" })),
	limit: Type.Optional(Type.Number({ description: "Maximum lines" })),
});
const itemSchema = Type.Object({
	op: StringEnum(["replace", "append", "prepend"] as const),
	pos: Type.Optional(Type.String({ description: "LINE#HASH reference" })),
	end: Type.Optional(Type.String({ description: "End LINE#HASH for a range" })),
	lines: Type.Array(Type.String(), { description: "Replacement or inserted lines" }),
	current: Type.Optional(Type.String({ description: "Exact current line for a single-line replace" })),
});
const editSchema = Type.Object({
	path: Type.String({ description: "File path, relative or absolute" }),
	edits: Type.Array(itemSchema),
	create_if_missing: Type.Optional(Type.Boolean()),
});
type Item = Static<typeof itemSchema>;

function pathOf(path: string, cwd: string) {
	return resolve(cwd, path.startsWith("@") ? path.slice(1) : path);
}

function parseEdits(items: Item[]): Edit[] {
	return items.map((item) => {
		if (item.op === "replace") {
			if (!item.pos) throw new Error("replace requires pos");
			const pos = parseTag(item.pos);
			const end = item.end && parseTag(item.end);
			if (!end && item.current === undefined) throw new Error("single-line replace requires current");
			return end ? { op: "replace" as const, pos, end, lines: item.lines } : { op: "replace" as const, pos, lines: item.lines, current: item.current! };
		}
		return { op: item.op, pos: item.pos != null ? parseTag(item.pos) : undefined, lines: item.lines };
	});
}

const noopCounts = new Map<string, { payload: string; count: number }>();

export default function hashlineEdit(pi: ExtensionAPI) {
	pi.on("session_start", async () => {
		pi.setActiveTools([...pi.getActiveTools().filter((name) => !["edit", "hashline_read", "hashline_edit"].includes(name)), "hashline_read", "hashline_edit"]);
	});

	pi.registerTool({
		name: "hashline_read",
		label: "Hashline Read",
		description: "Read a file as LINE#HASH:text. Use those references with hashline_edit. Output is limited to 2000 lines or 50KB.",
		parameters: readSchema,
		async execute(_id, params, _signal, _update, ctx) {
			const filePath = pathOf(params.path, ctx.cwd);
			try {
				const all = (await readFile(filePath, "utf8")).split("\n");
				const start = params.offset ? Math.max(0, params.offset - 1) : 0;
				const end = params.limit ? Math.min(all.length, start + params.limit) : all.length;
				let output = format(all.slice(start, end).join("\n"), start + 1);
				let shown = output.split("\n");
				let truncated = shown.length > MAX_LINES;
				if (truncated) shown = shown.slice(0, MAX_LINES);
				while (Buffer.byteLength(shown.join("\n"), "utf8") > MAX_BYTES) {
					truncated = true;
					shown.pop();
				}
				output = shown.join("\n");
				if (truncated) output += `\n\n[Showing ${shown.length} of ${all.length} lines. Use offset/limit for more.]`;
				else if (start || end < all.length) output += `\n\n[Showing lines ${start + 1}-${end} of ${all.length}.]`;
				return { content: [{ type: "text", text: output }], details: { totalLines: all.length, startLine: start + 1, shownLines: end - start } };
			} catch (error) {
				return { content: [{ type: "text", text: `Error reading file: ${error instanceof Error ? error.message : String(error)}` }], details: {}, isError: true };
			}
		},
	});

	pi.registerTool({
		name: "hashline_edit",
		label: "Hashline Edit",
		description: "Edit with LINE#HASH references from hashline_read. Supports replace, append, and prepend. All hashes are checked before any change. Returns the diff.",
		parameters: editSchema,
		async execute(_id, params, _signal, _update, ctx) {
			const filePath = pathOf(params.path, ctx.cwd);
			let text: string;
			try {
				text = await readFile(filePath, "utf8");
			} catch (error) {
				if (!params.create_if_missing || !(error && typeof error === "object" && "code" in error && error.code === "ENOENT")) {
					return { content: [{ type: "text", text: `File not found: ${params.path}. Use create_if_missing: true to create it.` }], details: {}, isError: true };
				}
				const lines = params.edits.flatMap((item) => item.op === "append" || item.op === "prepend" ? item.lines : []);
				if (!lines.length) return { content: [{ type: "text", text: "Cannot create file: no append/prepend lines provided." }], details: {}, isError: true };
				await mkdir(dirname(filePath), { recursive: true });
				const createdText = lines.join("\n");
				const diff = generateDiffString("", createdText).diff;
				await writeFile(filePath, createdText, "utf8");
				return { content: [{ type: "text", text: `Created ${params.path} (${lines.length} lines)\n\nDiff:\n${diff}` }], details: { created: true, lines: lines.length, diff } };
			}
			try {
				const edits = parseEdits(params.edits);
				const result = apply(text, edits);
				if (result.changed === undefined) {
					const key = filePath;
					const payload = JSON.stringify(params.edits);
					const previous = noopCounts.get(key);
					const count = previous && previous.payload === payload ? previous.count + 1 : 1;
					noopCounts.set(key, { payload, count });
					if (count >= 3) return { content: [{ type: "text", text: `STOP. The same edit to ${params.path} was a no-op ${count} times. Re-read the file.` }], details: {}, isError: true };
					return { content: [{ type: "text", text: "No changes applied." }], details: {} };
				}
				noopCounts.delete(filePath);
				const diff = generateDiffString(text, result.text).diff;
				await writeFile(filePath, result.text, "utf8");
				const warningText = result.warnings.length ? `\nWarnings:\n${result.warnings.map((warning) => `  - ${warning}`).join("\n")}` : "";
				return { content: [{ type: "text", text: `Applied ${params.edits.length} edit(s) to ${params.path}${warningText}\n\nDiff:\n${diff}` }], details: { firstChangedLine: result.changed, warnings: result.warnings, diff } };
			} catch (error) {
				return { content: [{ type: "text", text: error instanceof Error ? error.message : String(error) }], details: {}, isError: true };
			}
		},
	});
}
