---
type: adr
title: "Separate final architecture decisions from research logs"
tags: [devtools]
timestamp: 2026-07-11T08:10:57Z
---

# Separate ADRs from Research Logs

Status=Accepted

## Context

The `okf-docs` skill previously supplied one decision-log format. It could record an architecture choice, but it did not provide a structured place for hypotheses, failed experiments, or unfinished next steps. Mixing those details into final decision records makes both the final choice and research history harder to find.

## Decision

Use standard Architecture Decision Records (ADRs) for final architecture choices. ADRs follow Context, Decision, and Consequences.

Add Research Decision Records (RDRs) for exploratory work. RDRs capture the context and hypothesis, every experiment and its result, the current state, and next actions. Append attempts to the same RDR. Create or update a separate ADR when the research leads to a final architecture choice.

## Consequences

Good:

- Final architecture choices stay concise and searchable.
- Negative research results remain discoverable and are not retried without cause.
- Paused work retains clear next actions.

Cost:

- Authors must choose the record type and sometimes maintain an RDR plus a related ADR.
