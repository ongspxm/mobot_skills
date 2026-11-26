### Handoff

Clean pause and cold-start resume across sessions.

#### Pause
1. Stop at atomic step; kill loose background work and make no irreversible writes.
2. Commit dirty edits as one "wip: <scope>" commit (note broken tree in body if red).
3. Update todo.txt (todolist skill) and log state in worklog.tsv (log-work skill).
4. If session hit repeated mistakes or non-obvious quirks, suggest 1-3 concrete fixes via reflect skill (proposals only; edit nothing without OK).
5. Report current step, file and branch pointers, and exact first resume action.

#### Resume
1. Read todo.txt, worklog.tsv, "git log -n 10", and "git diff" against base.
2. Missing or stale trail -> rebuild brief from active harness chat history, open branches/PRs ("gh pr list"), and recent commits/issues; check live repo state first.
3. Trust prior trail; diff done vs pending and do not redo finished steps.
4. Verify resume state once on real artifact, then run matching playbook for remaining work.

Reply with: stop/resume point, inherited vs redone work, branch/tree status, reflect suggestions (if any), next action.
