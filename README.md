# mobot-skills

## Setup

- Git hooks: run `./scripts/setup-githooks.sh` once after clone.
- Dotfiles: from `dotfiles/`, run `./setup.sh` once. It symlinks files into `~` and loads `~/startup.sh` via `~/.bashrc`.
- PI extensions: `mkdir -p ~/.pi/agent && ln -sfn "$PWD/pi-extensions" ~/.pi/agent/extensions`
- Pi subagents: `mkdir -p ~/.pi/agent && ln -sfn "$PWD/pi-subagents" ~/.pi/agent/agents`
