---
name: principle-delete-first
description: Delete dead code and do cleanup before building. Prefer native stdlib, smallest diff wins.
disable-model-invocation: true
---

# Delete First

Code is liability. Remove before you build.

- Delete dead code, unused flags, stub refs, and speculative guards first.
- Prefer stdlib, native features, and reuse over new code.
- Consolidate repeated decisions behind one source of truth.
- Migrate internal callers and delete the old API in one wave. Do not keep throwaway compat shims.
- Make the smallest diff that solves observed usage, not hypothetical edge cases.
