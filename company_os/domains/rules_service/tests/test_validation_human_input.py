"""Tests for human input comment generation functionality."""

from pathlib import Path

from company_os.domains.rules_service.src.validation import (
    ValidationIssue, ValidationService, Severity, IssueCategory,
    HumanInputCommentGenerator, ExtractedRule
)


class TestHumanInputCommentGenerator:
    """Test the HumanInputCommentGenerator functionality."""

    def test_generate_comment_basic(self):
        """Test basic comment generation."""
        generator = HumanInputCommentGenerator()

        issue = ValidationIssue(
            rule_id="missing_field",
            severity=Severity.ERROR,
            category=IssueCategory.MISSING_CONTENT,
            message="Missing required field: owner",
            file_path="/test/doc.md"
        )

        comment = generator.generate_comment(issue)

        assert "HUMAN-INPUT-REQUIRED: MISSING-CONTENT" in comment
        assert "Issue: Missing required field: owner" in comment
        assert "Required Action:" in comment
        assert "Context:" in comment
        assert "Priority: high" in comment

    def test_generate_comment_all_categories(self):
        """Test comment generation for all categories."""
        generator = HumanInputCommentGenerator()

        test_cases = [
            (IssueCategory.MISSING_CONTENT, "MISSING-CONTENT"),
            (IssueCategory.INVALID_REFERENCE, "INVALID-REFERENCE"),
            (IssueCategory.INCOMPLETE_ANALYSIS, "INCOMPLETE-ANALYSIS"),
            (IssueCategory.CLARIFICATION_NEEDED, "CLARIFICATION-NEEDED"),
            (IssueCategory.DECISION_REQUIRED, "DECISION-REQUIRED"),
            (IssueCategory.FORMAT_ERROR, "FORMAT-ERROR"),
            (IssueCategory.REVIEW_NEEDED, "REVIEW-NEEDED"),
        ]

        for category, expected_label in test_cases:
            issue = ValidationIssue(
                rule_id="test",
                severity=Severity.ERROR,
                category=category,
                message="Test message",
                file_path="/test/doc.md"
            )

            comment = generator.generate_comment(issue)
            assert f"HUMAN-INPUT-REQUIRED: {expected_label}" in comment

    def test_priority_determination(self):
        """Test priority determination based on severity."""
        generator = HumanInputCommentGenerator()

        # Error should be high priority
        error_issue = ValidationIssue(
            rule_id="test",
            severity=Severity.ERROR,
            category=IssueCategory.MISSING_CONTENT,
            message="Error issue",
            file_path="/test/doc.md"
        )
        comment = generator.generate_comment(error_issue)
        assert "Priority: high" in comment

        # Warning should be medium priority
        warning_issue = ValidationIssue(
            rule_id="test",
            severity=Severity.WARNING,
            category=IssueCategory.REVIEW_NEEDED,
            message="Warning issue",
            file_path="/test/doc.md"
        )
        comment = generator.generate_comment(warning_issue)
        assert "Priority: medium" in comment

        # Info should be low priority
        info_issue = ValidationIssue(
            rule_id="test",
            severity=Severity.INFO,
            category=IssueCategory.CLARIFICATION_NEEDED,
            message="Info issue",
            file_path="/test/doc.md"
        )
        comment = generator.generate_comment(info_issue)
        assert "Priority: low" in comment

    def test_required_action_generation(self):
        """Test required action generation for different categories."""
        generator = HumanInputCommentGenerator()

        # Missing content
        issue = ValidationIssue(
            rule_id="test",
            severity=Severity.ERROR,
            category=IssueCategory.MISSING_CONTENT,
            message="Missing required field: owner",
            file_path="/test/doc.md"
        )
        comment = generator.generate_comment(issue)
        assert "Required Action: Add the required content" in comment

        # Invalid reference
        issue = ValidationIssue(
            rule_id="test",
            severity=Severity.ERROR,
            category=IssueCategory.INVALID_REFERENCE,
            message="Referenced file not found: /test/missing.md",
            file_path="/test/doc.md"
        )
        comment = generator.generate_comment(issue)
        assert "Required Action: Update reference to valid target" in comment

    def test_context_generation(self):
        """Test context generation with line numbers and suggestions."""
        generator = HumanInputCommentGenerator()

        # With line number
        issue = ValidationIssue(
            rule_id="test",
            severity=Severity.ERROR,
            category=IssueCategory.FORMAT_ERROR,
            message="Invalid format",
            file_path="/test/doc.md",
            line_number=42
        )
        comment = generator.generate_comment(issue)
        assert "Line 42" in comment

        # With suggestion
        issue = ValidationIssue(
            rule_id="test",
            severity=Severity.WARNING,
            category=IssueCategory.CLARIFICATION_NEEDED,
            message="Unclear content",
            file_path="/test/doc.md",
            suggestion="Consider adding more detail"
        )
        comment = generator.generate_comment(issue)
        assert "Consider adding more detail" in comment

        # With rule source
        issue = ValidationIssue(
            rule_id="test",
            severity=Severity.ERROR,
            category=IssueCategory.DECISION_REQUIRED,
            message="Multiple options available",
            file_path="/test/doc.md",
            rule_source="/os/rules/test.rules.md"
        )
        comment = generator.generate_comment(issue)
        assert "Rule source: /os/rules/test.rules.md" in comment

    def test_batch_comment_generation(self):
        """Test generating comments for multiple issues."""
        generator = HumanInputCommentGenerator()

        issues = [
            ValidationIssue(
                rule_id="field1",
                severity=Severity.ERROR,
                category=IssueCategory.MISSING_CONTENT,
                message="Missing field 1",
                file_path="/test/doc.md"
            ),
            ValidationIssue(
                rule_id="field2",
                severity=Severity.WARNING,
                category=IssueCategory.REVIEW_NEEDED,
                message="Needs review",
                file_path="/test/doc.md"
            ),
            ValidationIssue(
                rule_id="field3",
                severity=Severity.INFO,
                category=IssueCategory.CLARIFICATION_NEEDED,
                message="Could be clearer",
                file_path="/test/doc.md"
            ),
        ]

        comments = generator.generate_comments(issues)

        assert len(comments) == 3
        assert all("HUMAN-INPUT-REQUIRED:" in c['comment'] for c in comments)
        assert comments[0]['priority'] == 'high'
        assert comments[1]['priority'] == 'medium'
        assert comments[2]['priority'] == 'low'


