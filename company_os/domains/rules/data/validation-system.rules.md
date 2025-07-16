---
title: "Rule Set: The Validation System"
version: 1.0
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-15T22:19:00-07:00"
parent_charter: "os/domains/charters/data/maintenance-service.charter.md"
tags: ["rules", "validation", "conformance", "quality", "automation"]
---

# **Rule Set: The Validation System**

This document provides the operational rules for how domain services implement validation capabilities for their document types. These rules operationalize the validation principles defined in the Repository Maintenance Service Charter.

---

## **0. Core Principles (The Mental Model)**

These are the foundational mental models for working with document validation.

* **Rule 0.1: Domain Ownership.** Each domain service owns and implements validation logic for its document types. The Rules Service validates `.rules.md`, the Specs Service would validate `.spec.md`, etc.
* **Rule 0.2: Orchestration, Not Implementation.** The Repository Maintenance Service orchestrates validation across domains but does not perform validation itself. It calls domain services and aggregates results.
* **Rule 0.3: Template-Driven Validation.** Extract validation rules directly from templates to maintain single source of truth.
* **Rule 0.4: Human-in-Loop for Ambiguity.** When automated fixes aren't deterministic, request human input via standardized comments.
* **Rule 0.5: Validation as Intelligence.** Every validation failure is a signal that feeds system improvement.

---

## **1. Rules for Validation Schema Management**

Follow these rules when defining and maintaining validation schemas.

* **Rule 1.1: Schema Source of Truth.** Validation rules must be derived from:
    * Document templates in service `/data/` directories
    * Operational rules in `/os/domains/rules/data/`
    * Charter requirements in `/os/domains/charters/data/`
    * Embedded `_validation` metadata in templates

* **Rule 1.2: Schema Versioning.** Every validation schema must include:
    * **Version**: Semantic version number (e.g., "1.0.0")
    * **Document Type**: The type of document being validated
    * **Last Generated**: Timestamp of schema generation
    * **Source Files**: List of templates/rules used to generate schema

* **Rule 1.3: Field Validation Rules.** For each document field, define:
    * **Required vs Optional**: Explicitly state requirement level
    * **Pattern**: Regex pattern for format validation
    * **Allowed Values**: Enumeration of valid values where applicable
    * **Cross-References**: Whether field values must exist as files

* **Rule 1.4: Section Validation Rules.** For each document section, define:
    * **Required vs Optional**: Whether section must be present
    * **Subsections**: Required nested sections
    * **Minimum Content**: Character or line count requirements
    * **Content Patterns**: Expected content structure

---

## **2. Rules for Validation Execution**

Follow these rules when validating documents.

* **Rule 2.1: Validation Triggers.** Run validation:
    * On pre-commit hooks for changed markdown files
    * When explicitly requested via CLI command
    * During CI/CD pipeline execution
    * When signal threshold indicates validation friction

* **Rule 2.2: Validation Severity Levels.** Classify issues as:
    * **Error**: Document is invalid and must be fixed
    * **Warning**: Document has issues that should be addressed
    * **Info**: Minor improvements possible but not required

* **Rule 2.3: Validation Output.** For each issue found, provide:
    * **Location**: File path and line number
    * **Rule**: Which validation rule was violated
    * **Message**: Clear description of the issue
    * **Suggestion**: How to fix the issue if possible

* **Rule 2.4: Batch Validation.** When validating multiple files:
    * Process all files even if early ones fail
    * Aggregate results by severity and type
    * Generate summary statistics
    * Exit with appropriate error code

---

## **3. Rules for Human Input Requests**

Follow these rules when human intervention is required.

* **Rule 3.1: Standardized Comment Format.** Use this exact format:
```markdown
<!-- HUMAN-INPUT-REQUIRED: [CATEGORY]
Issue: [Specific problem description]
Required Action: [What needs to be done]
Context: [Additional helpful information]
Priority: [high|medium|low]
-->
```

* **Rule 3.2: Human Input Categories.** Valid categories are:
    * **MISSING-CONTENT**: Required section or field is empty
    * **INVALID-REFERENCE**: Referenced file or ID doesn't exist
    * **INCOMPLETE-ANALYSIS**: Content needs more detail
    * **CLARIFICATION-NEEDED**: Ambiguous or unclear content
    * **DECISION-REQUIRED**: Multiple options need human selection
    * **FORMAT-ERROR**: Can't be auto-fixed
    * **REVIEW-NEEDED**: Content complete but needs review

* **Rule 3.3: Comment Placement.** Place comments:
    * Immediately after the problematic content
    * At the top of empty required sections
    * Next to invalid field values in frontmatter
    * Before sections that need expansion

* **Rule 3.4: Comment Lifecycle.** Human input comments:
    * Are added during validation with --fix flag
    * Must be resolved before document is considered valid
    * Are removed when issue is addressed
    * Generate signals if unresolved for > 7 days

---

## **4. Rules for Auto-Fix Capabilities**

