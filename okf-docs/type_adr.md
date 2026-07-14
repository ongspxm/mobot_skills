# STANDARD ARCHITECTURE DECISION RECORD (ADR)

```markdown
---
type: adr
title: "<Action-oriented title>"
tags: [<tags from docs/index.md>]
timestamp: <ISO 2026-07-09T09:38:26Z string>
---

# [Decision Name]

Status=[Proposed | Accepted | Superseded by Link]

## Context
[Problem, durable constraints, and options.]

## Decision
[Chosen architectural direction, alternatives and why it wins.]

## Consequences
[Durable gains, costs, risks, limits, and migration impact.]
```

# ADR STRUCTURE

ADRs record final architecture choices. Use RDRs for research and iterations.

Nygard order: **Context -> Decision -> Consequences**.

- **Context**: problem, facts, constraints, options. No rationale or tradeoffs.
- **Decision**: chosen architecture and rationale. Name a product, protocol, or pattern only when its selection is the decision.
- **Consequences**: durable gains, costs, limits, risks, follow-up, migration impact. Use `Good:` and `Cost:` when useful.

## EXCLUDE IMPLEMENTATION DETAILS

Record architectural **what** and **why**, not code-level **how**.

Exclude code, file/class/function names, API routes and fields, schemas, UI layouts, config values, task lists, test cases, and step-by-step build, rollout, or migration instructions. Put them in a design/RFC, runbook, README, issue, PR, or code.

Rule of thumb: if a normal refactor makes the ADR incorrect, remove or generalize that detail.

Exception: include an implementation detail when it is the architecture choice, such as Kafka for asynchronous event delivery.

Example: **Decision**: retain original history; do not map source messages to relayed messages. **Consequences**: simpler state; edits become extra messages, not in-place updates.

# INSTRUCTIONS

1. Get Context, Decision, and Consequences from input or Git diff.
2. Keep rationale in `## Decision`; benefits and costs in `## Consequences`; exclude code-level detail.
3. Create `$REPO_ROOT/docs/decisions/YYYY-MM-DD-<slug>.md`.
4. Add an entry at the top of its date in `$REPO_ROOT/docs/decisions/log.md`.

# `log.md` FORMAT

```markdown
# Directory Update Log

## 2026-07-09
- (create) Established 2026-07-09-use-postgres.md to move ledger data out of flat files.
- (update) Added database tags to root index file.

## 2026-06-15
- (delete) Deprecated custom JWT auth scheme in 2025-11-04-custom-auth.md.
```
