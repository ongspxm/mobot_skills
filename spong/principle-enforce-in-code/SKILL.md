---
name: principle-enforce-in-code
description: Encode repeated rules and manual work in a lint, hook, type, or script.
---

# Enforce in Code

Prose decays. Gates stick.

- Lesson repeats: put in lint, hook, type, schema, check, or script.
- Repo review rules: script in ".githooks/", run from "pre-commit". Scope to passed or staged files.
- Repeated manual work: automate with script.
- Make tool safe to rerun and retry.
- Needs human judgment: keep in prose with one bad-vs-good example.
