---
name: botbot-gtask
description: Use when you need to list Google Task lists or tasks, add or complete a task, or interactively edit a task title and notes (whitelist enforced) through gog.
---

# Botbot Google Tasks

## Workflows
```bash
uv run <path-to-skill>/scripts/botbot_gtask.py [--config /path/to/botbot-gtask.json] <command> [args]
```

## When to Use
Supports:
- `ls` (list task lists)
- `tasks [--list <title-or-id>]` (list incomplete tasks in a task list; defaults to the first list)
- `add [--title <title>] [--notes <notes>] [--list <title-or-id>]` (create a task; omit `--title` to open an editor)
- `edit [--list <title-or-id>]` (select and edit an incomplete task title and notes)
- `done [--list <title-or-id>]` (select and complete an incomplete task)

If `--list` is omitted, the first list from `ls` is used.

## Boundaries
- Always run with `uv run`.
- Requires `gog` with Google Tasks access for the selected account and client.
- gog owns OAuth client setup, consent, token storage, and token refresh.
- The command passes `--no-input`; configure gog before use.
- `add`, `edit`, and `done` are always gated by `edit_whitelist`.
- `add` opens `$EDITOR`, falling back to `$VISUAL` and then `vim` when `--title` is omitted. Line 1 is the title; the remaining text is notes (max 4000 characters). With `--title`, it is noninteractive; `--notes` requires `--title`.
- `edit` opens `$EDITOR`, falling back to `$VISUAL`. Line 1 is the title, line 2 must be blank, remaining text is notes (max 4000 characters).
- Failed edits and additions are saved to `/tmp/gog-gtask.txt` with mode `0600`.

## Configuration
Config path precedence:
1. `--config /path/to/botbot-gtask.json`
2. `$BOTBOT_HOME/botbot-gtask.json`
3. `~/.botbot/botbot-gtask.json`

Example: `assets/botbot-gtask.example.json`

```json
{
  "gog": {
    "account": "you@example.com",
    "client": "your-client-name"
  },
  "edit_whitelist": ["Personal", "work-list-id"]
}
```

## Examples
```bash
uv run <path-to-skill>/scripts/botbot_gtask.py ls
uv run <path-to-skill>/scripts/botbot_gtask.py tasks
uv run <path-to-skill>/scripts/botbot_gtask.py tasks --list "Personal"
uv run <path-to-skill>/scripts/botbot_gtask.py edit --list "Personal"
uv run <path-to-skill>/scripts/botbot_gtask.py done --list "Personal"
uv run <path-to-skill>/scripts/botbot_gtask.py add --list "Personal"
uv run <path-to-skill>/scripts/botbot_gtask.py add --list "Personal" --title "Buy milk" --notes "2 liters"
uv run <path-to-skill>/scripts/botbot_gtask.py --config ~/.botbot/botbot-gtask.json ls
```

## Resources
- Entrypoint: `scripts/botbot_gtask.py`
- Replace `<path-to-skill>` with your installed skill path (for example `~/.code/skills/botbot-gtask`).
