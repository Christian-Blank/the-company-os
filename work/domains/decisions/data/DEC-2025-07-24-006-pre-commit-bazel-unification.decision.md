---
title: "Decision: Pre-commit and Bazel Unification Strategy"
type: "decision"
decision_id: "DEC-2025-07-24-006"
status: "accepted"
date_proposed: "2025-07-24"
date_decided: "2025-07-24"
deciders: ["Christian Blank", "Cline AI"]
parent_charter: "company_os/domains/charters/data/service-architecture.charter.md"
related_signals: ["Dual tool management causing version drift risks"]
related_brief: ""
related_project: "work/domains/projects/data/bazel-quality-tools-integration.vision.md"
supersedes: ""
superseded_by: ""
depends_on: ["DEC-2025-07-24-004", "DEC-2025-07-24-005"]
tags: ["pre-commit", "bazel", "unification", "single-source-of-truth", "migration"]
---

# **Decision: Pre-commit and Bazel Unification Strategy**

**Status**: accepted
**Decision ID**: DEC-2025-07-24-006
**Date Decided**: 2025-07-24
**Deciders**: Christian Blank, Cline AI

---

## **Context**

### **Problem Statement**
With the decision to create Bazel-based quality tools (DEC-2025-07-24-004), we need a strategy to unify pre-commit hooks with Bazel targets. Currently, pre-commit uses external repositories (ruff-pre-commit, mirrors-mypy) which creates version management complexity and violates our single source of truth principle.

### **Triggering Signals**
- Pre-commit using ruff v0.12.5 while requirements_lock.txt may have different version
- External pre-commit repos can update independently causing drift
- Developers confused about which tool version is authoritative
- CI/CD and local environments may use different tool versions

### **Constraints**
- **Technical**: Pre-commit must continue working during migration
- **Resource**: Cannot require developers to change workflow immediately
- **Business**: Zero disruption to current development velocity
- **Philosophical**: Single source of truth must be achieved

### **Assumptions**
- Developers are comfortable with current pre-commit workflow
- Bazel command performance is acceptable for pre-commit hooks
- Migration can be done incrementally
- Team will adapt to new commands with proper documentation

### **Environment State**
- **System Version**: Pre-commit 3.5.0+ installed via pipx
- **Team Composition**: All developers actively using pre-commit
- **External Factors**: Pre-commit is industry standard tool
- **Dependencies**: Existing hooks for validation, formatting, linting

---

## **Options Considered**

### **Option A**: Immediate Full Migration
**Description**: Replace all external pre-commit repos with Bazel commands immediately

**Pros**:
- Clean cut-over to single source of truth
- No confusion about which system to use
- Immediate benefits of hermetic builds

**Cons**:
- High risk of disruption
- No fallback if issues arise
- Requires all developers to adapt immediately
- Potential for lost productivity

**Estimated Effort**: 5 complexity points
**Risk Assessment**: High - disruption risk

### **Option B**: Parallel Operation with Gradual Migration
**Description**: Run both systems in parallel, gradually migrate developers

**Pros**:
- Zero disruption to current workflow
- Time to identify and fix issues
- Developers can opt-in when ready
- Fallback available if problems

**Cons**:
- Temporary complexity increase
- Potential for confusion
- Longer migration period
- Dual maintenance burden

**Estimated Effort**: 10 complexity points
**Risk Assessment**: Low - safe migration path

### **Option C**: Feature Flag Approach
**Description**: Use environment variable to switch between external and Bazel hooks

**Pros**:
- Single configuration file
- Easy to switch back and forth
- Can be controlled per-developer
- Clean eventual removal

**Cons**:
- Complex pre-commit configuration
- Requires environment setup
- May not work well with pre-commit design

**Estimated Effort**: 15 complexity points
**Risk Assessment**: Medium - implementation complexity

### **Option D**: Staged Replacement by Tool
**Description**: Replace one tool at a time, starting with most stable

**Pros**:
- Incremental risk
- Learn from each migration
- Can prioritize problematic tools
- Maintains momentum

**Cons**:
- Extended migration period
- Mixed configuration complexity
- Requires careful coordination

**Estimated Effort**: 8 complexity points
**Risk Assessment**: Low - controlled migration

---

## **Decision**

### **Selected Option**: Option D - Staged Replacement by Tool

### **Rationale**
The staged replacement approach was selected because:

