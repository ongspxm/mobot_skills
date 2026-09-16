---
id: okf-docs
name: okf-docs
description: Create, update, and check OKF repository docs.
---

# OKF Documentation

Use one idea per concept file. Keep decisions in `docs/adr_log.md` as a dated list, newest first.

## Rules

- Every `.md` file under `docs/`, except `index.md` and `adr_log.md`, is a concept.
- Each concept needs YAML frontmatter with `type`, `title`, `tags`, and `timestamp`.
- Register all tags in `docs/index.md`.
- Include useful project and environment context.
- At setup, create only `docs/index.md`. Add folders or indexes when needed.

## Types

- `guide`: setup and normal use.
- `runbook`: repeatable tasks and fixes.
- `adr`: decisions and their reasons.
- `rdr`: experiments and research.
- `reference`: facts about a system or part.

Other clear types are allowed.

Use `type_adr.md` for decisions. Record each one as a short Y-statement in `docs/adr_log.md`. Do not create separate ADR files.

Use `type_rdr.md` for research, including hypotheses, tests, failures, current state, and next steps.

## Format

```yaml
---
type: guide
title: "[Project Name] Contextual Title"
tags: [<registered tags>]
timestamp: 2026-07-09T22:04:00Z
---
```

`docs/index.md` maps project context, tags, and other knowledge maps. Maps should group docs by purpose or type and show useful details such as dates and status.

## Workflow

After changing docs, run:

```sh
uv run --with pyyaml $skill_dirname/validate_okf.py
```

The validator updates timestamps only for real content changes. It checks frontmatter, tags, and links.
