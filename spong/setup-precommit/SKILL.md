---
name: setup-precommit
description: setting up pre-commit hooks for a repo
---

# Set Up Pre-commit
1. if pre-commit missing, do "pipx install pre-commit"
2. Create/update .pre-commit-config.yaml based on rules below
3. Validate config with "pre-commit run --all-files"
4. make sure ".pre-commit-config.yaml" is commited

pre-commit rules:
select whatever sane items from here: github.com/pre-commit/pre-commit-hooks/blob/main/.pre-commit-hooks.yaml

then figure out what language the repo is in, add the relevant rules.
Flag any missing language, check with user what they want to install.
- For Python, use only "astral-sh/ruff-pre-commit" with "ruff-check --fix" and "ruff-format".
- For shell files, use "shellcheck-py/shellcheck-py" and exclude "SC1091". Never install "codespell"
- For web files ("html/js/css"), use "biomejs/pre-commit" with version "> v2.1.3" and "biome-check".
