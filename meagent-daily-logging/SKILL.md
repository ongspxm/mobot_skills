---
name: meagent-daily-logging
description: Use when you need stage-1 Telegram daily logging into monthly markdown files.
---

# Meagent Daily Logging

## Overview

Pulls text messages from configured Telegram chats using a user-authenticated Telethon StringSession, then writes them to monthly Markdown logs.

This skill does not run a scheduler or listen continuously. Run it from cron, a systemd timer, or another automation service.

## Workflow

```bash
uv run <path-to-skill>/scripts/meagent_daily_logging.py run [--date YYYY-MM-DD] [--config /path/to/config.json]
```

- Uses Telegram MTProto through Telethon.
- The first run prompts for the Telegram phone number, login code, and 2FA password when needed.
- Reuses the authenticated `session_string` stored in the config on later runs; no session file is created.
- The logged-in user account must have access to every configured chat.
- Reads config from `~/.botbot/meagent-daily-logging.json` unless `--config` is provided.
- Pulls text messages from `chats` (`tag -> numeric chat_id`).
- Uses a `02:00 -> next day 02:00` window in the configured timezone.
- Without `--date`, processes the previous local calendar day.
- Writes/replaces the target day section in `YYYY-MM.md` under `log_folder`.
- Rebuilds monthly logs by day chunks and sorts them oldest to newest.
- Prints logged lines to stdout.

## Setup

1. Create a Telegram application at <https://my.telegram.org> and copy its `api_id` and `api_hash`.
2. Create the config file at `~/.botbot/meagent-daily-logging.json`.
3. Ensure the Telegram user account can read the configured chats.
4. Run the command interactively once; it stores the authenticated `session_string` in the config.
5. Schedule later runs externally.

Protect the config file. Its `session_string` grants access to the authenticated Telegram account.

## Configuration

JSON object in `~/.botbot/meagent-daily-logging.json`:

- `api_id` (required integer): Telegram application ID.
- `session_string` (optional string): Telethon StringSession value; written to the config after the first interactive login.
- `api_hash` (required string): Telegram application hash.
- `timezone` (optional, default `Asia/Singapore`): timezone for the logging window.
- `log_folder` (optional, default `~/docs/_journal`): output directory.
- `chats` (required object): mapping of output tags to integer Telegram chat IDs.

Example:

```json
{
  "api_id": 123456,
  "api_hash": "replace-with-telegram-api-hash",
  "session_string": "",
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
# Default: previous local calendar day
uv run <path-to-skill>/scripts/meagent_daily_logging.py run

# Backfill a specific day
uv run <path-to-skill>/scripts/meagent_daily_logging.py run --date 2026-03-04
```
