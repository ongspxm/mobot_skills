#!/usr/bin/env bash

# A real ~/.vim may contain installed plugins; move it aside before switching.
if [ -e "$HOME/.vim" ] && [ ! -L "$HOME/.vim" ]; then
    echo "Move ~/.vim out of the way before linking the dotfiles Vim config." >&2
    exit 1
fi

cpfile() {
    echo "cpfile for $1"
    if [ "$1" == "$0" ]; then return; fi
    rm "$HOME/$1"
    ln -s "$(pwd)/$1" "$HOME"
}

for f in *; do
    [ "$f" = "vim" ] && continue
    cpfile "$f"
done
for f in .*; do cpfile "$f"; done

# setup pa: https://github.com/biox/pa
rm -rf "~/.local/share/pa"
mkdir -p ~/.local/share
ln -sfn "~/docs/_pa" "~/.local/share/pa"

ln -sfn "$(pwd)/vim" "$HOME/.vim"

ln -sfn "$(pwd)/../USER.AGENTS.md" "$HOME/AGENTS.md"
ln -sfn "$HOME/AGENTS.md" "$HOME/CLAUDE.md"

mkdir -p "$HOME/.agents/skills"
ln -sfn "$HOME/AGENTS.md" "$HOME/.agents/AGENTS.md"

aifiles() {
    echo "aifiles for $1"
    mkdir -p "$1"
    ln -sfn "$HOME/AGENTS.md" "$1/AGENTS.md"
    ln -sfn "$HOME/.agents/skills" "$1/skills"

    if [[ $(basename $1) == ".copilot" ]]; then
        ln -sfn "$HOME/AGENTS.md" "$1/copilot-instructions.md"
    fi
}

aifiles "$HOME/.codex"
aifiles "$HOME/.claude"
aifiles "$HOME/.cursor"
aifiles "$HOME/.pi/agent"
aifiles "$HOME/.prime/agent"
aifiles "$HOME/.config/opencode"
aifiles "$HOME/.copilot"

grep -Fqx "source \$HOME/startup.sh" ~/.bashrc || echo "source \$HOME/startup.sh" >> ~/.bashrc
ln -sfn "$HOME/.vim/vimrc" "$HOME/.vimrc"

echo "run vim setup too? ctrl+c to exit" && read
bash $HOME/.vim/setup.sh
