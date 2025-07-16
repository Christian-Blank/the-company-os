---
title: "Navigation: Operating System Boundary"
type: "navigation"
parent_charter: "os/domains/charters/data/service-architecture.charter.md"
tags: ["navigation", "os", "core-services", "system"]
---

# OS Boundary: Core System Services

This boundary contains the foundational services that power the Company OS itself. These services provide the essential capabilities for system governance, evolution, and operation.

## Governing Documents
- **Parent Charter**: [Service Architecture](domains/charters/data/service-architecture.charter.md)
- **Company Charter**: [Company OS Charter](domains/charters/data/company-os.charter.md)

## Service Domains

### [Charters](domains/charters/) - Governance & Vision
- **Purpose**: Manages all charter documents that define system vision and principles
- **Stage**: 0 (File-based)
- **Key Documents**: 
  - [Company OS Charter](domains/charters/data/company-os.charter.md)
  - [Service Architecture](domains/charters/data/service-architecture.charter.md)
  - [Repository Architecture](domains/charters/data/repository-architecture.charter.md)
  - [Knowledge Architecture](domains/charters/data/knowledge-architecture.charter.md)
  - [Brand Charter](domains/charters/data/brand.charter.md)

### [Rules](domains/rules/) - Operational Governance
- **Purpose**: System rules and operational guidance derived from charters
- **Stage**: 0 (File-based)
- **Key Documents**:
  - [Service System Rules](domains/rules/data/service-system.rules.md)
  - [Repository System Rules](domains/rules/data/repository-system.rules.md)
  - [Knowledge System Rules](domains/rules/data/knowledge-system.rules.md)

### [Processes](domains/processes/) - Development Methodology
- **Purpose**: Process definitions and methodological frameworks
- **Stage**: 0 (File-based)
- **Key Documents**:
  - [Synapse Methodology](domains/processes/data/synapse.methodology.md)

### [Knowledge](domains/knowledge/) - System Memory
- **Purpose**: Knowledge graph and system memory management
- **Stage**: 0 (File-based)
- **Governing Charter**: [Knowledge Architecture](domains/charters/data/knowledge-architecture.charter.md)

### [Registry](domains/registry/) - Service Discovery
- **Purpose**: Central registry of all system services and their states
- **Stage**: 0 (File-based)
- **Key Documents**:
  - [Services Registry](domains/registry/data/services.registry.md)

### [Configuration](domains/configuration/) - System Config
- **Purpose**: Agent and system configuration management
- **Stage**: 0 (File-based)
- **Current State**: Empty, ready for configuration files

### [Evolution](domains/evolution/) - System Improvement
- **Purpose**: System improvement and learning mechanisms
- **Stage**: 0 (File-based)
- **Current State**: Empty, ready for evolution tracking

## Working with OS Services

1. **Finding Information**: Start with the [Service Registry](domains/registry/data/services.registry.md)
2. **Understanding Governance**: Follow charter hierarchy from [Company OS Charter](domains/charters/data/company-os.charter.md)
3. **Operational Rules**: Check relevant rules in [Rules domain](domains/rules/)
4. **Development Process**: Follow [Synapse Methodology](domains/processes/data/synapse.methodology.md)

## Service Evolution

All OS services follow the standard evolution stages (0-4). Current services can advance stages based on measured friction and actual need, not predetermined timelines.
