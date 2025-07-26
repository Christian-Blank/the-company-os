#!/usr/bin/env python3
"""
Proper pre-commit hooks implementation that follows service architecture.

This implementation:
1. Checks for proper service initialization
2. Uses shared configuration loading
3. Provides helpful error messages
4. Follows the same code paths as the CLI
"""

import sys
from pathlib import Path
from typing import Optional

# Add the project root to Python path
project_root = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(project_root))

try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.table import Table

    from company_os.domains.rules_service.src.config import RulesServiceConfig
    from company_os.domains.rules_service.src.discovery import RuleDiscoveryService
    from company_os.domains.rules_service.src.sync import SyncService
    from company_os.domains.rules_service.src.validation import ValidationService
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please ensure all dependencies are available:")
    print("  Option 1 (Recommended): Use Bazel CLI instead:")
    print(
        "    bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules sync"
    )
    print(
        "    bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- validate validate --auto-fix"
    )
    print("  Option 2: Install dependencies manually:")
    print("    uv pip compile requirements.in -o requirements_lock.txt")
    print("    uv pip install -r requirements_lock.txt")
    print("  Option 3: Install missing package directly:")
    print("    pip install PyYAML rich typer pydantic")
    sys.exit(3)

# Initialize console
console = Console()


def check_service_initialized() -> bool:
    """Check if Rules Service is properly initialized."""
    config_path = Path(".rules-service.yaml")
    rules_dir = Path("company_os/domains/rules/data")

    if not config_path.exists():
        console.print("\n[red]❌ Rules Service not initialized![/red]")
        console.print(
            "[yellow]The Rules Service requires initialization before use.[/yellow]"
        )
        console.print("\n[bold]To initialize, run:[/bold]")
        console.print(
            "  [cyan]bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules init[/cyan]"
        )
        console.print(
            "\n[dim]This will create a .rules-service.yaml configuration file.[/dim]"
        )
        return False

    if not rules_dir.exists() or not list(rules_dir.glob("*.rules.md")):
        console.print(
            "\n[yellow]⚠️  No rule files found in company_os/domains/rules/data/[/yellow]"
        )
        console.print(
            "[dim]The service will run but won't validate against any rules.[/dim]"
        )
        console.print("[dim]Add .rules.md files to define validation rules.[/dim]\n")

    return True


def load_config() -> Optional[RulesServiceConfig]:
    """Load configuration using the same method as CLI."""
    config_path = Path(".rules-service.yaml")

    try:
        if config_path.exists():
            return RulesServiceConfig.from_file(config_path)
        else:
            return None
    except Exception as e:
        console.print(f"[red]❌ Failed to load configuration: {e}[/red]")
        return None


def validate_main() -> int:
    """
    Proper validation implementation using shared service components.

    Returns:
        0 on success, 1 for warnings, 2 for errors, 3 for configuration failures
    """
    # Check if service is initialized
    if not check_service_initialized():
        return 3

    # Load configuration
    config = load_config()
    if not config:
        return 3

    # Get files to validate
    files = sys.argv[1:] if len(sys.argv) > 1 else []
    markdown_files = [f for f in files if f.endswith(".md")]

    if not markdown_files:
        console.print("No markdown files to validate.")
        return 0

    try:
        # Display header
        console.print("\n[bold blue]" + "=" * 80 + "[/bold blue]")
        console.print(
            f"[bold blue]RULES SERVICE VALIDATION - {len(markdown_files)} file(s)[/bold blue]".center(
                80
            )
        )
        console.print("[bold blue]" + "=" * 80 + "[/bold blue]\n")

        # Use discovery service to find rules
        discovery_service = RuleDiscoveryService(Path("."))

        with console.status("[bold green]Discovering rules..."):
            rules, errors = discovery_service.discover_rules()
            if errors:
                console.print("[yellow]Discovery errors:[/yellow]")
                for error in errors:
                    console.print(f"  [yellow]• {error}[/yellow]")

        if not rules:
            console.print(
                "[yellow]No rules found. Validation will check basic formatting only.[/yellow]\n"
            )
        else:
            console.print(
                f"[green]✓[/green] Found {len(rules)} rule(s) to validate against\n"
            )

        # Initialize validation service
        rule_contents = {}
        for rule in rules:
            if hasattr(rule, "file_path") and rule.file_path:
                try:
                    with open(rule.file_path, "r", encoding="utf-8") as f:
                        rule_contents[rule.file_path] = f.read()
                except Exception:
                    pass

        validation_service = ValidationService(rules, rule_contents)

        # Validate files
        total_warnings = 0
        total_errors = 0
        all_results = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Validating files...", total=len(markdown_files))

            for file_path in markdown_files:
                progress.update(
                    task, description=f"Validating {Path(file_path).name}..."
                )

                path_obj = Path(file_path)
                content = path_obj.read_text(encoding="utf-8")

                result = validation_service.validate_and_fix(
                    path_obj, content, auto_fix=True, add_comments=False
                )

                validation_result = result["validation_result"]
                all_results.append(validation_result)

                if result["auto_fix_log"]:
                    path_obj.write_text(result["fixed_content"], encoding="utf-8")

                total_errors += validation_result.error_count
                total_warnings += validation_result.warning_count

                progress.advance(task)

        # Display summary
        console.print("\n[bold blue]" + "=" * 80 + "[/bold blue]")
        console.print("[bold blue]VALIDATION SUMMARY[/bold blue]".center(80))
        console.print("[bold blue]" + "=" * 80 + "[/bold blue]\n")

        table = Table(show_header=True, header_style="bold")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", justify="right")

        table.add_row("Files Processed", str(len(markdown_files)))
        table.add_row("Rules Applied", str(len(rules)))
        if total_warnings > 0:
            table.add_row("[yellow]⚠️  Warnings[/yellow]", str(total_warnings))
        if total_errors > 0:
            table.add_row("[red]❌ Errors[/red]", str(total_errors))

        console.print(table)

        # Return appropriate exit code
        if total_errors > 0:
            console.print(
                "\n[red]❌ Validation FAILED - Errors must be fixed before committing[/red]"
            )
            return 2
        elif total_warnings > 0:
            console.print("\n[yellow]⚠️  Validation completed with warnings[/yellow]")
            return 1
        else:
            console.print("\n[green]✅ All validations PASSED![/green]")
            return 0

    except Exception as e:
        console.print(f"\n[red]❌ Validation failed: {str(e)}[/red]")
        import traceback

        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        return 3


