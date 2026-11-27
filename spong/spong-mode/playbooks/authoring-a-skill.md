### Writing or modifying a skill

You own the skill's voice.

1. Pick kebab-case name + path: $SPONGPATH/../(skill-name)/SKILL.md or $SPONGPATH/playbooks/(name).md.
2. Add SKILL.md YAML frontmatter (name, description saying what skill does); check referenced files exist and cross-skill links resolve in spong.
3. Draft structural tests; skip subjective cases.
4. Pause at gate (spong-mode skill): show draft/diff + checks; wait for "ok to go?" before edits.
5. After OK, edit skill + tests -> run structural checks.

Style and voice:
- Smart caveman voice: simple words, clear steps, ASCII-only.
- No inline backticks and no bold; double-quote only when needed to separate a command, file, or literal.
- Be terse, delete stuff. Keep only prose that changes a decision.
- Tell it what to do and skip reason; explain only when rule is confusing.
- Delegate to sibling skills by name ("<name> skill") and playbooks by path (playbooks/<name>.md); do not repeat their steps.
- Playbooks end with "Reply with: ..." listing concrete deliverables.

Reply with: summary of skill, key design decisions, validation notes.
