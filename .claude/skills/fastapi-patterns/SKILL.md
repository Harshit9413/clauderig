---
name: typer-cli-patterns
description: Typer CLI patterns for commands, options, prompts, and output — as used in clauderig/cli.py.
---

# Typer CLI Patterns (clauderig)

## Command Structure

One `typer.Typer` instance; commands registered with `@app.command()`.

```python
# src/clauderig/cli.py
import typer
from rich.console import Console

app = typer.Typer(help="Bootstrap a production-grade .claude/ setup.", add_completion=False)
console = Console()

@app.command()
def init(
    lang: Optional[str] = typer.Option(None, help="Language: python, php, react"),
    target: Path = typer.Option(Path("."), help="Target directory"),
    force: bool = typer.Option(False, help="Overwrite existing .claude/"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print what would be copied"),
) -> None:
    """Bootstrap a .claude/ folder into a project."""
    ...

if __name__ == "__main__":
    app()
```

## Adding a New Command

```python
@app.command()
def validate(
    target: Path = typer.Option(Path("."), help="Project to validate"),
) -> None:
    """Validate an existing .claude/ setup."""
    dst = target / ".claude"
    if not dst.exists():
        console.print("[red]Error:[/red] No .claude/ found.")
        raise typer.Exit(1)
    console.print(f"[green]✓[/green] .claude/ found at {dst.resolve()}")
```

## Interactive Prompts (Rich)

```python
from rich.prompt import Prompt, Confirm

# Free-form prompt with default
target_str = Prompt.ask("Target directory?", default=".")

# Confirmed boolean
if not Confirm.ask("Overwrite?", default=False):
    console.print("[yellow]Aborted.[/yellow]")
    raise typer.Exit(0)

# Constrained choice (custom helper in cli.py)
def _prompt_choice(prompt: str, choices: list[str]) -> str:
    choices_str = ", ".join(choices)
    while True:
        value = Prompt.ask(f"{prompt} ({choices_str})").strip().lower()
        if value in choices:
            return value
        console.print(f"[red]Invalid choice:[/red] {value!r}")
```

## Rich Output Patterns

```python
from rich.table import Table

# Coloured status lines
console.print(f"[green]✓[/green] Installed {result.commands_count} commands")
console.print(f"[blue]→[/blue] Detected: [cyan]{stack}[/cyan]")
console.print("[red]Error:[/red] Use --force to overwrite.")

# Table (used in `list` command)
table = Table(title="Supported Stacks", header_style="bold blue")
table.add_column("Stack", style="cyan")
table.add_column("Commands", justify="center")
table.add_row("Python → FastAPI", "5")
console.print(table)
```

## Testing CLI Commands

```python
# tests/test_cli.py
from typer.testing import CliRunner
from clauderig.cli import app

runner = CliRunner()

def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "clauderig" in result.output

def test_init_dry_run(tmp_path):
    result = runner.invoke(app, ["init", "--lang", "python", "--framework", "fastapi",
                                  "--target", str(tmp_path), "--dry-run"])
    assert result.exit_code == 0
    assert "would copy" in result.output
```

## Exit Codes

```python
raise typer.Exit(0)  # success / user aborted
raise typer.Exit(1)  # error
```
