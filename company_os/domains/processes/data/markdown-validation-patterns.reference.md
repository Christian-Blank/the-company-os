---
title: "Reference: Markdown Validation Patterns"
version: 1.0
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-15T23:05:00-07:00"
parent_workflow: "os/domains/processes/data/markdown-validation.workflow.md"
related_rules: "os/domains/rules/data/validation-system.rules.md"
tags: ["reference", "validation", "markdown", "patterns", "schemas"]
---

# **Reference: Markdown Validation Patterns**

This reference document provides detailed validation patterns, schema definitions, and examples for the markdown validation workflow.

---

## **1. Document Type Detection Patterns**

### **1.1 Filename Patterns**

| Document Type | Pattern | Example |
|--------------|---------|---------|
| Decision | `*.decision.md` | `DEC-2025-07-15-001-core-adapter.decision.md` |
| Brief | `*.brief.md` | `BRIEF-2025-07-15-001-rules-service.brief.md` |
| Signal | `*.signal.md` | `SIG-2025-07-15-001-tech-stack.signal.md` |
| Vision | `*.vision.md` | `process_engine.vision.md` |
| Charter | `*.charter.md` | `rules-service.charter.md` |
| Rules | `*.rules.md` | `validation-system.rules.md` |
| Workflow | `*.workflow.md` | `markdown-validation.workflow.md` |
| Methodology | `*.methodology.md` | `synapse.methodology.md` |
| Registry | `*.registry.md` | `services.registry.md` |
| Template | `*-template.md` | `brief-template.md` |

### **1.2 Path-Based Detection**

| Path Pattern | Document Category | Validation Focus |
|-------------|------------------|------------------|
| `/work/domains/decisions/` | Decisions | ID format, status flow, alternatives |
| `/work/domains/briefs/` | Briefs | Objectives, deliverables, constraints |
| `/work/domains/signals/` | Signals | Trigger events, impact analysis |
| `/os/domains/charters/` | Charters | Purpose, ownership, evolution |
| `/os/domains/rules/` | Rules | Operational constraints, enforcement |

---

## **2. Frontmatter Validation Patterns**

### **2.1 Required Fields by Document Type**

#### **Decision Documents**
```yaml
id: "DEC-YYYY-MM-DD-NNN-slug"  # Format: DEC-{date}-{sequence}-{slug}
title: "Decision: {Topic}"       # Must start with "Decision:"
status: enum["Proposed", "Accepted", "Superseded", "Deprecated"]
impact: enum["Low", "Medium", "High", "Critical"]
owner: string                    # Must match registry
last_updated: ISO8601           # YYYY-MM-DDTHH:MM:SS-07:00
tags: array[string]             # At least one required
```

#### **Brief Documents**
```yaml
id: "BRIEF-YYYY-MM-DD-NNN-slug"
title: "Brief: {Topic}"
status: enum["Draft", "In Progress", "Completed", "Cancelled"]
priority: enum["P0", "P1", "P2", "P3"]
owner: string
target_date: ISO8601
estimated_effort: string        # Format: "Nd" or "Nw"
actual_effort: string          # Optional, same format
```

### **2.2 Cross-Reference Validation**

| Field | Validation Rule | Example |
|-------|----------------|---------|
| `parent_*` | Must exist in filesystem | `parent_charter: "os/domains/charters/data/rules-service.charter.md"` |
| `related_*` | Must exist or be external URL | `related_rules: ["../rules/validation.rules.md"]` |
| `owner` | Must exist in services.registry.md | `owner: "OS Core Team"` |
| `implements` | Must reference existing decision | `implements: "DEC-2025-07-15-002"` |

---

## **3. Content Structure Patterns**

### **3.1 Section Requirements**

#### **Decision Document Sections**
- **Context**: Required, min 50 words
- **Decision**: Required, clear statement
- **Consequences**: Required, positive and negative
- **Alternatives Considered**: Required if impact >= "High"
- **Implementation Notes**: Optional

#### **Brief Document Sections**
- **Objectives**: Required, numbered list
- **Context**: Required
- **Deliverables**: Required, measurable items
- **Constraints**: Required
- **Success Criteria**: Required, testable

### **3.2 Section Order Validation**

```
Expected Order for Decisions:
1. Frontmatter
2. Title (H1)
3. Context (H2)
4. Decision (H2)
5. Consequences (H2)
6. Alternatives Considered (H2) - if required
7. Implementation Notes (H2) - if present
```

---

## **4. Link and Reference Validation**

### **4.1 Internal Link Patterns**

| Link Type | Pattern | Validation |
|-----------|---------|------------|
| Relative File | `../category/file.md` | File must exist |
| Anchor Link | `#section-name` | Anchor must exist in target |
| Combined | `file.md#section` | Both file and anchor must exist |

### **4.2 External Link Validation**