Follow these rules for automatic issue remediation.

* **Rule 4.1: Safe Auto-Fixes.** Automatically fix only:
    * **Formatting**: Header hierarchy, list markers, spacing
    * **Frontmatter Order**: Reorder fields to match schema
    * **ID Generation**: Create IDs based on current timestamp
    * **Path Corrections**: Update relative paths for moved files
    * **Trailing Whitespace**: Remove unnecessary spaces
    * **Empty Sections**: Add section headers with human input comments

* **Rule 4.2: Unsafe Operations.** Never auto-fix:
    * **Content Changes**: Modifying actual text content
    * **Field Removal**: Deleting invalid fields
    * **Reference Creation**: Adding references that don't exist
    * **Status Changes**: Modifying document status fields

* **Rule 4.3: Fix Auditing.** For every auto-fix:
    * Log the original content
    * Log the fixed content
    * Record the rule that triggered the fix
    * Generate a signal for pattern analysis

* **Rule 4.4: Fix Verification.** After auto-fixing:
    * Re-validate the document
    * Ensure no new issues were introduced
    * Verify file still parses correctly
    * Check that frontmatter remains valid YAML

---

## **5. Rules for Signal Generation**

Follow these rules for creating validation signals.

* **Rule 5.1: Signal Triggers.** Generate signals when:
    * Same validation error occurs > 10 times
    * New validation pattern emerges
    * Auto-fix patterns indicate template issues
    * Human input requests timeout

* **Rule 5.2: Signal Content.** Validation signals must include:
    * Pattern of validation failures
    * Affected document types
    * Frequency and distribution
    * Suggested template or rule improvements

* **Rule 5.3: Signal Severity.** Set severity based on:
    * **Critical**: Blocks document creation or CI/CD
    * **High**: Affects > 50% of documents of a type
    * **Medium**: Recurring issue affecting productivity
    * **Low**: Minor improvement opportunity

* **Rule 5.4: Brief Generation.** When signals indicate systematic issues:
    * Synthesize related validation signals
    * Create improvement briefs per Brief System Rule 1.6
    * Link to affected templates and rules
    * Propose specific remediation actions

---

## **6. Rules for Integration**

Follow these rules for service integration.

* **Rule 6.1: Rules Service Integration.** Validation must:
    * Read rules from Rules Service when available
    * Sync validation rules to agent-specific directories
    * Update when rules change
    * Generate signals about rule effectiveness

* **Rule 6.2: Template Integration.** When templates change:
    * Re-extract validation rules automatically
    * Notify affected document owners
    * Provide migration guidance
    * Track compliance rates

* **Rule 6.3: CI/CD Integration.** In pipelines:
    * Run validation before merge
    * Block merge on errors (not warnings)
    * Generate reports for review
    * Track validation trends over time

* **Rule 6.4: IDE Integration.** For development environments:
    * Provide real-time validation feedback
    * Show inline error markers
    * Offer quick-fix suggestions
    * Support validation-on-save

---

## **7. Rules for Evolution**

Follow these rules to evolve the validation system.

* **Rule 7.1: Stage Advancement Triggers.**
    * **Stage 0 → 1**: When validation runs exceed 100/week
    * **Stage 1 → 2**: When document count exceeds 1000
    * **Stage 2 → 3**: When cross-repo validation needed
    * **Stage 3 → 4**: When ML-powered validation beneficial

* **Rule 7.2: Validation Rule Evolution.** Rules evolve through:
    * Analysis of validation failure patterns
    * Feedback from document authors
    * Template structure changes
    * New document type introduction

* **Rule 7.3: Performance Monitoring.** Track:
    * Validation execution time
    * Memory usage for large document sets
    * Cache hit rates for repeat validations
    * API response times (Stage 1+)

* **Rule 7.4: Success Metrics.** Measure effectiveness via:
    * Reduction in validation errors over time
    * Decrease in human input requests
    * Increase in auto-fix success rate
    * Time saved through automation

---

## **8. Rules for Cross-Document Validation**

Follow these rules for validating relationships between documents.

* **Rule 8.1: Reference Validation.** Verify that:
    * All linked files exist
    * Referenced IDs match actual documents
    * Cross-references are bidirectional where required
    * Link paths are correct and accessible

* **Rule 8.2: Dependency Validation.** Check that:
    * Parent charters exist for all documents
    * Decision supersession chains are valid
    * Brief implementation links are accurate
    * Signal-to-brief mappings are complete

* **Rule 8.3: Consistency Validation.** Ensure that:
    * Shared metadata matches across related documents
    * Status progressions follow defined rules
    * Dates and timelines are logically consistent
    * Version numbers align with change history

* **Rule 8.4: Graph Integrity.** Maintain:
    * No orphaned documents
    * No circular dependencies
    * Complete traceability chains
    * Valid hierarchy relationships

This validation system serves as the quality assurance layer of the Company OS, ensuring all documents conform to their schemas while generating intelligence about system improvement opportunities.
