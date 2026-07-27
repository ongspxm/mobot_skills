# mobot-skills

## Setup

- **Dotfiles:** from `dotfiles/`, run `./setup.sh` once. It symlinks files into `~` and loads `~/startup.sh` via `~/.bashrc`.
- **PI WEB plugins:**
  ```bash
  mkdir -p ~/.pi-web && ln -sfn "$PWD/pi-web-plugins" ~/.pi-web/plugins
  ```
  Hard reload PI WEB after changes.
- **Pi subagents:** link role prompts into Pi from the repository root:
  ```bash
  mkdir -p ~/.pi/agent && ln -sfn "$PWD/pi-subagents" ~/.pi/agent/agents
  ```
  Changes are available immediately.
