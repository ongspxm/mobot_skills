---
name: blast-radius
description: Find hidden breakage beyond direct callers and prove one safety fact by running real code.
disable-model-invocation: true
---

# Blast Radius

Find what breaks beyond direct symbol search before merge. Prove safety by run, not writeup.

## Proof ladder

Push each safety fact as far down as cheap; name where it stopped:
1. Claimed in prose (worthless alone).
2. Pointed to file:line or dependency source.
3. Walked failure path step by step.
4. Ran script or test calling real code that fails loud if wrong (default target).
5. Reproduced in running app.

## Steps

1. Read diff, commits, and changed symbols or contracts, including implicit behavior.
2. Name one or two core facts safety depends on. Spend time here, not listing maybes.
3. Check where symbol search stops. Examples include, but are not limited to:
   - JSON/DB/wire/config formats read by another script or service.
   - Async/microtask/teardown/lock order.
   - Pinned dependency source or local patches.
   - Feature flags, env vars, string keys, or downstream side effects via shared state or events.
4. Prove step 2 fact via principle-run-it-yourself skill: run smallest script or test on real code and capture output.
5. Separate confirmed risks (file:line, likelihood, cost, check) from cleared checks. Cite real file:line; never invent callers or APIs.

Reply with: what changed, safety fact + proof level + real output (or UNPROVEN), confirmed risks, cleared checks, cheapest repro/test.
