---
title: "Rule Set: The Brief System"
version: 1.0
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-14T18:20:32-07:00"
parent_charter: "os/domains/charters/data/evolution-architecture.charter.md"
tags: ["rules", "briefs", "opportunities", "synthesis", "strategy", "intelligence"]
---

# **Rule Set: The Brief System**

This document provides the operational rules for creating, maintaining, and processing opportunity briefs within the Company OS Evolution Architecture. These rules operationalize the intelligence synthesis principles defined in the Evolution Architecture Charter.

---

## **0. Core Principles (The Mental Model)**

These are the foundational mental models for working with opportunity briefs.

* **Rule 0.1: Evidence-Based Opportunities.** Every brief must be grounded in captured signals and concrete evidence, not opinion or speculation.
* **Rule 0.2: Charter Alignment.** All opportunity briefs must align with and reference governing charter principles.
* **Rule 0.3: Actionable Outcomes.** Briefs must define clear, measurable outcomes that can be implemented through projects or decisions.
* **Rule 0.4: Strategic Synthesis.** Briefs synthesize multiple signals into coherent opportunities that serve broader strategic purposes.

---

## **1. Rules for Creating Briefs**

Follow these rules when synthesizing signals into opportunity briefs.

* **Rule 1.1: Brief Generation Triggers.** Create opportunity briefs when:
    * Multiple related signals indicate a systematic issue
    * A single critical signal requires immediate strategic attention
    * Signal patterns align with charter evolution opportunities
    * Sufficient evidence exists to define both problem and solution space

* **Rule 1.2: Complete Brief Metadata.** Every brief MUST include:
    * **Unique ID**: Format `BRIEF-YYYY-MM-DD-NNN` (sequential number for the day)
    * **Brief Type**: `strategic`, `operational`, `tactical`, `technical`
    * **Priority**: `low`, `medium`, `high`, `critical`
    * **Governing Charter**: Reference to primary charter this brief serves
    * **Source Signals**: Links to all signals that contributed to this brief
    * **Strategic Theme**: High-level category or area of focus
    * **Estimated Effort**: `small`, `medium`, `large`, `epic`

* **Rule 1.3: Verify Timestamps.** Before creating briefs, verify current date/time using `date` command per Knowledge System Rule 1.6.

* **Rule 1.4: Problem-Solution Structure.** Every brief must clearly define:
    * **Problem Statement**: What issue or opportunity the brief addresses
    * **Evidence**: Supporting signals and data that validate the problem
    * **Proposed Solution**: High-level approach to addressing the problem
    * **Success Criteria**: How success will be measured
    * **Implementation Approach**: General strategy for execution

* **Rule 1.5: Strategic Alignment.** Briefs must demonstrate:
    * Alignment with governing charter principles
    * Contribution to strategic objectives
    * Impact on system effectiveness
    * Relationship to other briefs and initiatives

---

## **2. Rules for Brief Lifecycle Management**

Follow these rules for managing briefs through their lifecycle.

* **Rule 2.1: Brief Status Progression.** Valid brief statuses:
    * `draft`: Initial creation, under development
    * `review`: Submitted for stakeholder review
    * `approved`: Approved for implementation
    * `active`: Currently being implemented
    * `completed`: Implementation finished successfully
    * `cancelled`: Cancelled before completion
    * `deferred`: Postponed for future consideration

* **Rule 2.2: Status Transitions.** Briefs must move through statuses systematically:
    * `draft` → `review` (when complete and ready for evaluation)
    * `review` → `approved` (when stakeholders approve implementation)
    * `approved` → `active` (when implementation begins)
    * `active` → `completed` (when implementation succeeds)
    * `active` → `cancelled` (when implementation is terminated)
    * Any status → `deferred` (when postponed for future consideration)

* **Rule 2.3: Brief Relationships.** Track brief connections:
    * `source_signals`: Links to signals that contributed to this brief
    * `related_briefs`: Links to other briefs addressing similar themes
    * `implemented_by`: Reference to project or decision implementing this brief
    * `superseded_by`: Reference to newer brief that replaces this one
    * `depends_on`: Reference to other briefs that must be completed first

* **Rule 2.4: Never Delete Briefs.** Briefs are permanent strategic records. Use status changes and archiving instead of deletion.

---

## **3. Rules for Brief Quality**

Follow these rules to ensure brief usefulness for implementation.

* **Rule 3.1: Sufficient Signal Evidence.** Every brief must reference:
    * Minimum 3 related signals (unless single critical signal)
    * Quantitative data when available
    * Specific examples and instances
    * Cross-references to related decisions or projects

* **Rule 3.2: Clear Problem Definition.** Problem statements must be:
    * Specific and concrete, not vague or general
    * Supported by evidence from multiple sources
    * Quantified when possible (time, frequency, impact)
    * Contextual within the broader system architecture

* **Rule 3.3: Actionable Solution Framework.** Solutions must be:
    * Feasible within current system constraints
    * Aligned with charter principles and strategic direction
    * Scalable and maintainable long-term
    * Testable with clear success criteria

