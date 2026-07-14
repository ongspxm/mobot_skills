---
name: botbot-news
description: Use when you need market headlines from Reuters, Bloomberg, FT, and WSJ.
---

# Botbot Market News

## Overview
`botbot-news` - lightweight multi-source market-news RSS CLI that prints headlines in plain text.

## Workflows
```bash
uv run <path-to-skill>/scripts/botbot_news.py
```

## When to Use
Fetches separate Reuters, Bloomberg, Financial Times, and Wall Street Journal feeds. Merges, de-duplicates, sorts newest-first, and prints one `title` per line.

Feed URLs are built in as defaults in the script. There is no config override for feed URLs.

## Resources
- Entrypoint: `scripts/botbot_news.py`
- Replace `<path-to-skill>` with your installed skill path (for example `~/.code/skills/botbot-news`).
