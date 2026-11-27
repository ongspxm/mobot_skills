### Perf

Measurable speedups, trace analysis, and metric hillclimb.

1. Set one metric, target direction, stop rule, regression gate before edits.
2. Capture baseline + vet every number before acting or reporting:
   - Profile unmeasured run -> name limiter ("why not double?").
   - Match prod tuning on both sides: release flags, warm/cold cache, batching, same data.
   - Check math against hardware/time limits (cutting 10% step cannot save 50%).
   - Count errors; verify timed work actually ran (not cached, lazy, or dropped).
   - Run >=5 interleaved A/B/A/B samples; report median + spread (delta < spread = inconclusive). Use 1 run only for quick ballpark, and label it.
   - Report micro speedup + share of full end-to-end user path.
   - Dump large traces to sqlite or script -> find hot frames (file:line).
3. Pause at gate (spong-mode skill): show metric, vetted baseline, limiter, first tries; wait for "ok to go?".
4. After OK, copy remaining steps to todo.txt via todolist skill; update as you work.
5. Record each try in todo.txt (keep numeric A/B rows in "/tmp/perf-<topic>.tsv" if needed): decision, hypothesis, before->after artifact, kept or reverted.
6. Try fixes in mantra order, cheapest first:
   1. Skip unused work.
   2. Cache repeated work.
   3. Do less work per item.
   4. Defer work until needed.
   5. Move work off critical path.
   6. Run concurrently (split shared state first).
   7. Optimize hot algorithm or data layout.
7. Test one hypothesis per change -> measure after -> keep only if past noise and gate green; else revert full. Pause before commit/push.
8. On plateau, switch category or reread trace; never relax stop rule.

Reply with: metric and target, baseline to final delta, run count + spread, limiter, kept vs reverted tries, artifact path, next idea.
