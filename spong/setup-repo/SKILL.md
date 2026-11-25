---
name: setup-repo
description: Set up pre-commit and Git hooks for a repo.
---

# Set Up Repository

1. Run setup-precommit skill.
2. Copy templates/ files to target repo, keeping relative paths.
3. Make both hooks in .githooks/ and scripts/setup-githooks.sh executable.
4. Run scripts/setup-githooks.sh; add one-line setup note in repo README or AGENTS.md dev section.
5. Commit .pre-commit-config.yaml, .githooks/, and scripts/setup-githooks.sh.
