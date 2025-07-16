---
title: "Decision: Pre-commit Hook Auto-fix Enhancement"
type: "decision"
decision_id: "DEC-2025-07-16-001"
status: "accepted"
date_proposed: "2025-07-16"
date_decided: "2025-07-16"
deciders: ["Christian Blank", "Cline AI"]
parent_charter: "../../../os/domains/charters/data/knowledge-architecture.charter.md"
related_signals: ["SIG-2025-07-16-001-pre-commit-validation-failures"]
related_brief: "/work/domains/briefs/data/BRIEF-2025-07-15-003-validation-service-implementation.brief.md"
related_project: "/work/domains/projects/data/rules-service-v0/"
supersedes: ""
superseded_by: ""
tags: ["pre-commit", "validation", "automation", "git-workflow", "developer-experience"]
---

# **Decision: Pre-commit Hook Auto-fix Enhancement**

**Status**: accepted
**Decision ID**: DEC-2025-07-16-001
**Date Decided**: 2025-07-16
**Deciders**: Christian Blank, Cline AI

---

## **Context**

### **Problem Statement**
The pre-commit validation hook was failing due to path resolution issues and developers were forgetting to commit auto-fixed files, leading to incomplete commits and workflow friction.

### **Triggering Signals**
- **Path Resolution Failure**: Hook couldn't find files like `docs/developers/contributing.md`
- **Developer Workflow Friction**: Auto-fixed files not being committed with original changes
- **Dependency Management Issues**: CLI failing due to version conflicts in build environment

### **Constraints**
- **Technical**: Must work within Bazel build system's execution context
- **Workflow**: Cannot break existing pre-commit hook behavior
- **Developer Experience**: Must provide clear feedback about auto-fixes
- **Reversibility**: Must be easily removable if not desired

### **Assumptions**
- Developers prefer automatic handling of auto-fixes over manual git operations
- Clear warnings about auto-fixes are more important than silent fixes
- The project root can be reliably determined from hook execution context
- Git staging area is the appropriate place for auto-fixed files

### **Environment State**
- **Bazel Version**: 8.3.1 with bzlmod
- **Pre-commit Framework**: Active with rules-service hooks
- **Build System**: Running CLI through Bazel in sandboxed environment
- **Git Workflow**: Feature branch development with pre-commit validation

---

## **Options Considered**

### **Option A**: Path Resolution Only
**Description**: Fix only the path resolution issue without auto-git handling

**Pros**:
- Minimal change to existing behavior
- Lower risk of unintended consequences
- Simple implementation

**Cons**:
- Developers still need to manually commit auto-fixes
- Workflow friction remains
- Easy to forget fixed files

**Estimated Effort**: 5 complexity points
**Risk Assessment**: Low - minimal change

### **Option B**: Auto-fix with Git Integration (Selected)
**Description**: Fix path resolution and automatically add auto-fixed files to git staging

**Pros**:
- Seamless developer experience
- Prevents forgotten auto-fixes
- Clear feedback about what was changed
- Maintains git history integrity

**Cons**:
- More complex implementation
- Potential for unexpected git behavior
- Requires careful error handling

**Estimated Effort**: 15 complexity points
**Risk Assessment**: Medium - git integration complexity

### **Option C**: Manual Override Flag
**Description**: Add flag to disable auto-fix or auto-git behavior

**Pros**:
- Maximum developer control
- Easy to revert if issues arise
- Supports different workflows

**Cons**:
- Adds complexity to interface
- Most developers would use default anyway
- Configuration overhead

**Estimated Effort**: 20 complexity points
**Risk Assessment**: Medium - interface complexity

---

## **Decision**

### **Selected Option**: Option B - Auto-fix with Git Integration

### **Rationale**
The auto-fix with git integration provides the best developer experience by eliminating manual steps that are easy to forget. The warning system ensures transparency about what changes were made. The implementation can be easily removed if it causes issues.

### **Charter Alignment**
- **Knowledge Architecture Charter**: Supports "Documentation as Code" by making fixes seamless
- **Rules Service Charter**: Enhances validation capabilities with better workflow integration
- **Developer Experience**: Reduces friction in contribution workflow

---

## **Consequences**

### **Immediate Impact**
- Path resolution fixed for validation hook
- Auto-fixed files automatically added to git staging
- Clear warnings displayed when files are auto-fixed
- Improved developer workflow experience

### **Long-term Effects**
- **Enables**: Seamless validation workflow, consistent document quality
- **Prevents**: Forgotten auto-fixes, incomplete commits, workflow friction
- **Creates**: Expectation of automatic git handling in other hooks

### **Success Metrics**
- Pre-commit hook success rate > 95%
- Developer reports of workflow friction < 5%
- Auto-fix detection accuracy > 99%
- Zero instances of forgotten auto-fixes

### **Risk Mitigation**
- **Risk**: Auto-git fails → **Mitigation**: Clear error messages, fallback to manual
- **Risk**: Unexpected git behavior → **Mitigation**: Thorough testing, easy removal
- **Risk**: Performance impact → **Mitigation**: File checksum optimization

