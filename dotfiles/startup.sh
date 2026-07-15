#!/usr/bin/env bash

set -o vi
export EDITOR=vim
alias gitpush="git pull --rebase && git push"

tmux0() {
    tmux new-session -As "$(basename "$PWD")-$(printf %s "$PWD" | md5sum | cut -c -7)"
}

# piweb web term works better when tmux is doing the buffering
[[ $IS_PIWEB == "1" ]] && tmux0
