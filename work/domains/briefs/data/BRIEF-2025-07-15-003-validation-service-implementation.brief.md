---
title: "Brief: Implement Markdown Validation Service Stage 0"
type: "brief"
brief_id: "BRIEF-2025-07-15-003"
brief_type: "technical"
priority: "high"
status: "draft"
governing_charter: "/os/domains/charters/data/maintenance-service.charter.md"
source_signals: ["/work/domains/signals/data/SIG-2025-07-14-001-system-complexity-automation-need.signal.md"]
strategic_theme: "Automation Infrastructure"
estimated_effort: "20"
date_created: "2025-07-15"
date_reviewed: ""
date_approved: ""
related_briefs: ["BRIEF-2025-07-16-001", "BRIEF-2025-07-15-001"]
depends_on: ["BRIEF-2025-07-15-002"]
implemented_by: ""
superseded_by: ""
tags: ["validation", "automation", "stage-0", "quality"]
---

# **Brief: Implement Markdown Validation Service Stage 0**

**Type**: technical  
**Priority**: high  
**Status**: draft  
**Strategic Theme**: Automation Infrastructure  
**Estimated Effort**: 20 complexity points  
**Date Created**: 2025-07-15

---

## **Executive Summary**

### **The Opportunity**
Implement an automated markdown validation system that extracts rules from templates, validates documents, and generates signals for systematic improvements.

### **The Impact**
Eliminate manual validation burden, ensure consistent document quality, and enable systematic improvement through validation-driven signals and briefs.

### **The Investment**
20 complexity points to deliver Stage 0 validation with template parsing, core validation engine, human input system, and CLI integration.

---

## **Problem Statement**

### **Current State**
- Manual validation of growing markdown repository exceeding human capacity
- Inconsistent document formats across different authors and AI agents
- No systematic way to detect and fix document quality issues
- Broken links and references discovered only after merge

### **Pain Points**
- **Manual Review Burden**: Every document requires human validation
- **Inconsistent Quality**: Different agents produce different formats
- **Late Discovery**: Issues found after documents are committed
- **No Pattern Detection**: Can't identify systematic problems

### **Impact Assessment**
- **Frequency**: Every document creation/update (>50 per week)
- **Complexity**: Multiple document types with different schemas
- **Scope**: Affects all contributors (humans and AI agents)
- **Cost**: 2-3 hours daily manual review time

---

## **Signal Evidence**

### **Supporting Signals**

**SIG-2025-07-14-001**: System complexity exceeding manual maintenance capacity
- **Type**: friction
- **Severity**: critical
- **Summary**: Manual processes failing to scale with repository growth
- **Link**: /work/domains/signals/data/SIG-2025-07-14-001-system-complexity-automation-need.signal.md

### **Pattern Analysis**
- Common themes: Manual processes, quality inconsistency, late error detection
- Root causes: Lack of automation, no validation framework
- Affected systems: All document types across all service domains

### **Validation**
- Signal count: 1 critical signal (sufficient for critical severity)
- Evidence quality: Direct observation of daily friction
- Stakeholder alignment: Directly supports Maintenance Service Charter

---

## **Proposed Solution**

### **Solution Overview**
Build validation as an integrated part of the Rules Service, extracting validation rules from templates and providing automated checking with human-in-loop for ambiguous fixes.

### **Key Components**
1. **Template Parser**: Extract validation rules from markdown templates
2. **Validation Engine**: Check documents against extracted rules
3. **Human Input System**: Request human intervention via standardized comments
4. **Signal Generator**: Create signals for validation patterns

### **Implementation Approach**
- **Phase 1**: Core validation engine (Milestone 0.1 - 8 points)
- **Phase 2**: Template rule extraction (Milestone 0.2 - 5 points)
- **Phase 3**: CLI integration (Milestone 0.3 - 7 points)

### **Success Criteria**
- **Metric 1**: >90% markdown documents pass validation
- **Metric 2**: >80% formatting issues auto-fixed
- **Metric 3**: <10 human input requests per 100 documents

---

## **Charter Alignment**

### **Governing Charter**
Repository Maintenance Service Charter - directly implements validation and conformance checking mandate.

### **Charter Principles**
- **Fail Fast, Fix Fast**: Detect issues in pre-commit, not post-merge
- **Deterministic Repair**: All auto-fixes are reproducible
- **Human-in-Loop by Default**: Ambiguous fixes require human input

### **Strategic Objectives**
Enables the self-evolving system by generating signals about document quality patterns that feed into the learning loop.

---

## **Resource Requirements**

### **Estimated Effort**
20 complexity points broken down as:
- Core validation engine: 8 points
- Template parser: 5 points  
- CLI integration: 7 points

### **Skills Required**
- Python 3.13 with type hints
- Pydantic v2 for data models
- Bazel build system
- Markdown parsing (mistune)
- YAML frontmatter handling

### **Dependencies**
- Developer CLI v0 (BRIEF-2025-07-15-002)
- Rules Service v0 (BRIEF-2025-07-15-001)
- Existing markdown templates

### **Constraints**
- **Technical**: Must work with file-based Stage 0 architecture
- **Resource**: Single developer implementation
- **Business**: No additional infrastructure costs

---

## **Risk Assessment**

