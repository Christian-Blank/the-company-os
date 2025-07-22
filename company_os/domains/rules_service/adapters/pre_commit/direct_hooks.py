#!/usr/bin/env python3
"""
Direct pre-commit hooks that import the rules service directly.

This avoids the Bazel dependency resolution issues by directly importing
and using the rules service modules.
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Optional
import hashlib

# Add the project root to Python path
project_root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(project_root))

try:
    # Direct imports to avoid Bazel dependency issues
    from company_os.domains.rules_service.src.validation import (
        ValidationService,
        ValidationResult,
        ValidationIssue,
        Severity
    )
    from company_os.domains.rules_service.src.sync import SyncService
    from company_os.domains.rules_service.src.config import RulesServiceConfig
    from company_os.domains.rules_service.src.models import RuleDocument

    # Import rich directly for output formatting
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import print as rprint
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please ensure all dependencies are installed:")
    print("  pip install -r requirements.txt")
    sys.exit(3)


# Initialize Rich console
console = Console()


def get_file_checksum(file_path: str) -> str:
    """Get MD5 checksum of a file."""
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        return hashlib.md5(content).hexdigest()
    except Exception:
        return ""


def add_files_to_git(files: List[str]) -> bool:
    """Add files to git staging area."""
    try:
        import subprocess
        cmd = ["git", "add"] + files
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        return result.returncode == 0
    except Exception:
        return False


def validate_main() -> int:
    """
    Direct validation implementation without Bazel.

    Returns:
        0 on success, 1 for warnings, 2 for errors, 3 for failures
    """
    # Get files from command line arguments
    files = sys.argv[1:] if len(sys.argv) > 1 else []

    # Filter for markdown files only
    markdown_files = [f for f in files if f.endswith('.md')]

    if not markdown_files:
        console.print("No markdown files to validate.")
        return 0

    try:
        # Display header
        console.print("\n[bold blue]" + "=" * 80 + "[/bold blue]")
        console.print(f"[bold blue]RULES SERVICE VALIDATION - {len(markdown_files)} file(s)[/bold blue]".center(80))
        console.print("[bold blue]" + "=" * 80 + "[/bold blue]\n")

        console.print("[yellow]⚠️  Auto-fix is enabled - fixable issues will be corrected automatically[/yellow]\n")

        # Initialize validation service with default config
        # For pre-commit, we don't need the full config - just use defaults
        config_dict = {
            "version": "1.0",
            "agent_folders": [
                {"path": ".cursor/rules/", "description": "Cursor AI rules", "enabled": True},
                {"path": ".vscode/rules/", "description": "VSCode rules", "enabled": True},
                {"path": ".cline/rules/", "description": "Cline rules", "enabled": True},
                {"path": ".claude/rules/", "description": "Claude rules", "enabled": True},
            ]
        }
        config = RulesServiceConfig(**config_dict)

        # Load rules - we need to find the rules files manually
        rules_dir = project_root / "os" / "domains" / "rules" / "data"
        rule_docs = []

        if rules_dir.exists():
            for rule_file in rules_dir.glob("*.rules.md"):
                # Create a basic RuleDocument
                rule_doc = RuleDocument(
                    title=rule_file.stem.replace('.rules', ''),
                    file_path=str(rule_file),
                    version="1.0",
                    status="Active",
                    owner="Company OS",
                    last_updated="",
                    applies_to=[],
                    parent_charter="",
                    tags=[]
                )
                rule_docs.append(rule_doc)

        # Read rule contents
        rule_contents = {}
        for rule_doc in rule_docs:
            try:
                with open(rule_doc.file_path, 'r', encoding='utf-8') as f:
                    rule_contents[rule_doc.file_path] = f.read()
            except Exception:
                pass

        validation_service = ValidationService(rule_docs, rule_contents)

        # Store file checksums before validation
        file_checksums_before = {}
        for file_path in markdown_files:
            file_checksums_before[file_path] = get_file_checksum(file_path)

        # Track results
        total_warnings = 0
        total_errors = 0
        fixed_files = []
        all_results = []

        # Validate each file with progress indicator
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Validating files...", total=len(markdown_files))

            for file_path in markdown_files:
                progress.update(task, description=f"Validating {Path(file_path).name}...")

                # Read file content
                path_obj = Path(file_path)
                content = path_obj.read_text(encoding='utf-8')

                # Validate and potentially fix the file
                result = validation_service.validate_and_fix(
                    path_obj, content, auto_fix=True, add_comments=False
                )

                validation_result = result['validation_result']
                all_results.append(validation_result)

                # Check if file was modified
                if result['auto_fix_log']:
                    fixed_files.append(file_path)
                    # Write fixed content back
                    path_obj.write_text(result['fixed_content'], encoding='utf-8')

                # Count issues
                total_errors += validation_result.error_count
                total_warnings += validation_result.warning_count

                progress.advance(task)

        # Add auto-fixed files to git
        if fixed_files:
            if add_files_to_git(fixed_files):
                console.print(f"\n[green]✅ Added {len(fixed_files)} auto-fixed file(s) to git staging[/green]")
            else:
                console.print("\n[red]❌ Failed to add auto-fixed files to git[/red]")
                console.print("[yellow]⚠️  You may need to manually add these files[/yellow]")

        # Display summary
        console.print("\n[bold blue]" + "=" * 80 + "[/bold blue]")
        console.print("[bold blue]VALIDATION SUMMARY[/bold blue]".center(80))
        console.print("[bold blue]" + "=" * 80 + "[/bold blue]\n")

        # Summary table
        table = Table(show_header=True, header_style="bold")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", justify="right")

        table.add_row("Files Processed", str(len(markdown_files)))
        table.add_row("[green]✅ Passed[/green]", str(len(markdown_files) - len(set(r.file_path for r in all_results))))
        if fixed_files:
            table.add_row("[cyan]🔧 Auto-fixed[/cyan]", str(len(fixed_files)))
        if total_warnings > 0:
            table.add_row("[yellow]⚠️  Warnings[/yellow]", str(total_warnings))
        if total_errors > 0:
            table.add_row("[red]❌ Errors[/red]", str(total_errors))

        console.print(table)

        # Display issues by file
        if any(r.issues for r in all_results):
            console.print("\n[bold]Issues Found:[/bold]")

            for result in all_results:
                if result.issues:
                    has_errors = result.error_count > 0
                    icon = "❌" if has_errors else "⚠️ "
                    color = "red" if has_errors else "yellow"

                    console.print(f"\n  [{color}]{icon} {result.file_path}[/{color}]")
                    for issue in result.issues:
                        level_icon = "❌" if issue.severity == Severity.ERROR else "⚠️ "
                        console.print(f"     [dim]• {level_icon} {issue.rule_id}: {issue.message}[/dim]")
                        if issue.line_number:
                            console.print(f"       [dim]Line {issue.line_number}[/dim]")

        # Display auto-fixed files
        if fixed_files:
            console.print("\n[bold]Auto-fixed Files:[/bold]")
            for file_path in fixed_files:
                console.print(f"  [cyan]🔧 {file_path}[/cyan]")

        # Final status
        console.print()
        if total_errors > 0:
            console.print("[red]❌ Validation FAILED - Errors must be fixed before committing[/red]")
            return_code = 2
        elif total_warnings > 0:
            console.print("[yellow]⚠️  Validation completed with warnings[/yellow]")
            return_code = 1
        else:
            console.print("[green]✅ All validations PASSED![/green]")
            return_code = 0

        console.print("\n[dim]" + "─" * 80 + "[/dim]")
        return return_code

    except Exception as e:
        console.print(f"\n[red]❌ Validation failed with unexpected error: {str(e)}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        return 3


def sync_main() -> int:
    """
    Direct sync implementation without Bazel.

    Returns:
        0 on success, non-zero on failure
    """
    try:
        # Display header
        console.print("\n[bold blue]" + "=" * 80 + "[/bold blue]")
        console.print("[bold blue]RULES SERVICE SYNC[/bold blue]".center(80))
        console.print("[bold blue]" + "=" * 80 + "[/bold blue]\n")

        # Initialize sync service with default config
        config_dict = {
            "version": "1.0",
            "agent_folders": [
                {"path": ".cursor/rules/", "description": "Cursor AI rules", "enabled": True},
                {"path": ".vscode/rules/", "description": "VSCode rules", "enabled": True},
                {"path": ".cline/rules/", "description": "Cline rules", "enabled": True},
                {"path": ".claude/rules/", "description": "Claude rules", "enabled": True},
            ]
        }
        config = RulesServiceConfig(**config_dict)
        sync_service = SyncService(config, project_root)

        # Load rules to sync
        rules_dir = project_root / "os" / "domains" / "rules" / "data"
        rule_docs = []

        if rules_dir.exists():
            for rule_file in rules_dir.glob("*.rules.md"):
                # Create a basic RuleDocument
                rule_doc = RuleDocument(
                    title=rule_file.stem.replace('.rules', ''),
                    file_path=str(rule_file),
                    version="1.0",
                    status="Active",
                    owner="Company OS",
                    last_updated="",
                    applies_to=[],
                    parent_charter="",
                    tags=[]
                )
                rule_docs.append(rule_doc)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Syncing rules to agent folders...")

            # Perform sync
            result = sync_service.sync_rules(rule_docs, dry_run=False)

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

            # Show agent folders
            console.print("\n[bold]Synced to:[/bold]")
            for folder in config.agent_folders:
                if folder.enabled:
                    console.print(f"  [cyan]📁 {folder.path}[/cyan]")

            return 0

    except Exception as e:
        console.print(f"\n[red]❌ Rules sync failed: {str(e)}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        return 1


if __name__ == "__main__":
    # Determine which hook to run based on script name or command
    script_name = Path(sys.argv[0]).name

    if "sync" in script_name:
        sys.exit(sync_main())
    elif "validate" in script_name:
        sys.exit(validate_main())
    else:
        console.print("[red]❌ Error: Unknown hook type[/red]")
        sys.exit(1)
