---
title: "Decision: Time-Independent Metrics for Asynchronous Systems"
version: 1.0
status: "Active"
owner: "OS Core Team"
decision_id: "DEC-2025-07-14-003"
decision_type: "architectural"
urgency: "high"
last_updated: "2025-07-14T19:00:19-07:00"
parent_charter: "os/domains/charters/data/company-os.charter.md"
affected_services: ["signals", "briefs", "projects", "evolution"]
stakeholders: ["OS Core Team", "Project Teams", "AI Agents"]
tags: ["metrics", "asynchronous", "distributed", "time-independent", "deterministic"]
---

# **Decision: Time-Independent Metrics for Asynchronous Systems**

**Decision ID**: DEC-2025-07-14-003
**Type**: Architectural
**Status**: Active
**Urgency**: High
**Date**: 2025-07-14

---

## **Summary**

This decision establishes the principle of using time-independent metrics throughout the Company OS, recognizing that in a deterministic asynchronous distributed system, time is merely an expression of available resources rather than a fundamental measure.

### **Decision**
Replace time-based measurements with deterministic, resource-based metrics except where time directly measures system performance (latency, timeouts).

### **Outcome**
A measurement system that scales with available resources and remains deterministic regardless of execution context.

---

## **Context**

### **Background**
The Company OS is designed as a deterministic asynchronous distributed system where:
- Work can be executed by humans or AI agents
- Resources can scale from one person to thousands of agents
- Work can pause and resume without losing context
- The same task might take days or minutes depending on resources

Currently, we use time-based measurements in several places:
- Signal synthesis reviews (weekly/biweekly/monthly)
- Brief effort estimates (weeks/months)
- Project timelines and milestones
- Review cycles and schedules

### **Problem Statement**
Time-based measurements create false constraints and expectations:
- A "2-week" task might take 2 days with 10 agents
- A "weekly" review might be too frequent with low activity
- A "monthly" cycle might be too slow with high volume
- Time estimates become meaningless without resource context

### **Constraints**
- Some time measurements remain valid (system latency, timeouts)
- Must maintain compatibility with human expectations
- Need clear alternative metrics that are understandable
- Transitions must be gradual and well-documented

---

## **Decision Drivers**

### **Key Factors**
1. **Resource Variability**: Available resources change dramatically
2. **Async Nature**: Work happens when resources are available
3. **Determinism**: Need predictable, reproducible processes
4. **Scale Independence**: Metrics should work at any scale

### **Philosophical Alignment**
This aligns with Company OS First Principles:
- **Process-First**: Define what, not when
- **Effectiveness as Truth**: Measure outcomes, not time spent
- **Self-Evolution**: Adapt to actual needs, not schedules

---

## **Options Considered**

### **Option 1: Keep Time-Based Metrics**
**Description**: Continue using weeks/months/days as primary measurements.
- **Pros**: Familiar to humans, simple to understand
- **Cons**: Meaningless in async context, creates false expectations
- **Decision**: Not selected - fundamentally incompatible with async systems

### **Option 2: Hybrid Time/Resource Metrics**
**Description**: Use both time and resource measurements together.
- **Pros**: Gradual transition, maintains familiarity
- **Cons**: Complexity, potential confusion, half-measure
- **Decision**: Not selected - adds complexity without solving core issue

### **Option 3: Resource-Based Metrics (Selected)**
**Description**: Replace time with resource/complexity/volume-based metrics.
- **Pros**: Accurate, scalable, deterministic, honest
- **Cons**: Requires mindset shift, new measurement systems
- **Decision**: Selected - aligns with system architecture

---

## **Decision Details**

### **Metric Replacements**

1. **Signal Processing**:
   - **Old**: Review signals weekly/biweekly/monthly
   - **New**: Review when signal count reaches threshold (e.g., 10 new signals)
   - **New**: Review when critical signals are captured
   - **New**: Review when pattern density suggests opportunity

2. **Brief Effort Estimates**:
   - **Old**: Small (1-2 weeks), Medium (1-2 months), etc.
   - **New**: Complexity points (1-5, 5-20, 20-100, 100+)
   - **New**: Resource units (person-days as capability measure)
   - **New**: Dependency depth (standalone, few deps, many deps)

3. **Review Cycles**:
   - **Old**: Weekly standup, monthly planning
   - **New**: Friction-triggered reviews
   - **New**: Milestone-based checkpoints
   - **New**: Signal-threshold reviews

4. **Project Planning**:
   - **Old**: Gantt charts with dates
   - **New**: Dependency graphs with complexity
   - **New**: Resource allocation models
   - **New**: Outcome-based milestones

