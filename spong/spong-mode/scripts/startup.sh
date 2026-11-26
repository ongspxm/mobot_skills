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
    local mode="-d" wt githome branch
    while [ $# -gt 0 ]; do
        case "$1" in
            -D) mode="-D"; shift ;;
            -k) mode=""; shift ;;
            -h|--help) echo "usage: gwtdel [-D|-k]"; return 0 ;;
            *) echo "gwtdel: unknown flag: $1" >&2; return 2 ;;
        esac
    done
    wt=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "gwtdel: not in git repo" >&2; return 1; }
    githome=$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")
    if [ "$wt" = "$githome" ]; then
        echo "gwtdel: in main worktree" >&2
        return 1
    fi
    branch=$(git symbolic-ref --quiet --short HEAD 2>/dev/null || true)
    git -C "$githome" worktree remove "$wt" || return $?
    cd "$githome" || return 1
    if [ -n "$mode" ] && [ -n "$branch" ]; then
        git branch "$mode" "$branch"
    fi
}
