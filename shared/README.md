---
title: "Navigation: Shared Resources"
type: "navigation"
parent_charter: "os/domains/charters/data/service-architecture.charter.md"
tags: ["navigation", "shared", "cross-cutting", "libraries"]
---

# Shared Resources: Cross-Cutting Concerns

This directory contains resources shared across multiple service domains. It provides common schemas, libraries, and tools that support the service ecosystem without belonging to any single domain.

## Governing Documents
- **Parent Charter**: [Service Architecture](../os/domains/charters/data/service-architecture.charter.md)
- **Related Rules**: [Service System Rules](../os/domains/rules/data/service-system.rules.md)

## Structure

### [schemas/](schemas/) - Common Data Contracts
- **Purpose**: Shared data schemas and contracts used across service domains
- **Current State**: Empty, ready for schema definitions
- **Examples**:
  - `frontmatter.schema.yaml` - Standard document metadata
  - `signal.schema.yaml` - Signal record format
  - `brief.schema.yaml` - Opportunity brief format

### [libraries/](libraries/) - Shared Code Libraries
- **Purpose**: Common code libraries and utilities used by multiple services
- **Current State**: Empty, ready for shared code
- **Examples**:
  - Document parsing utilities
  - Validation libraries
  - Common API patterns

### [mcp-servers/](mcp-servers/) - Model Context Protocol Servers
- **Purpose**: MCP server implementations for AI agent access to services
- **Current State**: Empty, ready for MCP servers
- **Future Structure**:
  ```
  mcp-servers/
  ├── charters/     # MCP server for charter service
  ├── projects/     # MCP server for project service
  └── signals/      # MCP server for signal service
  ```

## Usage Patterns

### For Service Development
1. **Schema Definition**: Define shared contracts in [schemas/](schemas/)
2. **Code Reuse**: Create utilities in [libraries/](libraries/) for common patterns
3. **AI Integration**: Implement MCP servers in [mcp-servers/](mcp-servers/) for agent access

### For Service Evolution
As services evolve to Stage 1+, they typically:
- Define APIs using shared schemas
- Implement MCP servers for AI agent integration
- Use shared libraries for common functionality

## Cross-Domain Coordination

Shared resources require coordination across service domains:
- **Schema Changes**: Impact multiple services, require careful versioning
- **Library Updates**: Must maintain backward compatibility
- **MCP Servers**: Should follow consistent patterns for agent usability

## Relationship to Service Domains

Shared resources support the hexagonal architecture pattern:
- **Ports**: Defined by shared schemas and interfaces
- **Adapters**: Implemented using shared libraries
- **Integration**: Enabled through MCP servers and common patterns

This enables services to evolve independently while maintaining interoperability.
