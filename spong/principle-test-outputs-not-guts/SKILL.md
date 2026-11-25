---
name: principle-test-outputs-not-guts
description: Test observable behavior through public interfaces. Not internal calls or state.
disable-model-invocation: true
---

# Test Outputs, Not Guts

Test what callers observe.

- Assert return values, errors, persisted state, and effects on outside systems.
- Do not assert private helper calls, internal call order, or intermediate data.
- Sanity check each test: if behavior broke, would it fail? If internals changed, would it still pass?
- Test both sides of a rule: a case where it succeeds and a concrete bad input that triggers the error/guard.
