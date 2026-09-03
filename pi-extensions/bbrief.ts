/**
 * Enable brief replies with /bbrief and append the instruction to the latest user message.
 * Load with: pi -e ./bbrief.ts
 */
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const BRIEF_SUFFIX = "\n\nALWAYS keep replies compact, be clear, use simple words";

export default function brief(pi: ExtensionAPI) {
	let enabled = true;

	pi.registerCommand("bbrief", {
		description: "Toggle brief replies for this session",
		handler: async (_args, ctx) => {
			enabled = !enabled;
			ctx.ui.notify(`brief replies ${enabled ? "enabled" : "disabled"}`, "info");
		},
	});

	pi.on("context", (event) => {
		if (!enabled) return;

		const userIndex = event.messages.findLastIndex((message) => message.role === "user");
		if (userIndex === -1) return;

		const messages = event.messages.map((message, index) => {
			if (index !== userIndex) return message;

			if (typeof message.content === "string") {
				return { ...message, content: message.content + BRIEF_SUFFIX };
			}

			const content = [...message.content];
			const textIndex = content.findLastIndex((part) => part.type === "text");
			if (textIndex === -1) return message;

			const text = content[textIndex];
			if (text.type === "text") {
				content[textIndex] = { ...text, text: text.text + BRIEF_SUFFIX };
			}

			return { ...message, content };
		});

		return { messages };
	});
}
