---
title: "Workflow: Document Standardization"
version: 1.0
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-17T15:59:58-07:00"
parent_charter: "../charters/data/knowledge-architecture.charter.md"
related_methodology: "../processes/data/synapse.methodology.md"
related_rules: "../rules/data/knowledge-system.rules.md"
tags: ["workflow", "standardization", "documents", "quality", "compliance"]
---

# **Workflow: Document Standardization**

This workflow provides a systematic process for reviewing, standardizing, and ensuring compliance of documents within the Company OS. It can be applied to individual documents, batches of documents, or entire directories.

---

## **Overview**

This workflow transforms documents from various states of compliance into standardized, validated documents that follow Company OS conventions. It combines automated fixes with human input to achieve comprehensive standardization.

### **Input**: Documents requiring standardization
### **Output**: Compliant documents with tracking reports
### **Duration**: 5-30 minutes per document (depending on complexity)

---

## **Phase 1: Document Discovery and Assessment**

### **Step 1.1: Identify Target Documents**

**For Individual Documents:**
```bash
# Single document
target_file="path/to/document.md"
```

**For Batch Processing:**
```bash
# Git commit-based (recommended)
git diff --name-only HEAD~1 HEAD | grep '\.md$' > target_files.txt

# Directory-based
find work/domains/analysis/data -name "*.md" > target_files.txt
```

### **Step 1.2: Initial Compliance Check**

For each target document:
1. **Detect Document Type**: Determine `.type.md` from filename and path
2. **Check Basic Structure**: Verify frontmatter exists and basic markdown structure
3. **Assess Compliance Level**: Quick scan for major issues

**Create Assessment Record:**
```markdown
## Document: [filename]
- Type: [detected_type]
- Current Status: [compliant|minor_issues|major_issues|non_compliant]
- Key Issues: [list of 2-3 main problems]
```

---

## **Phase 2: Standards Application**

### **Step 2.1: Apply Applicable Rules**

1. **Load Document Type Rules**: Reference `knowledge-system.rules.md` for specific type
2. **Load Universal Rules**: Apply rules that affect all documents
3. **Create Compliance Checklist**: Generate specific checklist for this document

**Example Checklist:**
- [ ] Frontmatter present and complete
- [ ] Required fields populated
- [ ] Proper naming convention
- [ ] Consistent formatting
- [ ] Valid cross-references
- [ ] Proper section structure

### **Step 2.2: Identify Fix Categories**

Categorize issues by fix approach:
- **Auto-fixable**: Formatting, timestamps, field ordering
- **Template-based**: Missing sections, standard content
- **Human-required**: Content gaps, invalid references, decision points

---

## **Phase 3: Automated Fixes**

### **Step 3.1: Apply Safe Auto-Fixes**

Execute in order:
1. **Formatting Fixes**:
   - Trailing whitespace removal
   - Consistent list formatting
   - Header spacing
   - Line ending normalization

2. **Frontmatter Fixes**:
   - Add missing required fields with placeholders
   - Correct field ordering
   - Update timestamp formats
   - Generate missing IDs

3. **Structural Fixes**:
   - Add missing sections with placeholders
   - Correct header hierarchy
   - Fix markdown syntax errors

### **Step 3.2: Verify Auto-Fixes**

1. **Re-validate Document**: Run validation after each fix category
2. **Document Changes**: Log all automated changes
3. **Preserve Content**: Ensure no content loss or corruption

**Fix Log Entry:**
```markdown
### Auto-Fix Applied: [timestamp]
- Fix Type: [formatting|frontmatter|structural]
- Issues Fixed: [count]
- Issues Remaining: [count]
- Changes: [specific changes made]
```

---

## **Phase 4: Human Input Integration**

### **Step 4.1: Generate Human Input Comments**

For issues requiring human attention:
1. **Categorize Issue**: Determine comment type (MISSING-CONTENT, DECISION-REQUIRED, etc.)
2. **Create Contextual Comment**: Include specific guidance
3. **Place Strategically**: Position comment near relevant content

**Comment Template:**
```markdown
<!-- HUMAN-INPUT-REQUIRED: [CATEGORY]
Issue: [specific description]
Required Action: [what needs to be done]
Context: [relevant background]
Priority: [high|medium|low]
-->
```

### **Step 4.2: Insert Comments**

