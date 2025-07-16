---
title: "Charter: The Repository Architecture"
version: 2.0
status: "Draft"
owner: "OS Core Team"
last_updated: "2025-07-14T16:50:00-07:00"
parent_charter: "os/domains/charters/data/service-architecture.charter.md"
tags: ["charter", "architecture", "repository", "file-structure", "services", "organization"]
---

# **Charter: The Repository Architecture**

This Charter defines the physical organization of our repository, implementing the Service Architecture principles for file-based service domains. It creates a workspace that supports both human navigation and service evolution.

---

## **1. Vision: The Service-Oriented Workshop**

To create a repository structure that embodies service-oriented architecture from day one. Every directory represents a potential service domain, organized to provide clarity for current file-based operations while enabling seamless evolution to API-driven services.

The repository becomes a living workspace where the boundaries between files and services blur, allowing natural progression from simple organization to sophisticated automation.

---

## **2. The "Why" (Core Rationale)**

Building on the Service Architecture principles, this structure solves for:

1. **Service-Ready Organization**: Every domain is structured to become a service without reorganization.
2. **Clear Domain Boundaries**: Physical separation reinforces logical service boundaries.
3. **Evolution-Friendly Layout**: File paths that make sense become API endpoints that make sense.
4. **Self-Building System**: The OS's own services live alongside the products built with it.

---

## **3. First Principles (The Repository Laws)**

*Extending the Service Architecture principles for physical organization:*

1. **Domains Over Directories**: Organize by service domain, not by file type or arbitrary categories.
2. **Service Structure from Day One**: Even file-based domains follow the `/data`, `/api`, `/adapters` pattern.
3. **Clear Boundary Types**: Distinguish between OS domains (`/os`), workspace domains (`/work`), and product domains (`/products`).
4. **Flat Within Domains**: Inside each domain's `/data`, maintain shallow structure for clarity.
5. **Evolution Preserves Paths**: As services evolve, logical paths remain stable.

---

## **4. The Canonical Structure (v2.0)**

```
/os/                    # Core OS service domains
  /domains/
    /{service}/         # Each core capability as a service
      /data/            # Service data (initially .md files)
      /api/             # Interface definitions
      /adapters/        # Storage/integration adapters
      /schemas/         # Domain schemas
      /docs/            # Service documentation

/work/                  # Workspace service domains
  /domains/
    /{service}/         # Each work capability as a service
      (same structure as above)

/products/              # Product-specific domains
  /{product-name}/
    /domains/
      /{service}/       # Product-specific services
        (same structure as above)

/shared/                # Cross-cutting concerns
  /schemas/             # Shared data contracts
  /libraries/           # Shared code libraries
  /mcp-servers/         # MCP server implementations

/infrastructure/        # Deployment and operations
  /environments/        # Environment configurations
  /scripts/             # Operational scripts
```

---

## **5. Domain Allocation Rules**

### OS Domains (`/os/domains/`)
- **charters**: Charter management service
- **processes**: Process/workflow management
- **knowledge**: Knowledge graph service
- **evolution**: System improvement service
- **configuration**: Agent and system configuration

### Work Domains (`/work/domains/`)
- **projects**: Project management service
- **signals**: Signal capture and analysis
- **briefs**: Opportunity brief management
- **decisions**: Decision recording service

### Product Domains (`/products/{name}/domains/`)
- Product-specific services using OS patterns
- Independent evolution from core OS
- Can consume OS services via APIs

---

## **6. Migration Patterns**

As domains evolve from files to services:

1. **Path Stability**: `/work/domains/projects/data/project-001.md` becomes API endpoint `/projects/project-001`
2. **Gradual Enhancement**: Add `/api` and `/adapters` without moving `/data`
3. **Backward Compatibility**: File-based access remains available through adapters

---

## **7. Process for Evolution**

This architecture inherits the Service Architecture evolution process. Changes must consider impact on physical organization and service boundaries. The repository structure itself is a service domain that can evolve.
