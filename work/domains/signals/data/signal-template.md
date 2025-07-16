---
title: "Signal: [Brief descriptive title]"
type: "signal"
signal_id: "SIG-YYYY-MM-DD-NNN"
signal_type: "friction|opportunity|reflection|feature|exploration"
severity: "low|medium|high|critical"
status: "new"
source: "[who or what generated this signal]"
context: "[project/task/process where this originated]"
date_captured: "YYYY-MM-DD"
related_signals: ["links to related signals if any"]
related_decisions: ["links to decisions if this came from decision outcomes]"
related_projects: ["links to projects if this emerged from project work]"
governing_charter: "[path to relevant charter if applicable]"
synthesized_into: "[brief ID when incorporated into opportunity brief]"
implemented_by: "[project/decision ID when addressed]"
tags: ["relevant", "categorization", "tags"]
---

# **Signal: [Brief descriptive title]**

**Type**: [friction|opportunity|reflection|feature|exploration]
**Severity**: [low|medium|high|critical]
**Status**: [new|reviewed|clustered|synthesized|implemented|archived]
**Source**: [who or what generated this signal]
**Context**: [project/task/process where this originated]
**Date Captured**: [YYYY-MM-DD]

---

## **Description**

[Provide a clear, detailed description of the signal. Be specific about what happened, when it occurred, and why it matters. Include concrete examples.]

### **What Happened**
[Describe the specific situation, event, or observation that triggered this signal]

### **When & Where**
[Specify the context - during which project, task, or process this occurred]

### **Impact & Implications**
[Explain why this matters - what is the effect or potential effect on the system, team, or outcomes]

---

## **Evidence & Examples**

### **Specific Examples**
[Provide concrete, specific examples of this signal in action:]
- Example 1: [Detailed description]
- Example 2: [Detailed description]
- Example 3: [Detailed description]

### **Supporting Data**
[Include any quantitative data, metrics, or measurements that support this signal:]
- Frequency: [How often this occurs]
- Duration: [How long this takes or affects work]
- Impact: [Measurable effect on time, quality, or outcomes]

### **Related Documentation**
[Link to any relevant documents, code, decisions, or other signals:]
- [Link 1]: [Brief description]
- [Link 2]: [Brief description]
- [Link 3]: [Brief description]

---

## **Analysis**

### **Root Cause**
[If known, describe what you believe is the underlying cause of this signal]

### **Potential Solutions**
[If you have ideas for how this could be addressed, describe them briefly]

### **Charter Alignment**
[Explain how this signal relates to our charter principles - does it support or conflict with them?]

---

## **Relationships**

### **Related Signals**
[List any other signals that are related to this one]

### **Connected Systems**
[Identify which service domains, processes, or charters this signal affects]

### **Dependencies**
[Note any dependencies - other signals, projects, or decisions that relate to this one]

---

## **Notes**

[Any additional context, thoughts, or information that doesn't fit in the above sections]

---

**Instructions for Using This Template:**

1. **Before creating**: Run `date` command to verify current timestamp
2. **Signal ID**: Use format SIG-YYYY-MM-DD-NNN (sequential for the day)
3. **Be specific**: Avoid vague language; provide concrete details and examples
4. **Include context**: Someone unfamiliar with the situation should understand from your description
5. **Link extensively**: Reference related signals, decisions, projects, and charters
6. **Choose appropriate severity**: Consider impact on work, team, and charter alignment
7. **Follow rules**: Adhere to all rules in `signal-system.rules.md`

**Signal Types:**
- **friction**: Problems, blockers, inefficiencies, pain points
- **opportunity**: Potential improvements, new capabilities, enhancements
- **reflection**: Insights, lessons learned, post-completion analysis
- **feature**: Specific functionality requests, capability needs
- **exploration**: Ideas to investigate, experiments to try, questions to answer

**Severity Guidelines:**
- **critical**: Blocks work, causes significant delays, threatens charter alignment
- **high**: Regular friction, affects multiple people, prevents optimization
- **medium**: Occasional friction, affects few people, minor efficiency impact
- **low**: Rare friction, minimal impact, nice-to-have improvement
