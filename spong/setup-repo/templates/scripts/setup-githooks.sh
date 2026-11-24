#!/usr/bin/env bash
set -euo pipefail

root=$(git rev-parse --show-toplevel)
git -C "$root" config core.hooksPath .githooks

printf 'Configured Git hooks: %s\n' "$root/.githooks"
