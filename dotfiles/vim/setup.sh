#!/usr/bin/env bash
set -euo pipefail

plugins_dir="$HOME/.local/share/vim/pack/plugins/start"

plugin_urls=(
    https://github.com/dense-analysis/ale.git
    https://github.com/ctrlpvim/ctrlp.vim.git
    https://github.com/editorconfig/editorconfig-vim.git
    https://github.com/preservim/nerdtree
    https://github.com/ziglang/zig.vim.git
    https://github.com/Exafunction/codeium.vim.git
    https://github.com/ap/vim-buftabline.git
    https://github.com/itchyny/lightline.vim
    https://github.com/maximbaz/lightline-ale.git
    https://tpope.io/vim/fugitive.git
    https://github.com/mhinz/vim-signify.git
)

mkdir -p "$plugins_dir"
for url in "${plugin_urls[@]}"; do
    name="${url##*/}"
    name="${name%.git}"
    git clone --depth 1 "$url" "$plugins_dir/$name" || true
done
