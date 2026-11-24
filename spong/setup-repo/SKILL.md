---
name: setup-repo
description: setting up pre-commit and Git hooks for a repo
---

# Set Up Repository
1. Run the setup-precommit skill
2. Copy template files to "<repo>", preserving their relative paths.
3. Make both hooks in ".githooks" and "scripts/setup-githooks.sh" executable.
4. Run "scripts/setup-githooks.sh", add one-liner setup instructions to the repo's README / AGENTS.md equivalent, in the for devs section
5. Commit ".pre-commit-config.yaml", ".githooks/", and "scripts/setup-githooks.sh".
