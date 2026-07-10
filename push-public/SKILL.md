---
name: push-public
description: Publish main's tree on public as clean commits, without main history.
---

# PUSH-PUBLIC(1)

## NAME

`push-public` — snapshot `main` content onto `public`.

## SYNOPSIS

```bash
git fetch --all --prune
orig_ref=$(git symbolic-ref -q --short HEAD || git rev-parse --short HEAD)
git checkout main && git pull --ff-only origin main && git checkout "$orig_ref"
root=$(git rev-parse --show-toplevel)
if ! git worktree list --porcelain | grep -qx 'branch refs/heads/public'; then
  git -C "$root" worktree add .worktree-public public
fi
cd "$root/.worktree-public"
git read-tree --reset -u main
git diff --stat
git add -A
git commit -m "<type>: <actual change>"
git push origin public
```

## DESCRIPTION

`public` gets `main`'s files. Its commits stay separate. Use `.worktree-public`; keep it for later syncs. Never create another `public` checkout.

`read-tree --reset -u main` replaces tracked files and index with `main` while `HEAD` remains `public`.

Inspect `git diff` before committing. Use `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, or `test:`. One cohesive change: one commit. Mixed changes: split commits.
