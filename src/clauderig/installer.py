from __future__ import annotations
import asyncio
import json
import shutil
import stat
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path


def _ensure_templates(meipass: Path) -> Path:
    templates_dir = meipass / "templates"
    sentinel = templates_dir / "python-fastapi" / ".claude"
    if not sentinel.exists():
        zip_file = meipass / "templates_bundle.zip"
        if not zip_file.exists():
            raise RuntimeError(
                f"clauderig bundle is corrupt: templates_bundle.zip not found in {meipass}"
            )
        templates_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(str(zip_file)) as zf:
            for member in zf.infolist():
                target = templates_dir / member.filename
                target.parent.mkdir(parents=True, exist_ok=True)
                if not member.filename.endswith("/"):
                    with zf.open(member) as src, open(target, "wb") as dst:
                        dst.write(src.read())
    return templates_dir


def _template_src(stack: str) -> Path:
    if getattr(sys, "frozen", False):
        templates_dir = _ensure_templates(Path(sys._MEIPASS))  # type: ignore[attr-defined]
        base = templates_dir / stack
        with_dot_claude = base / ".claude"
        return with_dot_claude if with_dot_claude.is_dir() else base
    return Path(__file__).parent / "templates" / stack / ".claude"


VALID_STACKS = frozenset({
    "python-fastapi",
    "python-django",
    "php",
    "react-web",
    "react-native",
})


@dataclass
class InstallResult:
    commands_count: int
    skills_count: int
    hooks_count: int
    ruleset_count: int
    mcps_configured: list[str]
    target_path: Path


def _count_dir(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for _ in path.iterdir())


def _get_mcps(settings_path: Path) -> list[str]:
    if not settings_path.exists():
        return []
    try:
        return list(json.loads(settings_path.read_text()).get("mcpServers", {}).keys())
    except (json.JSONDecodeError, OSError):
        return []


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


async def check_prerequisites(mcps: list[str]) -> dict[str, bool]:
    """Concurrently probe whether MCP npm packages are resolvable."""
    results = await asyncio.gather(*[_probe_package(p) for p in mcps])
    return dict(results)


def install(stack: str, target: Path, force: bool, dry_run: bool) -> InstallResult:
    if stack not in VALID_STACKS:
        raise ValueError(f"Unknown stack: {stack!r}. Valid: {sorted(VALID_STACKS)}")

    dst = target / ".claude"

    if dst.exists() and not force:
        raise FileExistsError(
            f"`.claude/` already exists at {dst}. Use --force to overwrite."
        )

    src_path = _template_src(stack)

    if not src_path.is_dir():
        raise FileNotFoundError(
            f"Template source not found: {src_path}. "
            "The binary bundle may be corrupt — please reinstall clauderig."
        )

    if dry_run:
        for item in sorted(src_path.rglob("*")):
            if item.is_file():
                print(f"  would copy: {item.relative_to(src_path.parent.parent)}")
        return InstallResult(
            commands_count=0, skills_count=0, hooks_count=0,
            ruleset_count=0, mcps_configured=[], target_path=dst,
        )

    if dst.exists() and force:
        shutil.rmtree(str(dst))

    shutil.copytree(str(src_path), str(dst))

    hooks_dir = dst / "hooks"
    if hooks_dir.exists():
        for sh in hooks_dir.glob("*.sh"):
            sh.chmod(sh.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    mcps_list = _get_mcps(dst / "settings.json")
    asyncio.run(check_prerequisites(mcps_list))

    return InstallResult(
        commands_count=_count_dir(dst / "commands"),
        skills_count=_count_dir(dst / "skills"),
        hooks_count=_count_dir(dst / "hooks"),
        ruleset_count=_count_dir(dst / "rules"),
        mcps_configured=_get_mcps(dst / "settings.json"),
        target_path=dst,
    )
