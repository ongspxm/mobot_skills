---
name: principle-safe-to-rerun
description: Scripts and operations must be idempotent. Make them safe to re-run after crashes.
---

# Safe to Rerun

State-changing ops must be idempotent: same end state after reruns or mid-run crashes.

- Check current state vs goal before acting; apply only diff.
- Write to ".tmp" file then "mv" into place so crashes never leave half-written files.
- Tag locks/temp files (PID, timestamp, ".tmp") so next run spots stale leftovers and cleans them up.
- Test running twice and killing mid-step; add cleanup if leftovers break rerun.
