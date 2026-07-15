---
name: botbot-gcal
description: Use when you need to list Google Calendar events in a time range across configured calendars, or add a calendar event to primary calendar through gog.
---

# Botbot Google Calendar

## Workflows
```bash
uv run <path-to-skill>/scripts/botbot_gcal.py [--config /path/to/botbot-gcal.json] <command> [args]
```

## When to Use
Supports:
- `ls <start> <end>` (inclusive range across configured calendars) - ALWAYS run with raw_output=True
- `add <start> <end> <title>` (always inserts into `primary` calendar)

## Boundaries
- Always run with `uv run`.
- Requires `gog` with Calendar access for the selected account and client.
- gog owns OAuth client setup, consent, token storage, and token refresh.
- The command passes `--no-input`; configure gog before use.
- `ls` returns workflow-style text lines, not raw JSON.
- `default_timezone` controls input/output timestamp interpretation and rendering.
- `default_calendars` can contain calendar ids (recommended), `primary`, or calendar names.

## Configuration
Config path precedence:
1. `--config /path/to/botbot-gcal.json`
2. `$BOTBOT_HOME/botbot-gcal.json`
3. `~/.botbot/botbot-gcal.json`

Example: `assets/botbot-gcal.example.json`

```json
{
  "gog": {
    "account": "you@example.com",
    "client": "your-client-name"
  },
  "default_timezone": "+8",
  "default_calendars": ["primary", "work@example.com", "Team Calendar"]
}
```

## Examples
```bash
uv run <path-to-skill>/scripts/botbot_gcal.py ls 2026-02-22 2026-02-23
uv run <path-to-skill>/scripts/botbot_gcal.py add 2026-02-22T09:00:00Z 2026-02-22T09:30:00Z "Standup"
uv run <path-to-skill>/scripts/botbot_gcal.py --config ~/.botbot/botbot-gcal.json ls 2026-02-22 2026-02-23
```

## Resources
- Entrypoint: `scripts/botbot_gcal.py`
- Replace `<path-to-skill>` with your installed skill path (for example `~/.code/skills/botbot-gcal`).
