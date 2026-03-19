---
name: botbot-news
description: Use when you need market headlines from Reuters, Bloomberg, FT, and WSJ.
---

# BOTBOT-NEWS(1)

## NAME

`botbot-news` - lightweight multi-source market-news RSS CLI that prints headlines in plain text.

## SYNOPSIS

```bash
uv run <path-to-skill>/scripts/botbot_news.py
```

## DESCRIPTION

Fetches stories from separate feeds for these sources:

- Reuters
- Bloomberg
- Financial Times
- Wall Street Journal

The script merges all feeds, de-duplicates items, sorts by publish time (newest first), and prints plain-text output.

Output format:
- one line per item: `title`

Feed URLs are built in as defaults in the script. There is no config override for feed URLs.

## EXAMPLES

```bash
uv run <path-to-skill>/scripts/botbot_news.py
```

## FILES

- Entrypoint: `scripts/botbot_news.py`
- Replace `<path-to-skill>` with your installed skill path (for example `~/.code/skills/botbot-news`).
