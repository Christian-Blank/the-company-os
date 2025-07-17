---
title: "Signal: Missing Documentation Standard for Analysis Documents"
type: "signal"
signal_id: "SIG-2025-07-17-001"
signal_type: "opportunity"
severity: "medium"
status: "new"
source: "Document Standardization Workflow Analysis"
context: "Standardizing files from last git commit"
date_captured: "2025-07-17"
related_signals: []
related_decisions: []
related_projects: []
governing_charter: "knowledge-architecture.charter.md"
synthesized_into: ""
implemented_by: ""
tags: ["documentation", "standards", "analysis", "knowledge-system"]
---

# **Signal: Missing Documentation Standard for Analysis Documents**

**Type**: opportunity
**Severity**: medium
**Status**: new
**Source**: Document Standardization Workflow Analysis
**Context**: Standardizing files from last git commit
**Date Captured**: 2025-07-17

---

## **Description**

During the standardization of documents from the last git commit, we discovered a new document type `.analysis.md` that lacks formal documentation standards. While we have clear standards for other document types like `.charter.md`, `.rules.md`, and `.brief.md`, analysis documents have emerged organically without explicit rules.

### **What Happened**
Found `system-primitives.analysis.md` without proper frontmatter and no documented standard for the `.analysis.md` document type in our knowledge-system rules.

### **When & Where**
Discovered during the document standardization workflow while reviewing files from git commit HEAD on 2025-07-17.

### **Impact & Implications**
- Analysis documents may be created inconsistently across the system
- Validation tools cannot properly check analysis documents
- New contributors lack guidance on how to create analysis documents
- Automation and tooling cannot handle this document type

---

## **Evidence & Examples**

### **Specific Examples**
- Example 1: `work/domains/analysis/data/system-primitives.analysis.md` - Created without frontmatter
- Example 2: `work/domains/analysis/data/document-standardization-workflow.analysis.md` - Created with proposed standard
- Example 3: Other analysis documents in the system follow different patterns

### **Supporting Data**
- Frequency: Analysis documents are created for major system explorations and decision-making
- Duration: Takes ~10 minutes to manually standardize each document
- Impact: Affects all analysis documentation creation and maintenance

### **Related Documentation**
- `company_os/domains/rules/data/knowledge-system.rules.md`: Current documentation rules (missing analysis type)
- `work/domains/analysis/data/document-standardization-workflow.analysis.md`: Proposed standard

---

## **Analysis**

### **Root Cause**
Analysis documents emerged as a need to explore complex topics before formal decisions or implementations, but we didn't anticipate this document type when creating initial standards.

### **Potential Solutions**
1. Add `.analysis.md` standard to knowledge-system.rules.md
2. Create analysis-specific validation rules
3. Update rules service to handle analysis documents
4. Create template for analysis documents

### **Charter Alignment**
This aligns with Knowledge Architecture Charter's principle of "making implicit knowledge explicit" - we need explicit standards for all document types.

---

## **Relationships**

### **Related Signals**
- Will relate to SIG-2025-07-17-002 (other missing document types)

### **Connected Systems**
- Knowledge system rules
- Rules service validation
- Documentation templates

### **Dependencies**
- Requires update to knowledge-system.rules.md
- May require rules service code changes

---

## **Notes**

Proposed minimal standard for `.analysis.md` files:
```yaml
---
title: "Analysis: [Descriptive Title]"
version: 1.0
status: "Draft|Active|Superseded"
owner: "[Team or Individual]"
last_updated: "YYYY-MM-DDTHH:MM:SS-TZ:00"
parent_charter: "[relevant charter]"
tags: ["analysis", "relevant", "tags"]
---
```

Purpose: Analytical documents that explore problems, propose solutions, or synthesize information for decision-making.
