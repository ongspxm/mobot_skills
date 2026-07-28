---
name: meagent-daily-logging
description: Use when you need stage-1 Telegram daily logging into monthly markdown files.
---

# Meagent Daily Logging

## Workflows
```bash
uv run --with=telethon <path-to-skill>/scripts/meagent_daily_logging.py run [--date YYYY-MM-DD] [--config /path/to/config.json]
```

## When to Use
- Uses Telethon bot-token auth (`api_id`, `api_hash`, `bot_token`).
- Reads config from `~/.botbot/meagent-daily-logging.json`.
- `--config` can override the default config path.
- Uses session file `~/.botbot/meagent-daily-logging.session`.
- Pulls text messages from configured `chats` (`tag -> chat_id`).
- Writes/replaces the target day section in `YYYY-MM.md` under `log_folder`.
- Rebuilds monthly logs by day-chunks and writes them sorted by date (`oldest -> newest`).
- Day window is `02:00 -> next day 02:00` in configured timezone.
- If `--date` is not provided, it processes the previous local day.
- Prints logged lines to stdout.

## Configuration
JSON object in `~/.botbot/meagent-daily-logging.json`:

- `api_id` (required)
- `api_hash` (required)
- `bot_token` (required)
- `timezone` (optional, default `Asia/Singapore`)
- `log_folder` (optional, default `~/docs/_journal`)
- `chats` (required object): mapping `tag -> chat_id` (integer)

Example:

```json
{
  "api_id": 123456,
  "api_hash": "abc123...",
  "bot_token": "123456789:replace-with-bot-token",
  "timezone": "America/Los_Angeles",
  "log_folder": "/home/user/notes/daily-telegram",
  "chats": {
    "ops": -1001234567890,
    "ann": -1001987654321
  }
}
```

## Examples
```bash
# Default: previous local day
uv run --with=telethon <path-to-skill>/scripts/meagent_daily_logging.py run

# Backfill a specific day
uv run --with=telethon <path-to-skill>/scripts/meagent_daily_logging.py run --date 2026-03-04
```
