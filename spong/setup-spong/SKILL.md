---
name: setup-spong
description: Set up spong skills, AGENTS.md, and dotfiles links via dotfiles/setup.sh.
---

# Set Up Spong

Run "dotfiles/setup.sh" to symlink dotfiles, "USER.AGENTS.md", "spong" skills, and agent tool configs into "$HOME".

1. Locate and run "dotfiles/setup.sh" non-interactively (accepts vim plugin prompt):

```bash
setup="./dotfiles/setup.sh"
[ -f "$setup" ] || setup="$(realpath "${SPONGPATH:?set SPONGPATH or run from repo root}")/../../dotfiles/setup.sh"
printf '\n' | bash "$setup"
```

2. Source "$HOME/startup.sh" (symlinked from "dotfiles/startup.sh") if current shell needs helpers ("tmux0", "tuicr", "gwtadd", "gwtdel").
3. Verify installed links:

```bash
ls -la ~/AGENTS.md ~/startup.sh ~/.agents/skills ~/.copilot/skills
```
