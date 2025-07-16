
---
title: "Rule Set: Tech Stack Management"
version: 1.0
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-15T12:00:00-07:00"
parent_charter: "os/domains/charters/data/service-architecture.charter.md"
tags: ["rules", "tech-stack", "inventory", "standardization"]
---

# **Rule Set: Tech Stack Management**

This document provides the operational rules for managing technology stack decisions, inventory, and standardization within the Company OS.

---

## **0. Core Principles**

* **Rule 0.1: Stack First, Implementation Second.** Before implementing any solution, check existing stack decisions and standardized packages to avoid fragmentation.
* **Rule 0.2: Decision Record Required.** All new technology introductions must have a decision record documenting rationale and trade-offs.
* **Rule 0.3: Inventory Transparency.** Current tech stack must be queryable by both humans and AI agents.
* **Rule 0.4: Signal Inconsistencies.** When stack inconsistencies are discovered, create a signal immediately to preserve the metadata.

---

## **1. Rules for Stack Discovery**

* **Rule 1.1: Check Manifest Files First.** Before proposing implementations, examine:
  - `pyproject.toml` for Python dependencies
  - `package.json` for Node.js dependencies  
  - Decision records for architectural choices
  - Existing similar implementations in the codebase

* **Rule 1.2: Query Stack Service.** When available, use the tech stack service/agent to get current inventory and recommendations.

---

## **2. Rules for New Technology Introduction**

* **Rule 2.1: Justify Over Reuse.** Adding new packages requires justification over reusing existing ones for standardization.
* **Rule 2.2: Create Decision Record.** Document technology choices with full context, alternatives considered, and success criteria.
* **Rule 2.3: Update Inventory.** New technology must be registered in the stack inventory system.

---

## **3. Rules for Inconsistency Handling**

* **Rule 3.1: Signal Creation.** Create a signal when discovering:
  - Duplicate packages serving same purpose
  - Outdated dependencies
  - Missing standardization opportunities
  - Conflicting architectural patterns

* **Rule 3.2: User Decision on Critical Conflicts.** For critical inconsistencies that would impact current work, escalate to user for decision on whether to resolve first or proceed.