* **Rule 3.4: Strategic Context.** Briefs must explain:
    * How this opportunity serves broader strategic goals
    * What charter principles it advances
    * How it connects to other system initiatives
    * What risks it mitigates or creates

---

## **4. Rules for Brief Review and Approval**

Follow these rules for brief evaluation and approval processes.

* **Rule 4.1: Stakeholder Review Process.** Brief reviews must include:
    * Charter alignment assessment
    * Signal evidence validation
    * Solution feasibility analysis
    * Resource requirement evaluation
    * Strategic priority ranking

* **Rule 4.2: Approval Criteria.** Briefs are approved when they:
    * Demonstrate clear charter alignment
    * Show sufficient signal evidence
    * Propose feasible solutions
    * Define measurable success criteria
    * Fit within current resource constraints

* **Rule 4.3: Review Documentation.** All reviews must document:
    * Reviewer feedback and concerns
    * Required changes or improvements
    * Approval or rejection rationale
    * Implementation timeline and dependencies

* **Rule 4.4: Revision Process.** Brief revisions must:
    * Address all reviewer feedback
    * Maintain links to source signals
    * Update version numbers and timestamps
    * Document changes and rationale

---

## **5. Rules for Brief Implementation**

Follow these rules for executing approved opportunity briefs.

* **Rule 5.1: Implementation Planning.** Approved briefs must be:
    * Assigned to appropriate project or decision process
    * Broken down into actionable tasks
    * Scheduled within overall roadmap
    * Allocated necessary resources

* **Rule 5.2: Progress Tracking.** Active briefs must have:
    * Regular status updates
    * Milestone and deliverable tracking
    * Issue and blocker identification
    * Resource utilization monitoring

* **Rule 5.3: Outcome Measurement.** Brief completion must include:
    * Success criteria evaluation
    * Actual vs. expected outcomes
    * Lessons learned documentation
    * New signal generation for future improvement

* **Rule 5.4: Feedback Loop Completion.** Implementation outcomes must:
    * Generate reflection signals about brief effectiveness
    * Create opportunity signals for follow-up improvements
    * Inform future brief creation processes
    * Contribute to strategic theme evolution

---

## **6. Rules for Brief Integration**

Follow these rules for connecting briefs to other system components.

* **Rule 6.1: Project Integration.** Briefs must integrate with projects:
    * Serve as input to project vision documents
    * Provide context for project specifications
    * Define success criteria for project outcomes
    * Generate project retrospective signals

* **Rule 6.2: Decision Integration.** Briefs must integrate with decisions:
    * Provide context for strategic decisions
    * Reference relevant decision records
    * Generate decision outcome signals
    * Inform decision criteria and options

* **Rule 6.3: Charter Integration.** Briefs must integrate with charters:
    * Reference governing charter principles
    * Identify charter evolution opportunities
    * Flag charter conflicts or gaps
    * Contribute to charter effectiveness assessment

* **Rule 6.4: Service Integration.** Briefs must consider service impacts:
    * Identify affected service domains
    * Assess service evolution implications
    * Consider service boundary effects
    * Plan for cross-service coordination

---

## **7. Rules for Strategic Theme Management**

Follow these rules for organizing briefs into strategic themes.

* **Rule 7.1: Theme Definition.** Strategic themes must be:
    * Derived from multiple related briefs
    * Aligned with charter objectives
    * Measurable and time-bound
    * Regularly reviewed and updated

* **Rule 7.2: Theme Organization.** Briefs must be organized into themes:
    * Each brief assigned to primary theme
    * Cross-theme relationships identified
    * Theme priorities established
    * Theme roadmaps maintained

* **Rule 7.3: Theme Evolution.** Strategic themes must evolve:
    * Based on brief implementation outcomes
    * In response to new signal patterns
    * Aligned with charter updates
    * Documented with rationale

* **Rule 7.4: Theme Reporting.** Strategic themes must be reported:
    * Regular progress updates
    * Success metrics tracking
    * Resource utilization analysis
    * Strategic impact assessment

---

## **8. Rules for Brief Evolution**

Follow these rules to evolve the brief system itself.

* **Rule 8.1: Meta-Briefs.** Briefs about the brief system must be captured:
    * Opportunities to improve brief quality
    * Friction with brief creation process
    * Reflections on brief implementation effectiveness
    * Features needed for better brief management

* **Rule 8.2: System Improvement.** Brief system improvements must:
    * Originate from captured meta-signals
    * Be synthesized through the brief generation process
    * Align with evolution architecture principles
    * Generate new signals about their effectiveness

* **Rule 8.3: Process Evolution.** As the system evolves:
    * Update rules based on implementation experience
    * Maintain backward compatibility with existing briefs
    * Document changes and their rationale
    * Train users on new processes and tools

* **Rule 8.4: Quality Metrics.** Track brief system effectiveness:
    * Brief-to-project conversion rates
    * Implementation success rates
    * Signal synthesis quality
    * Strategic alignment scores

This brief system serves as the synthesis layer of the Company OS intelligence cycle, transforming raw signals into actionable strategic opportunities that drive system evolution and improvement.
