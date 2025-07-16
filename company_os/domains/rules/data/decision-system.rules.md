---
title: "Rule Set: The Decision System"
version: 1.0
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-14T17:51:24-07:00"
parent_charter: "os/domains/charters/data/knowledge-architecture.charter.md"
tags: ["rules", "decisions", "governance", "evolution", "deterministic", "adr"]
---

# **Rule Set: The Decision System**

This document provides the operational rules for creating, maintaining, and evolving decision records within the Company OS. These rules operationalize the decision record principles in the knowledge architecture charter and ensure deterministic system understanding.

---

## **0. Core Principles (The Mental Model)**

These are the foundational mental models for working with decision records.

* **Rule 0.1: Every Decision is Traceable.** All significant decisions must be captured with full context, rationale, and consequences to enable deterministic system understanding.
* **Rule 0.2: Decisions Enable Evolution.** Decision records are not just documentation but active components of the self-evolving system that generate learning signals.
* **Rule 0.3: Context is King.** The "why" behind decisions is more important than the "what" - capture all signals, constraints, and assumptions.
* **Rule 0.4: Decisions are Living Documents.** They can be superseded, but never deleted - the history of decision evolution is critical system knowledge.

---

## **1. Rules for Creating Decision Records**

Follow these rules when documenting decisions.

* **Rule 1.1: Unique Decision IDs.** Every decision must have a unique identifier using the format `DEC-YYYY-MM-DD-NNN` where NNN is a zero-padded sequential number for that day.
    * *Example:* `DEC-2025-07-14-001`
* **Rule 1.2: Complete Context Capture.** Every decision record MUST include:
    * **Triggering Signals**: Links to all signal records that led to this decision
    * **Problem Statement**: Clear articulation of the issue being addressed
    * **Constraints**: Technical, business, philosophical, or resource constraints
    * **Assumptions**: What was believed to be true at decision time
    * **Environment State**: System version, dependencies, team composition
* **Rule 1.3: Options Analysis Required.** Document at least 2 options with:
    * Detailed description of each option
    * Pros and cons analysis
    * Estimated effort/impact
    * Risk assessment
    * Clear rationale for selection
* **Rule 1.4: Consequences Documentation.** Specify:
    * **Immediate Impact**: What changes right away
    * **Long-term Effects**: What this enables or prevents
    * **Success Metrics**: How effectiveness will be measured
    * **Review Triggers**: Conditions that would cause reconsideration
* **Rule 1.5: Verify Timestamps.** Before creating decision records, verify current date/time using `date` command per Knowledge System Rule 1.6.

---

## **2. Rules for Decision Lifecycle**

Follow these rules for managing decision evolution.

* **Rule 2.1: Decision Status Management.** Valid statuses are:
    * `proposed`: Decision under consideration
    * `accepted`: Decision approved and active
    * `deprecated`: No longer recommended but not forbidden
    * `superseded`: Replaced by a newer decision (must link to replacement)
* **Rule 2.2: Supersession Process.** When replacing a decision:
    * Create new decision record with full context
    * Update old decision status to `superseded`
    * Add `superseded_by` field linking to new decision
    * Add `supersedes` field in new decision linking to old one
* **Rule 2.3: Never Delete Decisions.** Decision records are permanent system knowledge. Use status changes and supersession instead.
* **Rule 2.4: Regular Review Cycles.** Active decisions should be reviewed:
    * When review triggers are met
    * During quarterly system evolution cycles
    * When related signals indicate friction

---

## **3. Rules for Integration with Learning Loops**

Follow these rules for connecting decisions to the Double Learning Loop.

* **Rule 3.1: Signal Integration.** Decision records must:
    * Reference originating signals in the `context` section
    * Generate new signals about implementation outcomes
    * Link to related opportunity briefs when applicable
* **Rule 3.2: Project Integration.** When decisions are made during project execution:
    * Link to the relevant project document
    * Reference the decision in project documentation
    * Use decision outcomes to generate project signals
* **Rule 3.3: Charter Alignment.** Every decision must:
    * Reference the governing charter
    * Demonstrate alignment with charter principles
    * Note any charter conflicts requiring resolution
* **Rule 3.4: Evolution Feedback.** Decision effectiveness must:
    * Be measured against stated success metrics
    * Generate signals for system improvement
    * Inform future similar decisions

---

## **4. Rules for Deterministic Rebuilding**

Follow these rules to enable system reconstruction.

* **Rule 4.1: Environment Documentation.** Capture complete system state:
    * Software versions and dependencies
    * Team composition and roles
    * External factors affecting the decision
    * Market or organizational context
* **Rule 4.2: Decision Trees.** Document the logical path:
    * How signals led to opportunity identification
    * How options were generated and evaluated
    * What criteria were used for selection
    * What alternatives were rejected and why
* **Rule 4.3: Implementation Path.** Specify:
    * Exact steps taken to implement the decision
    * Tools and processes used
    * Timelines and milestones
    * Rollback procedures if needed
* **Rule 4.4: Learning Capture.** Record outcomes:
    * What worked as expected
    * What didn't work as expected
    * Unexpected consequences (positive and negative)
    * Lessons learned for future decisions

---

## **5. Rules for Decision Record Format**

Follow these rules for consistent structure.

* **Rule 5.1: Required Frontmatter Fields:**
    ```yaml
    title: "Decision: [Brief descriptive title]"
    type: "decision"
    decision_id: "DEC-YYYY-MM-DD-NNN"
    status: "proposed|accepted|deprecated|superseded"
    date_proposed: "YYYY-MM-DD"
    date_decided: "YYYY-MM-DD"
    deciders: ["list of people/agents"]
    parent_charter: "[governing charter path]"
    related_signals: ["signal file paths"]
    related_brief: "[brief file path if applicable]"
    related_project: "[project file path if applicable]"
    supersedes: "[previous decision id if replacing]"
    superseded_by: "[new decision id if replaced]"
    tags: ["relevant", "topic", "tags"]
    ```
* **Rule 5.2: Required Content Sections:**
    1. **Context** - Problem, signals, constraints, assumptions
    2. **Options Considered** - All alternatives with analysis
    3. **Decision** - Selected option and rationale
    4. **Consequences** - Impact analysis and success metrics
    5. **Implementation** - Action items and timeline
    6. **Review** - Conditions for reconsideration
* **Rule 5.3: File Naming Convention.** Use format: `DEC-YYYY-MM-DD-NNN-brief-description.decision.md`

---

## **6. Rules for System Evolution**

Follow these rules to evolve the decision system itself.

* **Rule 6.1: Meta-Decisions.** Decisions about the decision system must follow all decision rules and be marked with tag `meta-decision`.
* **Rule 6.2: Template Evolution.** Changes to decision record format require:
    * Signal identifying need for change
    * Decision record documenting the format change
    * Migration plan for existing records
    * Update to this rule set
* **Rule 6.3: Integration Evolution.** As the system evolves beyond Stage 0:
    * Decision APIs must preserve full context
    * Database schemas must capture all required metadata
    * External integrations must maintain decision traceability
