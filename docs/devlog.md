# devlog
entries cover:
- why the change
- current situation vs new change
- rough shape of change per component/area

split multiline, one point per line.
states: TODO for new, DONE for completed, PARK for future, REJECT for wontfix.
ORDER: older entries at bottom
entry heading: ## YYYY-MM-DD <STATE>. <short title>
Put one blank line before each entry heading.

migration: start clean devlog.md with header copied over,
save old file as YYYYMMDD-devlog.md (YYYYMMDD = most recent date in old file).
NOTE: when migrating, MOVE TODO and PARK entries into new devlog.md (MOVE not COPY).

potential backlog:
- (... one-liner that i haven't expanded on ...)

todos:
- (... one-liner that i haven't expanded on ...)

## 2026-11-26 DONE. merge log-work into todolist
need one worktree scratchpad instead of overlapping todo.txt and worklog.tsv
currently both exclude at root and log why/evidence/result while worklog.tsv rots
remove log-work and cleanup spong env

## 2026-11-26 DONE. verifiable todolist checks
need way to audit open todo.txt items and mark done without redoing work
currently tasks lack checks and skill has no check-off loop
spong/todolist/SKILL.md. add "Check todolist" flow, require caveman form + "check:" or "/tmp/*" artifact per task

## 2026-11-26 DONE. setup devlog
need one place for task context and decisions between dev and agent
currently task specs live in chat only; add docs/devlog.md as shared log
docs/devlog.md. seed header and entry format; AGENTS.md. add devlog read/edit rules

## 2026-11-26 DONE. Group Pi config and extensions
Pi config and extensions lived at repo root.
Move both under pi-stuff/ and update setup and docs.
