---
name: async-subprocess
description: asyncio subprocess patterns for concurrent process probing, as used in clauderig's MCP prerequisite checker.
---

# Async Subprocess Patterns (clauderig)

## Concurrent Process Probing

The pattern used in `src/clauderig/installer.py` to probe MCP npm packages in parallel:

```python
import asyncio
from pathlib import Path

async def _probe_package(package: str) -> tuple[str, bool]:
    try:
        proc = await asyncio.create_subprocess_exec(
            "npx", "--yes", "--dry-run", package,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await asyncio.wait_for(proc.wait(), timeout=8.0)
        return package, proc.returncode == 0
    except (asyncio.TimeoutError, FileNotFoundError, OSError):
        return package, False

async def check_prerequisites(packages: list[str]) -> dict[str, bool]:
    results = await asyncio.gather(*[_probe_package(p) for p in packages])
    return dict(results)

# Called from sync context:
available = asyncio.run(check_prerequisites(["@modelcontextprotocol/server-github"]))
```

## Capturing Output

```python
async def run_and_capture(cmd: list[str]) -> tuple[int, str]:
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=30.0)
    return proc.returncode, stdout.decode(errors="replace")
```

## Adding a New MCP Probe

To add a new package check to the installer:
1. The MCP server list comes from `settings.json` via `_get_mcps()` in `installer.py`
2. `check_prerequisites()` is called automatically during `install()`
3. No code changes needed — just add the MCP to the template's `settings.json`

## Testing Async Functions

```python
# tests/test_installer.py
import pytest
import asyncio
from clauderig.installer import check_prerequisites

def test_probe_unknown_package():
    result = asyncio.run(check_prerequisites(["@nonexistent/package-xyz-404"]))
    assert result["@nonexistent/package-xyz-404"] is False
```
