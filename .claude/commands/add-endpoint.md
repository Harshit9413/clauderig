---
name: add-command
description: Add a new clauderig CLI command with tests.
---

# /add-command

Ask the user:
1. What is the new command name? (e.g., `validate`, `upgrade`, `info`)
2. What should it do?
3. Does it need user prompts (interactive) or is it fully flag-driven?
4. Should it accept a `--target` directory option?

Then create or update:
- `src/clauderig/cli.py` — add `@app.command()` function; delegate filesystem work to `installer.py`
- `src/clauderig/installer.py` — add any new logic (pure filesystem ops, no prompts)
- `tests/test_cli.py` — add tests using `typer.testing.CliRunner`

Conventions:
- Command function body ≤ 20 lines; delegate to installer/analyzer
- No interactive prompts in `installer.py` — prompts only in `cli.py`
- Use `Path` everywhere; validate inputs before touching the filesystem
- Raise `typer.Exit(1)` on error, `typer.Exit(0)` on abort

After creating: run `pytest -xvs tests/` and show output.
