# Design Notes
- If a `--config` flag is provided, that explicit path still takes precedence.
- Code style: if a function is only used in one place, inline it; keep code clean, tight, and terse.
- Styling requirement: prefer low abstraction; avoid unnecessary helper layers and keep implementations direct.
- IMPT: make sure oni ascii chars in all the files

# Deprecated skills
- for skill that are no longer maintained, they will be moved to the DEPRECATED directory.
- they are NOT MEANT TO BE TOUCHED

# skill-prefix
## botbot
- For any `botbot-xxx` skill, the default runtime config file location must be under `~/.botbot`.
- Follow the existing convention: `~/.botbot/<skill-name>.json` (for example, `~/.botbot/botbot-gcal.json`).

## meagent
- `meagent-xxx` skills are reserved for the meagent bot, a bulter service bot.
- each skill should represent one task, and the task name should be the skill name.

# user AGENTS.md
USER.AGENTS.md is linked to ~/AGENTS.md (and agent dirs) via dotfiles/setup.sh, and loaded in all repos and subdirs.

# spong
Edit Spong skill source under spong/. Root setup-spong symlink points to spong/setup-spong/ for skill discovery.

# devlog (your interface with dev)
- dev gives task details via "docs/devlog.md"; read only portions relevant to task
- read "docs/devlog.md" and draft entry first; NEVER edit without explicit OK on draft
- Put one blank line before each "## YYYY-MM-DD ..." entry.
- CONSISTENCY: clarify when devlog details mismatch what you are asked to do
