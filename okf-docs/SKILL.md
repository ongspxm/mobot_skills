---
id: okf-docs
name: okf-docs
description: Use when you need to generate, maintain, or validate OKF repository documentation components.
---

# OKF Documentation

## Workflows
```sh
uv run --with pyyaml $skill_dirname/validate_okf.py
```

## When to Use
Use OKF docs to track one standalone idea, decision, or record per file.

## Boundaries
- Every `.md` file in `/docs`, except `index.md` and `log.md`, is an OKF Concept.
- YAML `tags` must match tokens in `docs/index.md`. Unlisted tags fail validation.
- Explain every non-self-explanatory registered tag in `docs/index.md`.
- Get context markers (project name, system constraints, environment names) from paths or Git origins. Use them in titles and descriptions.
- After creating or changing files, run `uv run --with pyyaml $skill_dirname/validate_okf.py` to sync concept timestamps from file modification times and check links, frontmatter, and tag limits.

## Document Formats
Use standard ADRs for final architecture choices. Use `$skill_dirname/type_adr.md`.

Use RDRs (Research Decision Records) for exploratory work: hypotheses, experiments, failures, current state, and next actions. Use `$skill_dirname/type_rdr.md`.

## Examples
```yaml
---
type: "<Specific concept type, prefably one word, like guidemap, runbook, dbtable, etc>"
title: "<[Project Name] Contextual Title>"
tags: [<list, match tags in docs/index.md>]
timestamp: <ISO 2026-07-09T22:04:00Z string>
---
```

### Root `docs/index.md` example

```markdown
# [Project Name]

Docs for [Project Name]. One-line project description.

## Registered taxonomies and tags
- **Component**: #bot, #data, #config
- **Feature**: #ticket-stages, #payment-utils

Tag notes:
- `#ticket-stages`: ticket lifecycle transitions and their guards.
- `#payment-utils`: payment-session creation, verification, and polling.

## Knowledge Maps
- [Decision Records](./decisions/index.md)
- [Research Records](./research/index.md)
```

## Folder Architecture
```text
docs/
|-- index.md             <-- Root index mapping global tags and maps
|-- decisions/
|   |-- index.md         <-- ADR index map
|   |-- log.md           <-- Sequential update ledger
|   `-- YYYY-MM-DD-x.md  <-- Final architecture decisions
`-- research/
    |-- index.md         <-- RDR index map
    |-- log.md           <-- Sequential update ledger
    `-- YYYY-MM-DD-x.md  <-- Exploratory research records
```

### `docs/<subfolder>/index.md` example

```markdown
# [Project Name] Knowledge Map

## Concepts
- [Service Authentication](./service-auth.md)
- [Database Backup Runbook](./database-backup.md)
- [Event Schema](./event-schema.md)

## Operations
- Read chronological changes in [Update Log](./log.md).
```
