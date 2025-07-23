"""
Source Truth Enforcement Service - Ignore Parser

This module handles parsing of ESLint-style ignore comments for suppressing violations.
"""

import re
from typing import Dict, List, Tuple, Optional, Set
from .models import IgnoreDirective, IgnoreContext


class IgnoreRange:
    """Represents a range of lines to ignore."""

    def __init__(self, start_line: int, end_line: int, reason: str):
        self.start_line = start_line
        self.end_line = end_line
        self.reason = reason

    def contains(self, line_number: int) -> bool:
        """Check if a line number is within this ignore range."""
        return self.start_line < line_number < self.end_line


class IgnoreParser:
    """Parses source-truth-ignore comments."""

    # Regex patterns for different ignore types
    IGNORE_NEXT_LINE_PATTERN = r"#\s*source-truth-ignore-next-line\s+(\S+)\s+--\s+(.+)$"
    IGNORE_START_PATTERN = r"#\s*source-truth-ignore-start\s+(\S+)\s+--\s+(.+)$"
    IGNORE_END_PATTERN = r"#\s*source-truth-ignore-end\s+(\S+)$"
    IGNORE_FILE_PATTERN = r"#\s*source-truth-ignore-file\s+(\S+)\s+--\s+(.+)$"

    # HTML/Markdown comment patterns (for documentation)
    HTML_IGNORE_NEXT_LINE_PATTERN = (
        r"<!--\s*source-truth-ignore-next-line\s+(\S+)\s+--\s+(.+)\s*-->"
    )
    HTML_IGNORE_START_PATTERN = (
        r"<!--\s*source-truth-ignore-start\s+(\S+)\s+--\s+(.+)\s*-->"
    )
    HTML_IGNORE_END_PATTERN = r"<!--\s*source-truth-ignore-end\s+(\S+)\s*-->"
    HTML_IGNORE_FILE_PATTERN = (
        r"<!--\s*source-truth-ignore-file\s+(\S+)\s+--\s+(.+)\s*-->"
    )

    def __init__(self, debug: bool = False):
        """Initialize the ignore parser.

        Args:
            debug: Enable debug output
        """
        self.debug = debug

    def parse_file_for_ignores(
        self, content: str, file_path: str = ""
    ) -> IgnoreContext:
        """Parse file content and extract all ignore directives.

        Args:
            content: File content to parse
            file_path: Path to the file (for debugging)

        Returns:
            IgnoreContext with all parsed ignore directives
        """
        context = IgnoreContext()
        lines = content.splitlines()

        # First pass: collect all directives
        all_directives = []
        for line_number, line in enumerate(lines, 1):
            directive = self._parse_line_for_ignore(line, line_number)
            if directive:
                all_directives.append(directive)
                if self.debug:
                    print(
                        f"  📝 {file_path}:{directive.line_number} - Found {directive.type} ignore for {directive.rule_name}: {directive.reason}"
                    )

        # Second pass: build complete ignore ranges
        ignore_ranges: Dict[
            str, List[IgnoreRange]
        ] = {}  # rule_name -> List[IgnoreRange]
        active_starts: Dict[
            str, Tuple[int, str]
        ] = {}  # rule_name -> (start_line, reason)

        for directive in all_directives:
            if directive.type == "file":
                context.file_ignores[directive.rule_name] = directive.reason

            elif directive.type == "next-line":
                context.next_line_ignores[directive.rule_name] = directive.reason

            elif directive.type == "start":
                if directive.rule_name in active_starts:
                    if self.debug:
                        print(
                            f"  ⚠️ {file_path}:{directive.line_number} - Warning: Block ignore for {directive.rule_name} already started"
                        )
                active_starts[directive.rule_name] = (
                    directive.line_number,
                    directive.reason,
                )

            elif directive.type == "end":
                if directive.rule_name not in active_starts:
                    if self.debug:
                        print(
                            f"  ⚠️ {file_path}:{directive.line_number} - Warning: Block ignore end for {directive.rule_name} without matching start"
                        )
                else:
                    start_line, reason = active_starts[directive.rule_name]
                    end_line = directive.line_number

                    # Create ignore range
                    if directive.rule_name not in ignore_ranges:
                        ignore_ranges[directive.rule_name] = []
                    ignore_ranges[directive.rule_name].append(
                        IgnoreRange(start_line, end_line, reason)
                    )

                    # Remove from active starts
                    del active_starts[directive.rule_name]

        # Store completed ranges in context
        context.ignore_ranges = ignore_ranges

        # Store any unclosed blocks as well (for validation)
        context.block_ignores = active_starts

        return context

    def _parse_line_for_ignore(
        self, line: str, line_number: int
    ) -> Optional[IgnoreDirective]:
        """Parse a single line for ignore directives.

        Args:
            line: Line content
            line_number: Line number in file

        Returns:
            IgnoreDirective if found, None otherwise
        """
        line = line.strip()

        # Try hash comment patterns first
        patterns = [
            (self.IGNORE_NEXT_LINE_PATTERN, "next-line"),
            (self.IGNORE_START_PATTERN, "start"),
            (self.IGNORE_END_PATTERN, "end"),
            (self.IGNORE_FILE_PATTERN, "file"),
        ]

        for pattern, directive_type in patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                if directive_type == "end":
                    # End directive doesn't have a reason
                    rule_name = match.group(1)
                    reason = ""
                else:
                    rule_name = match.group(1)
                    reason = match.group(2).strip()

                return IgnoreDirective(
                    type=directive_type,
                    rule_name=rule_name,
                    reason=reason,
                    line_number=line_number,
                )

        # Try HTML comment patterns for markdown/html files
        html_patterns = [
            (self.HTML_IGNORE_NEXT_LINE_PATTERN, "next-line"),
            (self.HTML_IGNORE_START_PATTERN, "start"),
            (self.HTML_IGNORE_END_PATTERN, "end"),
            (self.HTML_IGNORE_FILE_PATTERN, "file"),
        ]

        for pattern, directive_type in html_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                if directive_type == "end":
                    rule_name = match.group(1)
                    reason = ""
                else:
                    rule_name = match.group(1)
                    reason = match.group(2).strip()

                return IgnoreDirective(
                    type=directive_type,
                    rule_name=rule_name,
                    reason=reason,
                    line_number=line_number,
                )

        return None

    def _apply_directive(
        self, directive: IgnoreDirective, context: IgnoreContext, file_path: str
    ) -> None:
        """Apply an ignore directive to the context.

        Args:
            directive: The directive to apply
            context: Context to update
            file_path: File path for debugging
        """
        if self.debug:
            print(
                f"  📝 {file_path}:{directive.line_number} - Found {directive.type} ignore for {directive.rule_name}: {directive.reason}"
            )

        if directive.type == "file":
            context.file_ignores[directive.rule_name] = directive.reason

        elif directive.type == "next-line":
            context.next_line_ignores[directive.rule_name] = directive.reason

        elif directive.type == "start":
            if directive.rule_name in context.block_ignores:
                if self.debug:
                    print(
                        f"  ⚠️ {file_path}:{directive.line_number} - Warning: Block ignore for {directive.rule_name} already started"
                    )
            context.block_ignores[directive.rule_name] = (
                directive.line_number,
                directive.reason,
            )

        elif directive.type == "end":
            if directive.rule_name not in context.block_ignores:
                if self.debug:
                    print(
                        f"  ⚠️ {file_path}:{directive.line_number} - Warning: Block ignore end for {directive.rule_name} without matching start"
                    )
            # Don't remove from block_ignores - we need the range information

    def is_line_ignored(
        self, line_number: int, rule_name: str, context: IgnoreContext
    ) -> Tuple[bool, Optional[str]]:
        """Check if a line should be ignored for a specific rule.

        Args:
            line_number: Line number to check
            rule_name: Rule name to check
            context: Ignore context

        Returns:
            Tuple of (is_ignored, reason)
        """
        # Check file-wide ignores
        if rule_name in context.file_ignores:
            return True, context.file_ignores[rule_name]

        # Check next-line ignores (for the previous line)
        if rule_name in context.next_line_ignores:
            reason = context.next_line_ignores[rule_name]
            # Clear the next-line ignore after using it
            del context.next_line_ignores[rule_name]
            return True, reason

        # Check ignore ranges
        if hasattr(context, "ignore_ranges") and rule_name in context.ignore_ranges:
            for ignore_range in context.ignore_ranges[rule_name]:
                if ignore_range.contains(line_number):
                    return True, ignore_range.reason

        return False, None

    def validate_ignore_blocks(
        self, context: IgnoreContext, file_path: str = ""
    ) -> List[str]:
        """Validate that all ignore blocks are properly closed.

        Args:
            context: Ignore context to validate
            file_path: File path for error messages

        Returns:
            List of validation errors
        """
        errors = []

        for rule_name, (start_line, reason) in context.block_ignores.items():
            errors.append(
                f"Unclosed ignore block for rule '{rule_name}' started at line {start_line}"
            )

        return errors

    def validate_ignore_directive(
        self, directive: IgnoreDirective, valid_rules: Set[str]
    ) -> List[str]:
        """Validate an ignore directive.

        Args:
            directive: Directive to validate
            valid_rules: Set of valid rule names

        Returns:
            List of validation errors
        """
        errors = []

        # Check if rule name is valid
        if directive.rule_name not in valid_rules:
            errors.append(
                f"Unknown rule name '{directive.rule_name}' at line {directive.line_number}"
            )

        # Check if reason is provided (except for end directives)
        if directive.type != "end" and not directive.reason.strip():
            errors.append(
                f"Missing reason for ignore directive at line {directive.line_number}. Use: -- <reason>"
            )

        return errors

    def get_all_directives_in_file(self, content: str) -> List[IgnoreDirective]:
        """Get all ignore directives in a file (for validation and reporting).

        Args:
            content: File content

        Returns:
            List of all ignore directives found
        """
        directives = []
        lines = content.splitlines()

        for line_number, line in enumerate(lines, 1):
            directive = self._parse_line_for_ignore(line, line_number)
            if directive:
                directives.append(directive)

        return directives
