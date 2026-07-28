#!/usr/bin/env bash

set -o vi
export EDITOR=vim
command -v fzf >/dev/null && eval "$(fzf --bash)"

if command -v xset >/dev/null 2>&1 && [ -n "${DISPLAY:-}" ]; then
    xset s off && xset -dpms && xset s noblank
fi

# piweb web term works better when tmux is doing the buffering
tmux0() {
    pwd0=$(realpath .)
    tmux new-session -As "$(basename "$pwd0")-$(printf %s "$pwd0" | md5sum | cut -c -7)"
}

# git stuffz
alias gitpush="git pull --rebase && git push"
alias gwt="git worktree"
gwtadd() {
    gitbranch=${1:-$(git rev-parse --short HEAD)}
    githome=$(git rev-parse --show-toplevel)
    gitpath=$(echo "$gitbranch" | tr -cd '[:alnum:]' | tr '[:upper:]' '[:lower:]')
    if [ -n "$1" ] && ! git show-ref --verify --quiet "refs/heads/$gitbranch"; then
        git worktree add -b "$gitbranch" "$githome/.worktree-$gitpath" HEAD
    else
        git worktree add "$githome/.worktree-$gitpath" "$gitbranch"
    fi
}
