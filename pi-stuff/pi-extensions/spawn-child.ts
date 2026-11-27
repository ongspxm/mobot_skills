import { RpcClient, type ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";

export default function (pi: ExtensionAPI) {
	pi.registerTool({
		name: "spawn_child",
		label: "Spawn child",
		description: "Run task in a child Pi session linked to parent session; return child reply.",
		parameters: Type.Object({
			task: Type.String({ description: "Task for child session" }),
		}),
		async execute(_id, { task }, signal, _update, ctx) {
			const parentSession = ctx.sessionManager.getSessionFile();
			if (!parentSession) throw new Error("Parent session has no session file");
			const client = new RpcClient({ cliPath: process.argv[1], cwd: ctx.cwd });
			const abort = () => void client.abort().catch(() => {});
			signal.addEventListener("abort", abort, { once: true });
			try {
				await client.start();
				const created = await client.newSession(parentSession);
				if (created.cancelled) throw new Error("Child session creation cancelled");
				const settled = new Promise<void>((resolve, reject) => {
					const timeout = setTimeout(() => reject(new Error("Child session timed out")), 10 * 60_000);
					client.onEvent((event) => {
						if (event.type === "agent_settled") {
							clearTimeout(timeout);
							resolve();
						}
					});
				});
				await client.prompt(task);
				await settled;
				return { content: [{ type: "text", text: await client.getLastAssistantText() ?? "Child returned no reply." }], details: {} };
			} finally {
				signal.removeEventListener("abort", abort);
				await client.stop();
			}
		},
	});
}
