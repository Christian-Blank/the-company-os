---
title: "Decision: Remove python3.12-distutils from Ubuntu 24.04 Dev Container"
type: "decision"
decision_id: "DEC-2025-07-23-002"
status: "accepted"
date_proposed: "2025-07-23"
date_decided: "2025-07-23"
deciders: ["Cline AI Agent", "Christian Blank"]
parent_charter: "company_os/domains/charters/data/service-architecture.charter.md"
related_signals: []
related_brief: ""
related_project: ""
supersedes: ""
superseded_by: ""
tags: ["development", "environment", "python", "packaging", "ubuntu", "devcontainer", "pep632"]
---

# **Decision: Remove python3.12-distutils from Ubuntu 24.04 Dev Container**

**Status**: accepted
**Decision ID**: DEC-2025-07-23-002
**Date Decided**: 2025-07-23
**Deciders**: Cline AI Agent, Christian Blank

---

## **Context**

### **Problem Statement**
The dev container build was failing with package installation error when trying to install `python3.12-distutils`:
```
E: Unable to locate package python3.12-distutils
E: Couldn't find any package by glob 'python3.12-distutils'
E: Couldn't find any package by regex 'python3.12-distutils'
```

This prevented the successful creation of the Ubuntu 24.04 development container.

### **Triggering Signals**
This decision was made during implementation of DEC-2025-07-23-001 (Ubuntu Dev Container) when the container build failed. The error occurred immediately after fixing the PEP 668 issue with pipx/UV separation.

### **Constraints**
- **Technical**: Must work with Ubuntu 24.04 LTS and Python 3.12
- **Resource**: Need to maintain container build functionality
- **Business**: Cannot delay development environment setup
- **Philosophical**: Must align with modern Python packaging standards

### **Assumptions**
- Ubuntu 24.04 ships with Python 3.12 as the default version
- Modern Python toolchain (pipx, UV) does not require distutils
- PEP 632 compliance is more important than legacy distutils support
- The removal will not affect our development workflow

### **Environment State**
- **System Version**: Ubuntu 24.04 LTS with Python 3.12 default
- **Team Composition**: Mixed development team using Company OS toolchain
- **External Factors**: Python 3.12 removed distutils as part of PEP 632
- **Dependencies**: pipx, UV, pre-commit, ruff, mypy installation

---

## **Options Considered**

### **Option A**: Remove python3.12-distutils from Package List
**Description**: Simply remove the non-existent package from the apt install command

**Pros**:
- Simple, direct fix
- Aligns with Python 3.12 and PEP 632 standards
- No impact on modern toolchain functionality
- Maintains Ubuntu 24.04 compatibility

**Cons**:
- Need to verify no dependencies on distutils in our toolchain
- Could potentially affect legacy Python code (unlikely in our case)

**Estimated Effort**: 1 minute to remove line
**Risk Assessment**: Very low - modern Python packaging has moved away from distutils

### **Option B**: Use Alternative Package or Workaround
**Description**: Try to find an alternative package that provides distutils functionality

**Pros**:
- Might preserve legacy compatibility
- Could provide distutils if needed

**Cons**:
- No such package exists in Ubuntu 24.04
- Would be fighting against Python ecosystem evolution
- Unnecessary complexity for modern toolchain

**Estimated Effort**: Hours of research for likely no solution
**Risk Assessment**: High - would be fighting upstream decisions

### **Option C**: Downgrade Python or Ubuntu Version
**Description**: Use older versions that still include distutils

**Pros**:
- Would have distutils available
- Might avoid other Python 3.12 changes

**Cons**:
- Goes against decision to use Ubuntu 24.04 LTS
- Reduces long-term support window
- Contradicts modern Python development practices
- Would require updating entire container architecture

**Estimated Effort**: Significant rework of container and toolchain
**Risk Assessment**: High - creates technical debt and reduces supportability

---

## **Decision**

### **Selected Option**: Option A - Remove python3.12-distutils from Package List

### **Rationale**
The decision to remove `python3.12-distutils` was made because:

1. **PEP 632 Compliance**: Python 3.12 officially removed distutils from the standard library as part of PEP 632, making it unavailable in Ubuntu 24.04
2. **Modern Toolchain Compatibility**: Our toolchain (pipx, UV, pre-commit, ruff, mypy) does not depend on distutils
3. **Ubuntu 24.04 Reality**: The package simply doesn't exist in the Ubuntu 24.04 repositories
4. **Ecosystem Evolution**: The Python packaging ecosystem has moved to modern tools that don't require distutils

### **Charter Alignment**
This decision aligns with Company OS service architecture charter principles:
- **Explicit over Implicit**: We explicitly acknowledge Python's evolution away from distutils
- **Quality Gates**: Ensures container builds succeed reliably
- **Modern Standards**: Follows current Python packaging best practices
- **Long-term Supportability**: Aligns with Ubuntu 24.04 LTS lifecycle

---

## **Consequences**

### **Immediate Impact**
- Dev container builds successfully without package installation errors
- No functional impact on development workflow
- Container creation time remains the same
- All modern Python packaging tools continue to work

### **Long-term Effects**
- **Enables**: Full compatibility with Python 3.12 ecosystem evolution
- **Prevents**: Future issues with deprecated packaging tools
- **Creates**: Clean alignment with modern Python standards
- **Maintains**: Long-term supportability with Ubuntu 24.04 LTS

### **Success Metrics**
- **Container Build Success**: 100% successful builds
- **Tool Functionality**: All development tools (pipx, UV, pre-commit, ruff, mypy) work correctly
- **Developer Experience**: No impact on development workflow

### **Risk Mitigation**
- **Risk**: Legacy code depending on distutils → **Mitigation**: Our codebase uses modern packaging (UV), no legacy dependencies identified
- **Risk**: Third-party tools needing distutils → **Mitigation**: All our tools (pipx-installed) are modern and don't require distutils

---

## **Implementation**

### **Action Items**

1. **Remove python3.12-distutils from Dockerfile**
   - **Owner**: Cline AI Agent
   - **Timeline**: Immediate
   - **Dependencies**: None

2. **Test Container Build**
   - **Owner**: Christian Blank
   - **Timeline**: After Dockerfile update
   - **Dependencies**: Item 1 complete

3. **Verify Tool Functionality**
   - **Owner**: Development team
   - **Timeline**: During first container use
   - **Dependencies**: Item 2 complete

### **Implementation Path**
1. Edit `.devcontainer/Dockerfile` to remove `python3.12-distutils \` line
2. Rebuild container to verify successful build
3. Test all development tools to ensure no regression
4. Update documentation if needed

### **Rollback Plan**
- **Conditions**: If any critical functionality breaks (highly unlikely)
- **Steps**: The change is easily reversible, but since the package doesn't exist, rollback would require finding alternative solutions
- **Preservation**: No special data preservation needed

---

## **Review**

### **Review Triggers**
- **Time-based**: Review in 6 months during container maintenance
- **Event-based**: Review if any tool fails due to missing distutils
- **Metric-based**: Review if container build success rate drops below 95%

### **Review Process**
1. **Data gathering**: Check tool functionality, build success rates, developer feedback
2. **Analysis**: Assess if removal continues to be the right approach
3. **Decision**: Maintain status quo or investigate modern alternatives

---

## **Learning Capture**

### **Expected Outcomes**
- Container builds work reliably
- No functional impact on development
- Better alignment with Python ecosystem evolution
- Cleaner, more maintainable container definition

### **Monitoring Plan**
- **Data to collect**: Container build success rates, tool functionality, developer issue reports
- **Frequency**: Continuous monitoring of build processes
- **Responsible**: Platform team and container maintainers

### **Signal Generation**
- **Positive outcomes**: Generate signals about successful Python 3.12 adoption
- **Negative outcomes**: Generate signals if any distutils-dependent functionality is discovered
- **Unexpected consequences**: Monitor for edge cases in Python packaging ecosystem

---

## **Notes**

This decision represents the natural evolution of the Python packaging ecosystem. Python 3.12's removal of distutils (PEP 632) reflects the community's move toward modern packaging tools like pip, build, and setuptools (when needed). Our toolchain (UV, pipx) is well-positioned for this transition.

The error provided clear guidance - Ubuntu 24.04 simply doesn't have this package because Python 3.12 doesn't include distutils. This decision documents our acceptance of this reality and our commitment to modern Python development practices.
