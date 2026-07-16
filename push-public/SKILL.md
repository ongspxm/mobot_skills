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
git read-tree --reset -u main
git diff --stat
git diff
# read full diff, then group+commit (below); push when done
git push origin public
git log --oneline "$before..HEAD" # commits created
```

## When to Use
`public` gets `main`'s files. Its commits stay separate. Use `.worktree-public`; keep it for later syncs. Never create another `public` checkout.

`read-tree --reset -u main` replaces tracked files and index with `main` while `HEAD` remains `public`.

Always read the full `git diff` (not just `--stat`) before any commit; do not invent messages from filenames. Split by cohesive concern with path-scoped `git add` — prefer docs, then config/tooling, then one skill/feature area, then leftover chore. One concern = one commit (`feat:`/`fix:`/`chore:`/`docs:`/`refactor:`/`test:`); message must match that commit's diff. Do not one-file-per-commit when files share a concern; `git add -A` only when the whole remaining diff is one concern.
