---
type: guide
title: "Write concise task-oriented skills"
tags: [devtools]
timestamp: 2026-07-12T14:03:44Z
---

# Write Concise Task-Oriented Skills

Use this guide for new `SKILL.md` files and material revisions.

## Format

Start with YAML frontmatter:

```yaml
---
name: tool-identifier
description: Brief summary. Use when the user asks to [trigger], [trigger], or manage [subject].
---
```

Then include only sections that help the agent complete the task:

```markdown
# Skill Title

## Overview
What the skill does.

## When to Use
- Trigger or input condition.

## Boundaries
- Limits and non-goals.

## Workflows
### If condition X
1. Do the required steps.

## Examples
Concrete input and expected result.
```

## Rules

- Omit sections with no useful content.
- Prefer direct steps over boilerplate.
- Keep examples only when they remove ambiguity.
- Do not use manpage sections such as `NAME`, `SYNOPSIS`, or `DESCRIPTION` unless they are genuinely useful.
- Use ASCII characters only.
