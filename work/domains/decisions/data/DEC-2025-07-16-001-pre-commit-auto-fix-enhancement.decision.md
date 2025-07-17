---
title: "Decision: Post-commit Auto-fix with Signal Intelligence"
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
tags: ["post-commit", "validation", "automation", "git-workflow", "signal-intelligence", "developer-experience"]
---

# **Decision: Post-commit Auto-fix with Signal Intelligence**

**Status**: accepted
**Decision ID**: DEC-2025-07-16-001
**Date Decided**: 2025-07-16
**Deciders**: Christian Blank, Cline AI

---

## **Context**

### **Problem Statement**
The pre-commit validation hook was failing due to path resolution issues and the attempted pre-commit staging approach had technical limitations. More importantly, auto-fixes represent valuable signal intelligence about systemic documentation quality issues that should be captured and analyzed for continuous improvement rather than hidden in complex staging workflows.

### **Triggering Signals**
- **Path Resolution Failure**: Hook couldn't find files like `docs/developers/contributing.md`
- **Pre-commit Staging Complexity**: Universal auto-fix hook had git staging failures and technical debt
- **Missed Intelligence Opportunity**: Auto-fix patterns contain valuable signals about quality issues
- **Signal Intelligence Alignment**: Need to transform workflow problems into intelligence opportunities

### **Constraints**
- **Technical**: Must work within Bazel build system's execution context
- **Workflow**: Cannot break existing pre-commit hook behavior
- **Developer Experience**: Must provide clear feedback about auto-fixes
- **Signal Quality**: Must generate actionable intelligence about documentation patterns
- **Non-blocking**: Original commits must never fail due to auto-fix issues

### **Assumptions**
- Developers prefer non-blocking workflows over complex staging manipulation
- Signal intelligence about auto-fix patterns is more valuable than immediate staging
- Post-commit auto-fix commits provide better traceability than staging
- Pattern analysis can drive proactive quality improvements

### **Environment State**
- **Bazel Version**: 8.3.1 with bzlmod
- **Pre-commit Framework**: Active with rules-service hooks
- **Build System**: Running CLI through Bazel in sandboxed environment
- **Git Workflow**: Feature branch development with pre-commit validation
- **Signal Intelligence**: Active signal generation and analysis framework

---

## **Options Considered**

### **Option A**: Fix Pre-commit Staging Approach
**Description**: Debug and fix the universal auto-fix hook's staging failures

**Pros**:
- Preserves single-commit workflow
- Immediate auto-fix application
- Builds on existing implementation

**Cons**:
- Complex git staging manipulation in pre-commit context
- Technical debt and maintenance burden
- Misses signal intelligence opportunity
- Blocking failures impact developer workflow

**Estimated Effort**: 10 complexity points
**Risk Assessment**: High - git staging complexity in pre-commit context

### **Option B**: Post-commit Auto-fix with Signal Intelligence (Selected)
**Description**: Move auto-fix handling to post-commit with signal generation

**Pros**:
- Non-blocking original commits (100% success rate)
- Clean separation of concerns (user changes vs auto-fixes)
- Rich signal intelligence about quality patterns
- Better traceability with separate auto-fix commits
- Aligns with signal intelligence methodology

**Cons**:
- Two commits instead of one
- Requires post-commit hook setup
- New architecture to implement

**Estimated Effort**: 20 complexity points
**Risk Assessment**: Medium - new architecture but cleaner approach

### **Option C**: Manual Auto-fix Workflow
**Description**: Remove automatic staging, require manual handling of auto-fixes

**Pros**:
- Simple implementation
- Developer control over auto-fixes
- No technical complexity

**Cons**:
- Returns to original workflow friction
- Manual steps easy to forget
- No signal intelligence generation
- Defeats automation purpose

**Estimated Effort**: 2 complexity points
**Risk Assessment**: Low - but defeats the purpose

---

## **Decision**

### **Selected Option**: Option B - Post-commit Auto-fix with Signal Intelligence

### **Rationale**
The post-commit approach transforms auto-fixes from a workflow problem into a signal intelligence opportunity. This aligns with the Company OS methodology of extracting intelligence from operational patterns. The non-blocking nature ensures developer workflow reliability while the signal generation enables proactive quality improvements.

