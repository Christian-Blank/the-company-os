---
title: "Service Registry"
version: 1.0
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-14"
parent_charter: "os/domains/charters/data/service-architecture.charter.md"
tags: ["registry", "services", "directory"]
---

# Service Registry

## OS Services
- **charters**: Charter management (Stage 0)
- **rules**: System rules and operational governance (Stage 0)
- **processes**: Process/workflow management (Stage 0)
- **knowledge**: Knowledge graph (Stage 0)
- **evolution**: System improvement (Stage 0)
- **configuration**: Configuration management (Stage 0)
- **registry**: This service registry (Stage 0)
- **rules-service**: Rule discovery, synchronization, and validation (Stage 0)
- **repo-guardian**: AI-powered repository quality management workflow (Stage 0)

## Work Services
- **projects**: Project management (Stage 0)
- **signals**: Signal capture (Stage 0)
- **briefs**: Opportunity briefs (Stage 0)
- **decisions**: Decision records (Stage 0)

## Service Domains Structure

```
/os/domains/{service}/
├── data/           # Service data files
├── docs/           # Documentation and rules
├── api/            # Future: API definitions
├── mcp/            # Future: MCP server
└── adapters/       # Future: External integrations

/work/domains/{service}/
├── data/           # Service data files
├── docs/           # Documentation and rules
├── api/            # Future: API definitions
├── mcp/            # Future: MCP server
└── adapters/       # Future: External integrations
```

## Evolution Stages

- **Stage 0** (Current): Direct file manipulation
- **Stage 1**: Add API definitions and MCP servers
- **Stage 2**: Add local database caching
- **Stage 3**: Add external adapters (GitHub, etc.)
- **Stage 4**: Full platform migration

Each service evolves based on actual friction and need, not predetermined timeline.
