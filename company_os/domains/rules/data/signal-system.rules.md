---
title: "Rule Set: The Signal System"
version: 1.1
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-14T19:00:19-07:00"
parent_charter: "os/domains/charters/data/evolution-architecture.charter.md"
tags: ["rules", "signals", "intelligence", "capture", "synthesis", "meta-loop"]
---

# **Rule Set: The Signal System**

This document provides the operational rules for capturing, maintaining, and processing signals within the Company OS Evolution Architecture. These rules operationalize the signal collection principles defined in the Evolution Architecture Charter.

---

## **0. Core Principles (The Mental Model)**

These are the foundational mental models for working with signals.

* **Rule 0.1: Capture Everything, Lose Nothing.** Any insight, friction, opportunity, or reflection should be captured as a signal. It is better to capture too much than to lose valuable intelligence.
* **Rule 0.2: Atomic Signals.** Each signal should contain exactly one insight, problem, or opportunity. Complex issues should be broken into multiple related signals.
* **Rule 0.3: Context is Critical.** Signals without sufficient context cannot be synthesized effectively. Always include the full situation, constraints, and environment.
* **Rule 0.4: Signals Are Living Documents.** Signals evolve through their lifecycle from capture to synthesis to action. Their status and relationships change over time.

---

## **1. Rules for Creating Signals**

Follow these rules when capturing any type of signal.

* **Rule 1.1: Universal Signal Types.** Every signal must be categorized as one of five types:
    * **friction**: Problems, blockers, inefficiencies, or pain points
    * **opportunity**: Potential improvements, new capabilities, or enhancements
    * **reflection**: Insights, lessons learned, or post-completion analysis
    * **feature**: Specific functionality requests or capability needs
    * **exploration**: Ideas to investigate, experiments to try, or questions to answer

* **Rule 1.2: Complete Signal Metadata.** Every signal MUST include:
    * **Unique ID**: Format `SIG-YYYY-MM-DD-NNN` (sequential number for the day)
    * **Signal Type**: One of the five universal types
    * **Severity/Priority**: `low`, `medium`, `high`, `critical`
    * **Source**: Who or what generated this signal
    * **Context**: Where/when this signal originated (project, task, process)
    * **Detailed Description**: Full explanation of the signal with examples
    * **Supporting Evidence**: Links to relevant documents, decisions, or outcomes

* **Rule 1.3: Verify Timestamps.** Before creating signals, verify current date/time using `date` command per Knowledge System Rule 1.6.

* **Rule 1.4: Link Extensively.** Signals should reference:
    * Related signals (if this builds on or connects to other signals)
    * Originating decisions (if this signal comes from decision outcomes)
    * Relevant projects (if this signal emerged from project work)
    * Governing charters (if this signal relates to charter principles)

* **Rule 1.5: Provide Examples.** Concrete examples make signals more actionable:
    * For friction: Specific instances when the problem occurred
    * For opportunities: Specific improvements that could be made
    * For reflections: Specific lessons learned and their implications
    * For features: Specific use cases and user stories
    * For explorations: Specific hypotheses or questions to investigate

---

## **2. Rules for Signal Lifecycle Management**

Follow these rules for managing signals through their lifecycle.

* **Rule 2.1: Signal Status Progression.** Valid signal statuses:
    * `new`: Recently captured, awaiting review
    * `reviewed`: Examined during synthesis review
    * `clustered`: Grouped with related signals for analysis
    * `synthesized`: Incorporated into an opportunity brief
    * `implemented`: Addressed through project or decision
    * `archived`: Determined not actionable or no longer relevant

* **Rule 2.2: Status Transitions.** Signals must move through statuses systematically:
    * `new` → `reviewed` (during synthesis review)
    * `reviewed` → `clustered` (when grouped with related signals)
    * `clustered` → `synthesized` (when incorporated into brief)
    * `synthesized` → `implemented` (when addressed by project)
    * Any status → `archived` (when determined not actionable)

* **Rule 2.3: Signal Relationships.** Track signal connections:
    * `related_signals`: Links to signals addressing similar issues
    * `synthesized_into`: Reference to opportunity brief this signal contributed to
    * `implemented_by`: Reference to project or decision that addressed this signal
    * `superseded_by`: Reference to newer signal that replaces this one

* **Rule 2.4: Never Delete Signals.** Signals are permanent intelligence records. Use status changes and archiving instead of deletion.

---

## **3. Rules for Signal Quality**

Follow these rules to ensure signal usefulness for synthesis.

* **Rule 3.1: Sufficient Context.** Every signal must contain enough information for someone unfamiliar with the situation to understand:
    * What exactly happened or was observed
    * When and where it occurred
    * Who was involved or affected
    * What the impact or implications are

* **Rule 3.2: Specific and Actionable.** Avoid vague signals:
    * Instead of "Documentation is confusing" → "The decision record template lacks examples for the 'consequences' section"
    * Instead of "Process is slow" → "Signal synthesis review takes 2+ hours due to manual signal clustering"
    * Instead of "We need better tools" → "Header validation requires manual checking, causing inconsistent frontmatter"

