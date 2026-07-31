---
id: okf-docs
name: okf-docs
description: Use when you need to generate, maintain, or validate OKF repository documentation components.
---

# OKF Documentation

Use OKF docs for one standalone idea, decision, or record per file.

## Rules
- Every `.md` file under `docs/`, except `index.md` and `log.md`, is an OKF concept.
- Each concept needs YAML frontmatter with `type`, `title`, `tags`, and `timestamp`.
- Tags must be registered in `docs/index.md`; explain every non-obvious tag there.
- Use project, system-constraint, and environment context in titles and descriptions.
- During initialization, create only `docs/index.md`. Add subfolders, indexes, or logs only when the task requires them.

## Concept Types
Common types:
- `guide`: setup and normal workflows.
- `runbook`: repeatable operational procedures and troubleshooting.
- `adr`: architectural "why" decisions.
- `rdr`: experiments and exploratory research.
- `reference`: factual system or component documentation.

This list is not exhaustive. Any reasonable, descriptive concept type is valid.

Use standard ADRs for final architecture choices: `$skill_dirname/type_adr.md`.
Use RDRs for exploratory work, including hypotheses, experiments, failures, current state, and next actions: `$skill_dirname/type_rdr.md`.

## Format
```yaml
---
type: guide
title: "[Project Name] Contextual Title"
tags: [<registered tags>]
timestamp: 2026-07-09T22:04:00Z
---
```

`docs/index.md` is the root map for project context, registered tags, and any knowledge maps. Create separate map folders only when useful and requested. Knowledge maps should group concepts by purpose or type and expose useful metadata such as date and status, not only repeat a bare file list.

## Workflow
After creating or changing docs, run:

```sh
uv run --with pyyaml $skill_dirname/validate_okf.py
```

The validator syncs concept timestamps and checks frontmatter, tags, and links.
