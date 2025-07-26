"""Document validation engine for the Rules Service."""

import re
import datetime
from typing import List, Dict, Optional, Any, Callable, Union, Tuple
from pathlib import Path
from dataclasses import dataclass, field
import yaml
from yaml import YAMLError

from .models import RuleDocument


class DocumentType:
    """Constants for document types."""

    DECISION = "decision"
    BRIEF = "brief"
    SIGNAL = "signal"
    VISION = "vision"
    CHARTER = "charter"
    RULES = "rules"
    WORKFLOW = "workflow"
    METHODOLOGY = "methodology"
    REGISTRY = "registry"
    TEMPLATE = "template"
    REFERENCE = "reference"
    ANALYSIS = "analysis"
    PARADIGM = "paradigm"
    PRINCIPLE = "principle"
    UNKNOWN = "unknown"


class Severity:
    """Constants for validation issue severity levels."""

    ERROR = "error"  # Must fix - document is invalid
    WARNING = "warning"  # Should fix - document has issues
    INFO = "info"  # May fix - suggestions for improvement


class IssueCategory:
    """Categories for validation issues."""

    MISSING_CONTENT = "missing-content"
    INVALID_FORMAT = "invalid-format"
    INVALID_REFERENCE = "invalid-reference"
    INCOMPLETE_ANALYSIS = "incomplete-analysis"
    CLARIFICATION_NEEDED = "clarification-needed"
    DECISION_REQUIRED = "decision-required"
    FORMAT_ERROR = "format-error"
    REVIEW_NEEDED = "review-needed"


@dataclass
class ValidationIssue:
    """A validation issue found in a document."""

    rule_id: str
    severity: str  # error, warning, info
    category: str  # from IssueCategory
    message: str
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    file_path: Optional[str] = None
    suggestion: Optional[str] = None
    auto_fixable: bool = False
    rule_source: Optional[str] = None  # Which rule document this came from

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "category": self.category,
            "message": self.message,
            "line_number": self.line_number,
            "column_number": self.column_number,
            "file_path": self.file_path,
            "suggestion": self.suggestion,
            "auto_fixable": self.auto_fixable,
            "rule_source": self.rule_source,
        }


@dataclass
class ValidationResult:
    """Result of validating a document."""

    file_path: str
    document_type: str
    issues: List[ValidationIssue] = field(default_factory=list)
    validation_time: Optional[float] = None
    rule_count: int = 0

    @property
    def error_count(self) -> int:
        """Count of error-level issues."""
        return sum(1 for issue in self.issues if issue.severity == Severity.ERROR)

    @property
    def warning_count(self) -> int:
        """Count of warning-level issues."""
        return sum(1 for issue in self.issues if issue.severity == Severity.WARNING)

    @property
    def info_count(self) -> int:
        """Count of info-level issues."""
        return sum(1 for issue in self.issues if issue.severity == Severity.INFO)

    @property
    def is_valid(self) -> bool:
        """Check if document is valid (no errors)."""
        return self.error_count == 0

    @property
    def auto_fixable_count(self) -> int:
        """Count of auto-fixable issues."""
        return sum(1 for issue in self.issues if issue.auto_fixable)

    def get_issues_by_severity(self, severity: str) -> List[ValidationIssue]:
        """Get all issues of a specific severity."""
        return [issue for issue in self.issues if issue.severity == severity]

    def get_issues_by_category(self, category: str) -> List[ValidationIssue]:
        """Get all issues of a specific category."""
        return [issue for issue in self.issues if issue.category == category]

    def get_auto_fixable_issues(self) -> List[ValidationIssue]:
        """Get all auto-fixable issues."""
        return [issue for issue in self.issues if issue.auto_fixable]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "file_path": self.file_path,
            "document_type": self.document_type,
            "issues": [issue.to_dict() for issue in self.issues],
            "validation_time": self.validation_time,
            "rule_count": self.rule_count,
            "summary": {
                "total_issues": len(self.issues),
                "errors": self.error_count,
                "warnings": self.warning_count,
                "info": self.info_count,
                "auto_fixable": self.auto_fixable_count,
                "is_valid": self.is_valid,
            },
        }


@dataclass
class ExtractedRule:
    """A rule extracted from a rules document."""

    rule_id: str
    rule_type: str  # 'frontmatter', 'section', 'pattern', 'content'
    description: str
    pattern: Optional[str] = None
    required_fields: Optional[List[str]] = None
    validation_func: Optional[Callable] = None
    auto_fixable: bool = False
    severity: str = "error"  # error, warning, info
    applies_to: List[str] = field(default_factory=list)
    source_file: Optional[str] = None
    line_number: Optional[int] = None


