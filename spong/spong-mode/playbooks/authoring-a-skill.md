### Writing or modifying a skill

You own the skill's voice.

1. Skill name is kebab-case, live in $SPONGPATH/../(skill-name)/SKILL.md (or $SPONGPATH/playbooks/(name).md for playbooks).
2. Ensure yaml frontmatter name and description (say what is done) is populated for SKILL.md.
3. Validate referenced files exist and cross-skill links resolve in spong.
4. Add test cases for structural behavior; skip subjective cases.

Style and voice:
- Smart caveman voice: simple words, clear steps, ASCII-only.
- No inline backticks and no bold; double-quote only when needed to separate a command, file, or literal.
- Be terse, delete stuff. Keep only prose that changes a decision.
- Tell it what to do and skip reason; explain only when rule is confusing.
- Delegate to sibling skills by name ("<name> skill") and playbooks by path (playbooks/<name>.md); do not repeat their steps.
- Playbooks end with "Reply with: ..." listing concrete deliverables.

Reply with: summary of skill, key design decisions, validation notes.
