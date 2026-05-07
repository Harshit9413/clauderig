---
name: review
description: Review current branch changes for code quality, correctness, and test coverage.
---

# /review

Run in order:

1. `git diff main...HEAD` — list changed files
2. For each changed Python file in `src/clauderig/` check:
   - `from __future__ import annotations` present
   - Type hints on all functions and return values
   - No business logic or prompts in `analyzer.py` (must stay pure/side-effect-free)
   - No interactive prompts in `installer.py` (prompts only in `cli.py`)
   - All filesystem ops use `Path` (not `os.path`)
   - New stacks added to ALL required dicts in `cli.py` and `VALID_STACKS` in `installer.py`
   - No secrets or tokens logged
3. Check: do changed files have corresponding test updates in `tests/`?
4. Run `pytest -xvs` and report pass/fail
5. Run `ruff check .` and report any issues

Summary format:
- ✓ What looks good
- ✗ Issues to fix before merging
- ⚠ Suggestions (not blockers)