class RuleExtractor:
    """Extracts validation rules from markdown rule documents."""

    def __init__(self):
        self.extracted_rules: List[ExtractedRule] = []

    def extract_rules_from_document(
        self, rule_doc: RuleDocument, content: str
    ) -> List[ExtractedRule]:
        """Extract validation rules from a rule document's content."""
        self.extracted_rules = []

        # Extract rules from different sources
        self._extract_from_tables(content, rule_doc)
        self._extract_from_code_blocks(content, rule_doc)
        self._extract_from_lists(content, rule_doc)
        self._extract_from_yaml_blocks(content, rule_doc)

        # Add applies_to from rule document
        for rule in self.extracted_rules:
            if not rule.applies_to and rule_doc.applies_to:
                rule.applies_to = rule_doc.applies_to
            if not rule.source_file:
                rule.source_file = rule_doc.file_path

        return self.extracted_rules

    def _extract_from_tables(self, content: str, rule_doc: RuleDocument):
        """Extract rules from markdown tables using regex."""
        # Find tables with validation rules
        table_pattern = (
            r"\|[^\n]+\|[^\n]+\|[^\n]*\|\n\|[-:\s|]+\|\n((?:\|[^\n]+\|\n?)+)"
        )

        for table_match in re.finditer(table_pattern, content, re.MULTILINE):
            lines = table_match.group(0).strip().split("\n")
            if len(lines) < 3:
                continue

            # Parse headers
            headers = [h.strip() for h in lines[0].split("|") if h.strip()]

            # Check if this is a validation table
            header_lower = [h.lower() for h in headers]
            if not any(
                h in header_lower
                for h in ["field", "validation rule", "pattern", "requirement", "rule"]
            ):
                continue

            # Parse rows (skip header and separator)
            for line in lines[2:]:
                cells = [c.strip() for c in line.split("|") if c.strip()]
                if len(cells) >= 2:
                    self._parse_table_row(headers, cells, rule_doc)

    def _parse_table_row(
        self, headers: List[str], cells: List[str], rule_doc: RuleDocument
    ):
        """Parse a table row into an ExtractedRule."""
        row_data = {}
        for i, cell in enumerate(cells):
            if i < len(headers):
                row_data[headers[i].lower()] = cell

        # Extract rule information
        field_name = row_data.get("field", row_data.get("pattern", ""))
        validation_rule = row_data.get(
            "validation rule", row_data.get("rule", row_data.get("requirement", ""))
        )

        if field_name and validation_rule:
            rule_id = (
                f"{rule_doc.title}_{field_name}".replace(" ", "_")
                .replace(":", "")
                .lower()
            )

            # Determine rule type
            if "frontmatter" in field_name.lower() or "field" in headers[0].lower():
                rule_type = "frontmatter"
            else:
                rule_type = "pattern"

            self.extracted_rules.append(
                ExtractedRule(
                    rule_id=rule_id,
                    rule_type=rule_type,
                    description=validation_rule,
                    pattern=row_data.get("example", row_data.get("pattern", "")),
                    severity=self._determine_severity(validation_rule),
                )
            )

    def _extract_from_code_blocks(self, content: str, rule_doc: RuleDocument):
        """Extract validation patterns from code blocks."""
        # Find code blocks with language specifiers
        code_block_pattern = r"```(\w+)\n(.*?)\n```"

        for match in re.finditer(code_block_pattern, content, re.DOTALL):
            language = match.group(1).lower()
            code = match.group(2).strip()

            if language in ["regex", "regexp", "pattern"]:
                rule_id = (
                    f"{rule_doc.title}_pattern_{len(self.extracted_rules)}".replace(
                        " ", "_"
                    ).lower()
                )
                self.extracted_rules.append(
                    ExtractedRule(
                        rule_id=rule_id,
                        rule_type="pattern",
                        description=f"Pattern validation: {code[:50]}...",
                        pattern=code,
                        severity="error",
                    )
                )

    def _extract_from_yaml_blocks(self, content: str, rule_doc: RuleDocument):
        """Extract frontmatter requirements from YAML code blocks."""
        yaml_block_pattern = r"```yaml\n(.*?)\n```"

        for match in re.finditer(yaml_block_pattern, content, re.DOTALL):
            yaml_content = match.group(1).strip()

            # Extract field names from YAML
            required_fields = []
            for line in yaml_content.split("\n"):
                if ":" in line and not line.strip().startswith("#"):
                    field = line.split(":")[0].strip()
                    if field and not field.startswith("-"):
                        required_fields.append(field)

            if required_fields:
                # Find the section this YAML block is in
                position = match.start()
                lines_before = content[:position].split("\n")
                section = "Document"
                for line in reversed(lines_before):
                    if line.startswith("#"):
                        section = line.strip("#").strip()
                        break

                rule_id = f"{rule_doc.title}_{section}_frontmatter".replace(
                    " ", "_"
                ).lower()
                self.extracted_rules.append(
                    ExtractedRule(
                        rule_id=rule_id,
                        rule_type="frontmatter",
                        description=f"Required frontmatter fields for {section}",
                        required_fields=required_fields,
                        severity="error",
                    )
                )

    def _extract_from_lists(self, content: str, rule_doc: RuleDocument):
        """Extract rules from bullet point lists."""
        # Find sections with rules
        lines = content.split("\n")
        current_section = ""

        for i, line in enumerate(lines):
            if line.startswith("#"):
                current_section = line.strip("#").strip()
            elif line.strip().startswith(("- ", "* ", "+ ")):
                # Check if this line contains a rule
                text = line.strip().lstrip("-*+ ").strip()

                # Pattern for explicit rules
                rule_match = re.match(
                    r"^Rule\s+(\d+(?:\.\d+)?):?\s*(.+)", text, re.IGNORECASE
                )
                if rule_match:
                    rule_num = rule_match.group(1)
                    description = rule_match.group(2)
                    rule_id = f"{rule_doc.title}_rule_{rule_num}".replace(
                        " ", "_"
                    ).lower()

                    self.extracted_rules.append(
                        ExtractedRule(
                            rule_id=rule_id,
                            rule_type="content",
                            description=description,
                            severity=self._determine_severity(description),
                            line_number=i + 1,
                        )
                    )
                    continue

                # Pattern for must/should/shall rules
                modal_match = re.match(
                    r"^(Must|Should|Shall|May)\s+(.+)", text, re.IGNORECASE
                )
                if modal_match and (
                    "rule" in current_section.lower()
                    or "validation" in current_section.lower()
                ):
                    modal = modal_match.group(1).lower()
                    description = text
                    rule_id = f"{rule_doc.title}_{current_section}_{modal}_{len(self.extracted_rules)}".replace(
                        " ", "_"
                    ).lower()

                    self.extracted_rules.append(
                        ExtractedRule(
                            rule_id=rule_id,
                            rule_type="content",
                            description=description,
                            severity=self._determine_severity(text),
                            line_number=i + 1,
                        )
                    )

    def _determine_severity(self, text: str) -> str:
        """Determine severity level from rule text."""
        text_lower = text.lower()
        if any(word in text_lower for word in ["must", "required", "shall"]):
            return "error"
        elif any(word in text_lower for word in ["should", "recommended"]):
            return "warning"
        elif any(word in text_lower for word in ["may", "optional", "can"]):
            return "info"
        return "error"  # Default to error


