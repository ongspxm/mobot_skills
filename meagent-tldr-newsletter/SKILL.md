---
name: meagent-tldr-newsletter
description: Read newsletter items from Gmail, print short summaries with resolved links, and trash them on confirmation.
---

# Meagent TLDR Newsletter

Reads Gmail threads labeled `6.auto`, newest first. Parses TLDR, AI Secret, Robotics Herald, Marketing Secret, and Bay Area Letters blocks into title, description, and link. Follows tracking redirects, strips `utm_` params, trims text, dedupes by link.

```bash
uv run <path-to-skill>/scripts/meagent_tldr_newsletter.py read
uv run <path-to-skill>/scripts/meagent_tldr_newsletter.py trash
```

## Steps

1. Run `read` with `raw_output=True`, exec timeout `600s`. Show output as is.
2. Wait for user to say `ok`.
3. Run `trash`.

`read` saves the thread batch to `/tmp/meagent_tldr_newsletter_threads.json`. `trash` deletes that batch only.

Never run `trash` before `read`.


## Notes

- Needs `botbot-gmail` in the same skills root.
- `trash` cannot be undone.
- Replace `<path-to-skill>` with the installed path.
