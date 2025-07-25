---
title: "Decision: Implement Bazel-Based Quality Tools Integration"
type: "decision"
decision_id: "DEC-2025-07-24-004"
status: "accepted"
date_proposed: "2025-07-24"
date_decided: "2025-07-24"
deciders: ["Christian Blank", "Cline AI"]
parent_charter: "company_os/domains/charters/data/service-architecture.charter.md"
related_signals: ["DEVELOPMENT_TEST_PLAN.md failures for Bazel ruff/mypy targets"]
related_brief: ""
related_project: "work/domains/projects/data/bazel-quality-tools-integration.vision.md"
supersedes: ""
superseded_by: ""
tags: ["bazel", "quality-tools", "ruff", "mypy", "single-source-of-truth", "architecture"]
---

# **Decision: Implement Bazel-Based Quality Tools Integration**

**Status**: accepted
**Decision ID**: DEC-2025-07-24-004
**Date Decided**: 2025-07-24
**Deciders**: Christian Blank, Cline AI

---

## **Context**

### **Problem Statement**
The Company OS currently manages code quality tools (ruff, mypy) through two separate systems: uv pip dependencies in requirements.in -> requirements_lock.txt and external pre-commit repositories. This violates our single source of truth principle and creates version drift risks. Additionally, Bazel targets for these tools (`//:ruff`, `//:mypy`) are missing, causing test failures and preventing hermetic builds.

### **Triggering Signals**
From DEVELOPMENT_TEST_PLAN.md:
- **Signal 1**: "ERROR: no such target '//:ruff' - Bazel target not configured"
- **Signal 2**: "ERROR: no such target '//:mypy' - Bazel target not configured"
- **Signal 3**: Pre-commit using external repos (ruff-pre-commit v0.12.5, mirrors-mypy v1.17.0) instead of Bazel

### **Constraints**
- **Technical**: Must work with Bazel 8.x + bzlmod, Python 3.12, existing hexagonal architecture
- **Resource**: Single developer bandwidth, must be implementable incrementally
- **Business**: Should be done in one shot to avoid accidental complexity or drift.
- **Philosophical**: Must follow "single source of truth" and "hermetic builds" principles

### **Assumptions**
- Bazel py_binary can effectively wrap Python tools
- Performance overhead of Bazel wrapping is acceptable
- Developers are willing to adopt Bazel-based commands
- Tool configurations can be centralized in the repository

### **Environment State**
- **System Version**: Bazel 8.3.1, Python 3.12, UV for dependency management
- **Team Composition**: Mixed experience levels with Bazel
- **External Factors**: Industry trend toward hermetic, reproducible builds
- **Dependencies**: ruff, mypy already in requirements_lock.txt

---

## **Options Considered**

### **Option A**: Create Quality Tools Service with Bazel Wrappers
**Description**: Build a new service following hexagonal architecture that wraps quality tools as Bazel targets

**Pros**:
- Follows established Company OS patterns
- Single source of truth for tool versions
- Hermetic, reproducible execution
- Leverages Bazel caching
- Extensible to new tools

**Cons**:
- Initial implementation effort
- Learning curve for team
- Potential performance overhead

**Estimated Effort**: 20-30 complexity points
**Risk Assessment**: Low - proven pattern in Company OS

### **Option B**: Direct Bazel Rules Without Service
**Description**: Create Bazel rules directly in root BUILD.bazel without service structure

**Pros**:
- Simpler initial implementation
- Less code to maintain
- Direct tool access

**Cons**:
- Violates service architecture principles
- Harder to extend and maintain
- No clear ownership boundary
- Limited reusability

**Estimated Effort**: 10-15 complexity points
**Risk Assessment**: Medium - creates technical debt

### **Option C**: Keep External Pre-commit Repos
**Description**: Continue using external pre-commit repositories, accept missing Bazel targets

**Pros**:
- No implementation effort
- Familiar to developers
- Pre-commit ecosystem benefits

**Cons**:
- Violates single source of truth
- Version drift risk
- No hermetic builds
- Test failures continue

**Estimated Effort**: 0 complexity points
**Risk Assessment**: High - accumulating technical debt

### **Option D**: Custom Starlark Rules
**Description**: Write custom Starlark rules for each tool

**Pros**:
- Maximum flexibility
- Deep Bazel integration
- Potential for optimization

**Cons**:
- High complexity
- Requires Starlark expertise
- Maintenance burden
- Reinventing existing solutions

**Estimated Effort**: 50+ complexity points
**Risk Assessment**: High - over-engineering

---

## **Decision**

### **Selected Option**: Option A - Create Quality Tools Service with Bazel Wrappers

### **Rationale**
The Quality Tools Service approach was selected because:

