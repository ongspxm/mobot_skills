#!/usr/bin/env bash

set -o vi
export EDITOR=vim
command -v fzf >/dev/null && eval "$(fzf --bash)"

if command -v xset >/dev/null 2>&1 && [ -n "${DISPLAY:-}" ]; then
    xset s off && xset -dpms && xset s noblank
fi

tmux0() {
    pwd0=$(realpath .)
    tmux new-session -As "$(basename "$pwd0")-$(printf %s "$pwd0" | md5sum | cut -c -7)"
}

tuicr() {
    command tuicr --stdout "$@"
}

sshport() {
    local box=$1
    shift
    local -a ssh_args=()
    for port in "$@"; do
        ssh_args+=(-L "$port:localhost:$port")
    done
    # shellcheck disable=SC2029
    ssh "${ssh_args[@]}" "$box"
}

# git stuffz
alias gitpush="git pull --rebase && git push"
alias gwt="git worktree"
gwtadd() {
    gitbranch=${1:-$(git rev-parse --short HEAD)}
    githome=$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")
    gitpath=$(echo "$gitbranch" | tr -cd '[:alnum:]' | tr '[:upper:]' '[:lower:]')
    if [ -n "$1" ] && ! git show-ref --verify --quiet "refs/heads/$gitbranch"; then
        git worktree add -b "$gitbranch" "$githome/.worktree-$gitpath" HEAD
    else
        git worktree add "$githome/.worktree-$gitpath" "$gitbranch"
    fi
}
