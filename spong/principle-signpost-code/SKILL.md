---
name: principle-signpost-code
description: Mark sections, big steps, conventions, and non-obvious intent in flat code; delete narrating slop and workaround alibis.
disable-model-invocation: true
---

# Signpost Code

Flat code needs signposts, not syntax narration.

Keep or add only 4 comment shapes:
- File sections: "// === <group>" or "# === <group>" in multi-group files, with matching function prefixes (like "renderXXX", "apiXXX").
- Big steps: 1-line phase markers above multi-line blocks inside long or inlined functions ("// perform delete").
- Conventions and untyped shapes (once): top-of-file prefix rules, lock suffix rules ("xxxLocked expects s.Mu.Locked() to be called"), or map/unit shapes types cannot express ("// sessions[dirname][harness, sessid]"). Never repeat per function.
- Intent and constraints: negative choices ("ignore X because Y"), cross-thread coupling, external quirks, and public contracts.

Delete the rest: syntax narration ("// loop users"), dead commented code, workaround alibis ("IMPORTANT", "fine for now"), and bug-hiding lint suppressions. Comment excuses weak shape or workaround -> fix shape or encode rule in code, then delete comment.
