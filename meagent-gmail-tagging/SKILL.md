---
name: meagent-gmail-tagging
description: Use when you need a staged Gmail triage flow (fetch, rules, tag, status, push) that stores a local NDJSON queue before applying labels/trash actions.
---

# Meagent Gmail Tagging

## Workflows
```bash
uv run <path-to-skill>/scripts/meagent_gmail_tagging.py <command> [args]
```

## When to Use
Use this exact sequence, including `raw_output` mode (when calling the exec too, not part of the script):
1. `rules` with `raw_output=false`.
2. `fetch` with `raw_output=false`.
3. `tag <action|reading|junk> <idx1,idx2,...>` with `raw_output=false` for each tag batch
4. `status` with `raw_output=false` for iterative tagging rounds.
5. if `status` says there are still untagged rows, keep looping:
   run `tag ...` with `raw_output=false`, then `status` with `raw_output=false`.
6. stop the loop only when `status` says `everything is tagged, review these tags`.
7. run `status` once with `raw_output=true` for final verification.
8. if user requests tag changes, run `tag ...` with `raw_output=false`, then `status` with `raw_output=true` again.
9. run `push` only after user confirmation, with `raw_output=false` and `timeout_seconds=300`.
10. after `push`, run `print` with `raw_output=true`.

## Commands
- `fetch` - pull inbox threads via `botbot-gmail`, write `/tmp/tag_gmail.ndjson`, print rows.
- `rules` - print base tagging rules + Google Tasks rules (`email_gps` by default).
- `tag <action|reading|junk> <idx1,idx2,...>` - set one tag for comma-separated local queue indices.
- `status` - validate tags, clear invalid tags, print only 20 untagged rows per run until fully tagged.
- `push` - apply labels/trash to Gmail, clean queue state, and output JSON counts (`labelled`, `removed`, `labels_removed`).
- `print` - show untagged first, then grouped `action`/`reading`/`junk`.

## Boundaries
- Do not format outputs that are already formatted by the script.
- Default policy: when `raw_output` is not explicitly specified for a command, treat it as `raw_output=false`.
- `idx` is local queue id, not Gmail `threadid`.
- Keep `threadid` hidden from user-facing output.
- For the `tag` subcommand, EXPLICITLY list every idx

## Queue File
- Path: `/tmp/tag_gmail.ndjson`
- Row schema: `{idx, subject, from, snippet, threadid, tag}`

## Dependencies
Expected scripts:
- `botbot-gmail/scripts/botbot_gmail.py`
- `botbot-gtask/scripts/botbot_gtask.py`

Resolution base: main skills directory via current skill path (`../../`).
If missing, command fails with a clear "not installed" error.

## Examples
```bash
uv run <path-to-skill>/scripts/meagent_gmail_tagging.py fetch
uv run <path-to-skill>/scripts/meagent_gmail_tagging.py rules
uv run <path-to-skill>/scripts/meagent_gmail_tagging.py tag action 4,5,8
uv run <path-to-skill>/scripts/meagent_gmail_tagging.py status
uv run <path-to-skill>/scripts/meagent_gmail_tagging.py push
uv run <path-to-skill>/scripts/meagent_gmail_tagging.py print
```