1. **Risk Management**: Each tool migration is a controlled experiment
2. **Learning Opportunity**: Early migrations inform later ones
3. **Developer Confidence**: Success with first tool builds trust
4. **Flexibility**: Can adjust strategy based on feedback
5. **Maintainability**: Clear migration checkpoints

Migration order based on stability and importance:
1. **Phase 1**: Ruff (most stable, clear benefits)
2. **Phase 2**: MyPy (important for type safety)
3. **Phase 3**: Standard hooks (trailing-whitespace, end-of-file-fixer)
4. **Phase 4**: Remove external repositories

### **Charter Alignment**
- Achieves single source of truth incrementally
- Follows "evolution on demand" principle
- Maintains system stability during transition

---

## **Consequences**

### **Immediate Impact**
- Ruff hooks switch to Bazel immediately
- Other tools continue using external repos
- Clear migration timeline communicated
- Documentation updated with new patterns

### **Long-term Effects**
- **Enables**: True single source of truth for all tools
- **Prevents**: Version drift across environments
- **Creates**: Pattern for future tool migrations
- **Simplifies**: Dependency management to one file

### **Success Metrics**
- **Migration Speed**: Each tool migrated within 1 week
- **Developer Satisfaction**: No complaints about new workflow
- **Version Consistency**: Zero drift incidents post-migration
- **Performance**: Pre-commit runtime within 10% of original

### **Risk Mitigation**
- **Risk**: Bazel command slower → **Mitigation**: Profile and optimize, use caching
- **Risk**: Developer resistance → **Mitigation**: Clear benefits documentation
- **Risk**: Migration stalls → **Mitigation**: Set firm deadlines per phase

---

## **Implementation**

### **Migration Schedule**

**Week 1: Ruff Migration**
```yaml
# Replace in .pre-commit-config.yaml:
# OLD:
-   repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.12.5
    hooks:
    -   id: ruff
        args: [--fix]
    -   id: ruff-format

# NEW:
-   repo: local
    hooks:
    -   id: bazel-ruff-check
        name: Lint with Ruff (Bazel)
        entry: bazel run //:ruff -- check --fix
        language: system
        types: [python]
        pass_filenames: true

    -   id: bazel-ruff-format
        name: Format with Ruff (Bazel)
        entry: bazel run //:ruff -- format
        language: system
        types: [python]
        pass_filenames: true
```

**Week 2: MyPy Migration**
```yaml
# Replace mirrors-mypy with local Bazel target
```

**Week 3: Standard Hooks**
```yaml
# Create Bazel wrappers for standard pre-commit hooks
```

**Week 4: Cleanup**
```yaml
# Remove all external repository references
# Document new workflow
```

### **Communication Plan**
1. **Announcement**: Email/Slack about migration plan
2. **Documentation**: Update developer guide immediately
3. **Support**: Dedicated channel for questions
4. **Feedback**: Weekly survey on experience

### **Rollback Plan**
- **Conditions**: >3 developers report blocking issues
- **Steps**:
  1. Revert .pre-commit-config.yaml to previous version
  2. Document specific issues encountered
  3. Fix issues before re-attempting
- **Timeline**: Can rollback within 5 minutes

---

## **Review**

### **Review Triggers**
- **Time-based**: After each tool migration completes
- **Event-based**: If any migration fails or stalls
- **Metric-based**: If performance degrades >20%

### **Review Process**
1. **Data gathering**: Survey developers, collect metrics
2. **Analysis**: Compare before/after workflows
3. **Decision**: Continue, adjust, or rollback

---

## **Learning Capture**

### **Expected Outcomes**
- Smooth migration with minimal disruption
- Developers appreciate version consistency
- Pre-commit hooks faster due to Bazel caching
- Clear pattern for future tool integrations

### **Monitoring Plan**
- **Data to collect**: Hook execution times, developer feedback, error rates
- **Frequency**: Daily during migration, weekly after
- **Responsible**: Quality tools service owner

### **Signal Generation**
- **Positive outcomes**: Fast execution → expand Bazel usage
- **Negative outcomes**: Performance issues → optimization needed
- **Unexpected consequences**: Developer workflow improvements

---

## **Notes**

This migration strategy prioritizes stability and developer experience over speed. The staged approach allows us to learn and adapt, ensuring each tool migration is better than the last.

Key success factors:
1. Clear communication at each stage
2. Responsive support for issues
3. Visible benefits (performance, consistency)
4. Easy rollback if needed

The end state will have all pre-commit hooks running through Bazel, providing true single source of truth for all quality tools while maintaining the familiar pre-commit developer experience.