class RuleEngine:
    """Manages and applies extracted rules for validation."""

    def __init__(self):
        self.rules_by_type: Dict[str, List[ExtractedRule]] = {
            "frontmatter": [],
            "section": [],
            "pattern": [],
            "content": [],
        }
        self.rules_by_document_type: Dict[str, List[ExtractedRule]] = {}

    def add_rules(self, rules: List[ExtractedRule]):
        """Add extracted rules to the engine."""
        for rule in rules:
            # Organize by rule type
            if rule.rule_type in self.rules_by_type:
                self.rules_by_type[rule.rule_type].append(rule)

            # Organize by document type
            for doc_type in rule.applies_to:
                if doc_type not in self.rules_by_document_type:
                    self.rules_by_document_type[doc_type] = []
                self.rules_by_document_type[doc_type].append(rule)

    def get_rules_for_document(self, document_type: str) -> List[ExtractedRule]:
        """Get all rules that apply to a specific document type."""
        rules = []

        # Get type-specific rules
        if document_type in self.rules_by_document_type:
            rules.extend(self.rules_by_document_type[document_type])

        # Get universal rules (those without specific applies_to)
        for rule_list in self.rules_by_type.values():
            for rule in rule_list:
                if not rule.applies_to:  # Universal rule
                    rules.append(rule)

        # Remove duplicates
        seen = set()
        unique_rules = []
        for rule in rules:
            if rule.rule_id not in seen:
                seen.add(rule.rule_id)
                unique_rules.append(rule)

        return unique_rules


class DocumentTypeDetector:
    """Detects document type from file path and name."""

    # Mapping of file suffixes to document types
    SUFFIX_MAPPING = {
        ".decision.md": DocumentType.DECISION,
        ".brief.md": DocumentType.BRIEF,
        ".signal.md": DocumentType.SIGNAL,
        ".vision.md": DocumentType.VISION,
        ".charter.md": DocumentType.CHARTER,
        ".rules.md": DocumentType.RULES,
        ".workflow.md": DocumentType.WORKFLOW,
        ".methodology.md": DocumentType.METHODOLOGY,
        ".registry.md": DocumentType.REGISTRY,
        "-template.md": DocumentType.TEMPLATE,
        ".reference.md": DocumentType.REFERENCE,
        ".analysis.md": DocumentType.ANALYSIS,
        ".paradigm.md": DocumentType.PARADIGM,
        ".principle.md": DocumentType.PRINCIPLE,
    }

    # Path patterns for document types
    PATH_PATTERNS = {
        DocumentType.DECISION: ["/decisions/", "/work/domains/decisions/"],
        DocumentType.BRIEF: ["/briefs/", "/work/domains/briefs/"],
        DocumentType.SIGNAL: ["/signals/", "/work/domains/signals/"],
        DocumentType.CHARTER: ["/charters/", "/os/domains/charters/"],
        DocumentType.RULES: ["/rules/", "/os/domains/rules/"],
        DocumentType.WORKFLOW: ["/processes/", "/workflows/"],
        DocumentType.METHODOLOGY: ["/processes/", "/methodologies/"],
        DocumentType.REGISTRY: ["/registries/", "/registry/"],
    }

    @classmethod
    def detect_type(cls, file_path: Union[str, Path]) -> str:
        """
        Detect document type from file path.

        Args:
            file_path: Path to the document

        Returns:
            Document type constant from DocumentType class
        """
        path = Path(file_path)
        path_str = str(path).replace("\\", "/")  # Normalize path separators
        filename = path.name.lower()

        # First, check file suffix
        for suffix, doc_type in cls.SUFFIX_MAPPING.items():
            if filename.endswith(suffix):
                return doc_type

        # Then check path patterns
        for doc_type, patterns in cls.PATH_PATTERNS.items():
            for pattern in patterns:
                if pattern in path_str:
                    return doc_type

        # Check for generic markdown files in specific directories
        if filename.endswith(".md"):
            # Additional heuristics based on content or location
            if "template" in filename:
                return DocumentType.TEMPLATE
            elif "reference" in filename or "ref" in filename:
                return DocumentType.REFERENCE

        return DocumentType.UNKNOWN

    @classmethod
    def get_rules_for_type(
        cls, document_type: str, rule_engine: RuleEngine
    ) -> List[ExtractedRule]:
        """
        Get all rules that apply to a specific document type.

        Args:
            document_type: The document type
            rule_engine: The rule engine containing all rules

        Returns:
            List of rules that apply to this document type
        """
        return rule_engine.get_rules_for_document(document_type)

    @classmethod
    def get_type_info(cls, document_type: str) -> Dict[str, Any]:
        """
        Get information about a document type.

        Returns dict with:
        - name: Human-readable name
        - file_pattern: Expected file naming pattern
        - path_hint: Where these files are typically located
        - description: What this document type is for
        """
        type_info = {
            DocumentType.DECISION: {
                "name": "Decision Record",
                "file_pattern": "DEC-YYYY-MM-DD-NNN-slug.decision.md",
                "path_hint": "/work/domains/decisions/data/",
                "description": "Records of architectural and operational decisions",
            },
            DocumentType.BRIEF: {
                "name": "Opportunity Brief",
                "file_pattern": "BRIEF-YYYY-MM-DD-NNN-slug.brief.md",
                "path_hint": "/work/domains/briefs/data/",
                "description": "Synthesized opportunities from signal analysis",
            },
            DocumentType.SIGNAL: {
                "name": "Signal",
                "file_pattern": "SIG-YYYY-MM-DD-NNN-description.signal.md",
                "path_hint": "/work/domains/signals/data/",
                "description": "Captured friction points, opportunities, and insights",
            },
            DocumentType.VISION: {
                "name": "Project Vision",
                "file_pattern": "project-name.vision.md",
                "path_hint": "/work/domains/projects/data/",
                "description": "High-level vision and goals for a project",
            },
            DocumentType.CHARTER: {
                "name": "Charter",
                "file_pattern": "service-name.charter.md",
                "path_hint": "/os/domains/charters/data/",
                "description": "Foundational governance and vision documents",
            },
            DocumentType.RULES: {
                "name": "Rules Document",
                "file_pattern": "system-name.rules.md",
                "path_hint": "/os/domains/rules/data/",
                "description": "Operational rules and constraints",
            },
            DocumentType.WORKFLOW: {
                "name": "Workflow",
                "file_pattern": "process-name.workflow.md",
                "path_hint": "/os/domains/processes/data/",
                "description": "Defined workflows and processes",
            },
            DocumentType.METHODOLOGY: {
                "name": "Methodology",
                "file_pattern": "methodology-name.methodology.md",
                "path_hint": "/os/domains/processes/data/",
                "description": "Development and operational methodologies",
            },
            DocumentType.REGISTRY: {
                "name": "Registry",
                "file_pattern": "name.registry.md",
                "path_hint": "/os/domains/registry/data/",
                "description": "Service and component registries",
            },
            DocumentType.TEMPLATE: {
                "name": "Template",
                "file_pattern": "document-type-template.md",
                "path_hint": "Various locations",
                "description": "Templates for creating new documents",
            },
            DocumentType.REFERENCE: {
                "name": "Reference",
                "file_pattern": "topic.reference.md",
                "path_hint": "Various locations",
                "description": "Reference documentation and guides",
            },
            DocumentType.UNKNOWN: {
                "name": "Unknown",
                "file_pattern": "*.md",
                "path_hint": "N/A",
                "description": "Document type could not be determined",
            },
        }

        return type_info.get(document_type, type_info[DocumentType.UNKNOWN])


