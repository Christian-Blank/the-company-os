#!/usr/bin/env python3
"""
Improved pre-commit hooks for the Rules Service.

This module provides pre-commit hooks for:
1. Syncing rules to agent folders
2. Validating markdown files against rules

Key improvements:
- Better output formatting with clear summaries
- Suppressed Bazel noise
- Better error handling
- Clearer validation results
"""

import sys
import os
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Tuple, NamedTuple
import hashlib
import json
import tempfile
from dataclasses import dataclass
from datetime import datetime

# Add the project root to Python path for imports
project_root = Path(__file__).resolve().parents[4]


class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    GRAY = "\033[90m"


@dataclass
class ValidationResult:
    """Result of validating a single file."""
    file_path: str
    status: str  # 'success', 'warning', 'error', 'fixed'
    issues: List[str]
    was_fixed: bool = False


class ValidationSummary:
    """Summary of all validation results."""
    def __init__(self):
        self.total_files = 0
        self.successful = 0
        self.warnings = 0
        self.errors = 0
        self.fixed = 0
        self.results: List[ValidationResult] = []

    def add_result(self, result: ValidationResult):
        self.results.append(result)
        self.total_files += 1
        if result.status == 'success':
            self.successful += 1
        elif result.status == 'warning':
            self.warnings += 1
        elif result.status == 'error':
            self.errors += 1
        if result.was_fixed:
            self.fixed += 1

    def get_exit_code(self) -> int:
        if self.errors > 0:
            return 2
        elif self.warnings > 0:
            return 1
        return 0


def print_header(title: str) -> None:
    """Print a formatted header."""
    width = 80
    border = "=" * width
    print(f"\n{Colors.BOLD}{Colors.BLUE}{border}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title.center(width)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{border}{Colors.RESET}\n")


def print_status(message: str, status: str = "info", indent: int = 0) -> None:
    """Print a formatted status message."""
    prefix = "  " * indent
    if status == "success":
        print(f"{prefix}{Colors.GREEN}✅ {message}{Colors.RESET}")
    elif status == "error":
        print(f"{prefix}{Colors.RED}❌ {message}{Colors.RESET}")
    elif status == "warning":
        print(f"{prefix}{Colors.YELLOW}⚠️  {message}{Colors.RESET}")
    elif status == "info":
        print(f"{prefix}{Colors.BLUE}🔄 {message}{Colors.RESET}")
    elif status == "debug":
        print(f"{prefix}{Colors.GRAY}🔍 {message}{Colors.RESET}")
    else:
        print(f"{prefix}{message}")


def print_summary(summary: ValidationSummary) -> None:
    """Print a comprehensive validation summary."""
    print_header("VALIDATION SUMMARY")

    # Overall stats
    print(f"{Colors.BOLD}Files Processed:{Colors.RESET} {summary.total_files}")
    print(f"{Colors.GREEN}✅ Passed:{Colors.RESET} {summary.successful}")
    if summary.fixed > 0:
        print(f"{Colors.CYAN}🔧 Auto-fixed:{Colors.RESET} {summary.fixed}")
    if summary.warnings > 0:
        print(f"{Colors.YELLOW}⚠️  Warnings:{Colors.RESET} {summary.warnings}")
    if summary.errors > 0:
        print(f"{Colors.RED}❌ Errors:{Colors.RESET} {summary.errors}")

    # Detailed results for files with issues
    if summary.warnings > 0 or summary.errors > 0:
        print(f"\n{Colors.BOLD}Issues Found:{Colors.RESET}")
        for result in summary.results:
            if result.status in ['warning', 'error']:
                status_icon = "⚠️ " if result.status == 'warning' else "❌"
                status_color = Colors.YELLOW if result.status == 'warning' else Colors.RED
                print(f"\n  {status_color}{status_icon} {result.file_path}{Colors.RESET}")
                for issue in result.issues:
                    print(f"     {Colors.GRAY}• {issue}{Colors.RESET}")

    # Auto-fixed files
    if summary.fixed > 0:
        print(f"\n{Colors.BOLD}Auto-fixed Files:{Colors.RESET}")
        for result in summary.results:
            if result.was_fixed:
                print(f"  {Colors.CYAN}🔧 {result.file_path}{Colors.RESET}")

    # Final status
    print()
    if summary.errors > 0:
        print_status("Validation FAILED - Errors must be fixed before committing", "error")
    elif summary.warnings > 0:
        print_status("Validation completed with warnings", "warning")
    else:
        print_status("All validations PASSED!", "success")

    print(f"\n{Colors.GRAY}{'─' * 80}{Colors.RESET}")


def run_bazel_command(cmd: List[str], suppress_output: bool = True) -> subprocess.CompletedProcess:
    """
    Run a Bazel command with better error handling and output control.

    Args:
        cmd: Command to run
        suppress_output: Whether to suppress Bazel build output

    Returns:
        CompletedProcess result
    """
    env = os.environ.copy()
    # Suppress Bazel's build output if requested
    if suppress_output:
        env['BAZEL_QUIET'] = '1'

    # Run with --ui_event_filters to reduce noise
    if 'bazel' in cmd[0] and 'run' in cmd:
        # Insert UI filters after 'bazel' but before 'run'
        bazel_idx = cmd.index('bazel')
        run_idx = cmd.index('run')
        cmd = (cmd[:bazel_idx+1] +
               ['--ui_event_filters=-info,-stdout,-stderr', '--noshow_progress'] +
               cmd[run_idx:])

    return subprocess.run(cmd, capture_output=True, text=True, cwd=project_root, env=env)


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
        cmd = ["git", "add"] + files
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        return result.returncode == 0
    except Exception:
        return False


