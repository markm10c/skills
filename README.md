# mark-skills

Claude Code skills for QA.

| Skill | What it does |
| --- | --- |
| [prepare-qa-sheet](prepare-qa-sheet/SKILL.md) | Drafts the up-front QA sheet rows from a spec and the final designs. Asks for the spec, designs, other files and the sheet link. |
| [qa-test](qa-test/SKILL.md) | Runs an agent QA pass over the sheet on staging (web, admin or app via Argent), writes PASS/FAIL/SKIP and notes into the sheet, and publishes screenshot proof next to the designs. |

## Install

```bash
git clone git@github.com:markm10c/mark-skills.git ~/projects/mark-skills
ln -s ~/projects/mark-skills/prepare-qa-sheet ~/.claude/skills/prepare-qa-sheet
ln -s ~/projects/mark-skills/qa-test ~/.claude/skills/qa-test
```

Then run `/prepare-qa-sheet` or `/qa-test` in Claude Code.

`qa-test` needs the Argent MCP server and the Google Sheets connector.
