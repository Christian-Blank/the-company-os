#!/usr/bin/env python3
"""
Pre-commit hooks for the Rules Service.

This module provides pre-commit hooks for:
1. Syncing rules to agent folders
2. Validating markdown files against rules
"""

import sys
import os
import subprocess
from pathlib import Path
from typing import List, Optional

# Add the project root to Python path for imports
project_root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(project_root))

from rich.console import Console
from rich.panel import Panel
from rich.text import Text


console = Console()


def sync_main() -> int:
    """
    Main entry point for the rules-sync pre-commit hook.
    
    Returns:
        0 on success, non-zero on failure
    """
    try:
        console.print("\n[bold blue]🔄 Running Rules Service Sync...[/bold blue]")
        
        # Run the sync command via subprocess
        result = subprocess.run([
            "bazel", "run", "//company_os/domains/rules_service/adapters/cli:rules_cli", 
            "--", "rules", "sync"
        ], capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            console.print("[bold green]✅ Rules sync completed successfully![/bold green]\n")
            return 0
        else:
            console.print(f"[bold red]❌ Rules sync failed: {result.stderr}[/bold red]\n")
            return 1
            
    except Exception as e:
        console.print(f"[bold red]❌ Rules sync failed: {str(e)}[/bold red]\n")
        return 1


def validate_main() -> int:
    """
    Main entry point for the rules-validate pre-commit hook.
    
    Receives filenames from pre-commit and validates only markdown files.
    
    Returns:
        0 on success, 1 for warnings, 2 for errors, 3 for failures
    """
    # Get files from command line arguments (provided by pre-commit)
    files = sys.argv[1:] if len(sys.argv) > 1 else []
    
    # Filter for markdown files only
    markdown_files = [f for f in files if f.endswith('.md')]
    
    if not markdown_files:
        console.print("[dim]No markdown files to validate.[/dim]\n")
        return 0
    
    try:
        console.print(f"\n[bold blue]📝 Validating {len(markdown_files)} markdown file(s)...[/bold blue]")
        console.print("[bold yellow]✨ Auto-fix is enabled - issues will be fixed automatically when possible[/bold yellow]\n")
        
        # Run the validate command via subprocess
        cmd = [
            "bazel", "run", "//company_os/domains/rules_service/adapters/cli:rules_cli",
            "--", "validate", "validate", "--auto-fix"
        ] + markdown_files
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        
        # Print the output from the validation command
        if result.stdout:
            console.print(result.stdout)
        if result.stderr:
            console.print(result.stderr)
        
        if result.returncode == 0:
            console.print("\n[bold green]✅ All files passed validation![/bold green]\n")
        elif result.returncode == 1:
            console.print("\n[bold yellow]⚠️  Validation completed with warnings.[/bold yellow]\n")
        elif result.returncode == 2:
            console.print("\n[bold red]❌ Validation failed with errors.[/bold red]")
            console.print("[dim]Commit aborted. Please fix the errors and try again.[/dim]\n")
        else:
            console.print("\n[bold red]❌ Validation failed.[/bold red]\n")
            
        return result.returncode
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Validation failed with unexpected error: {str(e)}[/bold red]\n")
        return 3


if __name__ == "__main__":
    # For testing - determine which hook to run based on script name
    script_name = Path(sys.argv[0]).name
    
    if "sync" in script_name:
        sys.exit(sync_main())
    elif "validate" in script_name:
        sys.exit(validate_main())
    else:
        console.print("[bold red]Error: Unknown hook type[/bold red]")
        sys.exit(1)
