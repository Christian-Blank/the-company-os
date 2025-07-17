Of course. Here is a standalone document detailing the Layered Context Model, ready to be integrated into your Company OS.

-----

```markdown
---
title: "Layered Context Model: The Relevance Algorithm"
version: 1.0
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-16T16:48:04-07:00"
parent_charter: "/company_os/domains/charters/data/knowledge-architecture.charter.md"
tags: ["mental-model", "relevance", "context", "rules", "algorithm", "architecture"]
---

## 1. Purpose

This document defines the **Layered Context Model**, the core methodology for the Company OS to deterministically identify and apply relevant rules to any task. This model serves as the blueprint for the "relevance algorithm" that powers the proactive delivery of contextual information to both human and AI agents. It prioritizes the **logic of relevance** over the implementation details of search or storage technologies.

---

## 2. Core Principle: Context as a Composition

The central principle is that a complete operational context is not derived from a single trigger but is **composed from multiple, distinct layers**. Each layer observes a different facet of the agent's environment and actions. The final "Activated Rule Set" for any given moment is the dynamic union of rules gathered from each of these layers.

This approach transforms rule discovery from a manual search problem into an automatic **context composition** problem.

---

## 3. The Four Layers of Context

The algorithm evaluates four primary layers to build a complete context.

### Layer 1: The **Artifact** Layer 🔎
This is the most specific layer, focused on the direct object of work—the "noun."

* **Question:** What specific *thing* is being created, read, or modified?
* **Triggers:** File paths, naming conventions (`*.type.md`), and content patterns (e.g., specific imports or function calls).
* **Example:** Editing `DEC-2025-07-16-002.decision.md` activates rules tagged `decisions` and `governance`.

### Layer 2: The **Action** Layer ⚡️
This layer is concerned with the specific action being performed—the "verb."

* **Question:** What is the agent *doing* right now?
* **Triggers:** Shell commands (`git commit`, `bazel build`), IDE actions (`save`, `run test`), or system API calls.
* **Example:** Executing a `git commit` activates rules tagged `repository-system` and `version-control`.

### Layer 3: The **Environment** Layer 🌎
This layer considers the broader scope or project within which the action occurs.

* **Question:** What is the overall *goal or project* this work belongs to?
* **Triggers:** The current git branch, the parent project directory (`/work/domains/projects/...`), or an active project configuration file.
* **Example:** Working on the `feature/rules-v1-query` branch could add project-specific rules or guidelines to the context.

### Layer 4: The **Agent** Layer 👤
This is the most abstract layer, considering the identity and role of the actor.

* **Question:** *Who* or *what* is performing the work?
* **Triggers:** The user's role (Developer, Project Manager) or the type of AI agent (CodeRefactor, OnboardingAgent).
* **Example:** An `AI-CodeRefactor` agent automatically receives rules tagged `sdk`, `factorization`, and `non-breaking-changes`.

---

## 4. The Composition Algorithm

The final set of rules is the result of a union operation across all layers. This ensures that context is additive and comprehensive.

The formula for the **Activated Rule Set** ($R_{active}$) is:

$$ R_{active} = R_{Artifact} \cup R_{Action} \cup R_{Environment} \cup R_{Agent} $$

This composition ensures that an agent receives a complete set of guidelines, from the most specific (rules about the file they're touching) to the most general (rules about their role in the system).

---

## 5. Practical Example: Committing a Decision

**Scenario:** A developer named `Jane` (`Agent` layer) runs `git commit` (`Action` layer) on the `feature/new-adr` branch (`Environment` layer) to save changes to the file `DEC-2025-07-16-003.decision.md` (`Artifact` layer).

The Rule Oracle would compose the context as follows:

1.  **Artifact Rule:** Activates `decision-system.rules.md` because the file is a decision record.
2.  **Action Rule:** Activates `repository-system.rules.md` because the action is `git commit`.
3.  **Environment Rule:** Activates any rules specific to the `feature/new-adr` project, if they exist.
4.  **Agent Rule:** Activates general developer rules for `Jane`.

Jane's final context for the commit message linter includes the union of all four rule sets, ensuring her commit is compliant at every level.
```