* **Rule 3.3: Evidence-Based.** Support signals with concrete evidence:
    * Links to specific documents, code, or decisions
    * Quantitative data when available (time, frequency, impact)
    * Specific examples or instances
    * References to related signals or decisions

* **Rule 3.4: Appropriate Severity.** Assign severity based on:
    * **critical**: Blocks work, causes significant delays, or threatens charter alignment
    * **high**: Causes regular friction, affects multiple people, or prevents optimization
    * **medium**: Occasional friction, affects few people, or minor efficiency impact
    * **low**: Rare friction, minimal impact, or nice-to-have improvement

---

## **4. Rules for Signal Capture Integration**

Follow these rules for integrating signal capture with other processes.

* **Rule 4.1: Decision Outcome Signals.** Every decision implementation must generate at least one signal:
    * Friction signals for unexpected problems or blockers
    * Reflection signals for lessons learned or insights gained
    * Opportunity signals for improvements identified during implementation

* **Rule 4.2: Project Completion Signals.** Every project completion must generate reflection signals:
    * What worked well and should be repeated
    * What didn't work and should be avoided
    * What could be improved for future projects
    * What new capabilities or tools are needed

* **Rule 4.3: Daily Work Signals.** Encourage continuous signal capture:
    * Set up low-friction capture mechanisms
    * Capture signals immediately when friction occurs
    * Don't wait for formal reviews to capture insights
    * Use templates or shortcuts to speed capture

* **Rule 4.4: Signal Clustering.** Related signals should be explicitly linked:
    * Identify signals addressing the same underlying issue
    * Link signals that could be addressed by the same solution
    * Group signals by theme, domain, or affected service
    * Maintain cluster metadata for synthesis review

---

## **5. Rules for Signal Processing**

Follow these rules for synthesis review and signal processing.

* **Rule 5.1: Event-Driven Synthesis Triggers.** Conduct synthesis reviews based on signal volume and criticality:
    * When 10 new signals have been captured
    * When any critical signal is captured
    * When pattern density suggests opportunity (3+ related signals)
    * When stakeholder requests synthesis

    See [DEC-2025-07-14-003](../../../../work/domains/decisions/data/DEC-2025-07-14-003-time-independent-metrics.decision.md) for rationale on replacing time-based reviews with event-driven triggers.

* **Rule 5.2: Synthesis Review Process.** Each review must:
    * Review all `new` signals and move to `reviewed`
    * Identify clusters of related signals
    * Assess cluster significance and potential for brief generation
    * Update signal statuses and relationships
    * Generate opportunity briefs for significant clusters

* **Rule 5.3: Brief Generation Criteria.** Create opportunity briefs when:
    * Multiple signals point to the same underlying issue
    * A single critical signal warrants immediate attention
    * Signal patterns align with strategic charter priorities
    * Sufficient evidence exists to define problem and solution

* **Rule 5.4: Signal Archiving.** Archive signals that are:
    * Duplicates of existing signals
    * Too vague to be actionable
    * Outside the scope of current charter priorities
    * Addressed by existing decisions or projects
    * No longer relevant due to system changes

---

## **6. Rules for Signal Integration**

Follow these rules for connecting signals to other system components.

* **Rule 6.1: Charter Alignment.** Signals must reference relevant charters:
    * Link to governing charter that relates to the signal domain
    * Assess whether signal aligns with charter principles
    * Flag signals that might indicate charter evolution needs

* **Rule 6.2: Service Domain Mapping.** Tag signals by affected service:
    * Identify which service domains are impacted
    * Tag signals with relevant service evolution stages
    * Consider service boundary implications

* **Rule 6.3: Cross-Service Signals.** Handle signals affecting multiple services:
    * Tag with all affected service domains
    * Consider service integration implications
    * Assess need for cross-service coordination

* **Rule 6.4: Feedback Loop Completion.** Ensure signals complete learning loops:
    * Implementation outcomes generate new signals
    * Brief effectiveness generates reflection signals
    * System improvements generate opportunity signals

---

## **7. Rules for Signal Evolution**

Follow these rules to evolve the signal system itself.

* **Rule 7.1: Meta-Signals.** Signals about the signal system must be captured:
    * Friction with signal capture process
    * Opportunities to improve synthesis efficiency
    * Reflections on signal system effectiveness
    * Features needed for better signal management

* **Rule 7.2: System Improvement.** Signal system improvements must:
    * Originate from captured meta-signals
    * Be synthesized through the brief generation process
    * Align with evolution architecture principles
    * Generate new signals about their effectiveness

* **Rule 7.3: Process Evolution.** As the system evolves:
    * Update rules based on captured friction and opportunities
    * Maintain backward compatibility with existing signals
    * Document changes and their rationale
    * Train users on new processes and tools

This signal system serves as the foundation for the Company OS intelligence cycle, ensuring that valuable insights are captured, processed, and acted upon systematically.
