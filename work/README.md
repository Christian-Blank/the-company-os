---
title: "Navigation: Work Boundary"
type: "navigation"
parent_charter: "os/domains/charters/data/service-architecture.charter.md"
tags: ["navigation", "work", "execution", "operations"]
---

# Work Boundary: Execution & Operations

This boundary contains services that handle the execution and operational aspects of work within the Company OS. These services manage projects, capture signals, process opportunities, and track decisions.

## Governing Documents
- **Parent Charter**: [Service Architecture](../os/domains/charters/data/service-architecture.charter.md)
- **Development Process**: [Synapse Methodology](../os/domains/processes/data/synapse.methodology.md)

## Service Domains

### [Projects](domains/projects/) - Project Management
- **Purpose**: Manages project visions, specifications, and execution tracking
- **Stage**: 0 (File-based)
- **Key Documents**:
  - [Career Architect Vision](domains/projects/data/career_architect.vision.md)
  - [Process Engine Vision](domains/projects/data/process_engine.vision.md)

### [Signals](domains/signals/) - Signal Capture
- **Purpose**: Captures friction, opportunities, and insights from system operation
- **Stage**: 0 (File-based)
- **Current State**: Empty, ready for signal records
- **Related Process**: Meta Loop in [Synapse Methodology](../os/domains/processes/data/synapse.methodology.md)

### [Briefs](domains/briefs/) - Opportunity Management
- **Purpose**: Manages opportunity briefs synthesized from signal analysis
- **Stage**: 0 (File-based)
- **Current State**: Empty, ready for opportunity briefs
- **Process Flow**: Signals → Analysis → Briefs → Projects

### [Decisions](domains/decisions/) - Decision Records
- **Purpose**: Tracks decisions made throughout system evolution and project execution
- **Stage**: 0 (File-based)
- **Current State**: Empty, ready for decision records
- **Format**: Decision records following ADR (Architecture Decision Record) patterns

## Workflow Integration

The work services are designed to support the Double Learning Loop from the Synapse Methodology:

### Meta Loop (Improvement & Emergence)
1. **Sense**: [Signals](domains/signals/) capture system friction and opportunities
2. **Synthesize**: Analysis produces [Briefs](domains/briefs/) aligned with charters
3. **Define**: Approved briefs become [Project](domains/projects/) specifications

### Primary Loop (Execution)
1. **Build**: Projects execute using defined processes
2. **Refactor**: Completion generates new signals, closing the loop
3. **Learn**: [Decisions](domains/decisions/) record learning for future reference

## Working with Work Services

1. **Starting New Work**: Begin with signal capture or opportunity brief
2. **Project Management**: Use project service for vision and tracking
3. **Learning Capture**: Record decisions and generate signals from outcomes
4. **Process Guidance**: Follow [Synapse Methodology](../os/domains/processes/data/synapse.methodology.md)

## Service Evolution

Work services evolve based on actual usage patterns and friction. As volume increases, services may develop APIs for integration, databases for performance, and external adapters for ecosystem connectivity.
