---
name: why
description: Answer design rationale, regressions, and thresholds from repo history, docs, and issue/chat records.
---

# Why

Answer why code is shaped this way from historical record, not code guesses.

1. Search commit and blame history ("git log -S", "git log -L", "git blame") for origin and later edits.
2. When commit message is thin, check other records (examples, non-exhaustive: PR discussions via "gh pr view", GitHub issues via "gh issue list", devlogs such as "docs/devlog.md", design docs/ADRs/RFCs, Jira/Linear tickets, chat/incident threads).
3. Quote what authors wrote with exact source ID (commit SHA, PR/ticket ID, doc path, or date). Mark your own reasoning as inference and list what record does not answer.

Reply with: cited rationale timeline, author quotes vs inferences, open gaps in record.
