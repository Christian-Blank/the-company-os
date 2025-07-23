"""
Source Truth Enforcement Service - Data Models

This module defines the data models used throughout the source truth enforcement system.
"""

from enum import Enum
from typing import List, Optional, Dict, Any, Tuple
from pydantic import BaseModel, Field


class Severity(str, Enum):
    """Violation severity levels."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Violation(BaseModel):
    """Represents a source of truth consistency violation."""

    definition: str = Field(..., description="Name of the source of truth definition")
    file_path: str = Field(..., description="Path to the file containing the violation")
    line_number: int = Field(..., description="Line number where the violation occurs")
    message: str = Field(..., description="Human-readable description of the violation")
    severity: Severity = Field(..., description="Severity level of the violation")
    suggestion: Optional[str] = Field(
        None, description="Suggested fix for the violation"
    )
    context: Optional[str] = Field(
        None, description="Surrounding context for the violation"
    )

    def __str__(self) -> str:
        """String representation of the violation."""
        return f"{self.severity.upper()}: {self.file_path}:{self.line_number} - {self.message}"


class ScanStats(BaseModel):
    """Statistics from a consistency scan."""

    files_scanned: int = Field(0, description="Number of files scanned")
    violations_found: int = Field(0, description="Total number of violations found")
    high_severity_count: int = Field(
        0, description="Number of high severity violations"
    )
    medium_severity_count: int = Field(
        0, description="Number of medium severity violations"
    )
    low_severity_count: int = Field(0, description="Number of low severity violations")
    scan_duration_seconds: float = Field(
        0.0, description="Duration of the scan in seconds"
    )
    timestamp: str = Field(..., description="ISO timestamp when the scan was performed")


class Report(BaseModel):
    """Comprehensive report of source truth consistency check."""

    violations: List[Violation] = Field(
        default_factory=list, description="List of violations found"
    )
    stats: ScanStats = Field(..., description="Scan statistics")
    registry_path: str = Field(..., description="Path to the registry file used")
    success: bool = Field(..., description="Whether the check passed (no violations)")
    ignore_summary: Optional["IgnoreSummary"] = Field(
        None, description="Summary of ignored violations"
    )

    def get_violations_by_severity(self, severity: Severity) -> List[Violation]:
        """Get violations filtered by severity level."""
        return [v for v in self.violations if v.severity == severity]

    def get_violations_by_definition(self, definition: str) -> List[Violation]:
        """Get violations filtered by definition name."""
        return [v for v in self.violations if v.definition == definition]

    def get_exit_code(self) -> int:
        """Get appropriate exit code based on violations."""
        if not self.violations:
            return 0  # Success

        high_count = len(self.get_violations_by_severity(Severity.HIGH))
        medium_count = len(self.get_violations_by_severity(Severity.MEDIUM))

        if high_count > 0:
            return 2  # Errors
        elif medium_count > 0:
            return 1  # Warnings
        else:
            return 1  # Low severity = warnings


class RegistryDefinition(BaseModel):
    """Represents a single source of truth definition from the registry."""

    description: str = Field(..., description="Human-readable description")
    type: str = Field(..., description="Type of validation (exact_version, etc.)")
    severity: Severity = Field(..., description="Default severity for violations")
    source: Optional[str] = Field(None, description="Path to the source of truth file")
    scan_patterns: Optional[List[str]] = Field(
        None, description="Regex patterns to scan for"
    )
    scan_file_types: Optional[List[str]] = Field(
        None, description="File patterns to scan"
    )
    forbidden_patterns: Optional[List[str]] = Field(
        None, description="Patterns that should not exist"
    )
    auto_fix: bool = Field(False, description="Whether auto-fix is supported")

    # Additional fields for specific definition types
    validation_pattern: Optional[str] = Field(
        None, description="Pattern to validate source value"
    )
    forbidden_files: Optional[List[str]] = Field(
        None, description="Files that must not exist"
    )
    replacement_rules: Optional[List[Dict[str, Any]]] = Field(
        None, description="Auto-fix replacement rules"
    )


class RegistryConfig(BaseModel):
    """Global configuration from the registry."""

    default_scan_types: List[str] = Field(default_factory=lambda: ["*.md"])
    global_exclusions: Dict[str, List[str]] = Field(default_factory=dict)
    performance: Dict[str, Any] = Field(default_factory=dict)
    reporting: Dict[str, Any] = Field(default_factory=dict)


class CheckerConfig(BaseModel):
    """Configuration for the consistency checker."""

    registry_path: str = Field(
        ..., description="Path to the source truth registry file"
    )
    repository_root: str = Field(".", description="Root directory of the repository")
    verbose: bool = Field(False, description="Enable verbose output")
    debug: bool = Field(False, description="Enable debug output")
    parallel: bool = Field(True, description="Enable parallel processing")
    cache_enabled: bool = Field(True, description="Enable result caching")


class IgnoreDirective(BaseModel):
    """Represents an ignore directive comment."""

    type: str = Field(..., description="Type: 'next-line', 'start', 'end', 'file'")
    rule_name: str = Field(..., description="Rule name to ignore")
    reason: str = Field(..., description="Reason for ignoring")
    line_number: int = Field(..., description="Line where directive appears")


class IgnoreContext(BaseModel):
    """Tracks active ignore directives while scanning."""

    file_ignores: Dict[str, str] = Field(
        default_factory=dict, description="rule -> reason"
    )
    block_ignores: Dict[str, Tuple[int, str]] = Field(
        default_factory=dict, description="rule -> (start_line, reason)"
    )
    next_line_ignores: Dict[str, str] = Field(
        default_factory=dict, description="rule -> reason"
    )
    ignore_ranges: Dict[str, List[Any]] = Field(
        default_factory=dict, description="rule -> List[IgnoreRange]"
    )


class IgnoredViolation(BaseModel):
    """Represents a violation that was ignored."""

    violation: Violation = Field(..., description="The original violation")
    reason: str = Field(..., description="Reason for ignoring")
    ignore_type: str = Field(..., description="Type of ignore directive used")


class IgnoreSummary(BaseModel):
    """Summary of ignored violations."""

    total_ignored: int = Field(0, description="Total number of ignored violations")
    ignored_by_rule: Dict[str, int] = Field(
        default_factory=dict, description="Count by rule name"
    )
    ignored_violations: List[IgnoredViolation] = Field(
        default_factory=list, description="List of ignored violations"
    )

    def add_ignored_violation(
        self, violation: Violation, reason: str, ignore_type: str
    ) -> None:
        """Add an ignored violation to the summary."""
        ignored = IgnoredViolation(
            violation=violation, reason=reason, ignore_type=ignore_type
        )
        self.ignored_violations.append(ignored)
        self.total_ignored += 1

        rule_name = violation.definition
        self.ignored_by_rule[rule_name] = self.ignored_by_rule.get(rule_name, 0) + 1
