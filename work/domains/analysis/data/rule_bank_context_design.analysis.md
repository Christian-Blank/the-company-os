---
title: "Problem Definition: Contextual Rule Discovery & Delivery"
version: 1.1
status: "Draft"
owner: "OS Core Team"
last_updated: "2025-07-16T16:41:00-07:00"
parent_charter: "/company_os/domains/charters/data/rules-service.charter.md"
tags: ["problem-definition", "rules", "discovery", "context-awareness", "knowledge-graph", "mental-model"]
---

## 1. Problem Statement

The Company OS relies on a rich set of operational rules (`.rules.md`) to ensure clarity, consistency, and deterministic evolution. However, the current mechanism for accessing these rules is **passive and manual**. Both human developers and AI agents must proactively navigate to the `/os/domains/rules/data/` directory, read file names, and manually select the rules relevant to their current task.

This manual discovery process introduces significant **friction** and **cognitive load**, scales poorly as the number of rules increases, and creates a high risk of developers or agents working without the correct context, thereby undermining the system's core principles.

## 2. Why It Matters: Alignment with Core OS Philosophy

This problem directly challenges several foundational principles of the Company OS:

* **An Engine for Clarity:** The "greatest tax" of ambiguity is reintroduced when rules are hard to find. If an agent doesn't know a rule exists, the system's clarity is compromised.
* **A Symbiotic Partnership:** For an AI agent to be an equal peer, it cannot be expected to "guess" or "remember" to look for rules in a directory. A true partnership requires the system to proactively provide context to its partners, both human and AI.
* **Fluid Co-Development:** Seamless handoffs are impossible if the context (the rules) is not seamlessly transferred with the task. An AI agent starting a task needs the relevant rules injected into its context window automatically.
* **Effectiveness is the Measure of Truth:** The effectiveness of our rule system is diminished if the rules are not consistently applied. Our ability to measure the impact of rules is dependent on their consistent use.

## 3. Current State Analysis

### 3.1. Available Assets