- **HTTP/HTTPS URLs**: Check response code (200-299 = valid)
- **Domain Allowlist**: Optionally restrict to approved domains
- **Redirect Handling**: Follow up to 3 redirects

---

## **5. Formatting Validation Patterns**

### **5.1 Header Hierarchy**

```
Valid:
# Title (H1) - Only one allowed
## Section (H2)
### Subsection (H3)

Invalid:
# Title
### Subsection (H3) - Skipped H2
## Section
# Another Title - Multiple H1s
```

### **5.2 List Formatting**

```
Valid Unordered:
- Item 1
- Item 2
  - Nested item
  - Another nested

Valid Ordered:
1. First item
2. Second item
   1. Nested
   2. Another nested

Invalid:
- Item 1
 - Wrong indentation (1 space)
* Mixed markers in same list
- Item 2
```

### **5.3 Code Block Validation**

```
Valid:
```language
code here
```

Invalid:
```
code without language specifier
```

``` language
space before language
```
```

---

## **6. Content Quality Patterns**

### **6.1 Insufficient Detail Detection**

| Pattern | Issue Type | Example |
|---------|-----------|---------|
| Section < 20 words | `INSUFFICIENT-DETAIL` | "Context: We need to fix this." |
| Bullet points only | `INCOMPLETE-ANALYSIS` | No paragraph explanation |
| Missing rationale | `MISSING-CONTENT` | Decision without "why" |
| Vague language | `CLARIFICATION-NEEDED` | "various", "multiple", "etc" |

### **6.2 Completeness Checks**

- **TODOs and Placeholders**: `TODO:`, `TBD`, `[placeholder]`
- **Missing Dates**: `last_updated: TBD`
- **Empty Sections**: `## Deliverables\n\n## Next Section`
- **Incomplete Lists**: Lists ending with "..."

---

## **7. Human Input Comment Categories**

### **7.1 Category Definitions**

| Category | When to Use | Example Scenario |
|----------|-------------|------------------|
| `MISSING-CONTENT` | Required field/section empty | Empty "Alternatives" section |
| `INVALID-REFERENCE` | Broken link or reference | Link to non-existent file |
| `INCOMPLETE-ANALYSIS` | Content too brief | 10-word decision rationale |
| `CLARIFICATION-NEEDED` | Ambiguous content | Unclear technical terms |
| `DECISION-REQUIRED` | Multiple valid options | Which format to use |
| `FORMAT-ERROR` | Complex structural issue | Nested list formatting |
| `REVIEW-NEEDED` | Content requires expertise | Technical accuracy check |

### **7.2 Comment Placement Rules**

1. **After Content**: Place after the problematic line/section
2. **Before Section**: For missing sections, place before next section
3. **In Frontmatter**: For frontmatter issues, place as YAML comment
4. **End of File**: For document-wide issues

---

## **8. Auto-Fix Patterns**

### **8.1 Safe Formatting Fixes**

| Issue | Fix Pattern | Example |
|-------|------------|---------|
| Trailing whitespace | Remove all `\s+$` | `line   ` → `line` |
| Multiple blank lines | Replace `\n{3,}` with `\n\n` | 3+ blanks → 2 blanks |
| Header spacing | Ensure blank line before/after | Add missing blank lines |
| List marker consistency | Standardize to `-` | `* item` → `- item` |

### **8.2 Frontmatter Fixes**

| Issue | Fix Pattern | Safety |
|-------|------------|---------|
| Field order | Reorder to schema | Safe |
| Date format | Convert to ISO8601 | Safe |
| Missing ID | Generate from title+date | Safe with verification |
| Case normalization | Lowercase enums | Safe |

### **8.3 Path Fixes**

| Issue | Fix Pattern | Example |
|-------|------------|---------|
| Absolute → Relative | Convert `/os/` to `../../../os/` | Based on current location |
| Backslash → Forward | Replace `\` with `/` | Windows path fix |
| Missing extension | Add `.md` if exists | `../file` → `../file.md` |

---

## **9. Validation Severity Guidelines**

### **9.1 Error Level Issues**
- Missing required frontmatter fields
- Invalid document structure
- Broken internal links
- Malformed frontmatter
- Missing required sections

### **9.2 Warning Level Issues**
- Suboptimal formatting
- External link timeouts
- Near-minimum content length
- Missing optional fields
- Inconsistent style

### **9.3 Info Level Issues**
- Style preferences
- Optimization opportunities
- Migration suggestions
- Best practice reminders

---

## **10. Schema Evolution Patterns**

### **10.1 Version Migration**

When document schemas change:
1. Detect schema version from frontmatter
2. Apply migration rules in sequence
3. Update version after successful migration
4. Log all changes for review

### **10.2 Backwards Compatibility**

- Support last 2 major versions
- Provide migration warnings
- Auto-upgrade when safe
- Request human input for breaking changes

---

This reference provides the detailed patterns needed to implement comprehensive markdown validation while maintaining consistency across the Company OS documentation system.
