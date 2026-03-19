## fdocs + some misc setup
### fdocs lifecycle
fdocs are tracked in `docs/fdocs/`. Each FD has a dedicated file (`fdXXX_title.md`) and `docs/fdocs/_INDEX.md` is generated from FD file frontmatter.
- `closed`: `closed` date is set
- `planned`: `planned` date is set and `closed` is empty
- `open`: `active=true` and `planned`/`closed` are empty
- `backlog`: default when none of the above apply

### fdocs commands
- fdocs init: initialize docs/fdocs/ scaffolding and seed templates
- fdocs new: create a new fdocs using template
- fdocs status: regenerate index and show active docs
- fdocs status --grooming: move closed docs into docs/fdocs/archive/
- fdocs close: close and archive a specific FD
- fdocs explore: print fdocs status plus recent repo activity
- fdocs verify: workflow to run verification on a fdoc
- fdocs deep: workflow to do research for a fdoc

### fdocs conventions
- fdocs files: `docs/fdocs/fdXXX_title.md` (`XXX` is zero-padded)
- Archive: `docs/fdocs/archive/`
- Source of truth: fdocs files (index is derived output)
- Date format: `YYYY-MM-DD` for `planned` and `closed`

### misc dev guide
Keep long-lived engineering rules in `docs/dev_guide/` and keep `AGENTS.md` concise.
Before doing anything, do a ls on the directory to see what rules are in place.
- Source of truth: `docs/dev_guide/*.md` (`README.md` is the index)
- Add one short section per rule with: intent, hard requirement, examples
- Prefer project-specific rules over generic style guidance
- If a rule changes behavior across the codebase, update the relevant FD and mention the rule id/title

### misc Inline Annotations (`%%`)
- Treat each `%%` line as a direct user instruction.
- Address every `%%` line, then remove it.
- If any `%%` instruction is ambiguous, ask for clarification before editing.

### misc git worktrees
- keep all git worktrees in "(repo root)/.worktree"