class TestValidationServiceHumanInput:
    """Test ValidationService human input functionality."""

    def test_add_human_input_comments(self):
        """Test adding human input comments to a document."""
        service = ValidationService([])

        content = """---
title: Test Document
---

# Test Document

Some content here.

## Section Two

More content."""

        issues = [
            ValidationIssue(
                rule_id="missing_field",
                severity=Severity.ERROR,
                category=IssueCategory.MISSING_CONTENT,
                message="Missing required field: owner",
                file_path="/test/doc.md",
                line_number=2  # After title in frontmatter
            ),
            ValidationIssue(
                rule_id="empty_section",
                severity=Severity.WARNING,
                category=IssueCategory.INCOMPLETE_ANALYSIS,
                message="Section needs more detail",
                file_path="/test/doc.md",
                line_number=11  # After "More content."
            ),
        ]

        result_content, result_log = service.add_human_input_comments(content, issues)

        # Check that comments were added
        assert "HUMAN-INPUT-REQUIRED: MISSING-CONTENT" in result_content
        assert "HUMAN-INPUT-REQUIRED: INCOMPLETE-ANALYSIS" in result_content
        assert "Issue: Missing required field: owner" in result_content
        assert "Issue: Section needs more detail" in result_content

    def test_validate_and_fix_with_comments(self):
        """Test complete validation and fix process with comment generation."""
        service = ValidationService([])

        content = """---
title: Test Document
status: active
---

# Test Document

TODO: Add content here

## Empty Section

"""

        # Create a test rule that would trigger issues
        rule = ExtractedRule(
            rule_id="test_rule",
            rule_type="pattern",
            description="Must not contain TODO",
            pattern=r"TODO",
            severity="error",
            applies_to=[]
        )

        # Add the rule to the service
        service.rule_engine.add_rules([rule])

        # Run validation with fix and comments
        result = service.validate_and_fix(
            Path("/test/doc.md"),
            content,
            auto_fix=True,
            add_comments=True
        )

        # Should have found the TODO issue
        assert len(result['validation_result'].issues) > 0
        assert any("TODO" in issue.message for issue in result['validation_result'].issues)

        # Since TODO can't be auto-fixed, should add comment
        assert "HUMAN-INPUT-REQUIRED:" in result['fixed_content']

    def test_no_comments_for_auto_fixable(self):
        """Test that auto-fixable issues don't get comments."""
        service = ValidationService([])

        content = "Line with trailing spaces   \nAnother line"

        issues = [
            ValidationIssue(
                rule_id="trailing_ws",
                severity=Severity.WARNING,
                category=IssueCategory.FORMAT_ERROR,
                message="Remove trailing whitespace",
                auto_fixable=True
            )
        ]

        # Should not add comments for auto-fixable issues
        result_content, result_log = service.add_human_input_comments(content, issues)
        assert "HUMAN-INPUT-REQUIRED:" not in result_content
        assert result_content == content  # No changes

    def test_comment_insertion_positions(self):
        """Test correct positioning of comments."""
        service = ValidationService([])

        content = """---
title: Test
---

# Header

Content."""

        # Test frontmatter comment insertion
        fm_issue = ValidationIssue(
            rule_id="fm",
            severity=Severity.ERROR,
            category=IssueCategory.MISSING_CONTENT,
            message="Missing owner",
            file_path="/test/doc.md",
            line_number=2  # In frontmatter
        )

        result_content, result_log = service.add_human_input_comments(content, [fm_issue])
        lines = result_content.split('\n')

        # Comment should be in frontmatter section
        fm_end = next(i for i, line in enumerate(lines) if line == '---' and i > 0)
        comment_lines = [i for i, line in enumerate(lines) if 'HUMAN-INPUT-REQUIRED' in line]
        assert any(i < fm_end for i in comment_lines)

    def test_multiple_comments_same_location(self):
        """Test handling multiple issues at the same location."""
        service = ValidationService([])

        content = """# Document

## Section

Content here."""

        issues = [
            ValidationIssue(
                rule_id="issue1",
                severity=Severity.ERROR,
                category=IssueCategory.MISSING_CONTENT,
                message="Missing required info A",
                file_path="/test/doc.md",
                line_number=5  # After "Content here."
            ),
            ValidationIssue(
                rule_id="issue2",
                severity=Severity.ERROR,
                category=IssueCategory.REVIEW_NEEDED,
                message="Needs review for accuracy",
                file_path="/test/doc.md",
                line_number=5  # Same line
            ),
        ]

        result_content, result_log = service.add_human_input_comments(content, issues)

        # Both comments should be added
        assert result_content.count("HUMAN-INPUT-REQUIRED:") == 2
        assert "Missing required info A" in result_content
        assert "Needs review for accuracy" in result_content
