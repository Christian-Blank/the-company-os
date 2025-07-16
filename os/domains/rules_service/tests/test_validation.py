"""Unit tests for the validation module."""

import tempfile
from pathlib import Path
import pytest

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.validation import RuleExtractor, ExtractedRule, RuleEngine
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