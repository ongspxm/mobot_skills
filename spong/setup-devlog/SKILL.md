---
name: setup-devlog
description: Set up docs/devlog.md and AGENTS.md devlog interface for a repo.
---

# Set Up Devlog

Create "docs/devlog.md" from "templates/docs/devlog.md" and add devlog rules to "AGENTS.md" in target repo.

1. Read target "AGENTS.md" and "docs/devlog.md" if present. Draft exact changes -> pause at spong-mode gate before writing.
2. Create "docs/devlog.md" only if missing (never overwrite existing log):

```bash
top=$(git rev-parse --show-toplevel)
tpl="${SPONGPATH:-$HOME/.agents/skills/spong-mode}/../setup-devlog/templates/docs/devlog.md"
[ -f "$tpl" ] || tpl="$top/spong/setup-devlog/templates/docs/devlog.md"
mkdir -p "$top/docs"
if [ ! -e "$top/docs/devlog.md" ]; then
  sed "s/^## YYYY-MM-DD /## $(date +%F) /" "$tpl" > "$top/docs/devlog.md.tmp"
  mv "$top/docs/devlog.md.tmp" "$top/docs/devlog.md"
fi
```

3. Add "# devlog" section to "$top/AGENTS.md" if missing:

```bash
agents="$top/AGENTS.md"
if ! grep -q '^# devlog' "$agents" 2>/dev/null; then
  if [ -s "$agents" ]; then
    [ -z "$(tail -c 1 "$agents")" ] || printf '\n' >> "$agents"
    printf '\n' >> "$agents"
  fi
  cat <<'EOF' >> "$agents"
# devlog (your interface with dev)
- dev gives task details via "docs/devlog.md"; read only portions relevant to task
- read "docs/devlog.md" and draft entry first; NEVER edit without explicit OK on draft
- Put one blank line before each "## YYYY-MM-DD ..." entry.
- CONSISTENCY: clarify when devlog details mismatch what you are asked to do
EOF
fi
```

4. Verify "docs/devlog.md" and "AGENTS.md" with "git status" and "git diff". Commit only when asked.
