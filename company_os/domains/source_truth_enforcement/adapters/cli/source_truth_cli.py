"""
Source Truth Enforcement Service - CLI Implementation

Command-line interface for checking source of truth consistency.
"""

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from company_os.domains.source_truth_enforcement.src.models import CheckerConfig, Severity, Report, ScanStats
from company_os.domains.source_truth_enforcement.src.checker import SourceTruthChecker


app = typer.Typer(
    name="source-truth",
    help="Source of Truth Enforcement System",
    add_completion=False,
)
console = Console()


@app.command()
def check(
    all_definitions: bool = typer.Option(False, "--all", help="Check all source of truth definitions"),
    python_version: bool = typer.Option(False, "--python-version", help="Check Python version consistency only"),
    dependencies: bool = typer.Option(False, "--dependencies", help="Check dependency management only"),
    forbidden_files: bool = typer.Option(False, "--forbidden-files", help="Check for forbidden files"),
    registry_path: Optional[Path] = typer.Option(None, "--registry", help="Path to source truth registry file"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug output"),
    format_output: str = typer.Option("console", "--format", help="Output format (console, json)"),
    strict: bool = typer.Option(False, "--strict", help="Treat warnings as errors"),
):
    """Check source of truth consistency across the repository."""

    # Determine which check to run
    if not any([all_definitions, python_version, dependencies, forbidden_files]):
        console.print("❌ Please specify what to check (--all, --python-version, --dependencies, or --forbidden-files)")
        raise typer.Exit(1)

    # Default registry path
    if registry_path is None:
        service_dir = Path(__file__).parent.parent.parent
        registry_path = service_dir / "data" / "source_truth_registry.yaml"

    # Create configuration
    config = CheckerConfig(
        registry_path=str(registry_path),
        repository_root=".",
        verbose=verbose,
        debug=debug
    )

    try:
        # Initialize checker
        checker = SourceTruthChecker(config)

        # Run appropriate check
        if all_definitions:
            console.print("🔍 Checking all source of truth definitions...")
            report = checker.check_all()
        elif python_version:
            console.print("🐍 Checking Python version consistency...")
            report = checker.check_definition("python_version")
        elif dependencies:
            console.print("📦 Checking dependency management...")
            report = checker.check_definition("dependencies")
        elif forbidden_files:
            console.print("🚫 Checking for forbidden files...")
            violations = checker.check_forbidden_files()
            # Create a minimal report for forbidden files
            from datetime import datetime
            stats = ScanStats(
                violations_found=len(violations),
                scan_duration_seconds=0.0,
                timestamp=datetime.now().isoformat()
            )
            report = Report(
                violations=violations,
                stats=stats,
                registry_path=str(registry_path),
                success=len(violations) == 0
            )

        # Display results
        if format_output == "json":
            console.print(report.model_dump_json(indent=2))
        else:
            _display_console_report(report)

        # Determine exit code
        exit_code = report.get_exit_code()
        if strict and exit_code == 1:
            exit_code = 2

        raise typer.Exit(exit_code)

    except Exception as e:
        console.print(f"❌ Error: {e}")
        if debug:
            import traceback
            console.print(traceback.format_exc())
        raise typer.Exit(3)


def _display_console_report(report: Report) -> None:
    """Display a nicely formatted console report."""

    # Header
    if report.success:
        console.print(Panel("✅ All source of truth checks passed!", style="green"))
    else:
        console.print(Panel(f"❌ Found {len(report.violations)} violations", style="red"))

    # Statistics
    stats_table = Table(title="Scan Statistics")
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="white")

    stats_table.add_row("Files Scanned", str(report.stats.files_scanned))
    stats_table.add_row("Violations Found", str(report.stats.violations_found))
    stats_table.add_row("High Severity", str(report.stats.high_severity_count))
    stats_table.add_row("Medium Severity", str(report.stats.medium_severity_count))
    stats_table.add_row("Low Severity", str(report.stats.low_severity_count))
    stats_table.add_row("Scan Duration", f"{report.stats.scan_duration_seconds:.2f}s")

    console.print(stats_table)

    # Violations
    if report.violations:
        console.print("\n")
        violations_table = Table(title="Violations Found")
        violations_table.add_column("Severity", style="bold")
        violations_table.add_column("Definition", style="cyan")
        violations_table.add_column("File", style="white")
        violations_table.add_column("Line", style="white")
        violations_table.add_column("Message", style="white")

        for violation in report.violations:
            severity_style = {
                Severity.HIGH: "red",
                Severity.MEDIUM: "yellow",
                Severity.LOW: "blue"
            }.get(violation.severity, "white")

            violations_table.add_row(
                f"[{severity_style}]{violation.severity.upper()}[/{severity_style}]",
                violation.definition,
                str(Path(violation.file_path).name),  # Just filename for brevity
                str(violation.line_number),
                violation.message
            )

        console.print(violations_table)

        # Show suggestions if available
        violations_with_suggestions = [v for v in report.violations if v.suggestion]
        if violations_with_suggestions:
            console.print("\n💡 Suggestions:")
            for violation in violations_with_suggestions:
                console.print(f"  • {violation.file_path}:{violation.line_number} - {violation.suggestion}")


@app.command()
def info():
    """Show information about the source truth enforcement system."""
    console.print(Panel("Source Truth Enforcement System v1.0", style="blue"))
    console.print("\nThis tool validates that all technical specifications in the repository")
    console.print("are consistent with their authoritative sources.")
    console.print("\nFor more information, see the service README.md")


if __name__ == "__main__":
    app()
