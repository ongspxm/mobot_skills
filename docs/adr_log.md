# mobot_skills Decision Records

This is the decision register. Add new Y-statements at the top, newest first. Keep each entry short and concrete.

## 2026-07-15: (Accepted) Use gog for Google Automation

In the context of shared Google automation, considering duplicate authentication and API maintenance, we decided for gog as the common boundary against separate skill integrations, to achieve one setup and integration path, accepting a required external dependency. #automation

## 2026-07-12: (Accepted) Move Skills Away from Manpage Format

In the context of agent skill instructions, considering scanability and boilerplate, we decided for concise task-oriented Markdown against manpage-style sections, to achieve faster execution, accepting variation between skill layouts. #devtools

## 2026-07-11: (Accepted) Separate ADRs from Research Logs

In the context of documenting technical work, considering mixed final decisions and experiments, we decided for separate decision and RDR entries against one mixed log, to achieve clear final rationale and research history, accepting an extra record type. #devtools

## 2026-07-10: (Accepted) Develop the OKF Documentation Skill

In the context of repository knowledge, considering free-form and hard-to-search documentation, we decided for a lightweight OKF skill with validation against free-form or heavyweight systems, to achieve consistent, traceable docs, accepting authoring and validation work. #devtools

Research Decision Records (RDRs) are exploratory and belong in `docs/research/`; they should get their own register when that collection exists.
