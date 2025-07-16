---
title: "Decision: Implement Markdown Validation Service"
type: "decision"
decision_id: "DEC-2025-07-15-002"
status: "proposed"
date_proposed: "2025-07-15"
date_decided: "2025-07-15"
deciders: ["Christian Blank", "OS Core Team"]
parent_charter: "/os/domains/charters/data/maintenance-service.charter.md"
related_signals: ["/work/domains/signals/data/SIG-2025-07-14-001-system-complexity-automation-need.signal.md"]
related_brief: "/work/domains/briefs/data/BRIEF-2025-07-16-001-maintenance-foundations-v0.brief.md"
related_project: ""
supersedes: ""
superseded_by: ""
tags: ["validation", "automation", "quality", "maintenance"]
---

# **Decision: Implement Markdown Validation Service**

**Status**: proposed  
**Decision ID**: DEC-2025-07-15-002  
**Date Decided**: 2025-07-15  
**Deciders**: Christian Blank, OS Core Team

---

## **Context**

### **Problem Statement**
Manual validation of markdown documents is exceeding human capacity as the repository grows. We need automated validation that can check document conformance, request human input when needed, and generate signals for systematic improvements.

### **Triggering Signals**
- **SIG-2025-07-14-001**: System complexity exceeding manual maintenance capacity
  - Specifically: broken links, inconsistent formatting, missing required fields
  - Affects all document types: decisions, signals, briefs, charters

### **Constraints**
- **Technical**: Must integrate with existing file-based Stage 0 architecture
- **Resource**: Single developer bandwidth, must be implementable incrementally
- **Business**: No additional infrastructure costs for Stage 0
- **Philosophical**: Must maintain "human-in-loop" principle for ambiguous fixes

### **Assumptions**
- Templates will remain the source of truth for validation rules
- Python 3.13 and Pydantic v2 are acceptable technology choices
- Bazel build system is already in place
- Most validation issues are formatting/structural, not semantic

### **Environment State**
- **System Version**: Repository at Stage 0 (file-based)
- **Team Composition**: Christian (developer) + AI coding assistants
- **External Factors**: Multiple AI agents (Cline, Cursor, etc.) need consistent document structure
- **Dependencies**: Rules Service, Maintenance Service Charter

---

## **Options Considered**

### **Option A**: Standalone Validation Tool
**Description**: Build a separate validation tool independent of other services

**Pros**:
- Simple to implement
- No dependencies on other services
- Can start immediately

**Cons**:
- Duplicates functionality with Rules Service
- No integration with signal system
- Harder to maintain long-term

**Estimated Effort**: 15 complexity points
**Risk Assessment**: Medium - risk of divergence from system architecture

### **Option B**: Integrated Validation Service (Selected)
**Description**: Build validation as part of Rules Service with signal generation

**Pros**:
- Follows service architecture principles
- Automatic signal generation for patterns
- Reuses existing infrastructure
- Natural evolution path

**Cons**:
- Slightly more complex initial setup
- Requires coordination with Rules Service

**Estimated Effort**: 20 complexity points
**Risk Assessment**: Low - aligns with architecture

### **Option C**: Third-Party Linting Tools
**Description**: Use existing markdown linters and adapt them

**Pros**:
- Faster initial deployment
- Well-tested tools

**Cons**:
- Limited customization for our schemas
- No signal generation
- Difficult to add human-input comments
- External dependencies

**Estimated Effort**: 10 complexity points
**Risk Assessment**: High - won't meet our specific needs

---

## **Decision**

### **Selected Option**: Option B - Integrated Validation Service

### **Rationale**
The integrated approach aligns with our service architecture principles and enables the validation system to participate in the learning loop. By generating signals from validation failures, we can systematically improve our templates and documentation quality. The tight integration with Rules Service ensures validation rules stay synchronized with templates.

### **Charter Alignment**
- **Maintenance Service Charter**: Directly implements validation and conformance checking
- **Service Architecture Charter**: Follows hexagonal architecture and service evolution stages
- **Company OS Charter**: Supports "Shared, Explicit Memory" by ensuring document quality

---

## **Consequences**

### **Immediate Impact**
- Validation rules document created in `/os/domains/rules/data/`
- Rules Service Charter updated to include validation scope
- Brief System rules updated with validation-driven brief generation
- CLI will gain `validate` command

### **Long-term Effects**
- **Enables**: Automated quality assurance, pattern detection, systematic improvements
- **Prevents**: Document drift, broken references, inconsistent formatting
- **Creates**: Dependency on template structure for validation rules

### **Success Metrics**
- Validation coverage > 90% of markdown documents
- Auto-fix success rate > 80% for formatting issues
- < 10 human input requests per 100 documents validated
- Signal generation for patterns affecting > 10 documents

### **Risk Mitigation**
- **Risk**: Template changes break validation → **Mitigation**: Auto-regenerate rules on template change
- **Risk**: Too many false positives → **Mitigation**: Severity levels (error/warning/info)
- **Risk**: Performance issues → **Mitigation**: Stage evolution when needed

---

## **Implementation**

### **Action Items**
1. **Extract validation rules from templates**
   - **Owner**: Christian
   - **Timeline**: Milestone 0.1
   - **Dependencies**: Template files exist

2. **Implement core validation engine**
   - **Owner**: Christian
   - **Timeline**: Milestone 0.1
   - **Dependencies**: Pydantic v2, Python 3.13

3. **Add human input comment system**
   - **Owner**: Christian
   - **Timeline**: Milestone 0.1
   - **Dependencies**: Validation engine

4. **Integrate with CLI**
   - **Owner**: Christian
   - **Timeline**: Milestone 0.3
   - **Dependencies**: Developer CLI v0

### **Implementation Path**
1. Create `company_os_core/validation_service/` module
2. Implement template parser and rule extractor
3. Build validation engine with Pydantic models
4. Add signal generation for validation patterns
5. Integrate with `company-os validate` command
6. Add pre-commit hook for automatic validation

### **Rollback Plan**
- **Conditions**: Validation false positive rate > 50%
- **Steps**: 
  1. Disable pre-commit hook
  2. Remove validate command from CLI
  3. Archive validation rules
- **Data**: Preserve validation signals for analysis

---

## **Review**

### **Review Triggers**
- **Complexity-based**: After 100 validation runs
- **Event-based**: When new document type added
- **Metric-based**: If false positive rate > 20%

### **Review Process**
1. Analyze validation signal patterns
2. Survey document authors for friction points
3. Decide on rule adjustments or stage evolution

---

## **Learning Capture**

### **Expected Outcomes**
- Consistent document structure across repository
- Rapid identification of systematic issues
- Reduced manual review burden

### **Monitoring Plan**
- Track validation runs per week
- Monitor auto-fix vs human input ratio
- Measure time saved in document review

### **Signal Generation**
- **Positive**: High auto-fix rate → opportunity signal for more automation
- **Negative**: Many human inputs → friction signal for template improvement
- **Unexpected**: Validation patterns reveal architectural issues → exploration signal

---

## **Notes**

This decision implements the validation capabilities defined in the Repository Maintenance Service Charter. The staged approach allows us to start with simple file-based validation and evolve as needs grow, following our principle of "evolution on demand."

The validation system will work closely with the Rules Service to maintain synchronization between templates and validation rules, ensuring our "single source of truth" principle is maintained.
