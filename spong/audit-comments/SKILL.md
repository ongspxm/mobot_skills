---
name: audit-comments
description: Fresh-eyes comment audit on files or diff. Strip slop, fix alibi code, add missing signposts.
disable-model-invocation: true
---

# Audit Comments

Fresh eyes only: new subagents with no prior context.
Never let author grade own comments.
Scope: caller paths or diff; else diff vs "main" plus working tree.

1. Read-only audit: spawn subagent with read-only scope and principle-signpost-code skill. Report counts plus DELETE, MUST FIX, ADD ("file:line", 1-line reason):
   - DELETE: outside 4 signpost shapes (not legal header, issue/RFC link, "TODO:", "HACKY:") -> syntax narration, dead code, empty banners, repeated conventions.
   - MUST FIX: alibis ("IMPORTANT", "do not remove", "too risky", "fine for now"), internal excuses, or suppressions ("eslint-disable", "@ts-ignore", "@ts-expect-error", "# noqa"). Trace callers and "git log -S" first -> name weak symbol or quirk.
   - ADD: missing "=== <group>" headers in multi-group files, phase markers in long flat functions, or unexplained negative choices, lock/thread rules, and untyped map/unit shapes.
2. Filter against principle-signpost-code skill: reject valid signposts, "TODO:", "HACKY:", and noisy ADDs.
3. Show planned edits and ask "ok to go?" (spong-mode skill).
4. Apply accepted edits:
   - DELETE: strip slop.
   - MUST FIX: rename, reshape (principle-data-shape-first skill), fix root cause (principle-fix-root-cause skill), or encode check (principle-enforce-in-code skill) -> delete comment.
   - ADD: write missing headers, step markers, or 1-line intent.

Reply with: counts (deleted, added, fixed, encoded), rejected flags, open items.
