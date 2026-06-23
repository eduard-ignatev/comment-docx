# AGENTS.md - Comment DOCX

This is a skill to add comments in DOCX files for autonomous personal assistants (agents) that are driven by LLM models.

Sibling project of different skill is in `../docling-extract/` for reference.

Important! Do not add any vanity tests without permission (since bad tests are bad requirements that will cripple the codebase). When asking permission to add tests, explain testing design.

## Anchor comments

Add specially formatted comments throughout the codebase, where appropriate, for yourself as inline knowledge that can be easily `grep`ped for.

- Use `AICODE-NOTE:`, `AICODE-TODO:`, or `AICODE-QUESTION:` as prefix as appropriate.
- *Important:* Before scanning files, always first try to grep for existing `AICODE-…`.
- Update relevant anchors, after finishing any task.
- Make sure to add relevant anchor comments, whenever a file or piece of code is too complex, or very important, or could have a bug