### **Implementation Risks**
- **Risk 1**: Template format changes break validation - **Mitigation**: Version validation schemas
- **Risk 2**: Too many false positives - **Mitigation**: Severity levels (error/warning/info)
- **Risk 3**: Performance with large repos - **Mitigation**: Incremental validation, caching

### **Outcome Risks**
- **Risk 1**: Users disable validation due to friction - **Mitigation**: Good UX, clear error messages
- **Risk 2**: Auto-fixes introduce bugs - **Mitigation**: Safe operations only, extensive testing

### **Opportunity Costs**
Delaying implementation means continued manual validation burden and inconsistent document quality.

---

## **Alternative Solutions**

### **Alternative 1**: Third-Party Markdown Linters
**Description**: Use markdownlint or similar tools  
**Pros**: Faster initial setup, well-tested  
**Cons**: Can't handle our custom schemas, no signal generation  
**Why Not Selected**: Doesn't meet our specific validation needs

### **Alternative 2**: Manual Review Process
**Description**: Continue with human review  
**Pros**: No development effort  
**Cons**: Doesn't scale, error-prone, expensive  
**Why Not Selected**: Already failing at current scale

---

## **Implementation Plan**

### **Immediate Next Steps**
1. Set up `company_os_core/validation_service/` module structure
2. Create Pydantic models for validation rules and issues
3. Implement template parser for rule extraction

### **Implementation Sequence**

#### Milestone 0.1: Core Validation Engine (8 points)
```python
# Deliverables:
- ValidationRule, ValidationSchema, ValidationIssue models
- Document validator with frontmatter and section checking  
- Human input comment generation
- Bazel BUILD files with dependencies
- 90%+ test coverage

# Acceptance Criteria:
✓ Parse decision, signal, brief templates for rules
✓ Validate documents against schemas
✓ Generate signals for failures
✓ Insert HUMAN-INPUT-REQUIRED comments
✓ All core validation logic tested
```

#### Milestone 0.2: Template Rule Extractor (5 points)
```python
# Deliverables:
- Automatic rule extraction from templates
- Frontmatter pattern detection
- Section structure parsing
- Validation config generation

# Acceptance Criteria:
✓ Extract field patterns from examples
✓ Identify required vs optional fields
✓ Detect section hierarchies
✓ Generate complete ValidationSchema
```

#### Milestone 0.3: CLI Integration (7 points)
```python
# Deliverables:
- `company-os validate` command
- Batch validation with reports
- --fix flag for auto-fixes
- Pre-commit hook integration

# Acceptance Criteria:
✓ Validate files or directories
✓ Human-readable error reports
✓ Auto-fix formatting issues
✓ Generate signals in correct location
✓ Proper exit codes (0=success, 1=errors)
```

### **Milestones**
1. Core engine complete and tested
2. Templates parsed, rules extracted
3. CLI command available for use

### **Success Measurement**
- Validation coverage percentage
- Auto-fix success rate
- Time saved vs manual review
- Signal patterns identified

---

## **Stakeholder Analysis**

### **Primary Stakeholders**
- Document authors (humans and AI agents)
- Repository maintainers
- New contributors needing consistent examples

### **Decision Makers**
- Christian Blank (implementation)
- OS Core Team (approval)

### **Implementation Team**
- Developer: Christian
- AI Coding Assistant for implementation
- Users for testing and feedback

---

## **Related Initiatives**

### **Related Briefs**
- BRIEF-2025-07-16-001: Maintenance Foundations v0
- BRIEF-2025-07-15-001: Rules Service v0
- BRIEF-2025-07-15-002: Developer CLI v0

### **Existing Projects**
- Rules Service implementation
- Developer CLI framework

### **Strategic Themes**
- Automation Infrastructure
- Developer Experience
- Quality Assurance

---

## **Appendices**

### **Appendix A: Technical Implementation Details**

```python
# Core data models (Pydantic v2)
class ValidationRule(BaseModel):
    field_name: str
    rule_type: Literal["required", "pattern", "allowed_values"]
    parameters: dict[str, Any]
    severity: Literal["error", "warning", "info"] = "error"

class ValidationIssue(BaseModel):
    location: str  # file:line
    rule: ValidationRule
    message: str
    human_input_needed: bool = False
    suggested_fix: Optional[str] = None

# Bazel dependencies
py_library(
    name = "validation_service",
    srcs = glob(["**/*.py"]),
    deps = [
        "@pip//pydantic:pkg",
        "@pip//ruamel.yaml:pkg",
        "@pip//mistune:pkg",
    ],
)
```

### **Appendix B: Human Input Comment Format**

```markdown
<!-- HUMAN-INPUT-REQUIRED: [CATEGORY]
Issue: [Specific problem description]
Required Action: [What needs to be done]
Context: [Additional helpful information]
Priority: [high|medium|low]
-->
```

### **Appendix C: Evolution Triggers**

**Stage 0 → 1 Triggers**:
- Validation runs exceed 100/week
- Need for programmatic access from 3+ consumers
- Average validation time exceeds 50ms

---

**Instructions for Using This Brief:**

1. **Implementation Ready**: This brief provides concrete milestones for coding agents
2. **Test-Driven**: Each milestone includes specific acceptance criteria
3. **Type-Safe**: Use Python 3.13 with full type annotations
4. **Incremental**: Can be implemented one milestone at a time
5. **Evolution Path**: Clear triggers for when to advance stages
