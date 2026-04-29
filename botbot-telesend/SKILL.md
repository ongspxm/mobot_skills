---
name: botbot-telesend
description: Send Telegram messages with optional image batches through a bot token.
---

# BOTBOT-TELESEND(1)

## NAME

`botbot-telesend` - tiny Telegram sender CLI for text and high-resolution image uploads.

## SYNOPSIS

```bash
uv run <path-to-skill>/scripts/botbot_telesend.py send (--text "hello" | --textfile ./message.txt) [--img file1.jpg --img file2.jpg ...]
```

## DESCRIPTION

Sends a Telegram bot message to the configured default chat.

- Uses `sendMessage` when no `--img` flags are supplied.
- Uses `sendMediaGroup` for image batches of 2-10 documents (`type=document`).
- Uses `sendDocument` for single-image batches (for example, remainder after chunking).
- If more than 10 images are given, sends them in series of 10 per request.
- Message text is attached once: as text-only content, or as the caption on the first sent file/group.
- Text input supports either `--text` or `--textfile` (UTF-8 file).

Default config location is `~/.botbot/botbot-telesend.json`.

Required config keys:

- `bottkn`: Telegram bot token.
- `chatid`: target chat id (for example `-1001234567890`).

## EXAMPLES

```bash
uv run <path-to-skill>/scripts/botbot_telesend.py send --text "daily update"
```

```bash
uv run <path-to-skill>/scripts/botbot_telesend.py send --textfile ./message.txt --img ./a.jpg --img ./b.jpg
```

```bash
uv run <path-to-skill>/scripts/botbot_telesend.py send --text "look" --img ./a.jpg --img ./b.jpg
```

## FILES

- Entrypoint: `scripts/botbot_telesend.py`
- Example config: `assets/botbot-telesend.example.json`
