---
type: reference
updated: 2026-05-07
---
# Conventions — clauderig

## File Naming
- Source files: `snake_case` (e.g. `cli.py`, `installer.py`, `analyzer.py`)
- Template directories: `kebab-case` stack keys (e.g. `python-fastapi`, `react-native`)
- Build scripts: `build-<platform>.sh`

## CLI Command Pattern
Commands are registered with `@app.command()`. Interactive prompts only in `cli.py`.

```python
# src/clauderig/cli.py
@app.command()
def init(
    lang: Optional[str] = typer.Option(None, help="Language: python, php, react"),
    target: Path = typer.Option(Path("."), help="Target directory"),
    force: bool = typer.Option(False, help="Overwrite existing .claude/"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print what would be copied"),
) -> None:
    """Bootstrap a .claude/ folder into a project."""
    ...
    result = install(stack=stack, target=target, force=force, dry_run=dry_run)
```

## Dataclass Pattern
Results returned as `@dataclass`, never raw dicts.

```python
# src/clauderig/installer.py
@dataclass
class InstallResult:
    commands_count: int
    skills_count: int
    hooks_count: int
    ruleset_count: int
    mcps_configured: list[str]
    target_path: Path
```

## Analyzer Pattern
Detection functions are pure (no side effects). They return a stack key string or `None`.

```python
# src/clauderig/analyzer.py
def detect_stack(path: Path) -> str | None:
    scores: dict[str, int] = {"python-fastapi": 0, "python-django": 0, ...}
    # ... add to scores based on signals ...
    best = max(scores, key=lambda k: scores[k])
    return best if scores[best] > 0 else None
```

## Validation Pattern
Stack keys are validated against a frozenset before any filesystem operation.

```python
# src/clauderig/installer.py
VALID_STACKS = frozenset({"python-fastapi", "python-django", "php", "react-web", "react-native"})

def install(stack: str, ...) -> InstallResult:
    if stack not in VALID_STACKS:
        raise ValueError(f"Unknown stack: {stack!r}. Valid: {sorted(VALID_STACKS)}")
```

## Test Pattern (when tests are added)
- Use `tmp_path` pytest fixture for isolated filesystem operations
- Use `typer.testing.CliRunner` for CLI command tests
- Build signal fixtures manually (e.g. create `requirements.txt` with `fastapi`) for `analyzer.py` tests

```python
# tests/test_installer.py
def test_install_creates_claude_dir(tmp_path):
    result = install(stack="python-fastapi", target=tmp_path, force=False, dry_run=False)
    assert (tmp_path / ".claude").is_dir()
    assert result.commands_count > 0
```

## Template Content Conventions
Each template tree lives at `src/clauderig/templates/<stack>/.claude/` and contains:
- `settings.json` — permissions, hooks, MCP server configs
- `CLAUDE.md` — stack-specific project rules
- `commands/` — slash command markdown files
- `skills/` — skill SKILL.md files (one per subdirectory)
- `rules/` — coding standards
- `hooks/` — shell scripts (made executable by `install()`)