### **Where Time Remains Valid**

Time measurements remain appropriate for:
- **System Performance**: API latency, response times
- **Timeouts**: Connection timeouts, processing limits
- **Decay Functions**: Cache expiry, token refresh
- **Legal/Compliance**: Audit periods, retention policies
- **Human Constraints**: Meeting durations, work hours

### **Implementation Principles**

1. **Event-Driven Triggers**: Replace scheduled reviews with event triggers
2. **Volume-Based Thresholds**: Use quantity not time for batch processing
3. **Complexity Estimation**: Measure inherent difficulty not duration
4. **Resource Scaling**: Express capacity not calendar time
5. **Outcome Focus**: Measure completion not elapsed time

---

## **Consequences**

### **Benefits**
- Honest representation of work requirements
- Scales naturally with available resources
- No false urgency from arbitrary deadlines
- Better resource allocation decisions
- True async operation enablement

### **Risks & Mitigations**
- **Risk**: Human confusion with new metrics
- **Mitigation**: Clear documentation and examples

- **Risk**: Loss of predictability for planning
- **Mitigation**: Resource-based predictions more accurate

- **Risk**: Integration with external time-based systems
- **Mitigation**: Adapters at system boundaries

### **Trade-offs**
- Requires re-education of all participants
- Initial complexity in transitioning
- May feel less "natural" to humans initially
- Need new tools for measurement

---

## **Implementation Plan**

### **Immediate Actions**
1. Update Signal System Rules to use signal-count triggers
2. Update Brief System Rules to use complexity points
3. Update Brief Template effort estimation section
4. Create conversion guide for existing measurements

### **Phased Rollout**
1. **Phase 1**: Update rules and templates
2. **Phase 2**: Educate teams on new metrics
3. **Phase 3**: Transition active work to new metrics
4. **Phase 4**: Develop tooling for new measurements

### **Validation Steps**
1. Test signal review with count-based triggers
2. Estimate existing briefs in complexity points
3. Compare accuracy of new vs old estimates
4. Gather feedback from early adopters

---

## **Review & Learning**

### **Review Schedule**
- After 10 briefs estimated with new system
- After 50 signals processed with new triggers
- When first project completes under new metrics

### **Success Metrics**
- Estimation accuracy improvement
- Resource utilization efficiency
- Reduction in deadline-driven stress
- Increase in async work patterns

### **Learning Capture**
This fundamental shift in thinking about time will generate many signals about what works and what doesn't. Each learning should refine our understanding of resource-based metrics.

---

## **References**

### **Related Decisions**
- [DEC-2025-07-14-001](DEC-2025-07-14-001-decision-record-structure.decision.md): Established decision record pattern
- [DEC-2025-07-14-002](DEC-2025-07-14-002-llm-context-maintenance.decision.md): Example of event-driven process

### **Governing Documents**
- [Company OS Charter](../../../os/domains/charters/data/company-os.charter.md): First principles alignment
- [Evolution Architecture Charter](../../../os/domains/charters/data/evolution-architecture.charter.md): Intelligence cycle design

### **Affected Documents**
- [Signal System Rules](../../../os/domains/rules/data/signal-system.rules.md): Rule 5.1 needs update
- [Brief System Rules](../../../os/domains/rules/data/brief-system.rules.md): Effort estimates need update
- [Brief Template](../../../work/domains/briefs/data/brief-template.md): Timeline sections need revision

---

## **Appendices**

### **Appendix A: Metric Conversion Guide**

| Old (Time-Based) | New (Resource-Based) | Rationale |
|------------------|---------------------|-----------|
| 1-2 weeks | 5-10 complexity points | Based on task complexity |
| 1-2 months | 20-50 complexity points | Includes integration effort |
| Weekly review | Every 10 signals | Volume-driven trigger |
| Monthly planning | Every 5 completed briefs | Outcome-driven trigger |

### **Appendix B: Complexity Point Guidelines**

**1 Point**: Single file change, no dependencies, clear specification
**5 Points**: Multiple files, few dependencies, some ambiguity
**20 Points**: New service/feature, many dependencies, exploration needed
**100 Points**: Major architectural change, extensive coordination

### **Appendix C: Example Transformations**

**Before**: "Review signals every Monday at 10am"
**After**: "Review signals when 10 new or 1 critical received"

**Before**: "This project will take 3 months"
**After**: "This project is 150 complexity points, requiring 3 senior engineers or equivalent"

**Before**: "Brief review cycle is 2 weeks"
**After**: "Brief review triggered by stakeholder availability and readiness"