1. **Determine Placement**: After relevant content, before sections, or in frontmatter
2. **Insert Comments**: Add to document content
3. **Preserve Structure**: Maintain document readability

---

## **Phase 5: Quality Assurance and Tracking**

### **Step 5.1: Final Validation**

1. **Run Complete Validation**: Use rules service validation
2. **Generate Compliance Report**: Document current state
3. **Identify Remaining Issues**: Catalog what still needs human attention

### **Step 5.2: Create Tracking Record**

**For Individual Documents:**
```markdown
## Standardization Record: [filename]
- **Date**: [timestamp]
- **Initial Status**: [description]
- **Auto-Fixes Applied**: [count and types]
- **Human Input Required**: [count and categories]
- **Final Status**: [compliant|needs_human_input|failed]
- **Next Steps**: [specific actions needed]
```

**For Batch Processing:**
```markdown
## Batch Standardization Report: [batch_name]
- **Total Documents**: [count]
- **Fully Compliant**: [count]
- **Auto-Fixed**: [count]
- **Human Input Required**: [count]
- **Failed**: [count]
- **Summary**: [key findings and patterns]
```

---

## **Phase 6: Follow-up and Monitoring**

### **Step 6.1: Human Input Processing**

When human input is provided:
1. **Parse Responses**: Extract human-provided content
2. **Remove Comments**: Clean up resolved input requests
3. **Re-validate**: Ensure human input resolves issues
4. **Update Tracking**: Mark issues as resolved

### **Step 6.2: Pattern Recognition**

Track patterns across standardization efforts:
- **Common Issues**: What problems appear frequently?
- **Auto-Fix Opportunities**: What manual fixes could be automated?
- **Rule Gaps**: What standards need clarification?
- **Process Improvements**: How can the workflow be enhanced?

---

## **Execution Examples**

### **Single Document Standardization**

```bash
# 1. Start standardization
echo "Standardizing: work/domains/analysis/data/example.analysis.md"

# 2. Check current compliance
company-os validate work/domains/analysis/data/example.analysis.md

# 3. Apply auto-fixes
company-os validate work/domains/analysis/data/example.analysis.md --auto-fix

# 4. Add human input comments if needed
company-os validate work/domains/analysis/data/example.analysis.md --add-comments

# 5. Create tracking record
echo "Standardization completed, tracking record created"
```

### **Git Commit Standardization**

```bash
# 1. Get changed files
changed_files=$(git diff --name-only HEAD~1 HEAD | grep '\.md$')

# 2. Process each file
for file in $changed_files; do
    echo "Processing: $file"
    company-os validate "$file" --auto-fix --add-comments
done

# 3. Generate batch report
echo "Batch standardization completed"
```

---

## **Success Metrics**

- **Compliance Rate**: Percentage of documents meeting standards
- **Auto-Fix Success**: Percentage of issues resolved automatically
- **Human Input Efficiency**: Time to resolve human input requests
- **Pattern Recognition**: Identification of recurring issues
- **Process Improvement**: Workflow optimization over time

---

## **Integration Points**

### **Pre-commit Hook Integration**
```bash
# Standardize changed files before commit
git diff --cached --name-only | grep '\.md$' | xargs -I {} company-os validate {} --auto-fix
```

### **CI/CD Integration**
```yaml
# Continuous standardization monitoring
- name: Document Standardization Check
  run: |
    find . -name "*.md" -newer .last_standardization | \
    xargs -I {} company-os validate {} --report=standardization-report.json
```

### **Regular Maintenance**
```bash
# Weekly standardization sweep
find work/domains -name "*.md" -mtime -7 | \
xargs -I {} company-os validate {} --auto-fix --add-comments
```

---

## **Notes**

### **Workflow Evolution**
This workflow is designed for continuous improvement:
- **Monitor effectiveness** through success metrics
- **Capture signals** about workflow friction or opportunities
- **Evolve standards** based on real usage patterns
- **Automate more** as patterns become clear

### **Human-AI Collaboration**
The workflow balances automation with human judgment:
- **Automate the routine** (formatting, structure)
- **Guide human input** with clear, contextual requests
- **Preserve human expertise** for content and decision-making
- **Learn from patterns** to improve automation

---

*This workflow ensures consistent, high-quality documentation across the Company OS while respecting the balance between automation and human judgment.*
