"""Document validation engine for the Rules Service."""

import re
from typing import List, Dict, Optional, Any, Callable, Tuple, Union
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
    UNKNOWN = "unknown"


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
    
    def extract_rules_from_document(self, rule_doc: RuleDocument, content: str) -> List[ExtractedRule]:
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
        table_pattern = r'\|[^\n]+\|[^\n]+\|[^\n]*\|\n\|[-:\s|]+\|\n((?:\|[^\n]+\|\n?)+)'
        
        for table_match in re.finditer(table_pattern, content, re.MULTILINE):
            lines = table_match.group(0).strip().split('\n')
            if len(lines) < 3:
                continue
                
            # Parse headers
            headers = [h.strip() for h in lines[0].split('|') if h.strip()]
            
            # Check if this is a validation table
            header_lower = [h.lower() for h in headers]
            if not any(h in header_lower for h in ['field', 'validation rule', 'pattern', 'requirement', 'rule']):
                continue
            
            # Parse rows (skip header and separator)
            for line in lines[2:]:
                cells = [c.strip() for c in line.split('|') if c.strip()]
                if len(cells) >= 2:
                    self._parse_table_row(headers, cells, rule_doc)
    
    def _parse_table_row(self, headers: List[str], cells: List[str], rule_doc: RuleDocument):
        """Parse a table row into an ExtractedRule."""
        row_data = {}
        for i, cell in enumerate(cells):
            if i < len(headers):
                row_data[headers[i].lower()] = cell
        
        # Extract rule information
        field_name = row_data.get('field', row_data.get('pattern', ''))
        validation_rule = row_data.get('validation rule', row_data.get('rule', row_data.get('requirement', '')))
        
        if field_name and validation_rule:
            rule_id = f"{rule_doc.title}_{field_name}".replace(' ', '_').replace(':', '').lower()
            
            # Determine rule type
            if 'frontmatter' in field_name.lower() or 'field' in headers[0].lower():
                rule_type = 'frontmatter'
            else:
                rule_type = 'pattern'
            
            self.extracted_rules.append(ExtractedRule(
                rule_id=rule_id,
                rule_type=rule_type,
                description=validation_rule,
                pattern=row_data.get('example', row_data.get('pattern', '')),
                severity=self._determine_severity(validation_rule)
            ))
    
    def _extract_from_code_blocks(self, content: str, rule_doc: RuleDocument):
        """Extract validation patterns from code blocks."""
        # Find code blocks with language specifiers
        code_block_pattern = r'```(\w+)\n(.*?)\n```'
        current_section = ""
        
        # Track current section
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('#'):
                current_section = line.strip('#').strip()
        
        for match in re.finditer(code_block_pattern, content, re.DOTALL):
            language = match.group(1).lower()
            code = match.group(2).strip()
            
            if language in ['regex', 'regexp', 'pattern']:
                rule_id = f"{rule_doc.title}_pattern_{len(self.extracted_rules)}".replace(' ', '_').lower()
                self.extracted_rules.append(ExtractedRule(
                    rule_id=rule_id,
                    rule_type='pattern',
                    description=f"Pattern validation: {code[:50]}...",
                    pattern=code,
                    severity='error'
                ))
    
    def _extract_from_yaml_blocks(self, content: str, rule_doc: RuleDocument):
        """Extract frontmatter requirements from YAML code blocks."""
        yaml_block_pattern = r'```yaml\n(.*?)\n```'
        
        for match in re.finditer(yaml_block_pattern, content, re.DOTALL):
            yaml_content = match.group(1).strip()
            
            # Extract field names from YAML
            required_fields = []
            for line in yaml_content.split('\n'):
                if ':' in line and not line.strip().startswith('#'):
                    field = line.split(':')[0].strip()
                    if field and not field.startswith('-'):
                        required_fields.append(field)
            
            if required_fields:
                # Find the section this YAML block is in
                position = match.start()
                lines_before = content[:position].split('\n')
                section = "Document"
                for line in reversed(lines_before):
                    if line.startswith('#'):
                        section = line.strip('#').strip()
                        break
                
                rule_id = f"{rule_doc.title}_{section}_frontmatter".replace(' ', '_').lower()
                self.extracted_rules.append(ExtractedRule(
                    rule_id=rule_id,
                    rule_type='frontmatter',
                    description=f"Required frontmatter fields for {section}",
                    required_fields=required_fields,
                    severity='error'
                ))
    
    def _extract_from_lists(self, content: str, rule_doc: RuleDocument):
        """Extract rules from bullet point lists."""
        # Find sections with rules
        lines = content.split('\n')
        current_section = ""
        
        for i, line in enumerate(lines):
            if line.startswith('#'):
                current_section = line.strip('#').strip()
            elif line.strip().startswith(('- ', '* ', '+ ')):
                # Check if this line contains a rule
                text = line.strip().lstrip('-*+ ').strip()
                
                # Pattern for explicit rules
                rule_match = re.match(r'^Rule\s+(\d+(?:\.\d+)?):?\s*(.+)', text, re.IGNORECASE)
                if rule_match:
                    rule_num = rule_match.group(1)
                    description = rule_match.group(2)
                    rule_id = f"{rule_doc.title}_rule_{rule_num}".replace(' ', '_').lower()
                    
                    self.extracted_rules.append(ExtractedRule(
                        rule_id=rule_id,
                        rule_type='content',
                        description=description,
                        severity=self._determine_severity(description),
                        line_number=i + 1
                    ))
                    continue
                
                # Pattern for must/should/shall rules
                modal_match = re.match(r'^(Must|Should|Shall|May)\s+(.+)', text, re.IGNORECASE)
                if modal_match and ('rule' in current_section.lower() or 'validation' in current_section.lower()):
                    modal = modal_match.group(1).lower()
                    description = text
                    rule_id = f"{rule_doc.title}_{current_section}_{modal}_{len(self.extracted_rules)}".replace(' ', '_').lower()
                    
                    self.extracted_rules.append(ExtractedRule(
                        rule_id=rule_id,
                        rule_type='content',
                        description=description,
                        severity=self._determine_severity(text),
                        line_number=i + 1
                    ))
    
    def _determine_severity(self, text: str) -> str:
        """Determine severity level from rule text."""
        text_lower = text.lower()
        if any(word in text_lower for word in ['must', 'required', 'shall']):
            return 'error'
        elif any(word in text_lower for word in ['should', 'recommended']):
            return 'warning'
        elif any(word in text_lower for word in ['may', 'optional', 'can']):
            return 'info'
        return 'error'  # Default to error


