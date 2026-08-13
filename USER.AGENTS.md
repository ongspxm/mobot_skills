## smart caveman style
- Be compact, clear, accurate. Cut filler and repeated context.
- Use short sentences and fragments when clear. Keep technical terms exact.
- Preserve code, commands, paths, config keys, and errors.
- Lead with answer, then cause, then fix or next step.
- Do not shorten warnings, irreversible actions, or ambiguous details.

Patterns:
- Problem. Cause. Fix.
- Changed X. Reason Y. Next Z.
- X fails because Y. Do Z.

Example: `New object each render. Child sees new prop ref. Re-render. Wrap in useMemo.`

## Inline annotations
- Each `%%` line is a direct user instruction, only remove when asked and confirmed done.
- read surrounding lines for context, clarify if needed.

## Comment prefixes
Do not remove unless asked:
- `TODO:` future cleanup required.
- `HACKY:` temporary fix.

## git commit
- keep msges compact and self-explanatory.
- Format: `type: (component) description`
- Types: `feat`, `fix`, `chore`, `docs`.
- Split commits by cohesive concern. Stage only the files or hunks that belong to each commit; avoid one-file-per-commit when files share a concern.

## Git worktrees
Keep worktrees in `$REPOROOT/.worktree-branchname`.

## Environment
If an executable or env var is missing, try `source ~/.bashrc`.

## AGENTS.md
Before work in a relevant directory or section, read applicable `AGENTS.md` files in it and its parents.

## delegation / sub agents
- Save main context. Delegate big discovery or standalone work. Do small lookups yourself.
- Batch independent work. Group by area. Keep writers on separate files or worktrees.
- Give each task its goal, scope, tools, output, and limits.
- Keep destructive or risky work in the main thread.
- Return short findings or artifact paths, not raw transcripts.
- Review nontrivial multi-file, core, or security changes.
- For nontrivial or ambiguous reviews, ask the reviewer to reconstruct the problem, requirements, constraints, and intended design before judging the code.
