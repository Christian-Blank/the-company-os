"""Unit tests for the validation module."""

import tempfile
from pathlib import Path
import pytest

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.validation import RuleExtractor, ExtractedRule, RuleEngine, DocumentTypeDetector, DocumentType
from src.models import RuleDocument


class TestRuleExtractor:
    """Test the RuleExtractor functionality."""
    
    @pytest.fixture
    def sample_rule_doc(self):
        """Create a sample rule document."""
        return RuleDocument(
            title="Test Rules",
            version="1.0",
            status="active",
            owner="test",
            last_updated="2025-01-01T00:00:00Z",
            parent_charter="test.charter.md",
            applies_to=["decision", "brief"],
            file_path="/test/rules.md",
            tags=["test"]
        )
    
    def test_extract_from_tables(self, sample_rule_doc):
        """Test extracting rules from markdown tables."""
        content = """
# Test Rules

## Frontmatter Validation

| Field | Validation Rule | Example |
|-------|----------------|---------|
| title | Required, must start with "Decision:" | Decision: Choose Framework |
| status | Must be one of: Proposed, Accepted | Accepted |
| owner | Required field | John Doe |
"""
        extractor = RuleExtractor()
        rules = extractor.extract_rules_from_document(sample_rule_doc, content)
        
        assert len(rules) == 3
        assert any(r.rule_id.endswith('_title') for r in rules)
        assert any(r.description.startswith('Required, must start with') for r in rules)
        assert all(r.rule_type == 'frontmatter' for r in rules)
    
    def test_extract_from_code_blocks(self, sample_rule_doc):
        """Test extracting rules from code blocks."""
        content = '''
# Test Rules

## Required Frontmatter

```yaml
id: "DEC-YYYY-MM-DD-NNN"
title: string
status: enum
owner: string
```

## ID Pattern

```regex
^DEC-\\d{4}-\\d{2}-\\d{2}-\\d{3}$
```
'''
        extractor = RuleExtractor()
        rules = extractor.extract_rules_from_document(sample_rule_doc, content)
        
        # Should extract frontmatter fields and regex pattern
        assert any(r.rule_type == 'frontmatter' for r in rules)
        assert any(r.rule_type == 'pattern' for r in rules)
        
        # Check frontmatter rule
        fm_rule = next((r for r in rules if r.rule_type == 'frontmatter'), None)
        assert fm_rule is not None
        assert 'id' in fm_rule.required_fields
        assert 'title' in fm_rule.required_fields
    
    def test_extract_from_lists(self, sample_rule_doc):
        """Test extracting rules from bullet lists."""
        content = """
# Test Rules

## Validation Rules

- Rule 1.1: Documents must have a valid frontmatter
- Rule 1.2: Title field is required
- Must include at least one tag
- Should have a meaningful description
"""
        extractor = RuleExtractor()
        rules = extractor.extract_rules_from_document(sample_rule_doc, content)
        
        assert len(rules) >= 3
        assert any('rule_1.1' in r.rule_id for r in rules)
        assert any(r.severity == 'error' for r in rules)  # "Must" = error
        assert any(r.severity == 'warning' for r in rules)  # "Should" = warning
    
    def test_severity_detection(self, sample_rule_doc):
        """Test severity level detection from rule text."""
        content = """
# Test Rules

## Rules

- Must have a title (error)
- Should include description (warning)  
- May add optional tags (info)
"""
        extractor = RuleExtractor()
        rules = extractor.extract_rules_from_document(sample_rule_doc, content)
        
        must_rule = next((r for r in rules if 'Must have' in r.description), None)
        should_rule = next((r for r in rules if 'Should include' in r.description), None)
        may_rule = next((r for r in rules if 'May add' in r.description), None)
        
        assert must_rule and must_rule.severity == 'error'
        assert should_rule and should_rule.severity == 'warning'
        assert may_rule and may_rule.severity == 'info'
    
    def test_applies_to_inheritance(self, sample_rule_doc):
        """Test that rules inherit applies_to from parent document."""
        content = """
# Test Rules

- Rule 1: All documents must have frontmatter
"""
        extractor = RuleExtractor()
        rules = extractor.extract_rules_from_document(sample_rule_doc, content)
        
        assert len(rules) > 0
        assert all(r.applies_to == ["decision", "brief"] for r in rules)
        assert all(r.source_file == "/test/rules.md" for r in rules)


