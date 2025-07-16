---
title: "Milestone 4: Validation Core"
milestone_id: "M4"
project_id: "rules-service-v0"
status: "completed"
complexity: 8
estimated_duration: "3 days"
dependencies: ["M2"]
owner: "Christian Blank"
created_date: "2025-07-16T10:00:00-07:00"
last_updated: "2025-07-16T10:00:00-07:00"
tags: ["validation", "rules-engine", "linter", "markdown", "automation"]
---

# **Milestone 4: Validation Core (8 points)**

## **Objective**
Implement a document validation engine that can check a given markdown file against the full set of applicable rules extracted from the `.rules.md` files.

## **Strategic Context**
This is the centerpiece of the Rules Service. It operationalizes the documented rules by providing a mechanism to enforce them automatically. This directly reduces manual review time and ensures consistency and quality across the entire repository.

## **Deliverables**
- [x] Template-based rule extraction from markdown bodies
- [x] Document type detection
- [x] Validation issue classification (error, warning, info)
- [x] Auto-fix capability for safe operations (e.g., whitespace)
- [x] Human input comment generation for ambiguous cases

## **Acceptance Criteria**
- [x] Validates documents against all applicable extracted rules.
- [x] Correctly detects document type from filename/path (e.g., `.charter.md`, `.decision.md`).
- [x] Classifies validation issues by severity.
- [x] Auto-fixes safe, non-destructive formatting issues.
- [x] Generates structured human-in-the-loop (HITL) comments for issues requiring manual intervention.

## **Implementation Tasks**

### **Task 4.1: Implement template-based rule extraction**
- [x] Use a markdown parser (e.g., `mistune`) to traverse the AST of `.rules.md` files.
- [x] Extract rule logic from code blocks, tables, and lists.
- [x] Define a schema for how rules are represented in memory.

### **Task 4.2: Build document type detection**
- [x] Create a service to determine a document's type based on its filename suffix (e.g., `.decision.md`).
- [x] Map document types to the rules that apply to them (`applies_to` field in rule frontmatter).

### **Task 4.3: Create validation issue models and classification**
- [x] Define a `ValidationIssue` Pydantic model (line number, message, severity, rule_id).
- [x] Implement severity levels (error, warning, info).
- [x] Create a `ValidationResult` model to hold a list of issues.

### **Task 4.4: Implement auto-fix operations**
- [x] Identify a set of "safe" auto-fixable rules (e.g., trailing whitespace, incorrect list indentation).
- [x] Implement a mechanism to apply these fixes to the document content.
- [x] Ensure auto-fixes are idempotent.

### **Task 4.5: Add human input comment system**
- [x] Implement the comment generation format specified in `validation-system.rules.md`.
- [x] Generate comments for issues that are complex or require human judgment.
- [x] Insert comments directly into the file being validated.

## **Architecture Decisions**

### **Validation Service Interface**
```python
# /os/domains/rules_service/src/validation.py
from typing import List, Dict
from pathlib import Path
from .models import RuleDocument, ValidationResult

class ValidationService:
    """Service for validating documents against rules."""

    def __init__(self, rules: List[RuleDocument]):
        self.rules_by_type = self._organize_rules(rules)

    def validate_document(self, file_path: Path, content: str) -> ValidationResult:
        """Validate a single document."""
        ...

    def _organize_rules(self, rules: List[RuleDocument]) -> Dict[str, List[RuleDocument]]:
        """Organize rules by the document type they apply to."""
        ...
```

### **Rule Representation**
- Rules will be parsed into in-memory Python objects/functions.
- Regular expressions will be used for pattern-based rules.
- The markdown AST will be used for structural rules.

## **Dependencies**
- **Milestone 2**: Rules Discovery (provides the rules to validate against).
- **External**: `mistune` for markdown parsing, `Pydantic` for models.

## **Testing Strategy**
- **Unit Tests**: Test individual rule implementations.
- **Integration Tests**: Test the `ValidationService` with various documents and rule sets.
- **Fixture Tests**: Create a suite of valid and invalid markdown files to test against.

## **Success Metrics**
- Correctly identifies all violations in a test suite of invalid documents.
- Produces zero false positives on a test suite of valid documents.
- Auto-fixes are correct and do not corrupt files.
- Generated HITL comments are correctly formatted.

## **Potential Blockers**
- **Rule Complexity**: Implementing complex structural or semantic rules.
- **Markdown Parsing**: Inconsistencies or limitations in the markdown parser.
- **Performance**: Validating large files or a large number of files.

## **Completion Checklist**
- [x] All implementation tasks completed.
- [x] All acceptance criteria met.
- [x] >90% test coverage for validation logic.
- [ ] Documentation for the validation engine is written.
- [ ] Code committed.

## **Next Steps**
- **Milestone 5**: CLI Interface (the `validate` command will use this service).
