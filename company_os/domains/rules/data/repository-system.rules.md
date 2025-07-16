---
title: "Rule Set: The Repository System"
version: 1.1
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-14T19:00:19-07:00"
parent_charter: "os/domains/charters/data/repository-architecture.charter.md"
tags: ["rules", "repository", "file-structure", "organization", "services", "migration"]
---

# **Rule Set: The Repository System**

This document provides the operational rules for organizing files within the service-oriented repository structure. These rules operationalize the principles in the `repository-architecture.charter.md`.

---

## **0. Core Principles (The Mental Model)**

These are the foundational mental models for repository organization.

* **Rule 0.1: Services Define Structure.** The repository mirrors service boundaries. Every major directory represents a service domain or boundary type.
* **Rule 0.2: Evolution Preserves Paths.** As services evolve, file paths remain stable to prevent broken references.
* **Rule 0.3: Clarity Over Cleverness.** Simple, obvious organization beats complex hierarchies.

---

## **1. Rules for File Placement**

Follow these rules when determining where files belong.

* **Rule 1.1: Respect Domain Boundaries.** Files must be placed within their owning service domain:
    - Charter documents → `/os/domains/charters/data/`
    - Project files → `/work/domains/projects/data/`
    - Product-specific files → `/products/{product}/domains/{service}/data/`
* **Rule 1.2: Use Boundary Types.** Understand the three boundary types:
    - **OS Boundaries** (`/os/`): Core system capabilities
    - **Work Boundaries** (`/work/`): Execution and operational domains
    - **Product Boundaries** (`/products/`): External products built with the OS
* **Rule 1.3: Shared Resources.** Cross-cutting concerns go in `/shared/`:
    - Shared schemas → `/shared/schemas/`
    - Shared libraries → `/shared/libraries/`
    - MCP servers → `/shared/mcp-servers/`
* **Rule 1.4: Special Root Files.** Certain files require root-level placement for discoverability:
    - `README.md` - Primary repository documentation
    - `LLM-CONTEXT.md` - AI agent context guide (see [DEC-2025-07-14-002](../../../../work/domains/decisions/data/DEC-2025-07-14-002-llm-context-maintenance.decision.md))
    - `.gitignore` - Git configuration

    These files are exceptions to the service domain organization due to their cross-cutting nature and tool requirements.

---

## **2. Rules for Service Domain Structure**

Follow these rules for organizing within service domains.

* **Rule 2.1: Standard Subdirectories.** Every service domain follows this structure:
    ```
    /{domain}/
      /data/        # Primary data storage (Stage 0: .md files)
      /api/         # Service interface definitions (Stage 1+)
      /adapters/    # Storage adapters (Stage 2+)
      /schemas/     # Domain-specific schemas
      /docs/        # Service documentation
    ```
* **Rule 2.2: Start Minimal.** New domains start with only `/data/`. Add other directories as the service evolves.
* **Rule 2.3: Flat Data Storage.** Within `/data/`, maintain flat structure. Use prefixes for grouping if needed:
    - `project-001-spec.md`
    - `project-001-issues.md`
    - `project-002-spec.md`

---

## **3. Rules for Migration**

Follow these rules when migrating existing files to the new structure.

* **Rule 3.1: Map to Service Domains.** Current files map as follows:
    - `*.charter.md` → `/os/domains/charters/data/`
    - `*.methodology.md` → `/os/domains/processes/data/`
    - `*.rules.md` → Domain-specific `/docs/` directory
    - `/projects/*.vision.md` → `/work/domains/projects/data/`
* **Rule 3.2: Preserve Git History.** Use `git mv` to maintain file history during migration.
* **Rule 3.3: Update All References.** After moving files, update all internal links and parent references.

---

## **4. Rules for Cross-Domain References**

Follow these rules for linking between domains.

* **Rule 4.1: Use Relative Paths.** Link between domains using relative paths from repository root:
    - Good: `[Charter](/os/domains/charters/data/company-os.charter.md)`
    - Bad: `[Charter](../../os/domains/charters/data/company-os.charter.md)`
* **Rule 4.2: Reference Through Service.** Future-proof links by referencing the service, not deep paths:
    - Current: `/work/domains/projects/data/project-001.md`
    - Future API: `/projects/project-001`
* **Rule 4.3: Document External Dependencies.** If a domain depends on another, document it in `/docs/dependencies.md`.

---

## **5. Rules for Infrastructure**

Follow these rules for infrastructure and tooling.

* **Rule 5.1: Environment Configuration.** Environment-specific configs go in `/infrastructure/environments/{env}/`.
* **Rule 5.2: Operational Scripts.** Automation scripts go in `/infrastructure/scripts/` organized by purpose.
* **Rule 5.3: Service Deployment.** Each service domain may have deployment configs in `/infrastructure/services/{domain}/`.

---

## **6. Rules for System Evolution**

Follow these rules when evolving the repository structure.

* **Rule 6.1: New Service Domains.** Adding a new domain requires:
    1. Signal Record documenting the need
    2. Update to repository architecture charter
    3. Creation of domain directory structure
    4. Registration in service registry
* **Rule 6.2: Structural Changes.** Major reorganizations must follow the Synapse Methodology and consider:
    - Impact on existing links
    - Migration path for existing files
    - Update strategy for dependent systems
