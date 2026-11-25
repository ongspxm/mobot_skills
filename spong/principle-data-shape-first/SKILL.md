---
name: principle-data-shape-first
description: Design types and structures before logic. Make invalid states unrepresentable.
disable-model-invocation: true
---

# Data Shape First

Get the data shape right before logic.

- Replace scattered booleans and growing if/else chains with a table, registry, union, or state machine.
- In typed languages, brand distinct primitives and derive types from the authoritative schema.
- Do not force an abstraction over clear, local code that does not grow.
- Smell test: a new feature adds another synced boolean or copy-pasted branch -> switch to a state enum/table.
