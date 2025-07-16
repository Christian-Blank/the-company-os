---
title: "Milestone 2: Rules Discovery"
milestone_id: "M2"
project_id: "rules-service-v0"
status: "not_started"
complexity: 5
estimated_duration: "2 days"
dependencies: ["M1"]
owner: "Christian Blank"
created_date: "2025-07-16T00:06:00-07:00"
last_updated: "2025-07-16T00:06:00-07:00"
tags: ["discovery", "parsing", "rules", "frontmatter", "file-system"]
---

# **Milestone 2: Rules Discovery (5 points)**

## **Objective**
Implement rule file discovery and parsing system that can find, parse, and categorize all `.rules.md` files in the repository.

## **Strategic Context**
This milestone creates the core intelligence of the Rules Service - the ability to discover and understand the rule files that exist in the repository. This is foundational for both synchronization and validation capabilities.

## **Deliverables**
- [ ] Rule file discovery service
- [ ] Frontmatter parsing with schema validation
- [ ] Rule categorization by document type
- [ ] Tag-based rule querying

## **Acceptance Criteria**
- [ ] Discovers all `.rules.md` files in repository
- [ ] Parses frontmatter into typed models
- [ ] Supports tag-based filtering
- [ ] Handles malformed files gracefully

## **Implementation Tasks**

### **Task 2.1: Implement file globbing and discovery**
- [ ] Create `RuleDiscoveryService` class
- [ ] Implement recursive file system scanning
- [ ] Add pattern matching for `.rules.md` files
- [ ] Handle symlinks and hidden directories appropriately
- [ ] Add caching for performance optimization

### **Task 2.2: Create rule-specific Pydantic models**
- [ ] Define `RuleDocument` model extending `BaseDocument`
- [ ] Add rule-specific fields (rule_set_version, enforcement_level, etc.)
- [ ] Create validation rules for rule document frontmatter
- [ ] Add serialization/deserialization support

### **Task 2.3: Build frontmatter parser**
- [ ] Create `FrontmatterParser` class
- [ ] Implement YAML frontmatter extraction
- [ ] Add schema validation against rule document model
- [ ] Handle parsing errors gracefully with detailed error messages
- [ ] Support for both `---` and `+++` frontmatter delimiters

### **Task 2.4: Add tag query functionality**
- [ ] Implement tag-based filtering system
- [ ] Support for multiple tag queries (AND/OR logic)
- [ ] Add sorting and pagination capabilities
- [ ] Create query result models

## **Architecture Decisions**

### **Discovery Service Interface**
```python
# /os/domains/rules_service/src/discovery.py
from typing import List, Optional, Dict
from pathlib import Path
from .models import RuleDocument

class RuleDiscoveryService:
    """Service for discovering and parsing rule files"""
    
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self._cache: Dict[str, RuleDocument] = {}
    
    def discover_rules(self, refresh_cache: bool = False) -> List[RuleDocument]:
        """Discover all rule files in the repository"""
        ...
    
    def query_by_tags(self, tags: List[str], match_all: bool = True) -> List[RuleDocument]:
        """Query rules by tags"""
        ...
    
    def get_rule_by_path(self, path: Path) -> Optional[RuleDocument]:
        """Get a specific rule by file path"""
        ...
```

### **Rule Document Model**
```python
# /os/domains/rules_service/src/models.py
from pydantic import Field
from typing import Optional, List
from enum import Enum
import sys
sys.path.append('/shared/libraries')
from company_os_core.models import BaseDocument

class EnforcementLevel(str, Enum):
    STRICT = "strict"
    ADVISORY = "advisory"
    DEPRECATED = "deprecated"

class RuleDocument(BaseDocument):
    """Model for .rules.md documents"""
    rule_set_version: str
    enforcement_level: EnforcementLevel = EnforcementLevel.STRICT
    applies_to: List[str] = Field(default_factory=list)
    parent_charter: str  # Required for rules
    
    @property
    def rule_category(self) -> str:
        """Extract rule category from filename"""
        # Implementation to determine category
        ...
```

## **Dependencies**
- **Milestone 1**: Foundation (Base models, Bazel setup)
- **External**: ruamel.yaml for YAML parsing, pathlib for file operations

## **Testing Strategy**
- **Unit Tests**: Individual component testing (parser, discovery, models)
- **Integration Tests**: End-to-end discovery and parsing
- **Fixture Tests**: Test with sample rule files covering edge cases

## **Performance Considerations**
- **Caching**: In-memory cache for parsed rules
- **Lazy Loading**: Parse rules only when needed
- **Incremental Updates**: Only re-parse changed files

## **Error Handling**
- **Malformed YAML**: Graceful degradation with error reporting
- **Missing Files**: Handle deleted files in cache
- **Permission Issues**: Clear error messages for access problems

## **Success Metrics**
- Discovers all existing rule files (currently ~9 files)
- Parses frontmatter with 100% accuracy
- Tag queries return correct results
- Handles edge cases without crashing

## **Potential Blockers**
- **YAML Parsing**: Complex frontmatter structures
- **File System**: Permission or access issues
- **Performance**: Large repository scanning performance

## **Completion Checklist**
- [ ] All implementation tasks completed
- [ ] All acceptance criteria met
- [ ] Unit tests passing (>90% coverage)
- [ ] Integration tests passing
- [ ] Performance benchmarks met
- [ ] Error handling tested
- [ ] Documentation updated
- [ ] Code committed with logical commits

## **Next Steps**
Upon completion, this milestone enables:
- **Milestone 3**: Sync Engine (can begin immediately)
- **Milestone 4**: Validation Core (can begin immediately)
- **Milestone 5**: CLI Interface (partial - rules query commands)

---

**Status**: Not started (requires M1 completion)
**Estimated Completion**: 2 days after M1
**Actual Completion**: TBD
