---
title: "Decision: Quality Tools Service Structure and Organization"
type: "decision"
decision_id: "DEC-2025-07-24-005"
status: "accepted"
date_proposed: "2025-07-24"
date_decided: "2025-07-24"
deciders: ["Christian Blank", "Cline AI"]
parent_charter: "company_os/domains/charters/data/service-architecture.charter.md"
related_signals: []
related_brief: ""
related_project: "work/domains/projects/data/bazel-quality-tools-integration.vision.md"
supersedes: ""
superseded_by: ""
depends_on: ["DEC-2025-07-24-004"]
tags: ["architecture", "service-structure", "quality-tools", "hexagonal-architecture", "bazel"]
---

# **Decision: Quality Tools Service Structure and Organization**

**Status**: accepted
**Decision ID**: DEC-2025-07-24-005
**Date Decided**: 2025-07-24
**Deciders**: Christian Blank, Cline AI

---

## **Context**

### **Problem Statement**
Having decided to implement Bazel-based quality tools integration (DEC-2025-07-24-004), we need to determine the specific structure and organization of the quality_tools service. The structure must follow Company OS patterns while being practical for wrapping command-line tools.

### **Triggering Signals**
- Need for consistent service structure across Company OS domains
- Requirement to wrap multiple quality tools (ruff, mypy, black, isort, etc.)
- Desire for easy extensibility when adding new tools
- Goal of maintaining clear separation of concerns

### **Constraints**
- **Technical**: Must follow hexagonal architecture principles
- **Resource**: Should be simple enough for single developer to maintain
- **Business**: Must not over-engineer for current needs
- **Philosophical**: Follow "evolution on demand" principle

### **Assumptions**
- Quality tools are primarily command-line utilities
- Configuration files can be centralized
- Most tools follow similar invocation patterns
- Service will start at Stage 0 (file-based)

### **Environment State**
- **System Version**: Existing services use hexagonal architecture
- **Team Composition**: Developers familiar with current service patterns
- **External Factors**: Industry standard quality tools evolve independently
- **Dependencies**: Must integrate with Bazel build system

---

## **Options Considered**

### **Option A**: Full Hexagonal with Adapters per Tool
**Description**: Create separate adapter for each quality tool with full port/adapter separation

**Structure**:
```
quality_tools/
├── src/
│   ├── domain/
│   ├── ports/
│   └── use_cases/
├── adapters/
│   ├── ruff/
│   ├── mypy/
│   ├── black/
│   └── cli/
```

**Pros**:
- Maximum flexibility and separation
- Each tool fully encapsulated
- Follows pure hexagonal architecture

**Cons**:
- Over-engineered for wrapping CLIs
- Significant boilerplate code
- Harder to maintain consistency

**Estimated Effort**: 40-50 complexity points
**Risk Assessment**: Medium - over-engineering risk

### **Option B**: Simplified Structure with Bazel Focus
**Description**: Minimal structure focused on Bazel integration with shared wrapper logic

**Structure**:
```
quality_tools/
├── src/
│   └── tool_wrapper.py
├── adapters/
│   └── bazel/
│       ├── BUILD.bazel
│       ├── ruff_wrapper.py
│       ├── mypy_wrapper.py
│       └── tools.bzl
└── config/
    ├── ruff.toml
    └── mypy.ini
```

**Pros**:
- Simple and focused
- Minimal boilerplate
- Easy to understand and extend
- Shared wrapper logic reduces duplication

**Cons**:
- Less flexibility for complex tools
- Tighter coupling to Bazel
- Limited evolution path

**Estimated Effort**: 15-20 complexity points
**Risk Assessment**: Low - matches current needs

### **Option C**: Hybrid with Evolution Path
**Description**: Start simple but structure for future growth

**Structure**:
```
quality_tools/
├── __init__.py
├── BUILD.bazel
├── README.md
├── src/
│   ├── __init__.py
│   ├── BUILD.bazel
│   └── core/
│       ├── __init__.py
│       ├── base_wrapper.py
│       └── models.py
├── adapters/
│   ├── __init__.py
│   ├── bazel/
│   │   ├── BUILD.bazel
│   │   ├── __init__.py
│   │   ├── ruff_runner.py
│   │   ├── mypy_runner.py
│   │   └── wrapper_factory.py
│   └── cli/
│       ├── BUILD.bazel
│       ├── __init__.py
│       └── __main__.py
├── config/
│   ├── BUILD.bazel
│   ├── ruff.toml
│   ├── mypy.ini
│   └── pyproject.toml
└── tests/
    ├── BUILD.bazel
    ├── __init__.py
    ├── test_ruff_runner.py
    └── test_mypy_runner.py
```