class HumanInputCommentGenerator:
    """Generates human input comments for validation issues."""

    # Valid comment categories
    CATEGORIES = {
        IssueCategory.MISSING_CONTENT: "MISSING-CONTENT",
        IssueCategory.INVALID_REFERENCE: "INVALID-REFERENCE",
        IssueCategory.INCOMPLETE_ANALYSIS: "INCOMPLETE-ANALYSIS",
        IssueCategory.CLARIFICATION_NEEDED: "CLARIFICATION-NEEDED",
        IssueCategory.DECISION_REQUIRED: "DECISION-REQUIRED",
        IssueCategory.FORMAT_ERROR: "FORMAT-ERROR",
        IssueCategory.REVIEW_NEEDED: "REVIEW-NEEDED",
    }

    def generate_comment(self, issue: ValidationIssue) -> str:
        """
        Generate a human input comment for a validation issue.

        Args:
            issue: The validation issue requiring human input

        Returns:
            Formatted comment string
        """
        category = self.CATEGORIES.get(issue.category, "REVIEW-NEEDED")
        priority = self._determine_priority(issue)

        comment = f"""<!-- HUMAN-INPUT-REQUIRED: {category}
Issue: {issue.message}
Required Action: {self._get_required_action(issue)}
Context: {self._get_context(issue)}
Priority: {priority}
-->"""

        return comment

    def _determine_priority(self, issue: ValidationIssue) -> str:
        """Determine priority based on severity and category."""
        if issue.severity == Severity.ERROR:
            return "high"
        elif issue.severity == Severity.WARNING:
            return "medium"
        else:
            return "low"

    def _get_required_action(self, issue: ValidationIssue) -> str:
        """Get specific action required for the issue."""
        if issue.suggestion:
            return issue.suggestion

        # Default actions based on category
        actions = {
            IssueCategory.MISSING_CONTENT: "Add the required content",
            IssueCategory.INVALID_REFERENCE: "Update reference to valid target",
            IssueCategory.INCOMPLETE_ANALYSIS: "Expand analysis with more detail",
            IssueCategory.CLARIFICATION_NEEDED: "Clarify the ambiguous content",
            IssueCategory.DECISION_REQUIRED: "Choose appropriate option",
            IssueCategory.FORMAT_ERROR: "Manually fix the formatting issue",
            IssueCategory.REVIEW_NEEDED: "Review and approve the content",
        }

        return actions.get(issue.category, "Address the validation issue")

    def _get_context(self, issue: ValidationIssue) -> str:
        """Get additional context for the issue."""
        context_parts = []

        if issue.rule_source:
            context_parts.append(f"Rule source: {issue.rule_source}")

        if issue.line_number:
            context_parts.append(f"Line {issue.line_number}")

        if issue.rule_id:
            context_parts.append(f"Rule ID: {issue.rule_id}")

        return "; ".join(context_parts) if context_parts else "No additional context"

    def generate_comments(self, issues: List[ValidationIssue]) -> List[Dict[str, Any]]:
        """
        Generate human input comments for multiple validation issues.

        Args:
            issues: List of validation issues

        Returns:
            List of comment dictionaries with 'comment' and 'priority' keys
        """
        comments = []
        for issue in issues:
            comment = self.generate_comment(issue)
            priority = self._determine_priority(issue)
            comments.append(
                {
                    "comment": comment,
                    "priority": priority,
                    "issue_id": issue.rule_id,
                    "category": issue.category,
                }
            )
        return comments

    def insert_comments_in_content(
        self, content: str, issues: List[ValidationIssue]
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Insert human input comments into document content.

        Args:
            content: Original document content
            issues: List of issues requiring human input

        Returns:
            Tuple of (content with comments, insertion log)
        """
        if not issues:
            return content, []

        lines = content.split("\n")
        insertion_log = []

        # Sort issues by line number (reverse to avoid offset issues)
        sorted_issues = sorted(
            [i for i in issues if not i.auto_fixable],
            key=lambda x: x.line_number or 0,
            reverse=True,
        )

        for issue in sorted_issues:
            comment = self.generate_comment(issue)
            placement = self._determine_placement(issue, lines)

            if placement["type"] == "after_line":
                line_idx = placement["line"] - 1  # Convert to 0-based
                if 0 <= line_idx < len(lines):
                    lines.insert(line_idx + 1, comment)
                    insertion_log.append(
                        {
                            "issue_id": issue.rule_id,
                            "category": issue.category,
                            "inserted_at": line_idx + 2,  # 1-based for log
                            "placement": "after_line",
                        }
                    )
            elif placement["type"] == "before_section":
                line_idx = placement["line"] - 1
                if 0 <= line_idx < len(lines):
                    lines.insert(line_idx, comment)
                    insertion_log.append(
                        {
                            "issue_id": issue.rule_id,
                            "category": issue.category,
                            "inserted_at": line_idx + 1,
                            "placement": "before_section",
                        }
                    )
            elif placement["type"] == "in_frontmatter":
                # Find end of frontmatter
                fm_end = self._find_frontmatter_end(lines)
                if fm_end > 0:
                    lines.insert(fm_end, comment)
                    insertion_log.append(
                        {
                            "issue_id": issue.rule_id,
                            "category": issue.category,
                            "inserted_at": fm_end + 1,
                            "placement": "in_frontmatter",
                        }
                    )
            elif placement["type"] == "end_of_file":
                lines.append(comment)
                insertion_log.append(
                    {
                        "issue_id": issue.rule_id,
                        "category": issue.category,
                        "inserted_at": len(lines),
                        "placement": "end_of_file",
                    }
                )

        return "\n".join(lines), insertion_log

    def _determine_placement(
        self, issue: ValidationIssue, lines: List[str]
    ) -> Dict[str, Any]:
        """Determine where to place the comment."""
        # If we have a line number, place after that line
        if issue.line_number:
            return {"type": "after_line", "line": issue.line_number}

        # For missing sections, place before the next section or at end
        if (
            issue.category == IssueCategory.MISSING_CONTENT
            and "section" in issue.message.lower()
        ):
            # Find appropriate location for section
            section_match = re.search(r"section:\s*(.+)", issue.message)
            if section_match:
                # For now, add at end of file
                return {"type": "end_of_file"}

        # For frontmatter issues, place in frontmatter
        if "frontmatter" in issue.message.lower() or "field" in issue.message.lower():
            return {"type": "in_frontmatter"}

        # Default to end of file
        return {"type": "end_of_file"}

    def _find_frontmatter_end(self, lines: List[str]) -> int:
        """Find the line index after frontmatter closing delimiter."""
        if not lines or not lines[0].startswith("---"):
            return -1

        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return i

        return -1


class ValidationService:
    """Service for validating documents against rules."""

    def __init__(
        self, rules: List[RuleDocument], rule_contents: Optional[Dict[str, str]] = None
    ):
        """
        Initialize with rule documents and their content.

        Args:
            rules: List of RuleDocument objects with metadata
            rule_contents: Optional dict mapping file paths to content strings.
                          If not provided, will attempt to read from file_path in RuleDocument.
        """
        self.rule_engine = RuleEngine()
        self.rule_extractor = RuleExtractor()
        self.auto_fixer = AutoFixer()
        self.comment_generator = HumanInputCommentGenerator()

        # Extract rules from all rule documents
        for rule_doc in rules:
            content = self._get_rule_content(rule_doc, rule_contents)
            if content:
                extracted_rules = self.rule_extractor.extract_rules_from_document(
                    rule_doc, content
                )
                self.rule_engine.add_rules(extracted_rules)

    def _get_rule_content(
        self, rule_doc: RuleDocument, rule_contents: Optional[Dict[str, str]]
    ) -> Optional[str]:
        """
        Get content for a rule document.

        Args:
            rule_doc: The rule document metadata
            rule_contents: Optional pre-loaded content dict

        Returns:
            Content string or None if not found
        """
        # First try the provided content dict
        if rule_contents and rule_doc.file_path in rule_contents:
            return rule_contents[rule_doc.file_path]

        # Then try to read from file system if file_path is available
        if rule_doc.file_path:
            try:
                file_path = Path(rule_doc.file_path)
                if file_path.exists():
                    return file_path.read_text(encoding="utf-8")
            except (OSError, IOError) as e:
                # Log error but don't fail initialization
                print(f"Warning: Could not read rule file {rule_doc.file_path}: {e}")

        return None

    def validate_document(self, file_path: Path, content: str) -> ValidationResult:
        """
        Validate a single document against applicable rules.

        Args:
            file_path: Path to the document
            content: Document content

        Returns:
            ValidationResult with all found issues
        """
        import time

        start_time = time.time()

        # Detect document type
        doc_type = DocumentTypeDetector.detect_type(file_path)

        # Get applicable rules
        rules = self.rule_engine.get_rules_for_document(doc_type)

        # Create result
        result = ValidationResult(
            file_path=str(file_path), document_type=doc_type, rule_count=len(rules)
        )

        # Apply each rule
        for rule in rules:
            issues = self._apply_rule(rule, content, file_path)
            result.issues.extend(issues)

        result.validation_time = time.time() - start_time
        return result

    def _apply_rule(
        self, rule: ExtractedRule, content: str, file_path: Path
    ) -> List[ValidationIssue]:
        """Apply a single rule to document content."""
        issues: List[ValidationIssue] = []

        if rule.rule_type == "frontmatter":
            issues.extend(self._validate_frontmatter(rule, content, file_path))
        elif rule.rule_type == "pattern":
            issues.extend(self._validate_pattern(rule, content, file_path))
        elif rule.rule_type == "content":
            issues.extend(self._validate_content(rule, content, file_path))
        elif rule.rule_type == "section":
            issues.extend(self._validate_sections(rule, content, file_path))

        return issues

    def _validate_frontmatter(
        self, rule: ExtractedRule, content: str, file_path: Path
    ) -> List[ValidationIssue]:
        """Validate frontmatter fields."""
        issues: List[ValidationIssue] = []

        # Extract frontmatter
        frontmatter = self._extract_frontmatter(content)

        if not frontmatter and rule.required_fields:
            issues.append(
                ValidationIssue(
                    rule_id=rule.rule_id,
                    severity=rule.severity,
                    category=IssueCategory.MISSING_CONTENT,
                    message="Document is missing required frontmatter",
                    line_number=1,
                    file_path=str(file_path),
                    rule_source=rule.source_file,
                )
            )
            return issues

        # Check required fields
        if rule.required_fields:
            for field in rule.required_fields:
                if field not in frontmatter:
                    issues.append(
                        ValidationIssue(
                            rule_id=rule.rule_id,
                            severity=rule.severity,
                            category=IssueCategory.MISSING_CONTENT,
                            message=f"Missing required frontmatter field: {field}",
                            line_number=1,
                            file_path=str(file_path),
                            suggestion=f"Add '{field}:' to the frontmatter",
                            rule_source=rule.source_file,
                        )
                    )

        return issues

    def _validate_pattern(
        self, rule: ExtractedRule, content: str, file_path: Path
    ) -> List[ValidationIssue]:
        """Validate content against regex pattern."""
        issues: List[ValidationIssue] = []

        if not rule.pattern:
            return issues

        try:
            pattern = re.compile(rule.pattern)

            # Check if pattern should match or not match
            if (
                "must not" in rule.description.lower()
                or "should not" in rule.description.lower()
            ):
                # Pattern should NOT match
                for i, line in enumerate(content.split("\n"), 1):
                    if pattern.search(line):
                        issues.append(
                            ValidationIssue(
                                rule_id=rule.rule_id,
                                severity=rule.severity,
                                category=IssueCategory.INVALID_FORMAT,
                                message=f"Line violates pattern rule: {rule.description}",
                                line_number=i,
                                file_path=str(file_path),
                                rule_source=rule.source_file,
                            )
                        )
            else:
                # Pattern should match
                if not pattern.search(content):
                    issues.append(
                        ValidationIssue(
                            rule_id=rule.rule_id,
                            severity=rule.severity,
                            category=IssueCategory.INVALID_FORMAT,
                            message=f"Document does not match required pattern: {rule.description}",
                            file_path=str(file_path),
                            rule_source=rule.source_file,
                        )
                    )
        except re.error:
            # Invalid regex pattern
            pass

        return issues

    def _validate_content(
        self, rule: ExtractedRule, content: str, file_path: Path
    ) -> List[ValidationIssue]:
        """Validate content-based rules."""
        issues: List[ValidationIssue] = []

        # Simple content checks based on rule description
        if (
            "minimum" in rule.description.lower()
            and "words" in rule.description.lower()
        ):
            # Extract word count requirement
            match = re.search(r"(\d+)\s*words?", rule.description.lower())
            if match:
                min_words = int(match.group(1))
                word_count = len(content.split())
                if word_count < min_words:
                    issues.append(
                        ValidationIssue(
                            rule_id=rule.rule_id,
                            severity=rule.severity,
                            category=IssueCategory.INCOMPLETE_ANALYSIS,
                            message=f"Content too short: {word_count} words (minimum {min_words})",
                            file_path=str(file_path),
                            suggestion=f"Add more detail to meet the {min_words} word minimum",
                            rule_source=rule.source_file,
                        )
                    )

        return issues

    def _validate_sections(
        self, rule: ExtractedRule, content: str, file_path: Path
    ) -> List[ValidationIssue]:
        """Validate required sections."""
        issues: List[ValidationIssue] = []

        if not rule.required_fields:  # required_fields used for section names
            return issues

        # Extract section headers from content
        section_pattern = r"^#+\s+(.+)$"
        found_sections = []
        for match in re.finditer(section_pattern, content, re.MULTILINE):
            found_sections.append(match.group(1).strip())

        # Check for required sections
        for required_section in rule.required_fields:
            if not any(
                required_section.lower() in section.lower()
                for section in found_sections
            ):
                issues.append(
                    ValidationIssue(
                        rule_id=rule.rule_id,
                        severity=rule.severity,
                        category=IssueCategory.MISSING_CONTENT,
                        message=f"Missing required section: {required_section}",
                        file_path=str(file_path),
                        suggestion=f"Add a '## {required_section}' section",
                        rule_source=rule.source_file,
                    )
                )

        return issues

    def _extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """Extract frontmatter from markdown content."""
        if not content.startswith("---"):
            return {}

        try:
            # Find the end of frontmatter
            end_match = re.search(r"\n---\n", content[3:])
            if not end_match:
                return {}

            frontmatter_text = content[3 : end_match.start() + 3]
            return yaml.safe_load(frontmatter_text) or {}
        except YAMLError:
            return {}

    def auto_fix_document(
        self, content: str, issues: List[ValidationIssue]
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Apply auto-fixes to document content.

        Args:
            content: Original document content
            issues: Validation issues to fix

        Returns:
            Tuple of (fixed_content, fix_log)
        """
        # Filter for auto-fixable issues
        fixable_issues = [issue for issue in issues if issue.auto_fixable]

        if not fixable_issues:
            return content, []

        return self.auto_fixer.apply_fixes(content, fixable_issues)

    def add_human_input_comments(
        self, content: str, issues: List[ValidationIssue]
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Add human input comments to document for issues that can't be auto-fixed.

        Args:
            content: Document content
            issues: List of validation issues

        Returns:
            Tuple of (content with comments, insertion log)
        """
        # Filter for non-auto-fixable issues
        human_issues = [issue for issue in issues if not issue.auto_fixable]

        if not human_issues:
            return content, []

        return self.comment_generator.insert_comments_in_content(content, human_issues)

    def validate_and_fix(
        self,
        file_path: Path,
        content: str,
        auto_fix: bool = True,
        add_comments: bool = True,
    ) -> Dict[str, Any]:
        """
        Validate a document and optionally apply fixes and add comments.

        Args:
            file_path: Path to the document
            content: Document content
            auto_fix: Whether to apply auto-fixes
            add_comments: Whether to add human input comments

        Returns:
            Dictionary with validation results, fixed content, and logs
        """
        # First validate
        validation_result = self.validate_document(file_path, content)

        result = {
            "validation_result": validation_result,
            "original_content": content,
            "fixed_content": content,
            "auto_fix_log": [],
            "comment_log": [],
        }

        if not validation_result.issues:
            return result

        # Apply auto-fixes if requested
        if auto_fix:
            fixed_content, fix_log = self.auto_fix_document(
                content, validation_result.issues
            )
            result["fixed_content"] = fixed_content
            result["auto_fix_log"] = fix_log

            # Re-validate after fixes to get remaining issues
            if fix_log:
                revalidation = self.validate_document(file_path, fixed_content)
                remaining_issues = revalidation.issues
            else:
                remaining_issues = validation_result.issues
        else:
            remaining_issues = validation_result.issues

        # Add human input comments if requested
        if add_comments and remaining_issues:
            fixed_content_str = result["fixed_content"]
            assert isinstance(fixed_content_str, str)
            content_with_comments, comment_log = self.add_human_input_comments(
                fixed_content_str, remaining_issues
            )
            result["fixed_content"] = content_with_comments
            result["comment_log"] = comment_log

        return result


class AutoFixer:
    """Handles auto-fixing of validation issues."""

    def __init__(self):
        """Initialize auto-fixer with safe fix operations."""
        self.fixers = {
            # Formatting fixes
            "trailing_whitespace": self._fix_trailing_whitespace,
            "multiple_blank_lines": self._fix_multiple_blank_lines,
            "missing_final_newline": self._fix_missing_final_newline,
            "list_indentation": self._fix_list_indentation,
            "header_spacing": self._fix_header_spacing,
            # Frontmatter fixes
            "missing_frontmatter_field": self._fix_missing_frontmatter_field,
            "frontmatter_field_order": self._fix_frontmatter_field_order,
            "timestamp_format": self._fix_timestamp_format,
            # Structure fixes
            "missing_section": self._fix_missing_section,
            "empty_section": self._fix_empty_section,
        }

    def can_auto_fix(self, issue: ValidationIssue) -> bool:
        """Check if an issue can be auto-fixed."""
        return issue.auto_fixable and self._get_fix_type(issue) in self.fixers

    def apply_fixes(
        self, content: str, issues: List[ValidationIssue]
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Apply auto-fixes to document content.

        Args:
            content: Original document content
            issues: List of validation issues to fix

        Returns:
            Tuple of (fixed_content, fix_log)
        """
        fixed_content = content
        fix_log = []

        # Group issues by type to apply fixes in logical order
        grouped_issues = self._group_issues_by_type(issues)

        # Apply fixes in order: frontmatter, structure, formatting
        for fix_category in ["frontmatter", "structure", "formatting"]:
            for issue in grouped_issues.get(fix_category, []):
                if self.can_auto_fix(issue):
                    try:
                        fixed_content, fix_info = self._apply_single_fix(
                            fixed_content, issue
                        )
                        fix_log.append(
                            {
                                "issue_id": issue.rule_id,
                                "fix_type": self._get_fix_type(issue),
                                "message": issue.message,
                                "success": True,
                                "details": fix_info,
                            }
                        )
                    except Exception as e:
                        fix_log.append(
                            {
                                "issue_id": issue.rule_id,
                                "fix_type": self._get_fix_type(issue),
                                "message": issue.message,
                                "success": False,
                                "error": str(e),
                            }
                        )

        return fixed_content, fix_log

    def _get_fix_type(self, issue: ValidationIssue) -> str:
        """Determine fix type from issue."""
        # Map issue categories and messages to fix types
        message_lower = issue.message.lower()

        if "trailing" in message_lower and "whitespace" in message_lower:
            return "trailing_whitespace"
        elif "blank lines" in message_lower:
            return "multiple_blank_lines"
        elif "final newline" in message_lower:
            return "missing_final_newline"
        elif "list" in message_lower and "indent" in message_lower:
            return "list_indentation"
        elif "header" in message_lower and "spacing" in message_lower:
            return "header_spacing"
        elif "missing required field" in message_lower or (
            issue.category == IssueCategory.MISSING_CONTENT and "field" in message_lower
        ):
            return "missing_frontmatter_field"
        elif "field order" in message_lower:
            return "frontmatter_field_order"
        elif "timestamp" in message_lower or "date" in message_lower:
            return "timestamp_format"
        elif "missing required section" in message_lower or (
            issue.category == IssueCategory.MISSING_CONTENT
            and "section" in message_lower
        ):
            return "missing_section"
        elif "empty section" in message_lower:
            return "empty_section"
        else:
            return "unknown"

    def _group_issues_by_type(
        self, issues: List[ValidationIssue]
    ) -> Dict[str, List[ValidationIssue]]:
        """Group issues by fix category."""
        groups: Dict[str, List[ValidationIssue]] = {
            "frontmatter": [],
            "structure": [],
            "formatting": [],
        }

        for issue in issues:
            fix_type = self._get_fix_type(issue)
            if fix_type in [
                "missing_frontmatter_field",
                "frontmatter_field_order",
                "timestamp_format",
            ]:
                groups["frontmatter"].append(issue)
            elif fix_type in ["missing_section", "empty_section"]:
                groups["structure"].append(issue)
            else:
                groups["formatting"].append(issue)

        return groups

    def _apply_single_fix(
        self, content: str, issue: ValidationIssue
    ) -> Tuple[str, Dict[str, Any]]:
        """Apply a single fix to content."""
        fix_type = self._get_fix_type(issue)
        if fix_type in self.fixers:
            return self.fixers[fix_type](content, issue)
        else:
            raise ValueError(f"No fixer available for type: {fix_type}")

    # Formatting fixes
    def _fix_trailing_whitespace(
        self, content: str, issue: ValidationIssue
    ) -> Tuple[str, Dict[str, Any]]:
        """Remove trailing whitespace from lines."""
        lines = content.split("\n")
        fixed_lines = [line.rstrip() for line in lines]
        fixed_count = sum(1 for i, line in enumerate(lines) if line != fixed_lines[i])

        return "\n".join(fixed_lines), {"lines_fixed": fixed_count}

    def _fix_multiple_blank_lines(
        self, content: str, issue: ValidationIssue
    ) -> Tuple[str, Dict[str, Any]]:
        """Replace multiple consecutive blank lines with single blank line."""
        import re

        fixed = re.sub(r"\n\n\n+", "\n\n", content)
        replacements = len(re.findall(r"\n\n\n+", content))

        return fixed, {"replacements": replacements}

    def _fix_missing_final_newline(
        self, content: str, issue: ValidationIssue
    ) -> Tuple[str, Dict[str, Any]]:
        """Ensure file ends with a newline."""
        if not content.endswith("\n"):
            return content + "\n", {"added_newline": True}
        return content, {"added_newline": False}

    def _fix_list_indentation(
        self, content: str, issue: ValidationIssue
    ) -> Tuple[str, Dict[str, Any]]:
        """Fix inconsistent list indentation."""
        lines = content.split("\n")
        fixed_lines = []
        fixes = 0

        for line in lines:
            # Fix common list indentation issues
            if re.match(r"^(\s*)[*+-]\s", line):
                # Ensure consistent spacing after list marker
                fixed_line = re.sub(r"^(\s*)([*+-])\s+", r"\1\2 ", line)
                if fixed_line != line:
                    fixes += 1
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)

        return "\n".join(fixed_lines), {"lines_fixed": fixes}

    def _fix_header_spacing(
        self, content: str, issue: ValidationIssue
    ) -> Tuple[str, Dict[str, Any]]:
        """Ensure blank lines around headers."""
        lines = content.split("\n")
        fixed_lines = []
        fixes = 0

        for i, line in enumerate(lines):
            # Add current line
            fixed_lines.append(line)

            # Check if this is a header
            if re.match(r"^#+\s", line):
                # Ensure blank line after header (unless next line is also header or EOF)
                if (
                    i < len(lines) - 1
                    and lines[i + 1].strip()
                    and not re.match(r"^#+\s", lines[i + 1])
                ):
                    if i < len(lines) - 1 and lines[i + 1] != "":
                        fixed_lines.append("")
                        fixes += 1

        return "\n".join(fixed_lines), {"headers_fixed": fixes}

    # Frontmatter fixes
    def _fix_missing_frontmatter_field(
        self, content: str, issue: ValidationIssue
    ) -> Tuple[str, Dict[str, Any]]:
        """Add missing required frontmatter field with placeholder."""
        if not content.startswith("---"):
            # No frontmatter at all
            return content, {"error": "No frontmatter section found"}

        # Extract field name from issue
        field_match = re.search(r"field:\s*(\w+)", issue.message)
        if not field_match:
            return content, {"error": "Could not determine field name"}

        field_name = field_match.group(1)

        # Parse frontmatter
        try:
            fm_end = content.index("\n---\n", 3)
            fm_content = content[4:fm_end]
            after_fm = content[fm_end + 5 :]

            # Add field with placeholder
            placeholder = self._get_field_placeholder(field_name)
            new_fm = f"{fm_content}\n{field_name}: {placeholder}"

            return f"---\n{new_fm}\n---\n{after_fm}", {
                "field_added": field_name,
                "placeholder": placeholder,
            }
        except ValueError:
            return content, {"error": "Invalid frontmatter structure"}

    def _get_field_placeholder(self, field_name: str) -> str:
        """Get appropriate placeholder for field."""
        placeholders = {
            "title": '"PLACEHOLDER: Add title"',
            "status": '"PLACEHOLDER: Set status"',
            "owner": '"PLACEHOLDER: Set owner"',
            "last_updated": f'"{datetime.datetime.now().isoformat()}Z"',
            "version": '"1.0"',
            "tags": '["PLACEHOLDER"]',
        }
        return placeholders.get(field_name, '"PLACEHOLDER"')

    def _fix_frontmatter_field_order(
        self, content: str, issue: ValidationIssue
    ) -> Tuple[str, Dict[str, Any]]:
        """Reorder frontmatter fields according to standard order."""
        if not content.startswith("---"):
            return content, {"error": "No frontmatter section found"}

        try:
            # Extract frontmatter
            fm_end = content.index("\n---\n", 3)
            fm_content = content[4:fm_end]
            after_fm = content[fm_end + 5 :]

            # Parse YAML
            fm_dict = yaml.safe_load(fm_content)
            if not isinstance(fm_dict, dict):
                return content, {"error": "Invalid frontmatter"}

            # Standard field order
            field_order = [
                "id",
                "title",
                "version",
                "status",
                "owner",
                "last_updated",
                "parent_charter",
                "related_rules",
                "applies_to",
                "tags",
            ]

            # Reorder fields
            ordered_fm = {}
            for field in field_order:
                if field in fm_dict:
                    ordered_fm[field] = fm_dict[field]

            # Add any remaining fields
            for field, value in fm_dict.items():
                if field not in ordered_fm:
                    ordered_fm[field] = value

            # Convert back to YAML
            new_fm = yaml.dump(ordered_fm, default_flow_style=False, sort_keys=False)

            return f"---\n{new_fm}---\n{after_fm}", {
                "fields_reordered": len(ordered_fm)
            }
        except Exception as e:
            return content, {"error": f"Failed to reorder: {str(e)}"}

    def _fix_timestamp_format(
        self, content: str, issue: ValidationIssue
    ) -> Tuple[str, Dict[str, Any]]:
        """Fix timestamp format to ISO 8601."""
        # This would need the specific field and current value from the issue
        # For now, return unchanged
        return content, {"error": "Timestamp fix not implemented yet"}

    # Structure fixes
    def _fix_missing_section(
        self, content: str, issue: ValidationIssue
    ) -> Tuple[str, Dict[str, Any]]:
        """Add missing required section."""
        # Extract section name from issue
        section_match = re.search(r"section:\s*(.+)", issue.message)
        if not section_match:
            return content, {"error": "Could not determine section name"}

        section_name = section_match.group(1).strip()

        # Add section at end of document
        if not content.endswith("\n"):
            content += "\n"

        content += f"\n## {section_name}\n\n*This section needs to be completed.*\n"

        return content, {"section_added": section_name}

    def _fix_empty_section(
        self, content: str, issue: ValidationIssue
    ) -> Tuple[str, Dict[str, Any]]:
        """Add placeholder content to empty section."""
        # This would need line number from issue to find the section
        # For now, return unchanged
        return content, {"error": "Empty section fix requires line number"}
