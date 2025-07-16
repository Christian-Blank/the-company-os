---
title: "Decision: [Brief descriptive title]"
type: "decision"
decision_id: "DEC-YYYY-MM-DD-NNN"
status: "proposed"
date_proposed: "YYYY-MM-DD"
date_decided: "YYYY-MM-DD"
deciders: ["person or agent names"]
parent_charter: "[path to governing charter]"
related_signals: ["paths to signal records that triggered this decision"]
related_brief: "[path to opportunity brief if applicable]"
related_project: "[path to project if applicable]"
supersedes: "[previous decision id if replacing an existing decision]"
superseded_by: "[new decision id if this decision is later replaced]"
tags: ["relevant", "topic", "tags"]
---

# **Decision: [Brief descriptive title]**

**Status**: [proposed|accepted|deprecated|superseded]
**Decision ID**: [DEC-YYYY-MM-DD-NNN]
**Date Decided**: [YYYY-MM-DD]
**Deciders**: [List of people/agents involved]

---

## **Context**

### **Problem Statement**
[Clear articulation of the issue, opportunity, or challenge being addressed]

### **Triggering Signals**
[Links to all signal records that led to this decision. Explain how the signals relate to the problem.]

### **Constraints**
[Document all constraints affecting the decision:]
- **Technical**: [Technology limitations, dependencies, etc.]
- **Resource**: [Time, budget, personnel constraints]
- **Business**: [Policy, regulatory, strategic constraints]
- **Philosophical**: [Charter principles that must be maintained]

### **Assumptions**
[What we believe to be true at the time of this decision:]
- [Assumption 1]
- [Assumption 2]
- [etc.]

### **Environment State**
[Capture the complete system state at decision time:]
- **System Version**: [Current repository state, relevant software versions]
- **Team Composition**: [Who is involved, their roles and capabilities]
- **External Factors**: [Market conditions, organizational context, deadlines]
- **Dependencies**: [What other systems, decisions, or projects this depends on]

---

## **Options Considered**

### **Option A**: [Name/Description]
**Description**: [Detailed explanation of this approach]

**Pros**:
- [Advantage 1]
- [Advantage 2]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]

**Estimated Effort**: [Time, resources, complexity]
**Risk Assessment**: [What could go wrong, likelihood, impact]

### **Option B**: [Name/Description]
[Same structure as Option A]

### **Option C**: [Additional options as needed]
[Same structure as above]

---

## **Decision**

### **Selected Option**: [Which option was chosen]

### **Rationale**
[Detailed explanation of why this option was selected over the others. Reference specific criteria, constraints, and trade-offs that influenced the choice.]

### **Charter Alignment**
[Explain how this decision aligns with governing charter principles. Note any conflicts that needed resolution.]

---

## **Consequences**

### **Immediate Impact**
[What changes right away as a result of this decision:]
- [Change 1]
- [Change 2]

### **Long-term Effects**
[What this decision enables or prevents in the future:]
- **Enables**: [New capabilities, opportunities]
- **Prevents**: [Paths that are now closed off]
- **Creates**: [New dependencies, requirements]

### **Success Metrics**
[How we will measure whether this decision was effective:]
- [Metric 1]: [Target/threshold]
- [Metric 2]: [Target/threshold]

### **Risk Mitigation**
[How we will address identified risks:]
- **Risk**: [Description] → **Mitigation**: [How we'll handle it]

---

## **Implementation**

### **Action Items**
[Specific tasks required to implement this decision:]

1. **[Action Item 1]**
   - **Owner**: [Who is responsible]
   - **Timeline**: [When this should be completed]
   - **Dependencies**: [What needs to happen first]

2. **[Action Item 2]**
   [Same structure]

### **Implementation Path**
[Detailed steps for implementation:]
1. [Step 1 with specifics]
2. [Step 2 with specifics]
3. [etc.]

### **Rollback Plan**
[How to undo this decision if needed:]
- [Conditions that would trigger rollback]
- [Steps to reverse the implementation]
- [What data/state needs to be preserved for rollback]

---

## **Review**

### **Review Triggers**
[Conditions that would cause us to reconsider this decision:]
- [Time-based]: Review after [specific time period]
- [Event-based]: Review when [specific condition occurs]
- [Metric-based]: Review if [specific metric threshold]

### **Review Process**
[How the review will be conducted:]
1. [Step 1: Data gathering]
2. [Step 2: Analysis]
3. [Step 3: Decision on whether to maintain, modify, or supersede]

---

## **Learning Capture**

### **Expected Outcomes**
[What we expect to happen as a result of this decision]

### **Monitoring Plan**
[How we will track the effectiveness of this decision:]
- [Data to collect]
- [Frequency of monitoring]
- [Who is responsible for monitoring]

### **Signal Generation**
[How outcomes of this decision will feed back into the system:]
- [Positive outcomes that should be captured as signals]
- [Negative outcomes that should be captured as signals]
- [Unexpected consequences to watch for]

---

## **Notes**

[Any additional context, references, or information that doesn't fit in the above sections]

---

**Instructions for Using This Template:**

1. **Before creating**: Run `date` command to verify current timestamp
2. **Decision ID**: Use format DEC-YYYY-MM-DD-NNN (sequential for the day)
3. **Complete all sections**: Even if some seem not applicable, explain why
4. **Link extensively**: Reference all related signals, briefs, projects, charters
5. **Be specific**: Avoid vague language; provide concrete details
6. **Think deterministically**: Someone should be able to reconstruct this decision from the record
7. **Follow rules**: Adhere to all rules in `decision-system.rules.md`
