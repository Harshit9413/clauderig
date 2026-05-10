from __future__ import annotations
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm

from clauderig import __version__
from clauderig.analyzer import detect_framework, detect_language, detect_stack
from clauderig.installer import install

app = typer.Typer(
    help="Bootstrap a production-grade .claude/ setup into any project.",
    add_completion=False,
)
console = Console()

_FRAMEWORK_DISPLAY: dict[str, str] = {
    "fastapi": "FastAPI",
    "django": "Django",
    "reactjs": "ReactJS (Web)",
    "react-native": "React Native",
}

_LANG_FRAMEWORKS: dict[str, list[str]] = {
    "python": ["fastapi", "django"],
    "php": [],
    "react": ["reactjs", "react-native"],
}

_STACK_KEY: dict[str, str] = {
    "fastapi": "python-fastapi",
    "django": "python-django",
    "reactjs": "react-web",
    "react-native": "react-native",
    "php": "php",
}

_STACK_INFO: dict[str, dict[str, int]] = {
    "python-fastapi": {"commands": 5, "skills": 3, "hooks": 2, "mcps": 3, "agents": 6},
    "python-django": {"commands": 5, "skills": 3, "hooks": 2, "mcps": 3, "agents": 6},
    "php": {"commands": 4, "skills": 2, "hooks": 2, "mcps": 3, "agents": 6},
    "react-web": {"commands": 4, "skills": 3, "hooks": 2, "mcps": 3, "agents": 6},
    "react-native": {"commands": 4, "skills": 3, "hooks": 2, "mcps": 2, "agents": 6},
}

_STACK_DISPLAY: dict[str, str] = {
    "python-fastapi": "Python → FastAPI",
    "python-django": "Python → Django",
    "php": "PHP (Laravel-friendly)",
    "react-web": "React → ReactJS (Web)",
    "react-native": "React → React Native",
}


def _prompt_choice(prompt: str, choices: list[str]) -> str:
    """Prompt user to pick from a list. Keeps asking until valid input."""
    choices_str = ", ".join(choices)
    while True:
        value = Prompt.ask(f"{prompt} ({choices_str})").strip().lower()
        if value in choices:
            return value
        console.print(f"[red]Invalid choice:[/red] {value!r}. Choose one of: {choices_str}")


def _resolve_stack(lang: str, framework: str | None) -> str:
    if lang == "php":
        if framework is not None:
            console.print(f"[red]Error:[/red] --lang php does not accept --framework. Got: {framework!r}")
            raise typer.Exit(1)
        return "php"
    if lang not in _LANG_FRAMEWORKS:
        console.print(f"[red]Error:[/red] Unknown --lang: {lang!r}. Choose: python, php, react")
        raise typer.Exit(1)
    valid = _LANG_FRAMEWORKS[lang]
    if framework not in valid:
        console.print(
            f"[red]Error:[/red] --lang {lang} requires --framework "
            f"{' or '.join(valid)}. Got: {framework!r}"
        )
        raise typer.Exit(1)
    return _STACK_KEY[framework]


@app.command()
def init(
    lang: Optional[str] = typer.Option(None, help="Language: python, php, react"),
    framework: Optional[str] = typer.Option(None, help="Framework: fastapi, django, reactjs, react-native"),
    target: Path = typer.Option(Path("."), help="Target directory"),
    force: bool = typer.Option(False, help="Overwrite existing .claude/"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print what would be copied"),
) -> None:
    """Bootstrap a .claude/ folder into a project."""
    interactive = lang is None
    stack: str | None = None

    if interactive:
        # Try full stack auto-detection first
        detected = detect_stack(target)
        if detected:
            console.print(f"[blue]→[/blue] Detected stack: [cyan]{_STACK_DISPLAY.get(detected, detected)}[/cyan]")
            if Confirm.ask("Use detected stack?", default=True):
                stack = detected

        if stack is None:
            # Language detection
            detected_lang = detect_language(target)
            if detected_lang:
                console.print(f"[blue]→[/blue] Detected language: [cyan]{detected_lang}[/cyan]")
                lang = detected_lang
            else:
                lang = _prompt_choice("Primary language?", ["python", "php", "react"])

            if lang == "php":
                stack = "php"
            else:
                # Framework auto-detection
                fw: str | None = None
                detected_fw = detect_framework(target, lang)
                if detected_fw:
                    fw_label = _FRAMEWORK_DISPLAY.get(detected_fw, detected_fw)
                    console.print(f"[blue]→[/blue] Detected framework: [cyan]{fw_label}[/cyan]")
                    if Confirm.ask("Use detected framework?", default=True):
                        fw = detected_fw
                if fw is None:
                    fw = _prompt_choice("Framework?", _LANG_FRAMEWORKS[lang])
                stack = _STACK_KEY[fw]

        target_str = Prompt.ask("Target directory?", default=".")
        target = Path(target_str)

    if stack is None:
        stack = _resolve_stack(lang, framework)

    dst = target / ".claude"
    if dst.exists():
        console.print(f"[blue]→[/blue] .claude/ already exists in [cyan]{target.resolve()}[/cyan]")
        if not force:
            if interactive:
                if not Confirm.ask("Overwrite?", default=False):
                    console.print("[yellow]Aborted.[/yellow]")
                    raise typer.Exit(0)
                force = True
            else:
                console.print("[red]Error:[/red] Use --force to overwrite.")
                raise typer.Exit(1)

    try:
        result = install(stack=stack, target=target, force=force, dry_run=dry_run)
    except FileExistsError as exc:
        console.print(f"[red]Error:[/red] {exc} Use --force to overwrite.")
        raise typer.Exit(1)
    except FileNotFoundError as exc:
        console.print(f"[red]Error:[/red] Template not found: {exc}")
        console.print("[dim]Try reinstalling: pipx reinstall clauderig[/dim]")
        raise typer.Exit(1)
    except PermissionError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(1)

    if dry_run:
        return

    console.print(f"\n[green]✓[/green] Copied .claude/ to {result.target_path.resolve()}")
    console.print(
        f"[green]✓[/green] Installed: {result.commands_count} commands · "
        f"{result.skills_count} skills · {result.hooks_count} hooks · "
        f"{result.ruleset_count} ruleset · {result.agents_count} agents"
    )
    if result.mcps_configured:
        console.print(f"[green]✓[/green] MCPs pre-configured: {', '.join(result.mcps_configured)}")
    console.print("\n[blue]Next steps:[/blue]")
    console.print("  1. Run [cyan].claude/hooks/setup-mcps.sh[/cyan] once to install MCP prerequisites")
    console.print("  2. Open your project in Claude Code")
    console.print("  3. Run [cyan]/claude-fit[/cyan] to personalise your .claude/ setup")


@app.command(name="list")
def list_stacks() -> None:
    """List supported stacks and what each ships."""
    table = Table(title="Supported Stacks", header_style="bold blue")
    table.add_column("Stack", style="cyan")
    table.add_column("Commands", justify="center")
    table.add_column("Skills", justify="center")
    table.add_column("Hooks", justify="center")
    table.add_column("Agents", justify="center")
    table.add_column("MCPs", justify="center")

    for key, info in _STACK_INFO.items():
        table.add_row(
            _STACK_DISPLAY[key],
            str(info["commands"]),
            str(info["skills"]),
            str(info["hooks"]),
            str(info["agents"]),
            str(info["mcps"]),
        )

    console.print(table)


@app.command()
def version() -> None:
    """Print the clauderig version."""
    console.print(f"clauderig {__version__}")


if __name__ == "__main__":
    app()