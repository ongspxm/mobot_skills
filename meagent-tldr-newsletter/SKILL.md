---
name: meagent-tldr-newsletter
description: Use when you need to read newsletter items from Gmail, print concise summaries with resolved links, and optionally trash matching threads.
---

# Meagent TLDR Newsletter

## Workflows
```bash
uv run <path-to-skill>/scripts/meagent_tldr_newsletter.py read
uv run <path-to-skill>/scripts/meagent_tldr_newsletter.py trash
```

## When to Use
This skill:
- Reads messages with the `6.auto` Gmail label, newest-first.
- Parses TLDR, AI Secret, Robotics Herald, Marketing Secret, and Bay Area Letters article blocks.
- Extracts title, description, and article link.
- Follows newsletter tracking redirects and strips `utm_` parameters.
- Trims descriptions and deduplicates by resolved link.

## Workflow
1. Run `read` with `raw_output=True` and send output directly to user.
2. Wait for explicit user confirmation: `ok`.
3. Only after `ok`, run `trash`.

`read` stores the exact parsed thread batch to be deleted later.
`trash` deletes only that stored batch.

## Commands
- `read` - print parsed newsletter items as plain text blocks.
- `trash` - trash the stored newsletter threads and print result JSON.

## Boundaries
- Always run with `uv run`.
- This skill depends on `botbot-gmail` being installed in the same skills root.
- `trash` is destructive and cannot be undone from this tool.
- Always run `read` before `trash`.
- For `read`, keep `raw_output=True` and pass output straight to user.

## State File
- Path: `/tmp/meagent_tldr_newsletter_threads.json`
- Written by: `read`
- Consumed and deleted by: `trash`

## Resources
- Entrypoint: `scripts/meagent_tldr_newsletter.py`
- Replace `<path-to-skill>` with your installed skill path (for example `~/.code/skills/meagent-tldr-newsletter`).