class RuleEngine:
    """Manages and applies extracted rules for validation."""
    
    def __init__(self):
        self.rules_by_type: Dict[str, List[ExtractedRule]] = {
            'frontmatter': [],
            'section': [],
            'pattern': [],
            'content': []
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
        '.decision.md': DocumentType.DECISION,
        '.brief.md': DocumentType.BRIEF,
        '.signal.md': DocumentType.SIGNAL,
        '.vision.md': DocumentType.VISION,
        '.charter.md': DocumentType.CHARTER,
        '.rules.md': DocumentType.RULES,
        '.workflow.md': DocumentType.WORKFLOW,
        '.methodology.md': DocumentType.METHODOLOGY,
        '.registry.md': DocumentType.REGISTRY,
        '-template.md': DocumentType.TEMPLATE,
        '.reference.md': DocumentType.REFERENCE,
    }
    
    # Path patterns for document types
    PATH_PATTERNS = {
        DocumentType.DECISION: ['/decisions/', '/work/domains/decisions/'],
        DocumentType.BRIEF: ['/briefs/', '/work/domains/briefs/'],
        DocumentType.SIGNAL: ['/signals/', '/work/domains/signals/'],
        DocumentType.CHARTER: ['/charters/', '/os/domains/charters/'],
        DocumentType.RULES: ['/rules/', '/os/domains/rules/'],
        DocumentType.WORKFLOW: ['/processes/', '/workflows/'],
        DocumentType.METHODOLOGY: ['/processes/', '/methodologies/'],
        DocumentType.REGISTRY: ['/registries/', '/registry/'],
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
        path_str = str(path).replace('\\', '/')  # Normalize path separators
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
        if filename.endswith('.md'):
            # Additional heuristics based on content or location
            if 'template' in filename:
                return DocumentType.TEMPLATE
            elif 'reference' in filename or 'ref' in filename:
                return DocumentType.REFERENCE
        
        return DocumentType.UNKNOWN
    
    @classmethod
    def get_rules_for_type(cls, document_type: str, rule_engine: RuleEngine) -> List[ExtractedRule]:
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
                'name': 'Decision Record',
                'file_pattern': 'DEC-YYYY-MM-DD-NNN-slug.decision.md',
                'path_hint': '/work/domains/decisions/data/',
                'description': 'Records of architectural and operational decisions'
            },
            DocumentType.BRIEF: {
                'name': 'Opportunity Brief',
                'file_pattern': 'BRIEF-YYYY-MM-DD-NNN-slug.brief.md',
                'path_hint': '/work/domains/briefs/data/',
                'description': 'Synthesized opportunities from signal analysis'
            },
            DocumentType.SIGNAL: {
                'name': 'Signal',
                'file_pattern': 'SIG-YYYY-MM-DD-NNN-description.signal.md',
                'path_hint': '/work/domains/signals/data/',
                'description': 'Captured friction points, opportunities, and insights'
            },
            DocumentType.VISION: {
                'name': 'Project Vision',
                'file_pattern': 'project-name.vision.md',
                'path_hint': '/work/domains/projects/data/',
                'description': 'High-level vision and goals for a project'
            },
            DocumentType.CHARTER: {
                'name': 'Charter',
                'file_pattern': 'service-name.charter.md',
                'path_hint': '/os/domains/charters/data/',
                'description': 'Foundational governance and vision documents'
            },
            DocumentType.RULES: {
                'name': 'Rules Document',
                'file_pattern': 'system-name.rules.md',
                'path_hint': '/os/domains/rules/data/',
                'description': 'Operational rules and constraints'
            },
            DocumentType.WORKFLOW: {
                'name': 'Workflow',
                'file_pattern': 'process-name.workflow.md',
                'path_hint': '/os/domains/processes/data/',
                'description': 'Defined workflows and processes'
            },
            DocumentType.METHODOLOGY: {
                'name': 'Methodology',
                'file_pattern': 'methodology-name.methodology.md',
                'path_hint': '/os/domains/processes/data/',
                'description': 'Development and operational methodologies'
            },
            DocumentType.REGISTRY: {
                'name': 'Registry',
                'file_pattern': 'name.registry.md',
                'path_hint': '/os/domains/registry/data/',
                'description': 'Service and component registries'
            },
            DocumentType.TEMPLATE: {
                'name': 'Template',
                'file_pattern': 'document-type-template.md',
                'path_hint': 'Various locations',
                'description': 'Templates for creating new documents'
            },
            DocumentType.REFERENCE: {
                'name': 'Reference',
                'file_pattern': 'topic.reference.md',
                'path_hint': 'Various locations',
                'description': 'Reference documentation and guides'
            },
            DocumentType.UNKNOWN: {
                'name': 'Unknown',
                'file_pattern': '*.md',
                'path_hint': 'N/A',
                'description': 'Document type could not be determined'
            }
        }
        
        return type_info.get(document_type, type_info[DocumentType.UNKNOWN])