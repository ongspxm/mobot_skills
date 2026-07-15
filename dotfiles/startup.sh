#!/usr/bin/env bash

set -o vi
export EDITOR=vim

# piweb web term works better when tmux is doing the buffering
tmux0() {
    tmux new-session -As "$(basename "$PWD")-$(printf %s "$PWD" | md5sum | cut -c -7)"
}
[[ $IS_PIWEB == "1" ]] && tmux0

# git stuffz
alias gitpush="git pull --rebase && git push"
alias gwt="git worktree"
gwtadd() {
    gitcommit=${1:-$(git rev-parse --short HEAD)}
    githome=$(git rev-parse --show-toplevel)
    gitpath=$(echo "$gitcommit" | tr -cd '[:alnum:]' | tr '[:upper:]' '[:lower:]')
    gwt add "$githome/.worktree-$gitpath" "$gitcommit"
}
