---
name: push-public
description: Publish main's tree on public as clean commits, without main history.
---

# Push Public

Publish "main" as clean commits on "public/main". Public keeps its own history.

```bash
if ! git remote get-url public >/dev/null 2>&1; then
  echo "public remote missing" >&2
  exit 1
fi

git fetch public main
git fetch origin main --prune
orig_ref=$(git symbolic-ref -q --short HEAD || git rev-parse --short HEAD)
git checkout main && git pull --ff-only origin main && git checkout "$orig_ref"

root=$(git rev-parse --show-toplevel)
if ! git worktree list --porcelain | grep -qx 'branch refs/heads/public'; then
  git -C "$root" worktree add .wt-public public
fi

cd "$root/.wt-public"
before=$(git rev-parse HEAD)
git read-tree --reset -u main
git reset
[[ -e pushpublic.sh ]] && bash pushpublic.sh

git diff --stat
git diff

git push public public:main
git log --oneline "$before..HEAD"
```

Keep ".wt-public" for later syncs. Never create another "public" checkout.
"git read-tree --reset -u main" replaces the tracked tree and index with "main"; "HEAD" stays "public".
do "git status". if shows unstaged changes, continue. No changes means nothing to publish.
Read the full "git diff" before every commit. Group files and hunks by concern using git commit rules.

## pushpublic.sh
this script will cleanup the state before committing
cleanup can include things like removing secrets, logfiles, artifacts, etc etc
check that pushpublic.sh start with this guard, put it at the top of the file. add it if missing.

```
main_worktree=$(git worktree list --porcelain | sed -n '1s/^worktree //p')
current_worktree=$(git rev-parse --show-toplevel)
if [[ "$current_worktree" == "$main_worktree" ]]; then
    echo "pushpublic.sh must be run from a worktree, not the main worktree" >&2
    exit 1
fi
```
