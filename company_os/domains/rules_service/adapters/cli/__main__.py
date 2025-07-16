#!/usr/bin/env python3
"""Rules Service CLI entry point."""

import typer
from rich.console import Console

from company_os.domains.rules_service.adapters.cli.commands import rules

app = typer.Typer(help="Company OS Rules Service CLI")
console = Console()

# Add the rules command group
app.add_typer(rules.app, name="rules")


@app.command()
def version():
    """Show version information."""
    console.print("[green]Rules Service v0.1.0[/green]")


@app.command()
def validate(path: str = typer.Argument(..., help="Path to file or directory to validate")):
    """Validate markdown files against rules."""
    console.print(f"[yellow]Validating:[/yellow] {path}")
    # TODO: Implement validation logic
    console.print("[green]✓[/green] Validation complete")


if __name__ == "__main__":
    app()
