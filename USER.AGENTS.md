## Response style
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
- Each `%%` line is a direct user instruction. Complete it, then remove it.
- Ask before editing if a `%%` instruction is ambiguous.

## Comment prefixes
Do not remove unless asked:
- `TODO:` future cleanup required.
- `HACKY:` temporary fix.

## Commit messages
- Compact and self-explanatory.
- Format: `type: (component) description`
- Types: `feat`, `fix`, `chore`, `docs`.
- Split commits by cohesive concern. Stage only the files or hunks that belong to each commit; avoid one-file-per-commit when files share a concern.

## Git worktrees
Keep worktrees in `$REPOROOT/.worktree-branchname`.

## Environment
If an executable or env var is missing, try `source ~/.bashrc`.

## AGENTS.md
Before work in a relevant directory or section, read applicable `AGENTS.md` files in it and its parents.
