---
title: "Navigation: Projects Service Domain"
type: "navigation"
parent_charter: "../../../os/domains/charters/data/service-architecture.charter.md"
tags: ["navigation", "projects", "execution", "vision"]
---

# Projects Service Domain

The projects service manages project visions, specifications, and execution tracking within the work boundary. Projects represent concrete initiatives that implement opportunities derived from signal analysis and brief synthesis.

## Service Information
- **Evolution Stage**: 0 (File-based)
- **Service Registry**: [Work Services](../../../os/domains/registry/data/services.registry.md)
- **Governing Charter**: [Service Architecture](../../../os/domains/charters/data/service-architecture.charter.md)
- **Development Process**: [Synapse Methodology](../../../os/domains/processes/data/synapse.methodology.md)

## Structure

### [data/](data/) - Project Documents
Current project visions and specifications:

#### Active Projects
- **[Career Architect Vision](data/career_architect.vision.md)** - AI-powered career development platform
- **[Process Engine Vision](data/process_engine.vision.md)** - Workflow automation and orchestration system

### [docs/](docs/) - Supporting Documentation
*Currently empty - ready for project-related documentation, templates, and guidelines*

## Project Lifecycle

Projects flow through the Double Learning Loop defined in the Synapse Methodology:

### Meta Loop Integration
1. **Emergence**: Projects emerge from [Opportunity Briefs](../briefs/) synthesized from [Signals](../signals/)
2. **Alignment**: Project visions align with governing charters
3. **Definition**: Projects become APN (Agentic Process Notation) blueprints

### Primary Loop Execution
1. **Build**: Projects execute via Guided Path or Expert Path
2. **Refactor**: Completion includes mandatory refactoring step
3. **Learn**: Project outcomes generate new signals and decisions

## Cross-Service Integration

### Inputs (From Other Services)
- **Signals**: [Signal Service](../signals/) provides friction and opportunity data
- **Briefs**: [Brief Service](../briefs/) provides synthesized opportunities
- **Charters**: Governance and alignment from [Charter Service](../../../os/domains/charters/)

### Outputs (To Other Services)
- **Signals**: Project execution generates new signals about system friction
- **Decisions**: Project choices recorded in [Decision Service](../decisions/)
- **Evolution**: Successful patterns influence [System Evolution](../../../os/domains/evolution/)

## Working with Projects

### Creating Projects
1. **From Briefs**: Most projects start from approved opportunity briefs
2. **Direct Creation**: Urgent or small projects may be created directly
3. **Charter Alignment**: Ensure alignment with relevant governing charters
4. **Vision Definition**: Create clear vision document following knowledge system rules

### Managing Projects
1. **Status Tracking**: Update frontmatter status fields
2. **Version Control**: Use semantic versioning for major changes
3. **Signal Generation**: Capture friction and learning as signals
4. **Decision Recording**: Document key decisions in decision service

## Document Types

### Vision Documents
- **Purpose**: High-level project vision and goals
- **Format**: `{project-name}.vision.md`
- **Stage**: Initial project definition

### Future Document Types (As Service Evolves)
- **Specifications**: Detailed technical specifications
- **Progress Reports**: Regular status updates
- **Retrospectives**: Post-completion analysis
- **Dependencies**: Cross-project dependency tracking

## Service Evolution

Future evolution of this service might include:
- **Stage 1**: Project management API, status tracking
- **Stage 2**: Project database with timeline and dependency management
- **Stage 3**: Integration with external project management tools
- **Stage 4**: AI-powered project orchestration and resource allocation
