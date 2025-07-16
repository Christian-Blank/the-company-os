#!/usr/bin/env python3
"""Rules Service CLI entry point."""

import typer
from rich.console import Console

from company_os.domains.rules_service.adapters.cli.commands import rules, validate

app = typer.Typer(help="Company OS Rules Service CLI")
console = Console()

# Add the rules command group
app.add_typer(rules.app, name="rules")

# Add the validate command group
app.add_typer(validate.app, name="validate")


@app.command()
def version():
    """Show version information."""
    console.print("[green]Rules Service v0.1.0[/green]")


if __name__ == "__main__":
    app()
