---
name: meagent-gmail-tagging
description: Use to sort inbox mail into action, reading, or junk before changing Gmail.
---

# Meagent Gmail Tagging

This skill stages Gmail triage in a local queue. It does not change Gmail until `push`.

## Run

Run `uv run <path-to-skill>/scripts/meagent_gmail_tagging.py <command> [args]`.

1. Run `rules`, then `fetch`.
2. Tag the queue rows. Group rows with the same tag when you can, such as `uv run <path-to-skill>/scripts/meagent_gmail_tagging.py tag action 1,4,8`.
3. Run `status`. If rows are still untagged, tag the rows it shows and run `status` again.
4. Stop when it says `everything is tagged, review these tags`.
5. Run `status` once with `raw_output=true` for review.
6. Apply requested changes, if any, then run `status` again with `raw_output=true`.
7. Ask for approval. After approval, run `push` with `raw_output=false` and `timeout_seconds=300`.
8. After `push`, run `print` with `raw_output=true`.

Use `raw_output=false` for all other commands. This setting belongs to the exec call, not the script.

## Commands

- `rules` prints the tag rules and Google Tasks rules.
- `fetch` gets inbox threads and saves `/tmp/tag_gmail.ndjson`.
- `tag <action|reading|junk> <idx1,idx2,...>` sets tags by queue index.
- `status` shows untagged rows, up to 20 at a time, or reviews all tags.
- `push` adds labels, trashes junk, and clears the queue.
- `print` shows untagged and tagged mail from Gmail.

## Rules

- `action`: needs a reply, choice, or follow-up from me.
- `reading`: newsletters, articles, and updates to read later.
- `junk`: promos, spam, deals, and low-value alerts.
- `idx` means the local queue index, not the Gmail thread ID.
- List every `idx` in each `tag` call. Use one call per tag.
- Do not run `fetch` again.
- Do not reformat script output.
