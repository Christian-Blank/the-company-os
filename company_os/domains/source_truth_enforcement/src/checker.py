"""
Source Truth Enforcement Service - Main Checker

This module contains the main consistency checker that orchestrates the validation process.
"""

import re
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from .models import (
    Violation,
    Report,
    ScanStats,
    Severity,
    CheckerConfig,
    RegistryDefinition,
    IgnoreSummary,
)
from .registry import SourceTruthRegistry
from .ignore_parser import IgnoreParser


class SourceTruthChecker:
    """Main consistency checker that validates source of truth compliance."""

    def __init__(self, config: CheckerConfig):
        """Initialize the checker with configuration.

        Args:
            config: Checker configuration
        """
        self.config = config
        self.registry = SourceTruthRegistry(Path(config.registry_path))
        self.repository_root = Path(config.repository_root)
        self.ignore_summary = IgnoreSummary()

        # Validate configuration
        self.registry.validate_registry()

    def check_all(self) -> Report:
        """Check all source of truth definitions.

        Returns:
            Comprehensive report of violations found
        """
        start_time = time.time()
        all_violations = []

        if self.config.debug:
            print("🔍 Starting comprehensive source of truth check...")

        for name, definition in self.registry.list_definitions().items():
            if self.config.debug:
                print(f"📋 Checking {name}...")

            violations = self._check_definition(name, definition)
            all_violations.extend(violations)

        end_time = time.time()

        # Calculate statistics
        stats = self._calculate_stats(all_violations, start_time, end_time)

        return Report(
            violations=all_violations,
            stats=stats,
            registry_path=str(self.config.registry_path),
            success=len(all_violations) == 0,
            ignore_summary=self.ignore_summary
            if self.ignore_summary.total_ignored > 0
            else None,
        )

    def check_definition(self, definition_name: str) -> Report:
        """Check a specific source of truth definition.

        Args:
            definition_name: Name of the definition to check

        Returns:
            Report containing violations for this definition
        """
        start_time = time.time()

        definition = self.registry.get_definition(definition_name)
        if not definition:
            raise ValueError(f"Definition '{definition_name}' not found in registry")

        violations = self._check_definition(definition_name, definition)
        end_time = time.time()

        stats = self._calculate_stats(violations, start_time, end_time)

        return Report(
            violations=violations,
            stats=stats,
            registry_path=str(self.config.registry_path),
            success=len(violations) == 0,
        )

    def _check_definition(
        self, name: str, definition: RegistryDefinition
    ) -> List[Violation]:
        """Check a single definition and return violations."""
        violations = []

        try:
            # Get source of truth value
            source_value = self.registry.get_source_value(name)

            # Get files to scan
            files_to_scan = self._get_files_to_scan(definition)

            if self.config.parallel and len(files_to_scan) > 10:
                violations = self._scan_files_parallel(
                    name, definition, source_value, files_to_scan
                )
            else:
                violations = self._scan_files_sequential(
                    name, definition, source_value, files_to_scan
                )

        except Exception as e:
            if self.config.debug:
                print(f"❌ Error checking {name}: {e}")
            violations.append(
                Violation(
                    definition=name,
                    file_path="system",
                    line_number=0,
                    message=f"System error: {e}",
                    severity=Severity.HIGH,
                )
            )

        return violations

    def _scan_files_sequential(
        self,
        name: str,
        definition: RegistryDefinition,
        source_value: Optional[str],
        files: List[Path],
    ) -> List[Violation]:
        """Scan files sequentially."""
        violations = []

        for file_path in files:
            if self.config.verbose:
                print(f"   📄 Scanning {file_path}")

            file_violations = self._scan_file(name, definition, source_value, file_path)
            violations.extend(file_violations)

        return violations

    def _scan_files_parallel(
        self,
        name: str,
        definition: RegistryDefinition,
        source_value: Optional[str],
        files: List[Path],
    ) -> List[Violation]:
        """Scan files in parallel."""
        violations = []
        max_workers = self.registry.global_config.performance.get("max_workers", 4)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(
                    self._scan_file, name, definition, source_value, file_path
                ): file_path
                for file_path in files
            }

            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    file_violations = future.result()
                    violations.extend(file_violations)
                except Exception as e:
                    if self.config.debug:
                        print(f"⚠️ Error scanning {file_path}: {e}")

        return violations

    def _scan_file(
        self,
        name: str,
        definition: RegistryDefinition,
        source_value: Optional[str],
        file_path: Path,
    ) -> List[Violation]:
        """Scan a single file for violations."""
        violations = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse ignore directives from the file
            ignore_parser = IgnoreParser(debug=self.config.debug)
            ignore_context = ignore_parser.parse_file_for_ignores(
                content, str(file_path)
            )

            # Validate ignore blocks
            block_errors = ignore_parser.validate_ignore_blocks(
                ignore_context, str(file_path)
            )
            if block_errors and self.config.verbose:
                for error in block_errors:
                    print(f"⚠️ {file_path}: {error}")

            # Get potential violations (before filtering by ignores)
            potential_violations = self._get_violations_for_file(
                name, definition, source_value, file_path, content
            )

            # Filter out ignored violations
            for violation in potential_violations:
                is_ignored, reason = ignore_parser.is_line_ignored(
                    violation.line_number, name, ignore_context
                )

                if is_ignored:
                    # Track ignored violation
                    self.ignore_summary.add_ignored_violation(
                        violation,
                        reason or "Unknown reason",
                        "block" if reason else "file",
                    )
                    if self.config.debug:
                        print(
                            f"  🚫 Ignored violation at {file_path}:{violation.line_number} - {reason}"
                        )
                else:
                    violations.append(violation)

        except Exception as e:
            if self.config.debug:
                print(f"⚠️ Error reading {file_path}: {e}")

        return violations

    def _get_violations_for_file(
        self,
        name: str,
        definition: RegistryDefinition,
        source_value: Optional[str],
        file_path: Path,
        content: str,
    ) -> List[Violation]:
        """Get all potential violations for a file (before applying ignores)."""
        violations: List[Violation] = []

        # Check different types of violations based on definition type
        if definition.type == "exact_version":
            violations.extend(
                self._check_exact_version(
                    name, definition, source_value, file_path, content
                )
            )
        elif definition.type == "file_existence_and_workflow":
            violations.extend(
                self._check_file_existence_and_workflow(
                    name, definition, file_path, content
                )
            )
        elif definition.type == "minimum_version":
            violations.extend(
                self._check_minimum_version(
                    name, definition, source_value, file_path, content
                )
            )
        else:
            violations.extend(
                self._check_generic_patterns(name, definition, file_path, content)
            )

        return violations

    def _check_exact_version(
        self,
        name: str,
        definition: RegistryDefinition,
        source_value: Optional[str],
        file_path: Path,
        content: str,
    ) -> List[Violation]:
        """Check exact version violations (e.g., Python version)."""
        violations: List[Violation] = []

        if not source_value:
            return violations

        scan_patterns = definition.scan_patterns or []

        for pattern in scan_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                line_number = content[: match.start()].count("\n") + 1
                matched_text = match.group(0)

                # Check if the matched version matches the source
                if source_value not in matched_text:
                    suggestion = f"Use '{source_value}' instead of '{matched_text}'"

                    violations.append(
                        Violation(
                            definition=name,
                            file_path=str(file_path),
                            line_number=line_number,
                            message=f"Version mismatch: found '{matched_text}', expected '{source_value}'",
                            severity=definition.severity,
                            suggestion=suggestion,
                            context=self._get_line_context(content, line_number),
                        )
                    )

        return violations

    def _check_file_existence_and_workflow(
        self, name: str, definition: RegistryDefinition, file_path: Path, content: str
    ) -> List[Violation]:
        """Check for forbidden files and workflow patterns."""
        violations: List[Violation] = []

        # Check for forbidden file references in content
        forbidden_patterns = definition.forbidden_patterns or []

        for pattern in forbidden_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                line_number = content[: match.start()].count("\n") + 1
                matched_text = match.group(0)

                # Try to suggest correct pattern
                suggestion = self._get_workflow_suggestion(matched_text, definition)

                violations.append(
                    Violation(
                        definition=name,
                        file_path=str(file_path),
                        line_number=line_number,
                        message=f"Forbidden pattern: '{matched_text}'",
                        severity=definition.severity,
                        suggestion=suggestion,
                        context=self._get_line_context(content, line_number),
                    )
                )

        return violations

    def _check_minimum_version(
        self,
        name: str,
        definition: RegistryDefinition,
        source_value: Optional[str],
        file_path: Path,
        content: str,
    ) -> List[Violation]:
        """Check minimum version requirements."""
        # This would implement version comparison logic
        # For now, treat as generic pattern matching
        return self._check_generic_patterns(name, definition, file_path, content)

    def _check_generic_patterns(
        self, name: str, definition: RegistryDefinition, file_path: Path, content: str
    ) -> List[Violation]:
        """Check generic forbidden patterns."""
        violations: List[Violation] = []

        forbidden_patterns = definition.forbidden_patterns or []

        for pattern in forbidden_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                line_number = content[: match.start()].count("\n") + 1
                matched_text = match.group(0)

                violations.append(
                    Violation(
                        definition=name,
                        file_path=str(file_path),
                        line_number=line_number,
                        message=f"Forbidden pattern found: '{matched_text}'",
                        severity=definition.severity,
                        context=self._get_line_context(content, line_number),
                    )
                )

        return violations

    def _get_files_to_scan(self, definition: RegistryDefinition) -> List[Path]:
        """Get list of files to scan based on definition configuration."""
        scan_file_types = (
            definition.scan_file_types or self.registry.global_config.default_scan_types
        )
        excluded_dirs = set(
            self.registry.global_config.global_exclusions.get("directories", [])
        )
        excluded_patterns = set(
            self.registry.global_config.global_exclusions.get("file_patterns", [])
        )

        files_to_scan = []

        for pattern in scan_file_types:
            # Convert glob pattern to pathlib glob
            for file_path in self.repository_root.rglob(pattern):
                # Skip if in excluded directory
                if any(
                    excluded_dir in file_path.parts for excluded_dir in excluded_dirs
                ):
                    continue

                # Skip if matches excluded pattern
                if any(file_path.match(ex_pattern) for ex_pattern in excluded_patterns):
                    continue

                # Skip if too large
                max_size = (
                    self.registry.global_config.performance.get("max_file_size_mb", 10)
                    * 1024
                    * 1024
                )
                if file_path.stat().st_size > max_size:
                    continue

                files_to_scan.append(file_path)

        return files_to_scan

    def _get_workflow_suggestion(
        self, matched_text: str, definition: RegistryDefinition
    ) -> Optional[str]:
        """Get workflow suggestion based on replacement rules."""
        replacement_rules = definition.replacement_rules or []

        for rule in replacement_rules:
            find_pattern = rule.get("find", "")
            replace_pattern = rule.get("replace", "")

            if re.search(find_pattern, matched_text):
                return f"Use '{replace_pattern}' instead"

        return None

    def _get_line_context(
        self, content: str, line_number: int, context_lines: int = 2
    ) -> str:
        """Get surrounding lines for context."""
        lines = content.splitlines()
        start = max(0, line_number - context_lines - 1)
        end = min(len(lines), line_number + context_lines)

        context_lines_list = []
        for i in range(start, end):
            prefix = ">>> " if i == line_number - 1 else "    "
            context_lines_list.append(f"{prefix}{i + 1:4}: {lines[i]}")

        return "\n".join(context_lines_list)

    def _calculate_stats(
        self, violations: List[Violation], start_time: float, end_time: float
    ) -> ScanStats:
        """Calculate scan statistics."""
        high_count = len([v for v in violations if v.severity == Severity.HIGH])
        medium_count = len([v for v in violations if v.severity == Severity.MEDIUM])
        low_count = len([v for v in violations if v.severity == Severity.LOW])

        return ScanStats(
            files_scanned=0,  # TODO: Track this properly
            violations_found=len(violations),
            high_severity_count=high_count,
            medium_severity_count=medium_count,
            low_severity_count=low_count,
            scan_duration_seconds=end_time - start_time,
            timestamp=datetime.now().isoformat(),
        )

    def check_forbidden_files(self) -> List[Violation]:
        """Check for forbidden files in the repository."""
        violations = []

        for name, definition in self.registry.list_definitions().items():
            forbidden_files = definition.forbidden_files or []

            for forbidden_file in forbidden_files:
                # Check if forbidden file exists
                for file_path in self.repository_root.rglob(forbidden_file):
                    violations.append(
                        Violation(
                            definition=name,
                            file_path=str(file_path),
                            line_number=0,
                            message=f"Forbidden file found: {forbidden_file}",
                            severity=definition.severity,
                            suggestion="Remove this file or rename it",
                        )
                    )

        return violations
