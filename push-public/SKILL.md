---
name: push-public
description: Publish main's tree on public as clean commits, without main history.
---

# Push Public

## Workflows
```bash
git fetch --all --prune
orig_ref=$(git symbolic-ref -q --short HEAD || git rev-parse --short HEAD)
git checkout main && git pull --ff-only origin main && git checkout "$orig_ref"
root=$(git rev-parse --show-toplevel)
if ! git worktree list --porcelain | grep -qx 'branch refs/heads/public'; then
  git -C "$root" worktree add .worktree-public public
fi
cd "$root/.worktree-public"
before=$(git rev-parse HEAD)
git read-tree --reset -u main   # stages main tree into index
git reset                       # unstage: index back to HEAD, worktree keeps main tree
git diff --stat                 # now plain diff shows all changes vs public
git diff
# read full diff, then group+commit (below); push when done
git push origin public
git log --oneline "$before..HEAD" # commits created
```

## When to Use
`public` gets `main`'s files. Its commits stay separate. Use `.worktree-public`; keep it for later syncs. Never create another `public` checkout.

`read-tree --reset -u main` replaces tracked files and index with `main` while `HEAD` remains `public`.

After read-tree + reset, `git status` shows all changes unstaged. Review via `git diff`, stage per concern. No unstaged changes = nothing to do, push nothing.

Always read the full `git diff` (not just `--stat`) before any commit; do not invent messages from filenames. Split by cohesive concern: stage only the files or hunks that belong to each commit. Prefer docs, then config/tooling, then one skill/feature area, then leftover chore. One concern = one commit (`feat:`/`fix:`/`chore:`/`docs:`/`refactor:`/`test:`); message must match that commit's diff. Do not one-file-per-commit when files share a concern; `git add -A` only when the whole remaining diff is one concern.
