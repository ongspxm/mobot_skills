#!/usr/bin/env bash

cpfile() {
    if [ "$1" == "$0" ]; then return; fi
    rm "$HOME/$1"
    ln -s "$(pwd)/$1" "$HOME"
}

for f in *; do cpfile "$f"; done
for f in .*; do cpfile "$f"; done

grep -Fqx "source \$HOME/startup.sh" ~/.bashrc || echo "source \$HOME/startup.sh" >> ~/.bashrc