**Pros**:
- Balanced complexity
- Clear evolution path
- Follows Company OS patterns
- Testable components

**Cons**:
- Slightly more initial setup
- Some anticipatory structure

**Estimated Effort**: 20-25 complexity points
**Risk Assessment**: Low - good balance

---

## **Decision**

### **Selected Option**: Option C - Hybrid with Evolution Path

### **Rationale**
The hybrid approach was selected because:

1. **Balanced Complexity**: Not over-engineered but has room to grow
2. **Company OS Alignment**: Follows established patterns from other services
3. **Clear Boundaries**: Separates tool execution (adapters) from core logic
4. **Testability**: Each component can be tested independently
5. **Evolution Ready**: Can add API endpoints, metrics, or new tools easily

The structure provides:
- **src/core**: Base classes and shared logic for all tools
- **adapters/bazel**: Bazel-specific runners for each tool
- **adapters/cli**: Optional CLI for direct tool access
- **config/**: Centralized tool configurations
- **tests/**: Comprehensive test coverage

### **Charter Alignment**
- Follows hexagonal architecture with clear adapter boundaries
- Supports staged evolution (starting at Stage 0)
- Maintains single responsibility principle

---

## **Consequences**

### **Immediate Impact**
- Clear directory structure for implementation
- Standardized pattern for adding new tools
- Separation of tool logic from Bazel integration
- Testable components from day one

### **Long-term Effects**
- **Enables**: Easy addition of new quality tools
- **Prevents**: Tight coupling to specific tool versions
- **Creates**: Reusable patterns for other services
- **Maintains**: Flexibility for future requirements

### **Success Metrics**
- **Clarity**: New developer can add tool in <2 hours
- **Reusability**: >80% code shared between tool runners
- **Testability**: >90% code coverage achievable
- **Maintainability**: Single file change to update tool

### **Risk Mitigation**
- **Risk**: Over-abstraction → **Mitigation**: Start with 2 tools, refactor on third
- **Risk**: Performance overhead → **Mitigation**: Measure and optimize critical paths
- **Risk**: Complex testing → **Mitigation**: Focus on integration tests

---

## **Implementation**

### **File Templates**

**Base Wrapper (src/core/base_wrapper.py)**:
```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ToolResult:
    exit_code: int
    stdout: str
    stderr: str

class BaseToolWrapper(ABC):
    """Base class for all quality tool wrappers."""

    @abstractmethod
    def name(self) -> str:
        """Tool name for logging and identification."""
        pass

    @abstractmethod
    def run(self, args: List[str], cwd: Optional[str] = None) -> ToolResult:
        """Execute the tool with given arguments."""
        pass
```

**Tool Runner (adapters/bazel/ruff_runner.py)**:
```python
from company_os.domains.quality_tools.src.core.base_wrapper import BaseToolWrapper
import subprocess

class RuffRunner(BaseToolWrapper):
    def name(self) -> str:
        return "ruff"

    def run(self, args: List[str], cwd: Optional[str] = None) -> ToolResult:
        # Implementation details
        pass
```

**BUILD.bazel Structure**:
```starlark
# adapters/bazel/BUILD.bazel
py_binary(
    name = "ruff",
    srcs = ["ruff_main.py"],
    deps = [
        ":ruff_runner",
        "//company_os/domains/quality_tools/src:quality_tools_lib",
        "@pypi//ruff",
    ],
)
```

---

## **Review**

### **Review Triggers**
- **Event-based**: When adding 4th quality tool
- **Time-based**: After 60 days of usage
- **Metric-based**: If code duplication exceeds 30%

### **Review Process**
1. **Data gathering**: Analyze code patterns across tools
2. **Analysis**: Identify common abstractions
3. **Decision**: Refactor if patterns emerge

---

## **Learning Capture**

### **Expected Outcomes**
- Clear pattern for tool integration established
- Minimal boilerplate for new tools
- Consistent interface across all quality tools
- Easy testing and maintenance

### **Monitoring Plan**
- Track time to add new tools
- Monitor code duplication metrics
- Gather developer feedback on structure

### **Signal Generation**
- **Positive**: Quick tool additions → validate structure
- **Negative**: Repeated modifications → refactoring needed
- **Unexpected**: Performance issues → architecture review

---

## **Notes**

This structure balances immediate needs with future growth potential. The key insight is that quality tools are essentially command-line wrappers, so the architecture should facilitate that primary use case while allowing for future enhancements like metrics collection, caching, or API exposure.

The decision to include a CLI adapter from the start provides a useful debugging and testing interface, even if the primary usage is through Bazel targets.
