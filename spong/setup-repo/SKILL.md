---
name: setup-repo
description: Set up pre-commit and Git hooks for a repo.
---

# Set Up Repository

1. Run setup-precommit skill.
2. Copy templates/ files to target repo, keeping relative paths.
3. Make both hooks in .githooks/ and scripts/setup-githooks.sh executable.
4. Split repo guidance by reader:
   - AGENTS.md: exact dev commands, non-obvious repo conventions, and boundaries agents need to follow.
   - README.md: project overview, human setup and usage, and public API or CLI reference.
   - docs/: detailed architecture, procedures, and subsystem reference.
   Keep AGENTS.md short. Do not repeat code descriptions or facts agents can find in the repo. Link to detailed docs instead.
5. Run scripts/setup-githooks.sh; add one-line setup note in README.md or the AGENTS.md dev section.
6. Commit .pre-commit-config.yaml, .githooks/, and scripts/setup-githooks.sh.
