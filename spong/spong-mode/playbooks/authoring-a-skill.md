### Writing or modifying a skill

You own the skill's voice.

1. skill name is kebab-case, live in $SPONGPATH/../(skill-name)/SKILL.md
2. Ensure yaml frontmatter `name` and `description` (say what is done) in populated
3. Validate referenced files exist and cross-skill links (check that skill exist in spong).
4. Add test cases for structural behavior; skip subjective cases.

Be terse, delete stuff. Keep only prose that changes a decision.
Tell it to do the thing and skip reason. Explain only when rule is confusing.
Delegate to other skills if possible, do it by path (check that skill exist in $SPONGPATH/..)

reply with: summary of skill, key design decisions, validation notes.
