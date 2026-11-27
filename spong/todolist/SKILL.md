---
name: todolist
description: Maintain and verify an untracked todo.txt scratchpad at the active git worktree root tracking plan, why, check, and next steps.
---

# Todolist

Keep todo.txt at active git worktree root ("$(git rev-parse --show-toplevel)/todo.txt").
Live scratchpad written BEFORE edits and updated during work, NOT a post-hoc changelog (use "docs/devlog.md" or git commits for history).

Optional: To watch progress while work runs, run from worktree root: "watch tail -n 20 todo.txt"

## Setup (once per session)

```bash
top=$(git rev-parse --show-toplevel)
exclude="$(git rev-parse --path-format=absolute --git-common-dir)/info/exclude"
mkdir -p "$(dirname "$exclude")"
grep -qxF '/todo.txt' "$exclude" 2>/dev/null || printf '\n/todo.txt\n' >> "$exclude"
if [ -s "$top/todo.txt" ]; then
  open=$(grep -c '^- \[ \]' "$top/todo.txt" || true)
  done=$(grep -c '^- \[x\]' "$top/todo.txt" || true)
  printf 'EXISTING todo.txt (%s open, %s done) -> read and flag user\n' "$open" "$done"
else
  : > "$top/todo.txt"
  printf 'NEW todo.txt -> write first section before edits\n'
fi
```

## Check todolist

When user asks to check todo.txt or todolist:
1. Read "$top/todo.txt" and list every open "- [ ]" item.
2. Verify each open item against real state: run its "check:" command, inspect named artifact (e.g. "/tmp/xxx.txt"), or check code/tests. Never guess from memory.
3. If check passes: flip "[ ]" -> "[x] (<check/result>)" in place; drop "check:" and "next:".
4. If still open: keep "[ ]"; update "next:" if state moved.
5. If item has no verifiable check/artifact and cannot be verified cheaply: keep "[ ]", set "next: add check or artifact", and flag user.
6. Reply with 1 line per open item checked: done vs still open + evidence.

## Rules
- Never "git add" or commit todo.txt.
- If setup reports EXISTING todo.txt: read it and tell user in 1 line (open/done count + last topic). If open "[ ]" tasks exist, confirm whether to resume, check off done items, mark "NOFIX", or append new section below.
- Write "[ ]" tasks BEFORE editing code. Never add pre-checked "[x]" after work finishes.
- Write tasks in smart caveman form: terse, plain ASCII, no filler.
- Every "[ ]" task MUST have a verifiable "check:" (command, observable state, or artifact path like "/tmp/xxx.txt" + expected content) so done-ness can be checked without redoing work.
- For investigation/proof tasks, write output to an artifact (e.g. "/tmp/bug-xxx.txt") and cite what it must show in "check:".
- Update in place: flip "[ ]" -> "[x] (<check/result>)" only after real check passes, and drop "check:" and "next:" on done tasks. Never delete tasks mid-plan; drop 100%-done old sections when starting unrelated work.
- Record forks and failed tries in place with "- [x] DECIDE <choice> (<evidence>)" or "- [x] REVERT <try> (<evidence>)" and "why:". For numeric perf rows, write TSV to "/tmp/perf-<topic>.tsv" and cite path.

## Format

Use "# fixes" for independent light fixes on main (reuse trailing "# fixes" or append "# fixes" at bottom).
Use "# plan: <goal>" for multi-step work or playbooks (append new block at bottom when plan changes or new big task starts).

```text
# fixes
- [x] Fix sidebar cross alignment (manual UI check green)
  why: Crosses sat on right edge in web/index.html.
- [ ] Auto-close notices after 5s
  why: setNotice() keeps stale messages until dismissed.
  check: test_notice_timeout green; notice clears after 5s in app_harness.js
  next: Add per-key timeout in web/app_harness.js.

# plan: <what we are building>
shape: <key files / constraints>

- [x] Save bug repro trace -> /tmp/bug-yyy.txt (/tmp/bug-yyy.txt shows parse crash)
  why: Prove bug before editing parser.
- [ ] Make parser handle yyy msg
  why: yyy msg drops payload on colon.
  check: pytest tests/test_parser.py -k yyy green
  next: Update split_msg in src/parser.py.
- [x] REVERT pool cache (bench/oom.log shows OOM)
  why: Exceeded 512MB worker limit under load.
- [x] NOFIX <dropped step>
  why: <why no longer relevant>
```
