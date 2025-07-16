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


def print_status(message: str, status: str = "info") -> None:
    """Print a formatted status message."""
    if status == "success":
        print(f"✅ {message}")
    elif status == "error":
        print(f"❌ {message}")
    elif status == "warning":
        print(f"⚠️  {message}")
    elif status == "info":
        print(f"🔄 {message}")
    else:
        print(message)


def sync_main() -> int:
    """
    Main entry point for the rules-sync pre-commit hook.

    Returns:
        0 on success, non-zero on failure
    """
    try:
        print()
        print_status("Running Rules Service Sync...", "info")

        # Run the sync command via subprocess
        result = subprocess.run([
            "bazel", "run", "//company_os/domains/rules_service/adapters/cli:rules_cli",
            "--", "rules", "sync"
        ], capture_output=True, text=True, cwd=project_root)

        if result.returncode == 0:
            print_status("Rules sync completed successfully!", "success")
            print()
            return 0
        else:
            print_status(f"Rules sync failed: {result.stderr}", "error")
            print()
            return 1

    except Exception as e:
        print_status(f"Rules sync failed: {str(e)}", "error")
        print()
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
        print("No markdown files to validate.")
        print()
        return 0

    try:
        print()
        print_status(f"Validating {len(markdown_files)} markdown file(s)...", "info")
        print_status("Auto-fix is enabled - issues will be fixed automatically when possible", "warning")
        print()

        # Run the validate command via subprocess
        cmd = [
            "bazel", "run", "//company_os/domains/rules_service/adapters/cli:rules_cli",
            "--", "validate", "validate", "--auto-fix"
        ] + markdown_files

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)

        # Print the output from the validation command
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)

        if result.returncode == 0:
            print()
            print_status("All files passed validation!", "success")
            print()
        elif result.returncode == 1:
            print()
            print_status("Validation completed with warnings.", "warning")
            print()
        elif result.returncode == 2:
            print()
            print_status("Validation failed with errors.", "error")
            print("Commit aborted. Please fix the errors and try again.")
            print()
        else:
            print()
            print_status("Validation failed.", "error")
            print()

        return result.returncode

    except Exception as e:
        print()
        print_status(f"Validation failed with unexpected error: {str(e)}", "error")
        print()
        return 3


if __name__ == "__main__":
    # For testing - determine which hook to run based on script name
    script_name = Path(sys.argv[0]).name

    if "sync" in script_name:
        sys.exit(sync_main())
    elif "validate" in script_name:
        sys.exit(validate_main())
    else:
        print_status("Error: Unknown hook type", "error")
        sys.exit(1)