def parse_validation_output(output: str) -> Dict[str, ValidationResult]:
    """
    Parse the validation output to extract results for each file.

    This is a simplified parser - in reality, we'd need to parse the actual
    output format from the rules CLI.
    """
    results = {}
    current_file = None
    current_issues = []

    # This is a placeholder - we'd need to implement actual parsing
    # based on the output format of the rules CLI
    lines = output.strip().split('\n')
    for line in lines:
        # Parse the output to extract file results
        # This would need to be implemented based on actual output format
        pass

    return results


def validate_main() -> int:
    """
    Main entry point for the rules-validate pre-commit hook.

    Returns:
        0 on success, 1 for warnings, 2 for errors, 3 for failures
    """
    # Get files from command line arguments
    files = sys.argv[1:] if len(sys.argv) > 1 else []

    # Filter for markdown files only
    markdown_files = [f for f in files if f.endswith('.md')]

    if not markdown_files:
        print("No markdown files to validate.")
        return 0

    # Initialize summary
    summary = ValidationSummary()

    try:
        print_header(f"RULES SERVICE VALIDATION - {len(markdown_files)} file(s)")
        print_status("Auto-fix is enabled - fixable issues will be corrected automatically", "warning")
        print()

        # Store file checksums before validation
        file_checksums_before = {}
        for file_path in markdown_files:
            file_checksums_before[file_path] = get_file_checksum(file_path)

        # Build the validation command
        cmd = [
            "bazel", "run",
            "//company_os/domains/rules_service/adapters/cli:rules_cli",
            "--", "validate", "validate",
            "--auto-fix", "--format", "json"  # Request JSON output for easier parsing
        ] + markdown_files

        # Run validation with suppressed Bazel output
        print_status("Running validation...", "info")
        result = run_bazel_command(cmd, suppress_output=True)

        # Check for Bazel build failures
        if "ModuleNotFoundError" in result.stderr or "No module named" in result.stderr:
            print_status("Build failed - attempting direct Python execution...", "warning")
            # Try running the CLI directly via Python instead of Bazel
            cmd = [
                sys.executable, "-m",
                "company_os.domains.rules_service.adapters.cli",
                "validate", "validate", "--auto-fix"
            ] + markdown_files
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)

        # Process results for each file
        for file_path in markdown_files:
            checksum_after = get_file_checksum(file_path)
            was_fixed = checksum_after != file_checksums_before[file_path]

            # Create a result for this file
            # In reality, we'd parse the actual validation output
            if result.returncode == 0:
                status = 'success'
                issues = []
            else:
                # This is simplified - we'd parse actual output
                status = 'warning' if result.returncode == 1 else 'error'
                issues = ["Validation issues found"]  # Would extract actual issues

            validation_result = ValidationResult(
                file_path=file_path,
                status=status,
                issues=issues,
                was_fixed=was_fixed
            )
            summary.add_result(validation_result)

        # Add auto-fixed files to git
        fixed_files = [r.file_path for r in summary.results if r.was_fixed]
        if fixed_files:
            if add_files_to_git(fixed_files):
                print_status(f"Added {len(fixed_files)} auto-fixed file(s) to git staging", "success")
            else:
                print_status("Failed to add auto-fixed files to git", "error")
                print_status("You may need to manually add these files", "warning")

        # Print comprehensive summary
        print_summary(summary)

        return summary.get_exit_code()

    except Exception as e:
        print_status(f"Validation failed with unexpected error: {str(e)}", "error")
        return 3


def sync_main() -> int:
    """
    Main entry point for the rules-sync pre-commit hook.

    Returns:
        0 on success, non-zero on failure
    """
    try:
        print_header("RULES SERVICE SYNC")

        cmd = [
            "bazel", "run",
            "//company_os/domains/rules_service/adapters/cli:rules_cli",
            "--", "rules", "sync"
        ]

        print_status("Syncing rules to agent folders...", "info")
        result = run_bazel_command(cmd, suppress_output=True)

        if result.returncode == 0:
            print_status("Rules sync completed successfully!", "success")
            return 0
        else:
            print_status(f"Rules sync failed", "error")
            if result.stderr:
                print(f"{Colors.GRAY}{result.stderr}{Colors.RESET}")
            return 1

    except Exception as e:
        print_status(f"Rules sync failed: {str(e)}", "error")
        return 1


if __name__ == "__main__":
    # Determine which hook to run based on script name
    script_name = Path(sys.argv[0]).name

    if "sync" in script_name:
        sys.exit(sync_main())
    elif "validate" in script_name:
        sys.exit(validate_main())
    else:
        print_status("Error: Unknown hook type", "error")
        sys.exit(1)