class TestRuleEngine:
    """Test the RuleEngine functionality."""
    
    def test_add_and_organize_rules(self):
        """Test adding rules and organizing by type."""
        engine = RuleEngine()
        
        rules = [
            ExtractedRule(
                rule_id="test_fm_1",
                rule_type="frontmatter",
                description="Test frontmatter rule",
                applies_to=["decision"]
            ),
            ExtractedRule(
                rule_id="test_pattern_1",
                rule_type="pattern",
                description="Test pattern rule",
                applies_to=["brief"]
            ),
            ExtractedRule(
                rule_id="test_universal",
                rule_type="content",
                description="Universal rule",
                applies_to=[]  # Universal
            )
        ]
        
        engine.add_rules(rules)
        
        assert len(engine.rules_by_type['frontmatter']) == 1
        assert len(engine.rules_by_type['pattern']) == 1
        assert len(engine.rules_by_type['content']) == 1
        assert len(engine.rules_by_document_type['decision']) == 1
        assert len(engine.rules_by_document_type['brief']) == 1
    
    def test_get_rules_for_document(self):
        """Test retrieving rules for a specific document type."""
        engine = RuleEngine()
        
        rules = [
            ExtractedRule(
                rule_id="decision_rule",
                rule_type="frontmatter",
                description="Decision-specific rule",
                applies_to=["decision"]
            ),
            ExtractedRule(
                rule_id="universal_rule",
                rule_type="content",
                description="Universal rule",
                applies_to=[]  # Applies to all
            ),
            ExtractedRule(
                rule_id="brief_rule",
                rule_type="pattern",
                description="Brief-specific rule",
                applies_to=["brief"]
            )
        ]
        
        engine.add_rules(rules)
        
        # Get rules for decision documents
        decision_rules = engine.get_rules_for_document("decision")
        assert len(decision_rules) == 2
        assert any(r.rule_id == "decision_rule" for r in decision_rules)
        assert any(r.rule_id == "universal_rule" for r in decision_rules)
        
        # Get rules for brief documents
        brief_rules = engine.get_rules_for_document("brief")
        assert len(brief_rules) == 2
        assert any(r.rule_id == "brief_rule" for r in brief_rules)
        assert any(r.rule_id == "universal_rule" for r in brief_rules)
        
        # Get rules for unknown document type (should get universal rules)
        unknown_rules = engine.get_rules_for_document("unknown")
        assert len(unknown_rules) == 1
        assert unknown_rules[0].rule_id == "universal_rule"


