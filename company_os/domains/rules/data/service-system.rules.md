---
title: "Rule Set: The Service System"
version: 1.0
status: "Draft"
owner: "OS Core Team"
last_updated: "2025-07-14T16:51:00-07:00"
parent_charter: "os/domains/charters/data/service-architecture.charter.md"
tags: ["rules", "services", "architecture", "domains", "evolution", "hexagonal"]
---

# **Rule Set: The Service System**

This document provides the operational rules for creating, evolving, and managing services within the Company OS. These rules operationalize the principles in the `service-architecture.charter.md`.

---

## **0. Core Principles (The Mental Model)**

These are the foundational mental models for working with services.

* **Rule 0.1: Think Services, Not Files.** Every capability is a service domain. Its current implementation (files, API, database) is secondary to its service boundary.
* **Rule 0.2: Evolution is Incremental.** Services evolve through defined stages. Jump to complexity only when friction demands it.
* **Rule 0.3: Boundaries are Sacred.** Service boundaries define autonomy. Cross-domain operations must go through defined interfaces.

---

## **1. Rules for Creating Service Domains**

Follow these rules when establishing a new service domain.

* **Rule 1.1: One Domain, One Capability.** A service domain should encapsulate a single, cohesive business capability (e.g., project management, signal processing).
* **Rule 1.2: Follow the Standard Structure.** Every service domain MUST contain these directories:
    ```
    /{domain-name}/
      /data/        # Current storage implementation
      /api/         # Service interface definitions
      /adapters/    # Storage/integration adapters
      /schemas/     # Domain-specific schemas
      /docs/        # Service documentation
    ```
* **Rule 1.3: Start with Stage 0.** New services begin as organized markdown files in `/data`. Create other directories only when advancing stages.
* **Rule 1.4: Define Clear Boundaries.** Document what the service owns and what it doesn't in `/docs/boundaries.md`.

---

## **2. Rules for Service Evolution**

Follow these rules when evolving services through stages.

* **Rule 2.1: Measure Before Evolving.** Evolution requires documented friction. Create a Signal Record showing the pain point before advancing stages.
* **Rule 2.2: Preserve Backward Compatibility.** When adding new implementations, maintain existing interfaces. Old consumers should work unchanged.
* **Rule 2.3: Document Stage Transitions.** Each stage advancement must update `/docs/evolution-log.md` with:
    - Current stage
    - Reason for evolution
    - Migration plan
    - Rollback strategy

---

## **3. Rules for Inter-Service Communication**

Follow these rules for service interactions.

* **Rule 3.1: No Direct Data Access.** Services MUST NOT directly access another service's `/data` directory. Use defined interfaces only.
* **Rule 3.2: Events are Fire-and-Forget.** Event producers don't know about consumers. Use the signal service for event routing.
* **Rule 3.3: APIs are Contracts.** Once published, API interfaces are immutable. Use versioning for changes.

---

## **4. Rules for Service Implementation**

Follow these rules when implementing service functionality.

* **Rule 4.1: Stage 0 - File Conventions.**
    - Use consistent naming: `{entity}.{type}.md`
    - Include complete frontmatter
    - Store in flat structure within `/data`
* **Rule 4.2: Stage 1 - API Introduction.**
    - Create `/api/service.yaml` defining operations
    - Implement MCP server in `/shared/mcp-servers/{domain}/`
    - Add CLI in `/shared/cli/{domain}/`
* **Rule 4.3: Stage 2+ - Adapter Pattern.**
    - Define adapter interface in `/adapters/interface.yaml`
    - Implement adapters in `/adapters/{type}/`
    - Configure active adapter in `/api/config.yaml`

---

## **5. Rules for Service Discovery**

Follow these rules to find and use services.

* **Rule 5.1: Service Registry.** All active services must be registered in `/os/domains/registry/data/services.registry.md`.
* **Rule 5.2: API Documentation.** Service APIs must be documented in `/api/openapi.yaml` (once past Stage 0).
* **Rule 5.3: Health Checks.** Services past Stage 1 must implement a health check endpoint.

---

## **6. Rules for System Evolution**

Follow these rules to evolve the service system itself.

* **Rule 6.1: New Service Types.** Proposing a new service domain type requires:
    1. Signal Record identifying the capability gap
    2. Opportunity Brief with domain boundaries
    3. Pull request adding to service registry
* **Rule 6.2: Stage Definitions.** Changes to evolution stages require updating both this rule set and the parent charter.
