"""Validate command for the Rules Service CLI."""

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, TaskID
from rich.panel import Panel
from pathlib import Path
import glob
from typing import List, Optional

from company_os.domains.rules_service.src.validation import ValidationService, ValidationResult, ValidationIssue
from company_os.domains.rules_service.src.discovery import RuleDiscoveryService

app = typer.Typer(help="Document validation commands")
console = Console()


@app.command()
def validate(
    files: List[str] = typer.Argument(
        ...,
        help="File paths or glob patterns to validate"
    ),
    auto_fix: bool = typer.Option(
        False,
        "--auto-fix",
        "-f",
        help="Apply safe automatic fixes"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed validation output"
    ),
    config_path: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to configuration file"
    ),
    format_output: str = typer.Option(
        "table",
        "--format",
        help="Output format: table, json, or summary"
    ),
    exit_on_error: bool = typer.Option(
        True,
        "--exit-on-error/--no-exit-on-error",
        help="Exit with error code if validation issues found"
    )
):
    """Validate markdown files against rules."""

    # Expand glob patterns and collect all files
    all_files = []
    for pattern in files:
        if "*" in pattern or "?" in pattern:
            # Handle glob patterns
            expanded = glob.glob(pattern, recursive=True)
            all_files.extend([Path(f) for f in expanded])
        else:
            # Handle direct file paths
            file_path = Path(pattern)
            if file_path.is_file():
                all_files.append(file_path)
            elif file_path.is_dir():
                # If directory, find all .md files
                all_files.extend(file_path.rglob("*.md"))
            else:
                console.print(f"[red]✗[/red] File not found: {pattern}")
                if exit_on_error:
                    raise typer.Exit(1)

    if not all_files:
        console.print("[yellow]No files found to validate.[/yellow]")
        return

    # Remove duplicates and sort
    all_files = sorted(list(set(all_files)))

    console.print(f"[blue]Validating {len(all_files)} files...[/blue]")

    try:
        # Initialize services
        discovery_service = RuleDiscoveryService(".")

        # Discover rules
        with console.status("[bold green]Loading rules...") as status:
            rules = discovery_service.discover_rules()

        # Initialize validation service
        validation_service = ValidationService(rules)

        # Track results
        all_results = {}
        total_issues = 0
        total_errors = 0
        total_warnings = 0
        total_fixed = 0

        # Process files with progress bar
        with Progress() as progress:
            task = progress.add_task("[green]Validating files...", total=len(all_files))

            for file_path in all_files:
                try:
                    # Read file content
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Validate the file
                    result = validation_service.validate_document(file_path, content)

                    # Apply auto-fixes if requested
                    if auto_fix and result.auto_fixes:
                        fixed_content = content
                        for fix in result.auto_fixes:
                            fixed_content = fix.apply(fixed_content)

                        # Write back the fixed content
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(fixed_content)

                        total_fixed += len(result.auto_fixes)

                        # Re-validate after fixes
                        result = validation_service.validate_document(file_path, fixed_content)

                    all_results[file_path] = result

                    # Count issues by severity
                    for issue in result.issues:
                        total_issues += 1
                        if issue.severity == "error":
                            total_errors += 1
                        elif issue.severity == "warning":
                            total_warnings += 1

                except Exception as e:
                    console.print(f"[red]✗[/red] Error validating {file_path}: {e}")
                    if exit_on_error:
                        raise typer.Exit(1)

                progress.update(task, advance=1)

        # Display results
        if format_output == "table":
            _display_table_format(all_results, verbose)
        elif format_output == "json":
            _display_json_format(all_results)
        elif format_output == "summary":
            _display_summary_format(all_results)

        # Display summary
        if total_fixed > 0:
            console.print(f"[green]✓[/green] Applied {total_fixed} automatic fixes")

        if total_issues == 0:
            console.print("[green]✓[/green] All files passed validation")
        else:
            console.print(f"[yellow]Found {total_issues} validation issues:[/yellow]")
            if total_errors > 0:
                console.print(f"  [red]✗[/red] {total_errors} errors")
            if total_warnings > 0:
                console.print(f"  [yellow]⚠[/yellow] {total_warnings} warnings")

        # Exit with appropriate code
        if exit_on_error and total_errors > 0:
            raise typer.Exit(2)  # Validation errors found
        elif exit_on_error and total_warnings > 0:
            raise typer.Exit(1)  # Warnings found

    except Exception as e:
        console.print(f"[red]✗[/red] Validation failed: {e}")
        if exit_on_error:
            raise typer.Exit(3)  # General error


def _display_table_format(results: dict, verbose: bool = False):
    """Display results in table format."""

    for file_path, result in results.items():
        if not result.issues and not verbose:
            continue

        # Create panel for each file
        if result.issues:
            panel_style = "red" if any(i.severity == "error" for i in result.issues) else "yellow"
        else:
            panel_style = "green"

        # Create table for issues
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Line", style="dim", width=6)
        table.add_column("Rule", style="cyan", width=20)
        table.add_column("Severity", width=8)
        table.add_column("Message", style="white")

        for issue in result.issues:
            severity_style = {
                "error": "[red]ERROR[/red]",
                "warning": "[yellow]WARN[/yellow]",
                "info": "[blue]INFO[/blue]"
            }.get(issue.severity, issue.severity)

            table.add_row(
                str(issue.line_number) if issue.line_number else "-",
                issue.rule_id or "general",
                severity_style,
                issue.message
            )

        if result.issues or verbose:
            status_text = f"✓ Valid" if not result.issues else f"✗ {len(result.issues)} issues"
            console.print(Panel(table, title=f"[bold]{file_path}[/bold] - {status_text}", border_style=panel_style))


def _display_json_format(results: dict):
    """Display results in JSON format."""
    import json

    json_results = {}
    for file_path, result in results.items():
        json_results[str(file_path)] = {
            "issues": [
                {
                    "line_number": issue.line_number,
                    "rule_id": issue.rule_id,
                    "severity": issue.severity,
                    "message": issue.message
                }
                for issue in result.issues
            ],
            "auto_fixes_applied": len(result.auto_fixes) if result.auto_fixes else 0
        }

    console.print(json.dumps(json_results, indent=2))


def _display_summary_format(results: dict):
    """Display results in summary format."""

    total_files = len(results)
    valid_files = sum(1 for r in results.values() if not r.issues)
    invalid_files = total_files - valid_files

    console.print(f"[bold]Validation Summary[/bold]")
    console.print(f"Total files: {total_files}")
    console.print(f"[green]Valid files: {valid_files}[/green]")
    if invalid_files > 0:
        console.print(f"[red]Files with issues: {invalid_files}[/red]")

    # Show files with issues
    for file_path, result in results.items():
        if result.issues:
            error_count = sum(1 for i in result.issues if i.severity == "error")
            warning_count = sum(1 for i in result.issues if i.severity == "warning")
            console.print(f"  {file_path}: {error_count} errors, {warning_count} warnings")


if __name__ == "__main__":
    app()