### **Charter Alignment**
- **Knowledge Architecture Charter**: Supports "Documentation as Code" with intelligent quality feedback
- **Rules Service Charter**: Enhances validation capabilities with signal-driven insights
- **Signal Intelligence**: Transforms auto-fixes into valuable pattern detection
- **Developer Experience**: Provides reliable, non-blocking workflow

---

## **Architecture**

### **Post-commit Flow**
```
1. Developer: git commit -m "feature change"
2. Pre-commit hooks run (auto-fixes applied, not staged)
3. Original commit succeeds with user changes only
4. Post-commit hook detects auto-fixes via git diff
5. Auto-commit created: "Auto-fix: trailing whitespace in 3 files"
6. Signal generated if patterns detected (e.g., same file fixed 3+ times)
7. Signal routed to intelligence system for analysis
```

### **Signal Intelligence Integration**
- **Pattern Detection**: Files repeatedly needing same auto-fixes
- **Trend Analysis**: Auto-fix frequency over time by file, hook, developer
- **Root Cause Signals**: Systemic issues requiring process/tooling changes
- **Prevention Opportunities**: Training, documentation, or rule improvements

---

## **Implementation**

### **Technical Components**

#### **Post-commit Auto-fix Detector**
```python
class PostCommitAutoFixDetector:
    def detect_auto_fixes(self) -> List[AutoFixEvent]
    def create_auto_fix_commit(self, fixes: List[AutoFixEvent]) -> bool
    def generate_signals(self, fixes: List[AutoFixEvent]) -> List[Signal]
    def analyze_patterns(self, fixes: List[AutoFixEvent]) -> PatternAnalysis
```

**Detection Strategy**:
- Use `git diff HEAD~1` to compare pre/post hook states
- Categorize changes by hook type and file patterns
- Create descriptive auto-fix commits with affected files
- Generate structured signals for intelligence analysis

#### **Signal Generator**
```python
class AutoFixSignalGenerator:
    def track_auto_fix_event(self, event: AutoFixEvent) -> None
    def check_signal_thresholds(self) -> List[Signal]
    def generate_pattern_signals(self) -> List[Signal]
    def create_signal_document(self, pattern: Pattern) -> Signal
```

**Signal Types**:
1. **High-frequency Auto-fix Signal**: Same file auto-fixed 3+ times in 7 days
2. **Hook Effectiveness Signal**: Hook consistently needed across many files
3. **Developer Pattern Signal**: Individual auto-fix patterns indicating training needs
4. **Systemic Issue Signal**: Project-wide auto-fix trends indicating process issues

#### **Git Hook Integration**
```bash
#!/bin/sh
# .git/hooks/post-commit
bazel run //company_os/domains/rules_service/adapters/post_commit:auto_fix_detector
```

### **Data Storage and Analytics**
- **File**: `.rules-service/auto-fix-history.json`
- **Format**: Structured events with timestamps, files, hooks, commits
- **Retention**: 30 days detailed data, 1 year aggregated patterns
- **Analytics**: CLI commands for trend analysis and reporting

---

## **Migration Plan**

### **Phase 1: Implementation (Milestone 8)**
1. **Create post-commit auto-fix detector system**
2. **Implement signal generation and intelligence integration**
3. **Add analytics CLI for auto-fix pattern analysis**
4. **Test post-commit system thoroughly**

### **Phase 2: Cleanup and Migration**
1. **Remove universal auto-fix hook from pre-commit chain**
2. **Clean up BUILD files and dependencies**
3. **Update documentation to reflect new workflow**
4. **Deploy post-commit system project-wide**

### **Phase 3: Intelligence Integration**
1. **Integrate with broader signal intelligence dashboard**
2. **Train teams on signal interpretation and action**
3. **Establish improvement workflows based on signals**
4. **Monitor and refine signal thresholds**

---

## **Success Metrics**

### **Technical Metrics**
- **Commit Success Rate**: 100% (auto-fixes never block commits)
- **Post-commit Execution Time**: < 1 second average
- **Signal Accuracy**: 95% of generated signals are actionable
- **Pattern Detection Rate**: 80% of recurring issues identified

### **Developer Experience Metrics**
- **Developer Satisfaction**: Survey feedback on new workflow
- **Auto-fix Awareness**: Developers understand auto-fix commits
- **Workflow Reliability**: Zero commit failures due to auto-fix issues

