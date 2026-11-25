---
name: todolist
description: Maintain an untracked todo.txt scratchpad at the active git worktree root tracking plan, why, and next steps.
---

# Todolist

Keep todo.txt at active git worktree root ("$(git rev-parse --show-toplevel)/todo.txt").

## Setup (once per repo/worktree)

```bash
top=$(git rev-parse --show-toplevel)
exclude="$(git rev-parse --path-format=absolute --git-common-dir)/info/exclude"
mkdir -p "$(dirname "$exclude")"
grep -qxF '/todo.txt' "$exclude" 2>/dev/null || printf '\n/todo.txt\n' >> "$exclude"
[ -e "$top/todo.txt" ] || printf '# plan\ngoal:\nshape:\n' > "$top/todo.txt"
```

## Rules
- Never "git add" or commit todo.txt.
- Read todo.txt before starting or resuming work.
- Add new tasks at bottom. Update existing tasks in place ("[ ]" -> "[x]", "NOFIX", or "next:"); never delete old tasks.
- Keep plain ASCII.

## Format

```text
# plan
goal: <what we are building>
shape: <bigger plan / key files / constraints>

- [ ] <task>
  why: <context that helps impl>
  next: <concrete next step>

- [x] <task> (<check/result>)
  next: <what's next>

- [x] NOFIX <task>
  why: <why no longer relevant>
```

Append another "# plan" block at bottom if plan changes.
