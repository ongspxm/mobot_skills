---
type: decisionlog
title: "Build the OKF documentation skill"
tags: [devtools]
timestamp: 2026-07-10T15:59:56Z
---

# Develop the OKF Documentation Skill
Status=Accepted

Build `okf-docs`: a lightweight tool for documenting repository knowledge in a fixed, agent-searchable format.

## context

We needs a simple way to explain how things work and retain documentation over time. Free-form docs make information and implementation history harder for agents to find and use.

OKF fits this need because it is lightweight, has few required definitions, works well with Obsidian-style Markdown, and remains easy for agents to search. Its official minimum requirements are simple, so the skill includes its own validation script to ensure repository docs meet them. The skill also needs a specific decision-log format: architecture decisions need their rationale and history recorded where later agents can find them before changing an implementation.

Alternatives considered:

- Keep free-form Markdown and rely on commit history for context.
- Adopt a heavier documentation system with more required concepts and process.
- Build a lightweight OKF documentation skill with a decision-log format.

## Decision

Build the `okf-docs` skill. It defines an OKF format for repository documentation and includes a small custom validation script to enforce at least the official OKF minimum requirements.

Add a decision-log format to the skill. Use it to record architecture decisions, their context, and their consequences so future agents can understand why an implementation exists and how it evolved.

## Consequences

We now have a consistent, lightweight structure that is friendly to Obsidian and easy for agents to search. The custom validator provides a local check that docs meet the official OKF minimum requirements.

Architecture decisions have a durable, discoverable history outside of commit messages. Authors must follow the formats defined by the skill, run its validator, and maintain the associated documentation records.