---

## **Implementation**

### **Technical Details**

#### **Path Resolution Fix**
```python
# Get project root for proper path resolution
PROJECT_ROOT = Path(__file__).resolve().parents[4]

# Resolve file paths relative to project root
if not file_path.is_absolute():
    file_path = PROJECT_ROOT / file_path
```

#### **Auto-fix Detection**
```python
# Store file checksums before validation
file_checksums_before = {}
for file_path in markdown_files:
    file_checksums_before[file_path] = _get_file_checksum(file_path)

# After validation, detect modified files
modified_files = []
for file_path in markdown_files:
    checksum_after = _get_file_checksum(file_path)
    if checksum_after != file_checksums_before[file_path]:
        modified_files.append(file_path)
```

#### **Git Integration**
```python
def _add_files_to_git(files: List[str]) -> bool:
    """Add files to git staging area."""
    try:
        cmd = ["git", "add"] + files
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        return result.returncode == 0
    except Exception:
        return False
```

### **Implementation Quirks**

#### **Bazel Execution Context**
- **Issue**: Bazel runs CLI in sandboxed environment with different working directory
- **Solution**: Always resolve paths relative to detected project root
- **Quirk**: Must use `PROJECT_ROOT` constant consistently across all path operations

#### **File Checksum Strategy**
- **Issue**: Need to detect file modifications reliably
- **Solution**: MD5 checksums before and after validation
- **Quirk**: Empty files or read errors return empty string checksum

#### **Git Staging Behavior**
- **Issue**: Pre-commit runs in git staging context
- **Solution**: Add modified files to staging area, not working directory
- **Quirk**: Files are added to the same commit automatically

#### **Error Handling Philosophy**
- **Issue**: Git operations might fail in some environments
- **Solution**: Fail gracefully with clear warnings, don't block validation
- **Quirk**: Success of auto-fix doesn't depend on git success

### **Action Items**
1. **Fix path resolution in validation command**
   - **Owner**: Cline AI
   - **Status**: Complete
   - **Implementation**: PROJECT_ROOT constant and relative path resolution

2. **Implement auto-fix detection**
   - **Owner**: Cline AI
   - **Status**: Complete
   - **Implementation**: File checksum comparison system

3. **Add git integration**
   - **Owner**: Cline AI
   - **Status**: Complete
   - **Implementation**: Auto-add modified files to git staging

4. **Test and verify behavior**
   - **Owner**: Christian Blank
   - **Status**: Pending
   - **Implementation**: Real-world commit testing

---

## **Review**

### **Review Triggers**
- **Usage-based**: After 50 commits with auto-fixes
- **Issue-based**: If any git integration problems reported
- **Metric-based**: If auto-fix success rate < 90%

### **Review Process**
1. Collect developer feedback on workflow experience
2. Analyze git logs for auto-fix patterns
3. Assess performance impact of checksum operations
4. Decide on enhancements or simplifications

---

## **Learning Capture**

### **Expected Outcomes**
- Seamless validation workflow without manual git operations
- Improved developer experience and reduced friction
- Consistent document quality through automated fixes

### **Monitoring Plan**
- Track pre-commit hook success rates
- Monitor developer feedback on workflow
- Measure auto-fix detection accuracy

### **Signal Generation**
- **Positive**: High auto-fix success rate → opportunity for more automation
- **Negative**: Git integration failures → technical debt signal
- **Unexpected**: Pattern of specific auto-fixes → rule improvement signal

---

## **Notes**

### **Design Philosophy**
The implementation follows the principle of "seamless automation with transparency" - auto-fixes happen automatically but with clear feedback about what was changed. This maintains developer trust while reducing manual overhead.

### **Bazel Integration Lessons**
Working with Bazel's execution context required careful attention to:
- Path resolution relative to project root, not execution directory
- Subprocess execution from correct working directory
- Build system dependencies and caching implications

### **Git Workflow Considerations**
The auto-git functionality integrates smoothly with pre-commit's staging area model:
- Files are added to staging, not working directory
- Changes appear in the same commit as original modifications
- No additional git operations required from developer

### **Future Enhancements**
Potential improvements identified during implementation:
- Configurable auto-fix behavior per developer
- Integration with other validation hooks
- Performance optimizations for large file sets
- Enhanced error reporting and diagnostics

---

## **Rollback Plan**

### **Conditions**
- Git integration causes workflow issues
- Auto-fix detection has false positives
- Performance impact is unacceptable

### **Steps**
1. Remove auto-git functionality from hook
2. Revert to path-resolution-only fix
3. Preserve validation functionality
4. Update documentation

### **Data**
- Preserve validation logs and patterns
- Maintain git history of auto-fixes
- Document lessons learned for future attempts

---

*This decision implements enhanced pre-commit validation workflow with automatic git integration, improving developer experience while maintaining transparency and control.*