1. **Architectural Consistency**: Follows established hexagonal architecture patterns already proven in rules_service and source_truth_enforcement
2. **Single Source of Truth**: Eliminates dual management of tool versions between pip and pre-commit
3. **Hermetic Builds**: Provides reproducible execution environment across all contexts
4. **Extensibility**: Easy to add new tools (black, isort, bandit) following the same pattern
5. **Team Familiarity**: Developers already understand the service structure from other domains

The approach balances implementation complexity with long-term maintainability and aligns with Company OS principles.

### **Charter Alignment**
This decision directly supports:
- **Service Architecture Charter**: Clean boundaries, evolution stages, single responsibility
- **Repository Architecture Charter**: Proper domain organization and dependencies
- **Company OS Manifesto**: "Single source of truth" and "Evolution on demand"

---

## **Consequences**

### **Immediate Impact**
- New quality_tools service domain created
- Bazel targets `//:ruff` and `//:mypy` become available
- Pre-commit hooks updated to use Bazel commands
- All quality tool tests pass in DEVELOPMENT_TEST_PLAN.md

### **Long-term Effects**
- **Enables**: Consistent tool versions across all environments
- **Prevents**: Version drift between development and CI
- **Creates**: Foundation for advanced quality analytics
- **Simplifies**: Developer onboarding (no tool installation needed)

### **Success Metrics**
- **Functional**: 100% of quality tool Bazel targets operational
- **Performance**: <5 second incremental check time
- **Adoption**: 100% developer adoption within 2 weeks
- **Reliability**: Zero version-related issues in 30 days

### **Risk Mitigation**
- **Risk**: Performance degradation → **Mitigation**: Leverage Bazel caching, profile bottlenecks
- **Risk**: Developer resistance → **Mitigation**: Clear documentation, training, parallel operation
- **Risk**: Migration issues → **Mitigation**: Phased rollout, maintain backward compatibility

---

## **Implementation**

### **Action Items**

1. **Create Quality Tools Service Structure**
   - **Owner**: Cline AI
   - **Timeline**: Day 1
   - **Dependencies**: None

2. **Implement Bazel Wrappers**
   - **Owner**: Cline AI
   - **Timeline**: Day 1-2
   - **Dependencies**: Service structure

3. **Add Root-level Aliases**
   - **Owner**: Cline AI
   - **Timeline**: Day 2
   - **Dependencies**: Bazel wrappers

4. **Update Pre-commit Configuration**
   - **Owner**: Cline AI
   - **Timeline**: Day 2
   - **Dependencies**: Working Bazel targets

5. **Create ci/cd Workflow**
   - **Owner**: Cline AI
   - **Timeline**: Day 2
   - **Dependencies**: Working Bazel targets

6. **Documentation and Testing**
   - **Owner**: Christian Blank
   - **Timeline**: Day 3
   - **Dependencies**: All implementation complete

### **Implementation Path**
1. Create `company_os/domains/quality_tools/` directory structure
2. Implement py_binary wrappers for ruff and mypy
3. Add root BUILD.bazel aliases pointing to service targets
4. Update .pre-commit-config.yaml to use Bazel commands
5. Run full test suite to verify functionality
6. Remove external pre-commit repositories

### **Rollback Plan**
- **Conditions**: Critical issues blocking development
- **Steps**:
  1. Revert .pre-commit-config.yaml to external repos
  2. Keep Bazel targets for gradual migration
  3. Document issues for resolution
- **Preservation**: Maintain service structure for future attempt

---

## **Review**

### **Review Triggers**
- **Time-based**: Review after 30 days of production use
- **Event-based**: Review if new quality tools need integration
- **Metric-based**: Review if performance degrades >20%

### **Review Process**
1. **Data gathering**: Collect performance metrics, developer feedback
2. **Analysis**: Assess adoption rate, issue frequency, performance impact
3. **Decision**: Optimize, maintain, or consider alternative approaches

---

## **Learning Capture**

### **Expected Outcomes**
- Unified tool management reducing maintenance burden
- Improved developer experience with consistent tooling
- Foundation for advanced quality metrics and automation
- Blueprint for integrating other development tools

### **Monitoring Plan**
- **Data to collect**: Build times, cache hit rates, tool execution times
- **Frequency**: Weekly metrics review
- **Responsible**: Platform team lead

### **Signal Generation**
- **Positive outcomes**: Fast adoption → opportunity for more tool integration
- **Negative outcomes**: Performance issues → friction signal for optimization
- **Unexpected consequences**: Monitor for Bazel/tool incompatibilities

---

## **Notes**

This decision establishes a pattern for integrating any command-line development tool into the Bazel ecosystem. The quality tools service can serve as a reference implementation for future tool integrations.

The phased approach allows for gradual migration without disrupting current workflows, following the Company OS principle of "evolution on demand."

Future considerations include integrating security scanners (bandit, safety), documentation generators (sphinx), and custom Company OS-specific linting rules.
