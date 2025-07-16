---
title: "Milestone 1: Project Foundation"
milestone_id: "M1"
project_id: "rules-service-v0"
status: "not_started"
complexity: 3
estimated_duration: "1 day"
dependencies: []
owner: "Christian Blank"
created_date: "2025-07-16T00:06:00-07:00"
last_updated: "2025-07-16T00:06:00-07:00"
tags: ["foundation", "setup", "bazel", "pydantic", "architecture"]
---

# **Milestone 1: Project Foundation (3 points)**

## **Objective**
Establish project structure and core data models following hexagonal architecture pattern.

## **Strategic Context**
This milestone creates the foundational infrastructure for the entire Rules Service implementation. It establishes the hexagonal architecture pattern that will support clean separation of concerns and enable easy testing and future evolution.

## **Deliverables**
- [ ] Bazel BUILD files for all packages
- [ ] Base Pydantic models in `company_os_core`
- [ ] Project structure following hexagonal architecture
- [ ] Initial test framework setup

## **Acceptance Criteria**
- [ ] `bazel build //...` succeeds
- [ ] All packages import correctly
- [ ] Basic models validate with Pydantic v2
- [ ] Test framework runs (even if no tests yet)

## **Implementation Tasks**

### **Task 1.1: Create Bazel workspace configuration**
- [ ] Create `WORKSPACE` file with Python rules
- [ ] Set up `BUILD.bazel` files for each package
- [ ] Configure dependencies (Pydantic v2, Typer, mistune, ruamel.yaml)
- [ ] Test basic build with `bazel build //...`

### **Task 1.2: Define base document models**
- [ ] Create `src/company_os_core/models.py` with base document models
- [ ] Define `BaseDocument` Pydantic model with common fields
- [ ] Create ID type definitions and validation
- [ ] Add timestamp handling utilities

### **Task 1.3: Set up package structure**
- [ ] Create directory structure according to hexagonal architecture
- [ ] Set up `__init__.py` files for all packages
- [ ] Configure Python path and imports
- [ ] Verify package imports work correctly

### **Task 1.4: Configure test framework**
- [ ] Set up pytest configuration
- [ ] Create test directory structure
- [ ] Configure Bazel test rules
- [ ] Create sample test to verify framework works

## **Architecture Decisions**

### **Hexagonal Architecture Layout**
```
src/
├── company_os_core/          # Domain-agnostic shared library
│   ├── __init__.py
│   ├── models.py            # Base Pydantic models
│   ├── documents.py         # Document parsing utilities
│   └── validation/
│       ├── __init__.py
│       └── base.py          # Validation protocols
├── company_os/
│   └── services/
│       └── rules_service/   # Domain service
│           ├── __init__.py
│           ├── models.py    # Rule-specific models
│           ├── discovery.py # Rule discovery logic
│           ├── sync.py      # Synchronization logic
│           └── validation.py # Validation logic
└── adapters/                # Framework adapters
    ├── cli/
    │   ├── __init__.py
    │   └── commands/
    │       ├── __init__.py
    │       ├── rules.py     # Rules CLI commands
    │       └── validate.py  # Validation CLI commands
    └── pre_commit/
        ├── __init__.py
        └── hooks.py         # Pre-commit integration
```

### **Base Models Structure**
```python
# company_os_core/models.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class BaseDocument(BaseModel):
    """Base model for all markdown documents"""
    title: str
    version: str = "1.0"
    status: str
    owner: str
    last_updated: datetime
    parent_charter: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

## **Dependencies**
- **External**: Python 3.13, Bazel, Pydantic v2, Typer, mistune, ruamel.yaml
- **Internal**: None (foundation milestone)

## **Testing Strategy**
- **Unit Tests**: Basic model validation and serialization
- **Integration Tests**: Package import verification
- **Build Tests**: Bazel build success verification

## **Success Metrics**
- All packages build successfully
- All imports resolve without errors
- Basic models validate correctly
- Test framework executes without issues

## **Potential Blockers**
- **Bazel Configuration**: Complex dependency management
- **Python Path Issues**: Import resolution problems
- **Version Conflicts**: Pydantic v2 compatibility issues

## **Completion Checklist**
- [ ] All implementation tasks completed
- [ ] All acceptance criteria met
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Code committed with logical commits
- [ ] Next milestone dependencies satisfied

## **Next Steps**
Upon completion, this milestone enables:
- **Milestone 2**: Rules Discovery (can begin immediately)
- **Milestone 4**: Validation Core (can begin after M2)
- **Milestone 7**: Testing & Documentation (can begin testing infrastructure)

---

**Status**: Not started
**Estimated Completion**: 1 day from start
**Actual Completion**: TBD
