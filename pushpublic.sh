#!/usr/bin/env bash

main_worktree=$(git worktree list --porcelain | sed -n '1s/^worktree //p')
current_worktree=$(git rev-parse --show-toplevel)
if [[ "$current_worktree" == "$main_worktree" ]]; then
    echo "pushpublic.sh must be run from a worktree, not the main worktree" >&2
    exit 1
fi

rm -rf pstack
rm -rf DEPRECATED
rm -rf .agents
