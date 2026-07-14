---
type: adr
title: "Move skills away from manpage format"
tags: [devtools]
timestamp: 2026-07-12T08:30:34Z
---

# Move Skills Away from Manpage Format

Status=Accepted

## Context

Skill instructions must be quick to scan during execution. The manpage layout adds headings and boilerplate that do not improve task guidance, making skills longer and distracting from the required actions.

## Decision

Stop requiring manpage-style sections such as `NAME`, `SYNOPSIS`, and `DESCRIPTION` for skills. Write concise, task-oriented `SKILL.md` files using only sections that help execution, such as purpose, when to use, steps, boundaries, examples, and verification. Keep YAML frontmatter where the skill loader requires it.

Apply this format to new skills and when existing skills are materially revised. Do not reformat existing skills solely for consistency.

## Consequences

Good:

- Skills are shorter and easier to follow.
- Authors can express the workflow directly instead of fitting it into a command-reference template.

Cost:

- Skill layouts will vary when different sections are useful.
- Existing manpage-style skills remain until changed for another reason.
