set -o vi
export EDITOR=vim
alias gitpush="git pull --rebase && git push"

# piweb web term works better when tmux is doing the buffering
[[ $IS_PIWEB == "1" ]] && tmux new-session -As "$(basename $(pwd))-$(echo $(pwd) | md5sum | cut -c -7)"
