# What Was Added — Setup Summary

## 1. CLAUDE.md (project root)

**Path:** `CLAUDE.md`

Root-level dev reference for the project. Contains:

- **Commands table** — pytest, ruff, mypy, build-macos.sh, build-linux.sh, pip install -e .
- **PyInstaller Watch-outs** — zip bundling vs datas, sys.frozen, hidden imports, rthook rules
- **Python 3.12 Conventions** — type aliases (PEP 695), tomllib, TaskGroup, match/case, etc.

---

## 2. CONTEXT.md (project root)

**Path:** `CONTEXT.md`

Architecture decision record (ADR). Explains the "why" behind non-obvious choices:

- Why templates are bundled as `templates_bundle.zip` instead of PyInstaller `datas`
- Why PyInstaller was chosen over pip, Docker, Homebrew, pipx
- Release workflow decisions — two binaries, GPG signing, install.sh, version source of truth

---

## 3. Agent — code-reviewer

**Path:** `.claude/agents/code-reviewer.md`

A read-only subagent for code review.

- **Model:** claude-sonnet-4-6
- **Tools allowed:** Read, Glob, Grep only
- **What it does:** Reviews for correctness, style, type hints, test gaps, security issues
- **What it never does:** Edit, Write, or run Bash — reports only

---

## 4. Agent — security-auditor

**Path:** `.claude/agents/security-auditor.md`

A read-only subagent for security audits.

- **Model:** claude-sonnet-4-6
- **Tools allowed:** Read, Glob, Grep only
- **What it does:** Looks for command injection, path traversal, hardcoded secrets, unsafe file permissions in source and templates
- **What it never does:** Auto-fix anything — reports with CWE references and severity levels

---

## 5. Agent — build-engineer

**Path:** `.claude/agents/build-engineer.md`

A subagent for diagnosing PyInstaller build failures.

- **Model:** claude-sonnet-4-6
- **Tools allowed:** Read, Glob, Grep, Bash
- **What it does:** Investigates `clauderig.spec`, `rthook_clauderig.py`, `templates_bundle.zip`, and build scripts; runs smoke tests on the final binary
- **Default behavior:** Read and investigate only; patches spec/scripts only when explicitly asked

---

## 6. hooks.json

**Path:** `.claude/hooks/hooks.json`

Declares all three hook types in one reference file:

| Hook           | Trigger                         | Script                       |
| -------------- | ------------------------------- | ---------------------------- |
| `PreToolUse` | Before every Bash call          | `scripts/firewall.sh`      |
| `Stop`       | When Claude finishes a response | `scripts/test-enforcer.sh` |

These are also wired into `.claude/settings.json` so they actually run.

---

## 7. scripts/firewall.sh

**Path:** `.claude/hooks/scripts/firewall.sh`

Runs before every Bash command. Blocks:

- `rm -rf`
- `git push --force` / `git push -f`
- `DROP TABLE` / `DROP DATABASE` / `TRUNCATE TABLE`
- Any reference to `.env` files

Exits with code `2` (blocking) if a pattern matches, `0` otherwise.

---

## 7. scripts/test-enforcer.sh

**Path:** `.claude/hooks/scripts/test-enforcer.sh`

Runs when Claude stops (after each response). Executes `pytest -x --tb=short -q`.

- If `tests/` directory does not exist — exits silently (no false alarms)
- If tests fail — prints a warning message, but **never blocks** the session

---

## 8. settings.json — updated

**Path:** `.claude/settings.json`

Two changes made to the existing file:

### Deny list expanded

Added:

```
Bash(git push --force:*)
Bash(git push -f :*)
Bash(DROP TABLE:*)
Bash(DROP DATABASE:*)
Read(**/.env)
```
