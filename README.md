# clauderig

Bootstrap a production-grade `.claude/` setup into any project — one command.

```bash
pipx install clauderig
cd my-project
claude-setup init
```

---

## What You Get

- **`settings.json`** — permissions, allowed commands, auto-lint hook, pre-configured MCP servers
- **`commands/`** — slash commands: `/claude-fit`, stack-specific add/review commands
- **`skills/`** — 2–3 skill folders with real guidance (not lorem ipsum)
- **`hooks/post-edit-lint.sh`** — auto-runs linter after every file edit
- **`hooks/setup-mcps.sh`** — one-shot MCP prerequisite installer
- **`rules/coding-standards.md`** — dos and don'ts for your stack

---

## Supported Stacks

| Stack | CLI flags | Commands | Skills | MCPs |
|---|---|---|---|---|
| Python → FastAPI | `--lang python --framework fastapi` | 5 | 3 | 3 |
| Python → Django | `--lang python --framework django` | 5 | 3 | 3 |
| PHP (Laravel) | `--lang php` | 4 | 2 | 3 |
| React → Web | `--lang react --framework reactjs` | 4 | 3 | 3 |
| React → Native | `--lang react --framework react-native` | 4 | 3 | 2 |

---

## Install

```bash
# Recommended (isolated environment)
pipx install clauderig

# Or via pip
pip install clauderig
```

Requires Python 3.10+.

---

## Usage

### Initialize a project

```bash
# Interactive
claude-setup init

# Non-interactive
claude-setup init --lang python --framework fastapi --target .
claude-setup init --lang php --target .
claude-setup init --lang react --framework reactjs --force
```

### List supported stacks

```bash
claude-setup list
```

### Check version

```bash
claude-setup version
```

---

## The `/claude-fit` Command

After `claude-setup init`, open your project in Claude Code and run `/claude-fit`.

Claude will:
1. Scan your dependency files (`requirements.txt`, `package.json`, `composer.json`, etc.)
2. Detect libraries you're actually using (SQLAlchemy, Redis, Stripe, etc.)
3. Propose new skills and commands tailored to your specific project
4. Update `CLAUDE.md` with discovered project context (test command, folder structure, auth approach)

This turns a generic `.claude/` setup into one that knows your exact project.

---

## MCP Servers

Each stack ships with MCP servers pre-configured in `settings.json`. Claude Code reads these automatically.

| MCP | FastAPI | Django | PHP | React Web | React Native |
|---|---|---|---|---|---|
| GitHub | ✓ | ✓ | ✓ | ✓ | ✓ |
| Filesystem | ✓ | ✓ | ✓ | ✓ | ✓ |
| PostgreSQL | ✓ | ✓ | ✓ | | |
| Playwright | | | | ✓ | |

Run `.claude/hooks/setup-mcps.sh` once after init to install npm prerequisites.

Set `GITHUB_TOKEN` env var for GitHub MCP authentication.

---

## Publishing to PyPI

```bash
# Build
python -m build

# Upload (test first)
twine upload --repository testpypi dist/*

# Upload to production
twine upload dist/*
```

Requires a PyPI account and `twine` (`pip install twine`).

---

## License

MIT
