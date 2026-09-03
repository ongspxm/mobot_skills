# mobot-skills

## Setup

- Dotfiles: from `dotfiles/`, run `./setup.sh` once. It symlinks files into `~` and loads `~/startup.sh` via `~/.bashrc`.
- PI WEB plugins: `mkdir -p ~/.pi-web && ln -sfn "$PWD/pi-web-plugins" ~/.pi-web/plugins`
- PI extensions: `mkdir -p ~/.pi/agent && ln -sfn "$PWD/pi-extensions" ~/.pi/agent/extensions`
- Pi subagents: `mkdir -p ~/.pi/agent && ln -sfn "$PWD/pi-subagents" ~/.pi/agent/agents`
