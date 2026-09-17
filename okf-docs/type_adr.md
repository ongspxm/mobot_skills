# ARCHITECTURE DECISION RECORD (ADR)

Use one short, dated entry in `docs/adr_log.md` for every decision. Keep entries newest first.

## FORMAT

```markdown
# [Project name] Architecture Decision Record
This is the decision log. Add new Y-statements at the top, newest first. Keep each entry short and concrete.

## 2026-07-09: ([Proposed | Accepted | Rejected | Superseded]) [Decision]
[Y-statement]

## 2026-01-01: (Accepted) Example decision
In the context of documenting decisions, considering the need for an example, we decided for a short Y-statement against a long template, to achieve fast writing, accepting less detail. #optional_tag
```

A Y-statement has six parts: context, concern, chosen option, alternatives considered against it, intended quality, and accepted downside. Use: `In the context of [context], considering [concern], we decided to [option] instead of [alternatives], so that we can [quality], accepting that [downside].`

## SCOPE

Record the architectural what and why, not code-level how. Keep implementation steps, task lists, test cases, and current system documentation elsewhere.

## HISTORY

A decision record captures what was decided at the time. Do not rewrite its rationale to match later events.

- To change a decision, add a new dated entry and link to the earlier entry.
- Use `Superseded` when a later decision replaces an earlier one.
- Use `Rejected` when a considered option is not chosen; keep the entry as history.
- Keep research details in an RDR: `$skill_dirname/type_rdr.md`.

## INSTRUCTIONS

1. Add a Y-statement to the top of `docs/adr_log.md`.
2. Add a link to an RDR when research supports the decision.
3. Run the OKF validator.
