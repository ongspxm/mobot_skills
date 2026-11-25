---
name: log-work
description: Log observations and work done via log.sh. Use for /log-work, long multi-step tasks, or reviewing past decisions.
---

# Log Work

Keep one append-only TSV at worklog.tsv.
Always use scripts/log.sh; it creates file and formats rows.

## Log row

Run "$SPONGPATH/../log-work/scripts/log.sh [-f <logfile>] <decision> <why> <evidence> <result>".
Without "-f", it picks "$(git rev-parse --show-toplevel)/worklog.tsv" (or "./worklog.tsv" outside git).

- ts: UTC ISO8601 (added by log.sh).
- decision: choice or action, one line.
- why: plain reason, no jargon.
- evidence: real pointer (commit sha, "file:line", artifact path), no prose.
- result: state ("tests green", "reverted", "open", "blocked").

## Rules

- Log real decision points: forks, checked units, pivots/reverts, blockers, loop steps. Skip trivial noise.
- Append only. Never edit or delete old rows; add new row to override wrong call.
- Cells stay plain ASCII and single-line.
- Commit worklog.tsv only when asked or when PR needs trail to prove work.
- Before handback or on review, read log ("column -s$'\t' -t worklog.tsv"), verify each evidence pointer, and list weak proof or open items.

## Examples

```bash
LOGSH="$SPONGPATH/../log-work/scripts/log.sh"

"$LOGSH" "use stdlib csv over pandas" "small files, zero new deps" "src/import.py:12" "open"
"$LOGSH" "revert pool cache" "failed OOM test" "commit 9d4e210, bench/oom.log" "reverted"
"$LOGSH" "supersede 09:15Z row: keep pandas" "xlsx fixture failed" "tests/test_import.py:48" "tests green"
"$LOGSH" -f .audit/auth.tsv "use jwt" "stateless workers" "src/auth.py:8" "open"
```
