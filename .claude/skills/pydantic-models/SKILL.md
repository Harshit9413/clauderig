---
name: dataclasses-and-validation
description: Dataclass patterns and input validation as used in clauderig (InstallResult, VALID_STACKS, stack resolution).
---

# Dataclasses and Validation Patterns (clauderig)

## InstallResult Dataclass

Returned from `install()` to carry structured results — never use raw dicts.

```python
# src/clauderig/installer.py
from dataclasses import dataclass
from pathlib import Path

@dataclass
class InstallResult:
    commands_count: int
    skills_count: int
    hooks_count: int
    ruleset_count: int
    mcps_configured: list[str]
    target_path: Path
```

## Adding Fields to InstallResult

Add the field to the dataclass, then update all `InstallResult(...)` construction sites — there is one in `install()` and one in the `dry_run` early-return path.

```python
@dataclass
class InstallResult:
    commands_count: int
    skills_count: int
    hooks_count: int
    ruleset_count: int
    mcps_configured: list[str]
    target_path: Path
    warnings: list[str] = None  # use field(default_factory=list) in practice

    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []
```

## Stack Validation

```python
# src/clauderig/installer.py
VALID_STACKS = frozenset({
    "python-fastapi",
    "python-django",
    "php",
    "react-web",
    "react-native",
})

def install(stack: str, target: Path, force: bool, dry_run: bool) -> InstallResult:
    if stack not in VALID_STACKS:
        raise ValueError(f"Unknown stack: {stack!r}. Valid: {sorted(VALID_STACKS)}")
```

## Stack Resolution in CLI

```python
# src/clauderig/cli.py
_STACK_KEY: dict[str, str] = {
    "fastapi": "python-fastapi",
    "django": "python-django",
    "reactjs": "react-web",
    "react-native": "react-native",
    "php": "php",
}

def _resolve_stack(lang: str, framework: str | None) -> str:
    if lang == "php":
        return "php"
    valid = _LANG_FRAMEWORKS[lang]
    if framework not in valid:
        console.print(f"[red]Error:[/red] ...")
        raise typer.Exit(1)
    return _STACK_KEY[framework]
```

## Adding a New Stack

1. Add template tree: `src/clauderig/templates/<new-key>/.claude/`
2. Add to `VALID_STACKS` in `installer.py`
3. Add to `_STACK_KEY`, `_STACK_INFO`, `_STACK_DISPLAY`, `_LANG_FRAMEWORKS` in `cli.py`
4. Add detection signals to `detect_stack()` in `analyzer.py`

## JSON File Parsing (used in _get_mcps)

```python
# src/clauderig/installer.py
def _get_mcps(settings_path: Path) -> list[str]:
    if not settings_path.exists():
        return []
    try:
        return list(json.loads(settings_path.read_text()).get("mcpServers", {}).keys())
    except (json.JSONDecodeError, OSError):
        return []
```

Pattern: always return a safe default; catch both decode and IO errors; never let a bad config crash the install.
