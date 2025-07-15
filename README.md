# The Company OS

An experimental, self-evolving operating system for organizations, designed to orchestrate work between human and AI collaborators.

## Vision

This project explores a single, powerful idea: What if the systems we use to work were as intelligent and adaptive as the people they serve?

The Company OS is a prototype of such a system. It's a living framework that learns from workflows, identifies friction, and evolves its own processes and tools. The goal is to create a symbiotic environment where both humans and AI agents can operate in a state of "flow," focusing on high-impact, creative work while the OS handles the operational complexity.

This isn't just about automation; it's about creating a system of collective intelligence that gets smarter over time.

## The Manifesto: Our Guiding Principles

The entire philosophy, vision, and set of guiding principles for this project are codified in a single document. To truly understand the "why" behind this work, please read:

### **[The Company OS Charter](os/domains/charters/data/company-os.charter.md)**

## Architecture

The Company OS has been migrated to a service-oriented architecture with clear domain separation:

### **OS Services** (`/os/domains/`)
- **charters**: Charter and governance management
- **processes**: Process and workflow management  
- **knowledge**: Knowledge graph and memory
- **evolution**: System improvement and learning
- **configuration**: System configuration
- **registry**: Service discovery and registry

### **Work Services** (`/work/domains/`)
- **projects**: Project management and vision tracking
- **signals**: Signal capture and processing
- **briefs**: Opportunity brief management
- **decisions**: Decision records and tracking

### **Infrastructure** (`/infrastructure/`)
- **docs**: Migration guides and infrastructure documentation
- **environments**: Environment configurations
- **scripts**: Automation and deployment scripts

### **Shared Resources** (`/shared/`)
- **schemas**: Common data schemas
- **libraries**: Shared code libraries
- **mcp-servers**: Model Context Protocol servers

## Service Evolution

Each service evolves through defined stages based on actual friction and need:

- **Stage 0** (Current): Direct file manipulation
- **Stage 1**: Add API definitions and MCP servers  
- **Stage 2**: Add local database caching
- **Stage 3**: Add external adapters (GitHub, etc.)
- **Stage 4**: Full platform migration

## How It Works

The OS is being built as a polyglot, microservice-based architecture where:

* **Processes are Code:** All workflows are defined as explicit, version-controlled artifacts.
* **AIs & Humans are Peers:** Roles are assigned based on capability, not on whether the actor is a person or an algorithm.
* **Evolution is Automated:** A continuous feedback loop observes signals, generates insights, and refines the system.
* **Services are Autonomous:** Each domain service can evolve independently while maintaining clear interfaces.

For the complete service registry, see [Service Registry](os/domains/registry/data/services.registry.md).
