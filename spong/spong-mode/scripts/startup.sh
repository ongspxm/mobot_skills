#!/usr/bin/env bash

set -o vi
export EDITOR=vim

tmux0() {
    n="$(basename "$(realpath .)")-$(realpath . | md5sum | cut -c -7)"
    TERM=tmux-256color tmux -u new-session -As "${n//[.:]/_}"
}

tuicr() {
    command tuicr --stdout "$@"
}

# git stuffz
alias gitpush="git pull --rebase && git push"
alias gwt="git worktree"
gwtadd() {
    gitbranch=${1:-$(git rev-parse --short HEAD)}
    githome=$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")
    gitpath=$(echo "$gitbranch" | tr -cd '[:alnum:]' | tr '[:upper:]' '[:lower:]')
    if [ -n "$1" ] && ! git show-ref --verify --quiet "refs/heads/$gitbranch"; then
        git worktree add -b "$gitbranch" "$githome/.wt-$gitpath" HEAD
    else
        git worktree add "$githome/.wt-$gitpath" "$gitbranch"
    fi
}
gwtdel() {
    git worktree remove "$(pwd)"
}