* **Rule Store:** A version-controlled set of `.rules.md` files in a centralized directory.
* **Rule Structure:** Each rule file has structured frontmatter with `tags`, a `parent_charter`, and an `owner`. The body contains enumerated, human-readable rules.
* **Rules Service (v0):** A service with a hexagonal architecture capable of:
    * **Discovery:** Finding all `.rules.md` files.
    * **Sync:** Copying rules to specified target directories (e.g., for Cline's `.clinerules/` folder).
    * **Validation:** Linting the structure and metadata of the rule files themselves.
    * **Adapters:** A CLI and pre-commit hooks.

### 3.2. Current Workflow (The Friction Loop)

1.  A developer or AI agent starts a task (e.g., creating a new decision record).
2.  They must **remember** that rules for this task might exist.
3.  They **manually navigate** to `/os/domains/rules/data/`.
4.  They **read filenames** and guess which one is relevant (e.g., `decision-system.rules.md`).
5.  They **open the file** and read it to confirm its relevance.
6.  They attempt to hold these rules in their working memory (or context window for an AI) while performing the task.

### 3.3. Known Limitations

* **Not Scalable:** This process becomes untenable as the number of rules grows from ~10 to 50+.
* **High Cognitive Load:** It forces humans to shift context from *doing* the work to *searching for the rules about* the work.
* **AI-Unfriendly:** It's inefficient for AI agents, consuming valuable context window space and requiring complex instructions on how to browse and select files.
* **Static & Passive:** The system has no awareness of the user's context; it cannot *push* relevant information. The Cline "rules bank" model improves organization but still relies on manual `cp` and `rm` operations, which is not a scalable, intelligent solution.

## 4. Deeper Analysis: Mental Models & Future Strategies

To build a truly intelligent "Rule Oracle," we must look beyond simple keyword search and think about the *nature* of the relationships between work, context, and rules. This is fundamentally a **graph problem**.

### 4.1 The Knowledge Graph as the System's "Brain"

We should treat the entire Company OS not as a collection of files, but as a **Knowledge Graph**.

* **Nodes:** Every artifact is a node: a rule document, a specific rule, a charter, a signal, a decision record, a project file, a source code file, a developer, an AI agent.
* **Edges:** The relationships between them are edges: `parent_charter`, `related_signals`, `supersedes`, `imports`, `modifies`, `is_owned_by`, `is_triggered_by`.

In this model, finding the right rules becomes a graph traversal problem. The question changes from *"What files have the word 'decision' in them?"* to ***"Starting from the node `DEC-*.md` that I am currently editing, what `Rule` nodes have the strongest relationship to it?"***

### 4.2. A Taxonomy of Rules & Their Triggers

To build this graph, we must first understand the different *types* of rules and the contexts that trigger them. We can categorize rules by their **domain of influence**:

| Rule Category | Description | Primary Triggering Context | Example |
| :--- | :--- | :--- | :--- |
| **Artifact-Specific** | Governs the structure and lifecycle of a specific document type. | The creation or modification of a file matching a specific naming convention (`*.type.md`). | `decision-system.rules.md` is triggered when a file named `DEC-*.decision.md` is opened. |
| **Process & Workflow** | Defines the steps, roles, and handoffs for complex tasks. | A specific `git` action, a project phase change, or a task assignment. | `synapse.methodology.md` rules are relevant during the quarterly `synthesis` phase. |
| **Architectural** | Governs code structure, dependencies, and repository layout. | Changes to `BUILD.bazel` files, creation of new modules, or imports between services. | `code-factorization.rules.md` is triggered by a PR that adds a function to the `company_os_core` SDK. |
| **Normative & Cultural**| Encapsulates high-level principles, first principles, and cultural norms. | Broad contexts like onboarding, quarterly planning, or charter authoring. | The principles in a charter are triggered when creating a child charter. |

### 4.3. Parallels to Existing Concepts

This problem is a specific instance of broader, well-understood patterns:

* **Trait-Based Composition:** In programming (like Rust's traits), you compose functionality by adding traits to a struct. Here, we are composing a **context** for an agent (human or AI) by attaching the relevant rules based on the "traits" of the task (e.g., `is_a_decision_record`, `modifies_core_sdk`, `part_of_project_X`). The set of active rules becomes a dynamically composed "behavioral trait" for the agent.
* **Aspect-Oriented Programming (AOP):** AOP aims to inject cross-cutting concerns (like logging or security) into code without modifying the code itself. Our "Rule Oracle" is an AOP system for organizational processes, injecting the cross-cutting concern of "compliance with rules" into every developer action.
* **Organizational Theory:** Companies constantly struggle with disseminating policies and procedures. The traditional solution (intranets, wikis, handbooks) suffers from the exact same passive, manual discovery problem we've identified. The Company OS aims to solve this with code, automation, and deterministic context delivery.

## 5. Desired Future State: The "Rule Oracle"

In the ideal future state, rules are not "looked up"; they are **delivered**. The system should function as an intelligent "Rule Oracle" that proactively provides the right rules at the right time, based on the user's context.

* **For a Human:** When a developer creates a file named `DEC-*.md`, the IDE could automatically display a summary of the "Decision System" rules. Running a `git commit` could trigger a check against relevant coding rules.
* **For an AI Agent:** When an agent is given a task like "Refactor the validation module," its context should be automatically pre-populated with the `code-factorization.rules.md` and `validation-system.rules.md`.

## 6. Brainstorming: Potential Solution Vectors

Here are three potential evolutionary paths, aligning with the "Evolve Through Measured Friction" principle.

### Vector 1: Enhanced Querying (Stage 1 Evolution)

This approach focuses on making the existing rules easier to **pull** intelligently, moving beyond simple file discovery.

* **Concept:** Implement a powerful query engine within the `Rules Service`.
* **Implementation:**
    1.  The service builds an in-memory (or file-based) index of all rules, combining frontmatter tags, filenames, and full-text content.
    2.  Expose a new CLI command: `os-rules query "creating a decision record"`.
    3.  The command would perform a vector or keyword search on the index and return the top 1-3 most relevant rule files or even specific rule numbers (e.g., `decision-system.rules.md#Rule-1.1`).
* **Pros:** Relatively simple extension of the existing service. Doesn't require background processes. Empowers users with a "search" capability.
* **Cons:** Still a **pull** model. The user must initiate the query.

### Vector 2: Context-Aware Triggering (Stage 2 Evolution)

This approach makes the system **proactive**, delivering rules based on observed developer actions.

* **Concept:** The Rules Service listens for events and maps them to relevant rules based on the taxonomy defined in section 4.2.
* **Implementation:**
    1.  Develop a `triggers.yaml` map that explicitly defines the edges of our knowledge graph: `path_pattern` -> `rule_tags`.
    2.  Create adapters for different environments (IDE, shell) that watch for events and use the map to fetch and display relevant rules.
* **Pros:** A true **push** model. Reduces cognitive load significantly.
* **Cons:** More complex to build and maintain the trigger mapping.

### Vector 3: The Conversational Rule Agent (Stage 3 Evolution)

This is the ultimate vision of a symbiotic partnership, where rules are mediated by an intelligent agent.

* **Concept:** An AI agent with privileged access to the indexed rule base, serving as an interactive "Rule Oracle."
* **Implementation:**
    1.  Build upon the index from Vector 1 (likely with more advanced vector embeddings for semantic search).
    2.  Create a dedicated LLM agent with a single purpose: understanding the user's task and providing rule-based guidance.
    3.  Interaction model: An autonomous agent planning a task would first be required to consult the RuleBot to get its operational constraints, which are then added to its context.
* **Pros:** Most user-friendly and powerful. Handles ambiguity and provides synthesized, actionable guidance.
* **Cons:** Highest complexity. Depends on a robust and accurate index (Vector 1) and LLM agent technology.

## 7. Proposed Next Steps

We must evolve the system based on measured friction. The most logical path is to build foundational capabilities first.

1.  **Sense (Signal):** This document serves as **Signal: SIG-2025-07-16-001 - Rule Discovery Friction & Scalability Failure**.
2.  **Synthesize (Brief):** Create a new brief, **BRIEF-2025-07-16-001 - Rules Service v1: Intelligent Querying**, to synthesize the requirements for evolving the Rules Service from a simple sync/validation tool into an intelligent query engine.
3.  **Define (Project):** Define a new project based on the brief. The goal is to implement the "Enhanced Querying" capabilities described in Vector 1. This provides immediate value and serves as the necessary foundation (the indexed graph) for the more advanced solutions in Vectors 2 and 3.