#!/usr/bin/env bash

DIRNAME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIRNAME" || exit 1

# A real ~/.vim may contain installed plugins; move it aside before switching.
if [ -e "$HOME/.vim" ] && [ ! -L "$HOME/.vim" ]; then
    echo "[ERR] Move ~/.vim out of the way before linking the dotfiles Vim config." >&2
    exit 1
fi

cpfile() {
    local name="$1"
    echo "[LOG] cpfile for $name"
    if [ "$name" = "setup.sh" ] || [ "$name" = "." ] || [ "$name" = ".." ]; then return; fi
    rm -f "$HOME/$name"
    ln -sfn "$DIRNAME/$name" "$HOME/$name"
}

# folders copying
for f in *; do
    [ "$f" = "vim" ] && continue
    cpfile "$f"
done
for f in .*; do cpfile "$f"; done
ln -sfn "$DIRNAME/vim" "$HOME/.vim"

# setup pa: https://github.com/biox/pa
rm -rf "$HOME/.local/share/pa"
mkdir -p "$HOME/.local/share"
ln -sfn "$HOME/docs/_pa" "$HOME/.local/share/pa"

ln -sfn "$DIRNAME/../USER.AGENTS.md" "$HOME/AGENTS.md"
ln -sfn "$HOME/AGENTS.md" "$HOME/CLAUDE.md"

if [ -L "$HOME/.agents/skills" ]; then
    rm "$HOME/.agents/skills"
fi
mkdir -p "$HOME/.agents/skills"
find "$HOME/.agents/skills" -mindepth 1 -maxdepth 1 -type l -delete
for s in "$DIRNAME/../spong"/*/; do
    ln -sfn "${s%/}" "$HOME/.agents/skills/$(basename $s)"
done
ln -sfn "$HOME/AGENTS.md" "$HOME/.agents/AGENTS.md"

aifiles() {
    echo "[LOG] aifiles for $1"
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
