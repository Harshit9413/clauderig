---
name: add-stack
description: Add a new stack/template to clauderig (no database migrations needed — this project has no DB).
---

# /add-stack

clauderig has no database. Use this command to add a new supported stack instead.

Ask: what new stack/framework should clauderig support? (e.g., `python-flask`, `ruby-rails`)

Then:
1. Choose a stack key (kebab-case, e.g. `python-flask`)
2. Create the template tree: `src/clauderig/templates/<stack-key>/.claude/`
   - `settings.json` — permissions, hooks, MCP server configs
   - `CLAUDE.md` — project rules for this stack
   - `commands/` — slash command markdown files
   - `skills/` — skill SKILL.md files
   - `rules/coding-standards.md`
   - `hooks/post-edit-lint.sh`
3. Add `"<stack-key>"` to `VALID_STACKS` frozenset in `src/clauderig/installer.py`
4. Add to these dicts in `src/clauderig/cli.py`:
   - `_STACK_KEY` — maps framework name → stack key
   - `_STACK_INFO` — counts for `list` command
   - `_STACK_DISPLAY` — human-readable label
   - `_LANG_FRAMEWORKS` — language → list of framework names
5. Add detection signals to `detect_stack()` in `src/clauderig/analyzer.py`
6. Run `pytest -xvs` and verify no regressions
