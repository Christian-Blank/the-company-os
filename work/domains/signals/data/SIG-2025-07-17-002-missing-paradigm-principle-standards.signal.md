---
title: "Signal: Missing Documentation Standards for Paradigm and Principle Documents"
type: "signal"
signal_id: "SIG-2025-07-17-002"
signal_type: "opportunity"
severity: "medium"
status: "new"
source: "Document Standardization Workflow Analysis"
context: "Standardizing files from last git commit"
date_captured: "2025-07-17"
related_signals: ["SIG-2025-07-17-001"]
related_decisions: []
related_projects: []
governing_charter: "knowledge-architecture.charter.md"
synthesized_into: ""
implemented_by: ""
tags: ["documentation", "standards", "paradigm", "principle", "knowledge-system"]
---

# **Signal: Missing Documentation Standards for Paradigm and Principle Documents**

**Type**: opportunity
**Severity**: medium
**Status**: new
**Source**: Document Standardization Workflow Analysis
**Context**: Standardizing files from last git commit
**Date Captured**: 2025-07-17

---

## **Description**

While reviewing the last git commit, we discovered two new document types that have been introduced but lack formal documentation standards in our knowledge-system rules: `.paradigm.md` and `.principle.md`. These document types have clear examples and are already being used effectively, but their standards are not explicitly documented.

### **What Happened**
Found well-formed `.paradigm.md` and `.principle.md` documents with proper frontmatter, but these document types are not mentioned in `knowledge-system.rules.md` or any other rules documentation.

### **When & Where**
Discovered during the document standardization workflow while reviewing files from git commit HEAD on 2025-07-17, specifically in the new `paradigms/` and `principles/` directories.

### **Impact & Implications**
- Future paradigm and principle documents may deviate from established patterns
- Validation tools cannot verify these document types
- The knowledge-system rules are incomplete
- Developers lack official guidance for creating these important document types

---

## **Evidence & Examples**

### **Specific Examples**
- Example 1: `company_os/domains/paradigms/data/system-archetypes.paradigm.md` - Well-formed with clear pattern
- Example 2: `company_os/domains/principles/data/dual-flow.principle.md` - Follows consistent structure
- Example 3: Both README files clearly explain the purpose of these document types

### **Supporting Data**
- Frequency: Paradigm and principle documents are foundational but created rarely
- Duration: High-value documents requiring significant thought and review
- Impact: These documents guide all other system decisions

### **Related Documentation**
- `company_os/domains/paradigms/README.md`: Explains paradigm documents
- `company_os/domains/principles/README.md`: Explains principle documents
- `company_os/domains/rules/data/knowledge-system.rules.md`: Missing these types

---

## **Analysis**

### **Root Cause**
These document types were created to fill specific architectural needs (deep conceptual models and detailed principle explanations) but the formal rules weren't updated to reflect these new archetypes.

### **Potential Solutions**
1. Add `.paradigm.md` and `.principle.md` standards to knowledge-system.rules.md
2. Document the clear patterns already established
3. Update file naming conventions to include these types
4. Ensure rules service can validate these documents

### **Charter Alignment**
Directly supports Knowledge Architecture Charter's goal of explicit knowledge management and clear document organization.

---

## **Relationships**

### **Related Signals**
- SIG-2025-07-17-001: Missing analysis document standard (similar issue)

### **Connected Systems**
- Knowledge system rules
- Document validation systems
- System architecture documentation

### **Dependencies**
- Should be addressed alongside other missing document types
- May require coordinated update to rules and validation

---

## **Notes**

Observed patterns for these document types:

**`.paradigm.md`**:
- Title format: "Paradigm: [Concept Name]"
- Purpose: Foundational mental models and conceptual frameworks
- Structure: Abstract concepts, analogies, deep explanations

**`.principle.md`**:
- Title format: "Principle: [Principle Name]"
- Purpose: Detailed explanations of First Principles stated in charters
- Structure: Definition, problem solved, implementation guidance

Both types already follow the standard frontmatter pattern, making formalization straightforward.
