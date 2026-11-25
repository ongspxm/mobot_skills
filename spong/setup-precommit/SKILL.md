---
name: setup-precommit
description: Set up pre-commit hooks for a repo.
---

# Set Up Pre-commit

1. If pre-commit missing, run "pipx install pre-commit".
2. Create or update .pre-commit-config.yaml using rules below.
3. Validate with "pre-commit run --all-files".
4. Commit .pre-commit-config.yaml.

## Rules

- Pick sane generic hooks from github.com/pre-commit/pre-commit-hooks/blob/main/.pre-commit-hooks.yaml.
- Detect repo languages and add matching hooks; flag missing languages and ask user what to install.
- Python: use only "astral-sh/ruff-pre-commit" with "ruff-check --fix" and "ruff-format".
- Shell: use "shellcheck-py/shellcheck-py", exclude "SC1091". Never install codespell.
- Web (html/js/css): use "biomejs/pre-commit" (version "> v2.1.3") with "biome-check".
