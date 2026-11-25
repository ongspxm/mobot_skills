---
name: principle-cut-layers
description: Inline one-caller wrappers. Shrink mutable state. Cut reader load.
disable-model-invocation: true
---

# Cut Layers

Cut layers and hidden state. Keep data flow easy to trace.

- Inline one-caller functions, pass-through wrappers, and single-impl interfaces/classes/adapters.
- Shrink state scope: return values, locals, fields, module state, globals.
- Derive values instead of syncing copies.
- State an invariant once at the boundary, not in every consumer.
