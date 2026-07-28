---
name: botbot-gmail
description: Use when you need to list Gmail threads by query, read message bodies, delete a thread, or manage a label through gog.
---

# Botbot Gmail

## Workflows
```bash
uv run <path-to-skill>/scripts/botbot_gmail.py [--config /path/to/botbot-gmail.json] <command> [args]
```

## When to Use
Supports:
- `ls [query]` (NDJSON: `{threadid, from, subject, tstamp, labels}`; default query `in:INBOX`)
- `read <thread_id>` (latest message as JSON: `{body, headers}`; header names are lowercase)
- `del <thread_id>` (trash a thread)
- `tag <thread_id> <label>` (add a label)
- `untag <thread_id> <label>` (remove a label)
- `refresh` (verify gog can refresh the configured account token)

## Boundaries
- Always run with `uv run`.
- Requires `gog` with Gmail modify access for the selected account and client.
- gog owns OAuth client setup, consent, token storage, and token refresh.
- The command passes `--no-input`; configure gog before use.

## Configuration
Config path precedence:
1. `--config /path/to/botbot-gmail.json`
2. `$BOTBOT_HOME/botbot-gmail.json`
3. `~/.botbot/botbot-gmail.json`

Example: `assets/botbot-gmail.example.json`

```json
{
  "gog": {
    "account": "you@example.com",
    "client": "your-client-name"
  }
}
```

## Examples
```bash
uv run <path-to-skill>/scripts/botbot_gmail.py ls
uv run <path-to-skill>/scripts/botbot_gmail.py ls "from:alerts@example.com newer_than:7d"
uv run <path-to-skill>/scripts/botbot_gmail.py read 18f9abc123def456
uv run <path-to-skill>/scripts/botbot_gmail.py del 18f9abc123def456
uv run <path-to-skill>/scripts/botbot_gmail.py tag 18f9abc123def456 IMPORTANT
uv run <path-to-skill>/scripts/botbot_gmail.py refresh
```

`read` returns the latest message body and headers together:
```json
{"body":"...","headers":{"reply-to":"leo <leo@aisecret.us>"}}
```

## Resources
- Entrypoint: `scripts/botbot_gmail.py`
- Replace `<path-to-skill>` with your installed skill path (for example `~/.code/skills/botbot-gmail`).