### **Intelligence Metrics**
- **Signal Quality**: 90% of signals lead to actionable improvements
- **Root Cause Prevention**: 30% reduction in repeat auto-fixes after interventions
- **Trend Analysis**: Accurate forecasting of auto-fix patterns
- **Signal Utilization**: Teams actively respond to generated signals

---

## **Signal Generation Strategy**

### **Threshold Definitions**
- **High-frequency File**: Same file auto-fixed 3+ times in 7 days
- **Hook Effectiveness**: Hook triggered on 10+ files in 24 hours
- **Developer Pattern**: Individual with 5+ auto-fixes of same type in 3 days
- **Systemic Issue**: Project-wide auto-fix increase of 50% week-over-week

### **Signal Formats**
```yaml
# Example High-frequency Auto-fix Signal
signal_id: "SIG-2025-07-16-002-frequent-autofix-readme"
type: "high_frequency_autofix"
severity: "medium"
file_path: "docs/README.md"
hook_type: "trailing-whitespace"
frequency: 5
period: "7_days"
recommendation: "Review editing workflow or add pre-save hooks"
```

### **Intelligence Integration**
- **Signal Routing**: Auto-fix signals routed to signal intelligence dashboard
- **Pattern Analysis**: Machine learning for trend prediction and root cause analysis
- **Action Recommendations**: Automated suggestions for process improvements
- **Feedback Loops**: Track improvement effectiveness post-intervention

---

## **Risk Mitigation**

### **Risk 1: Post-commit Hook Reliability**
- **Mitigation**: Robust error handling, fallback detection, monitoring
- **Monitoring**: Track hook execution success rates and performance

### **Risk 2: Signal Quality and Noise**
- **Mitigation**: Careful threshold tuning, signal validation, feedback loops
- **Monitoring**: Track signal utilization rates and developer feedback

### **Risk 3: Developer Adoption**
- **Mitigation**: Clear communication, training, gradual rollout
- **Monitoring**: Survey developer satisfaction and workflow understanding

### **Risk 4: Two-commit Workflow Confusion**
- **Mitigation**: Clear commit messages, documentation, IDE integration
- **Monitoring**: Track developer questions and support requests

---

## **Future Enhancements**

### **Advanced Intelligence**
- **Machine Learning**: Pattern prediction and anomaly detection
- **Cross-repository Analysis**: Organization-wide auto-fix trends
- **Predictive Analytics**: Forecast quality issues before they occur

### **Developer Tools**
- **IDE Integration**: Real-time auto-fix feedback in editors
- **Dashboard**: Visual auto-fix analytics and trends
- **Notifications**: Proactive alerts for high-frequency patterns

### **Process Integration**
- **Code Review**: Auto-fix pattern awareness in PR reviews
- **CI/CD**: Build-time auto-fix analysis and reporting
- **Training**: Automated suggestions for developer skill development

---

## **Rollback Plan**

### **Conditions for Rollback**
- Post-commit hook reliability < 90%
- Developer satisfaction significantly decreases
- Signal generation creates excessive noise
- Performance impact exceeds acceptable thresholds

### **Rollback Steps**
1. **Disable post-commit hook system**
2. **Preserve core validation functionality**
3. **Document lessons learned and improvement opportunities**
4. **Plan alternative approach based on learnings**

### **Data Preservation**
- **Signal History**: Maintain all generated signals for analysis
- **Pattern Data**: Preserve auto-fix patterns for future intelligence
- **Performance Metrics**: Keep execution and reliability data

---

## **Learning Outcomes**

### **Expected Benefits**
- **Non-blocking Workflow**: 100% commit success rate
- **Signal Intelligence**: Rich data about documentation quality patterns
- **Proactive Improvement**: Root cause identification and prevention
- **Developer Experience**: Clear, reliable auto-fix handling

### **Knowledge Capture**
- **Auto-fix Patterns**: Which issues occur most frequently
- **Process Insights**: Where documentation workflow can improve
- **Tool Effectiveness**: Which hooks provide most value
- **Training Needs**: Individual and team skill development opportunities

---

*This decision transforms auto-fixes from a technical challenge into a valuable intelligence source, enabling continuous improvement and proactive quality management while ensuring reliable, non-blocking developer workflows.*
