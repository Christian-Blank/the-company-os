---
title: "Milestone 2: Rules Discovery"
milestone_id: "M2"
project_id: "rules-service-v0"
status: "complete_with_cleanup_tasks"
complexity: 5
estimated_duration: "2 days"
dependencies: ["M1"]
owner: "Christian Blank"
created_date: "2025-07-16T00:06:00-07:00"
last_updated: "2025-07-16T01:54:00-07:00"
tags: ["discovery", "parsing", "rules", "frontmatter", "file-system"]
verification_report: "milestone-2-verification-report.md"
---

# **Milestone 2: Rules Discovery (5 points)**

## **Objective**
Implement rule file discovery and parsing system that can find, parse, and categorize all `.rules.md` files in the repository.

## **Strategic Context**
This milestone creates the core intelligence of the Rules Service - the ability to discover and understand the rule files that exist in the repository. This is foundational for both synchronization and validation capabilities.

## **Deliverables**
- [x] Rule file discovery service
- [x] Frontmatter parsing with schema validation
- [x] Rule categorization by document type
- [x] Tag-based rule querying

## **Acceptance Criteria**
- [x] Discovers all `.rules.md` files in repository
- [x] Parses frontmatter into typed models
- [x] Supports tag-based filtering
- [x] Handles malformed files gracefully

## **Implementation Tasks**

### **Task 2.1: Implement file globbing and discovery**
- [x] Create `RuleDiscoveryService` class
- [x] Implement recursive file system scanning
- [x] Add pattern matching for `.rules.md` files
- [x] Handle symlinks and hidden directories appropriately
- [x] Add caching for performance optimization

### **Task 2.2: Create rule-specific Pydantic models**
- [x] Define `RuleDocument` model extending `BaseDocument`
- [x] Add rule-specific fields (rule_set_version, enforcement_level, etc.)
- [x] Create validation rules for rule document frontmatter
- [x] Add serialization/deserialization support

### **Task 2.3: Build frontmatter parser**
- [x] Create `FrontmatterParser` class
- [x] Implement YAML frontmatter extraction
- [x] Add schema validation against rule document model
- [x] Handle parsing errors gracefully with detailed error messages
- [x] Support for both `---` and `+++` frontmatter delimiters

### **Task 2.4: Add tag query functionality**
- [x] Implement tag-based filtering system
- [x] Support for multiple tag queries (AND/OR logic)
- [x] Add sorting and pagination capabilities
- [x] Create query result models

### **Task 2.5: Cleanup and Enhancement Tasks (Remaining)**
- [x] Fix import error in discovery.py line 28 (`yaml.YAMLError` → `YAMLError`)
- [x] Remove unused `import glob` from discovery.py
- [x] Fix hardcoded paths - make sys.path.append use relative paths
- [x] Verify and fix `+++` delimiter support
- [x] Add error collection mechanism - return errors with results
- [x] Create edge case tests (malformed YAML, permissions, empty repo)
- [ ] Add performance benchmarks for discovery operations
- [x] Complete method documentation with docstrings
- [ ] Create integration test for end-to-end discovery
- [ ] Add configuration support for paths

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
- [x] All implementation tasks completed (90% - cleanup tasks remaining)
- [x] All acceptance criteria met
- [x] Unit tests passing (core functionality tested)
- [ ] Integration tests passing (needs end-to-end test)
- [ ] Performance benchmarks met (not measured yet)
- [x] Error handling tested (basic error cases)
- [ ] Documentation updated (needs docstring completion)
- [x] Code committed with logical commits

## **Verification Report**
See [milestone-2-verification-report.md](milestone-2-verification-report.md) for detailed verification analysis.

## **Next Steps**
This milestone is sufficiently complete to enable:
- **Milestone 3**: Sync Engine (ready to begin)
- **Milestone 4**: Validation Core (ready to begin)
- **Milestone 5**: CLI Interface (rules query commands can be implemented)

The 10 remaining cleanup tasks can be completed in parallel with Milestone 3 development.

---

**Status**: Complete with cleanup tasks (90%)
**Estimated Completion**: 2 days
**Actual Completion**: 2025-07-16 (core implementation)
**Verification Date**: 2025-07-16T01:51:00-07:00