def sync_main() -> int:
    """
    Proper sync implementation using shared service components.

    Returns:
        0 on success, non-zero on failure
    """
    # Check if service is initialized
    if not check_service_initialized():
        return 3

    # Load configuration
    config = load_config()
    if not config:
        return 3

    try:
        # Display header
        console.print("\n[bold blue]" + "=" * 80 + "[/bold blue]")
        console.print("[bold blue]RULES SERVICE SYNC[/bold blue]".center(80))
        console.print("[bold blue]" + "=" * 80 + "[/bold blue]\n")

        # Use discovery service
        discovery_service = RuleDiscoveryService(Path("."))

        with console.status("[bold green]Discovering rules..."):
            rules, errors = discovery_service.discover_rules()
            if errors:
                console.print("[yellow]Discovery errors:[/yellow]")
                for error in errors:
                    console.print(f"  [yellow]• {error}[/yellow]")

        if not rules:
            console.print("[yellow]No rules found to sync.[/yellow]")
            console.print(
                "[dim]Add .rules.md files to company_os/domains/rules/data/ to sync.[/dim]"
            )
            return 0

        console.print(f"[green]✓[/green] Found {len(rules)} rule(s) to sync\n")

        # Initialize sync service
        sync_service = SyncService(config, project_root)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Syncing rules to agent folders...")

            result = sync_service.sync_rules(rules, dry_run=False)

            progress.update(task, description="Sync complete!")

        # Display results
        if result.total_changes > 0 or result.skipped > 0:
            console.print("\n[bold]Sync Results:[/bold]")

            table = Table(show_header=True, header_style="bold")
            table.add_column("Action", style="cyan")
            table.add_column("Count", justify="right")

            if result.added > 0:
                table.add_row("[green]✅ Added[/green]", str(result.added))
            if result.updated > 0:
                table.add_row("[cyan]🔄 Updated[/cyan]", str(result.updated))
            if result.deleted > 0:
                table.add_row("[red]🗑️  Deleted[/red]", str(result.deleted))
            if result.skipped > 0:
                table.add_row("[dim]⏭️  Skipped[/dim]", str(result.skipped))

            console.print(table)

        if result.errors:
            console.print("\n[red]❌ Errors occurred during sync:[/red]")
            for error in result.errors:
                console.print(f"  [red]• {error}[/red]")
            return 1
        else:
            console.print("\n[green]✅ Rules sync completed successfully![/green]")
            return 0

    except Exception as e:
        console.print(f"\n[red]❌ Rules sync failed: {str(e)}[/red]")
        import traceback

        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        return 1


if __name__ == "__main__":
    # Determine which hook to run
    args = sys.argv[1:]
    script_name = Path(sys.argv[0]).name

    # If first arg is 'sync' or 'validate', use as command
    if args and args[0] in ("sync", "validate"):
        cmd = args[0]
        sys.argv = [sys.argv[0]] + args[1:]  # Remove the command for downstream logic
        if cmd == "sync":
            # Ignore any filenames or config files passed by pre-commit
            sys.argv = [sys.argv[0]]
            sys.exit(sync_main())
        elif cmd == "validate":
            sys.exit(validate_main())
    # If first arg is a file or no args, default to validate
    elif args and (args[0].endswith(".md") or Path(args[0]).exists()):
        sys.exit(validate_main())
    else:
        # If only a config file is passed (e.g., .rules-service.yaml), ignore and run sync
        if args and args[0].endswith(".yaml"):
            sys.argv = [sys.argv[0]]
            sys.exit(sync_main())
        console.print("[red]❌ Error: Unknown hook type or missing arguments[/red]")
        sys.exit(1)
