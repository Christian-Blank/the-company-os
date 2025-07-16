"""Rules command group for the Rules Service CLI."""

import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path
import yaml
from typing import Optional, List

from company_os.domains.rules_service.src.discovery import RuleDiscoveryService
from company_os.domains.rules_service.src.sync import SyncService
from company_os.domains.rules_service.src.config import RulesServiceConfig, AgentFolder

app = typer.Typer(help="Rules Service commands")
console = Console()


@app.command()
def init(
    config_path: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to configuration file (default: .rules-service.yaml)"
    )
):
    """Initialize Rules Service configuration."""
    if config_path is None:
        config_path = Path(".rules-service.yaml")

    if config_path.exists():
        console.print(f"[yellow]Configuration file already exists:[/yellow] {config_path}")
        overwrite = typer.confirm("Overwrite existing configuration?")
        if not overwrite:
            console.print("[blue]Initialization cancelled.[/blue]")
            return

    # Create default configuration
    default_config = {
        "version": "1.0",
        "rules_service": {
            "repository_root": ".",
            "rules_directories": [
                "os/domains/rules/data"
            ],
            "agent_folders": [
                {
                    "name": "cursor",
                    "path": ".cursor/rules",
                    "enabled": True
                },
                {
                    "name": "vscode",
                    "path": ".vscode/rules",
                    "enabled": True
                },
                {
                    "name": "cline",
                    "path": ".cline/rules",
                    "enabled": True
                },
                {
                    "name": "claude",
                    "path": ".claude/rules",
                    "enabled": True
                }
            ],
            "sync": {
                "conflict_resolution": "overwrite",
                "cleanup_orphaned_files": True,
                "include_patterns": ["*.md"],
                "exclude_patterns": ["**/node_modules/**", "**/.git/**"]
            }
        }
    }

    try:
        with open(config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False, indent=2)

        console.print(f"[green]✓[/green] Configuration initialized: {config_path}")
        console.print("[blue]Edit the configuration file to customize settings.[/blue]")

    except Exception as e:
        console.print(f"[red]✗[/red] Failed to create configuration: {e}")
        raise typer.Exit(1)


@app.command()
def sync(
    config_path: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to configuration file"
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-n",
        help="Show what would be done without making changes"
    )
):
    """Synchronize rules to agent folders."""
    console.print("[blue]Starting rules synchronization...[/blue]")

    try:
        # Load configuration
        if config_path:
            config = RulesServiceConfig.from_file(config_path)
        else:
            # Create default config
            config = RulesServiceConfig(
                version="1.0",
                agent_folders=[
                    AgentFolder(path=".cursor/rules", description="Cursor rules"),
                    AgentFolder(path=".vscode/rules", description="VS Code rules"),
                    AgentFolder(path=".cline/rules", description="Cline rules"),
                    AgentFolder(path=".claude/rules", description="Claude rules")
                ]
            )

        # Initialize discovery service
        discovery_service = RuleDiscoveryService(".")

        # Discover rules first
        with console.status("[bold green]Discovering rules...") as status:
            rules = discovery_service.discover_rules()

        # Initialize sync service
        sync_service = SyncService(config, Path("."))

        if dry_run:
            console.print("[yellow]DRY RUN MODE - No files will be modified[/yellow]")

        # Perform synchronization
        with console.status("[bold green]Synchronizing rules...") as status:
            result = sync_service.sync_rules(rules, dry_run=dry_run)

        # Display results
        if result.added > 0:
            console.print(f"[green]✓[/green] Added: {result.added} files")
        if result.updated > 0:
            console.print(f"[blue]✓[/blue] Updated: {result.updated} files")
        if result.deleted > 0:
            console.print(f"[red]✓[/red] Deleted: {result.deleted} files")
        if result.skipped > 0:
            console.print(f"[yellow]⚠[/yellow] Skipped: {result.skipped} files")

        total_operations = result.added + result.updated + result.deleted
        if total_operations == 0:
            console.print("[green]✓[/green] All rules are up to date")
        else:
            console.print(f"[green]✓[/green] Synchronization complete: {total_operations} operations")

    except Exception as e:
        console.print(f"[red]✗[/red] Synchronization failed: {e}")
        raise typer.Exit(1)


@app.command()
def query(
    tag: Optional[str] = typer.Option(
        None,
        "--tag",
        "-t",
        help="Filter rules by tag"
    ),
    document_type: Optional[str] = typer.Option(
        None,
        "--type",
        help="Filter rules by document type they apply to"
    ),
    title: Optional[str] = typer.Option(
        None,
        "--title",
        help="Filter rules by title (partial match)"
    ),
    enforcement: Optional[str] = typer.Option(
        None,
        "--enforcement",
        help="Filter by enforcement level (strict, advisory, deprecated)"
    ),
    limit: int = typer.Option(
        50,
        "--limit",
        "-l",
        help="Maximum number of results to display"
    ),
    config_path: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to configuration file"
    )
):
    """Query rules in the repository."""
    console.print("[blue]Searching for rules...[/blue]")

    try:
        # Initialize discovery service with current directory
        discovery_service = RuleDiscoveryService(".")

        # Discover rules
        with console.status("[bold green]Discovering rules...") as status:
            rules = discovery_service.discover_rules()

        # Filter rules
        filtered_rules = rules

        if tag:
            filtered_rules = [r for r in filtered_rules if tag in (r.tags or [])]

        if document_type:
            filtered_rules = [r for r in filtered_rules if document_type in (r.applies_to or [])]

        if title:
            filtered_rules = [r for r in filtered_rules if title.lower() in r.title.lower()]

        if enforcement:
            filtered_rules = [r for r in filtered_rules if r.enforcement_level == enforcement]

        # Apply limit
        if limit > 0:
            filtered_rules = filtered_rules[:limit]

        # Display results
        if not filtered_rules:
            console.print("[yellow]No rules found matching the criteria.[/yellow]")
            return

        # Create table
        table = Table(title=f"Rules Query Results ({len(filtered_rules)} found)")
        table.add_column("Title", style="cyan", no_wrap=True)
        table.add_column("Type", style="magenta")
        table.add_column("Enforcement", style="yellow")
        table.add_column("Applies To", style="green")
        table.add_column("Tags", style="blue")

        for rule in filtered_rules:
            applies_to = ", ".join(rule.applies_to or [])
            tags = ", ".join(rule.tags or [])

            table.add_row(
                rule.title,
                rule.rule_category or "general",
                rule.enforcement_level or "strict",
                applies_to or "all",
                tags or "none"
            )

        console.print(table)

        if len(rules) > len(filtered_rules):
            console.print(f"[dim]Showing {len(filtered_rules)} of {len(rules)} total rules[/dim]")

    except Exception as e:
        console.print(f"[red]✗[/red] Query failed: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
