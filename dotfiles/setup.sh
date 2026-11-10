#!/usr/bin/env bash

# A real ~/.vim may contain installed plugins; move it aside before switching.
if [ -e "$HOME/.vim" ] && [ ! -L "$HOME/.vim" ]; then
    echo "Move ~/.vim out of the way before linking the dotfiles Vim config." >&2
    exit 1
fi
cd "$(dirname "$0")"

cpfile() {
    if [ "$1" == "$0" ]; then return; fi
    rm "$HOME/$1"
    ln -s "$(pwd)/$1" "$HOME"
}

for f in *; do
    [ "$f" = "vim" ] && continue
    cpfile "$f"
done
for f in .*; do cpfile "$f"; done

mkdir -p $HOME/.codex
ln -sfn "$(pwd)/../USER.AGENTS.md" "$HOME/.codex/AGENTS.md"
ln -sfn "$(pwd)/../USER.AGENTS.md" "$HOME/AGENTS.md"

ln -sfn "$(pwd)/vim" "$HOME/.vim"
ln -sfn "$HOME/.vim/vimrc" "$HOME/.vimrc"
bash $HOME/.vim/setup.sh

grep -Fqx "source \$HOME/startup.sh" ~/.bashrc || echo "source \$HOME/startup.sh" >> ~/.bashrc