class TestDocumentTypeDetector:
    """Test the DocumentTypeDetector functionality."""
    
    def test_detect_type_by_suffix(self):
        """Test document type detection by file suffix."""
        test_cases = [
            ("DEC-2025-01-01-001-test.decision.md", DocumentType.DECISION),
            ("BRIEF-2025-01-01-001-opportunity.brief.md", DocumentType.BRIEF),
            ("SIG-2025-01-01-001-friction.signal.md", DocumentType.SIGNAL),
            ("project.vision.md", DocumentType.VISION),
            ("service.charter.md", DocumentType.CHARTER),
            ("validation.rules.md", DocumentType.RULES),
            ("build.workflow.md", DocumentType.WORKFLOW),
            ("synapse.methodology.md", DocumentType.METHODOLOGY),
            ("services.registry.md", DocumentType.REGISTRY),
            ("decision-template.md", DocumentType.TEMPLATE),
            ("patterns.reference.md", DocumentType.REFERENCE),
            ("readme.md", DocumentType.UNKNOWN),
        ]
        
        for filename, expected_type in test_cases:
            detected = DocumentTypeDetector.detect_type(filename)
            assert detected == expected_type, f"Failed for {filename}: expected {expected_type}, got {detected}"
    
    def test_detect_type_by_path(self):
        """Test document type detection by path patterns."""
        test_cases = [
            ("/work/domains/decisions/data/test.md", DocumentType.DECISION),
            ("/work/domains/briefs/data/opportunity.md", DocumentType.BRIEF),
            ("/work/domains/signals/data/friction.md", DocumentType.SIGNAL),
            ("/os/domains/charters/data/service.md", DocumentType.CHARTER),
            ("/os/domains/rules/data/validation.md", DocumentType.RULES),
            ("/os/domains/processes/data/workflow.md", DocumentType.WORKFLOW),
            ("/some/random/path/file.md", DocumentType.UNKNOWN),
        ]
        
        for path, expected_type in test_cases:
            detected = DocumentTypeDetector.detect_type(path)
            assert detected == expected_type, f"Failed for {path}: expected {expected_type}, got {detected}"
    
    def test_suffix_takes_precedence(self):
        """Test that suffix detection takes precedence over path."""
        # Even though it's in decisions folder, the suffix should win
        path = "/work/domains/decisions/data/test.brief.md"
        detected = DocumentTypeDetector.detect_type(path)
        assert detected == DocumentType.BRIEF
    
    def test_template_detection_by_name(self):
        """Test template detection by filename pattern."""
        test_cases = [
            ("brief-template.md", DocumentType.TEMPLATE),
            ("template-for-signals.md", DocumentType.TEMPLATE),
            ("decision_template.md", DocumentType.TEMPLATE),
        ]
        
        for filename, expected_type in test_cases:
            detected = DocumentTypeDetector.detect_type(filename)
            assert detected == expected_type
    
    def test_reference_detection_by_name(self):
        """Test reference document detection."""
        test_cases = [
            ("api-reference.md", DocumentType.REFERENCE),
            ("ref-guide.md", DocumentType.REFERENCE),
            ("validation-patterns.reference.md", DocumentType.REFERENCE),
        ]
        
        for filename, expected_type in test_cases:
            detected = DocumentTypeDetector.detect_type(filename)
            assert detected == expected_type
    
    def test_windows_path_compatibility(self):
        """Test that Windows paths work correctly."""
        windows_path = r"C:\work\domains\decisions\data\test.decision.md"
        detected = DocumentTypeDetector.detect_type(windows_path)
        assert detected == DocumentType.DECISION
    
    def test_get_type_info(self):
        """Test getting information about document types."""
        info = DocumentTypeDetector.get_type_info(DocumentType.DECISION)
        
        assert info['name'] == 'Decision Record'
        assert 'DEC-YYYY-MM-DD' in info['file_pattern']
        assert 'decisions' in info['path_hint']
        assert 'architectural' in info['description']
        
        # Test unknown type
        unknown_info = DocumentTypeDetector.get_type_info("invalid_type")
        assert unknown_info['name'] == 'Unknown'
    
    def test_get_rules_for_type(self):
        """Test getting rules for a specific document type."""
        # Create a mock rule engine
        engine = RuleEngine()
        
        # Add some test rules
        decision_rule = ExtractedRule(
            rule_id="test_decision_rule",
            rule_type="frontmatter",
            description="Decision-specific rule",
            applies_to=["decision"]
        )
        
        engine.add_rules([decision_rule])
        
        # Get rules for decision type
        rules = DocumentTypeDetector.get_rules_for_type(DocumentType.DECISION, engine)
        assert len(rules) == 1
        assert rules[0].rule_id == "test_decision_rule"