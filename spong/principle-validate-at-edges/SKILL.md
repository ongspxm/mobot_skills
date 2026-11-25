---
name: principle-validate-at-edges
description: Parse and validate external data at boundaries. Keep core logic pure.
disable-model-invocation: true
---

# Validate at Edges

Parse and validate once where untrusted data enters.

- Validate CLI args, config, files, environment variables, and API data at the boundary.
- Trust internal types. Do not revalidate or add redundant nil checks inside.
- Keep business logic pure. Keep transport and framework types out of its public surface.
- Redundant checks inside internal callers add noise and mask upstream bugs -> remove them.
