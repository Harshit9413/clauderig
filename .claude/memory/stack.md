---
type: reference
updated: 2026-05-07
---
# Stack Details — clauderig

## Dependencies and Their Role
- `typer>=0.12` — CLI framework; builds the `app = typer.Typer()` with `@app.command()` decorators
- `rich>=13.0` — terminal output (Console, Table, Prompt, Confirm, colour markup)
- `asyncio` (stdlib) — used in `installer.py` for concurrent MCP package probing via `asyncio.create_subprocess_exec`
- `zipfile` (stdlib) — extracting `templates_bundle.zip` inside frozen PyInstaller binaries
- `shutil` (stdlib) — `copytree` / `rmtree` for template installation
- `pathlib.Path` (stdlib) — all filesystem paths

## Dev Dependencies
- `pytest>=8.0` — test runner
- `pytest-cov>=5.0` — coverage reporting
- `build>=1.0` — `python -m build` for wheel/sdist
- `twine>=5.0` — PyPI publishing
- `pyinstaller` — binary builds (installed by build scripts, not in pyproject.toml)

## Database Setup
- None — this project has no database

## Auth Implementation
- None — no auth

## Binary Distribution
- PyInstaller spec: `clauderig.spec`
- Template trees are zipped into `templates_bundle.zip` at build time and embedded in the binary
- At runtime under PyInstaller: `sys.frozen == True`, `sys._MEIPASS` is the temp extraction dir
- `_ensure_templates()` in `installer.py` extracts the zip on first run if templates aren't present

## Template Resolution (dev vs frozen)
```python
# src/clauderig/installer.py
def _template_src(stack: str) -> Path:
    if getattr(sys, "frozen", False):
        templates_dir = _ensure_templates(Path(sys._MEIPASS))
        base = templates_dir / stack
        with_dot_claude = base / ".claude"
        return with_dot_claude if with_dot_claude.is_dir() else base
    return Path(__file__).parent / "templates" / stack / ".claude"
```

## Async MCP Probing
```python
# src/clauderig/installer.py
async def _probe_package(package: str) -> tuple[str, bool]:
    proc = await asyncio.create_subprocess_exec(
        "npx", "--yes", "--dry-run", package, ...
    )
    await asyncio.wait_for(proc.wait(), timeout=8.0)
    return package, proc.returncode == 0
```
Called via `asyncio.run(check_prerequisites(mcps_list))` in `install()`.
