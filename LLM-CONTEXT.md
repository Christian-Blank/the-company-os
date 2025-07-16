# Company OS - LLM Context Guide

*This document provides comprehensive context for AI agents (ChatGPT, Claude, Gemini, etc.) to understand and assist with the Company OS project. This is a complete, standalone document containing all essential vision, principles, and mental models.*

## Project Overview

**The Company OS** is a self-evolving, intelligent operating system that acts as a living partner for organizations. It navigates the natural tension between universal entropy and our drive to create order, providing a framework for building coherent, meaningful systems in a complex world.

### Core Vision: The Symbiotic Partner

To create a self-evolving, intelligent operating system that acts as a living partner for our organization. The OS learns with us, adapts to us, and evolves as we grow, making processes adaptive, knowledge queryable, and collaboration seamless. Over time, it becomes an extension of our collective mind—an engine for translating intent into action and unlocking potential that was previously unimaginable.

## Core Philosophy

### 1. A Living System
An organization is a complex, adaptive system that balances order and chaos. Its operating model must be, too. The OS is designed for constant evolution, not stasis.

### 2. A Symbiotic Partnership
The future of work is human-with-machine. We treat AI agents and human contributors as equal peers with unique capabilities, working together within a unified framework.

### 3. An Engine for Clarity
The greatest tax on any organization is ambiguity. The OS is designed to turn ambiguity into order by making processes, context, and history transparent, deterministic, and replayable.

## First Principles (Non-Negotiable)

*All system designs, charters, and methodologies must adhere to these principles:*

### 1. Shared, Explicit Memory
All context—processes, rules, rationale, and status—must be explicitly documented in a single, shared system accessible to both humans and AI. There is no implicit knowledge.

### 2. Fluid Co-Development & Role Exchange
The system is built for a true partnership where the most capable agent—human or AI—is assigned to a task. Roles are fluid, and handoffs are seamless.

### 3. Process-First, Tools-Second
We must define a clear, version-controlled process before building tools to automate it.

### 4. Context Over Compliance (The Dual Path)
Understanding *why* a process exists is paramount. The system must support both:
- A structured, "opt-in" guided path for clarity
- An autonomous, "opt-out" expert path for velocity

### 5. Self-Evolution via a Double Learning Loop
Improvement is not a project; it is a continuous background process. The system must separate the act of *doing work* from the act of *improving work*.

### 6. Effectiveness is the Measure of Truth
Measurable outcomes, not opinions or dogma, define correctness and guide evolution. Any part of the system can be challenged and changed if a more effective path is demonstrated.

## The Cycle of Emergence

The OS learns and evolves through a continuous feedback cycle:

1. **Signals**: Constantly observe actions, outcomes, and friction points from all workflows
2. **Insights**: Analyze these signals to identify patterns, anomalies, and opportunities
3. **Actions**: Propose or implement small, high-leverage changes to its own processes or structures
4. **Memory**: Integrate the outcome of these changes into the system's canonical memory, making the entire OS smarter

## System Architecture

### Service Boundaries
```
/os/         - Core system services (charters, rules, processes, etc.)
/work/       - Execution services (projects, signals, briefs, decisions)
/shared/     - Cross-cutting resources (schemas, libraries, MCP servers)
/infrastructure/ - Deployment and operational support
```

### Key Services

#### OS Services (System Core)
- **Charters**: Vision and governance documents (the "constitution")
- **Rules**: Operational rules derived from charters
- **Processes**: Methodologies like Synapse for development
- **Knowledge**: Knowledge graph and documentation standards
- **Registry**: Service discovery and status tracking
- **Configuration**: System and agent configuration
- **Evolution**: System improvement and learning mechanisms

#### Work Services (Execution Layer)
- **Projects**: Project visions and specifications
- **Signals**: Friction, opportunities, and insights capture
- **Briefs**: Synthesized opportunities from signal analysis
- **Decisions**: Decision records with full context and rationale

### Evolution Stages
Services evolve through stages based on measured friction:
- **Stage 0**: File-based (current state for all services)
- **Stage 1**: APIs and automation
- **Stage 2**: Database caching
- **Stage 3**: External integrations
- **Stage 4**: Full platform

## Core Concepts & Mental Models

### 1. Company as Code
The entire organization operates as version-controlled code:
- **Processes as Code**: All workflows defined in markdown
- **Knowledge as Code**: All information explicitly captured
- **Decisions as Code**: All choices documented with context
- **Evolution as Code**: All improvements tracked through commits

### 2. Charter Hierarchy
Charters define vision and principles, forming a hierarchy:
```
Company OS Charter (root)
├── Service Architecture Charter
│   ├── Repository Architecture Charter
│   └── Knowledge Architecture Charter
├── Evolution Architecture Charter
└── Brand Charter
```

### 3. Knowledge Graph as Living Documentation
All documents are nodes in a graph:
- **Nodes**: Markdown files with structured frontmatter
- **Edges**: Links via `parent_charter` and hyperlinks
- **Navigation**: Via boundary/domain README files
- **Living**: Documents evolve through versioning
- **Self-Documenting**: The structure IS the documentation

### 4. Double Learning Loop (Synapse Methodology)

The Synapse methodology separates execution from improvement:

**Meta Loop** (System Improvement - Background Process):
- **Sense**: Capture signals (friction, opportunities, insights)
- **Synthesize**: Create briefs from signal patterns
- **Define**: Transform briefs into project specifications

**Primary Loop** (Task Execution - Foreground Process):
- **Build**: Execute defined tasks to specification
- **Refactor**: Clean and integrate work into the system
- **Learn**: Generate signals from execution experience

This separation ensures continuous improvement without disrupting active work.

### 5. Signal Intelligence System

A comprehensive organizational nervous system:
```
Signals → Analysis → Briefs → Roadmap → Projects → Outcomes → New Signals
```

**Signal Types**:
- **Friction**: Things that slow us down or cause pain
- **Opportunity**: Potential improvements or new capabilities
- **Reflection**: Insights from past work or decisions
- **Feature**: Specific capability requests
- **Exploration**: Learning from experiments or research

### 6. Decision Records as Time Machines
Comprehensive decision documentation enabling:
- **Deterministic Rebuilding**: Recreate any decision with full context
- **Time Travel**: Understand past choices without tribal knowledge
- **Learning Preservation**: Extract patterns from past decisions
- **Accountability**: Clear ownership and success metrics

### 7. Evolution Through Measured Friction
Services don't evolve based on roadmaps but on pain:
- Start simple (Stage 0: Files)
- Evolve only when friction demands it
- Each evolution stage addresses specific measured pain
- No premature optimization or over-engineering

### 8. Hexagonal Architecture Pattern
Clean separation of concerns:
- **Core Domain**: Business logic (the "what")
- **Ports**: Interfaces for external interaction
- **Adapters**: Implementations for specific technologies
- **Enables**: Easy testing, technology swapping, evolution

### 9. The Meta Signal Loop
The system improves itself:
- Signals about signals (meta-signals)
- The Signal Intelligence System generates signals about its own effectiveness
- Continuous self-improvement through self-observation

### 10. Context Windows as Design Constraint
Recognizing AI limitations as design principles:
- Keep documents focused and atomic
- Use explicit linking over implicit assumption
- Design for "cold start" understanding
- Optimize for AI agent collaboration

## Important Patterns

### File Naming Convention
`name.type.md` where type indicates document purpose:
- `.charter.md` - Vision and governance
- `.rules.md` - Operational rules
- `.methodology.md` - Process definitions
- `.signal.md` - Captured signals
- `.brief.md` - Opportunity briefs
- `.decision.md` - Decision records
- `.vision.md` - Project visions

### Frontmatter Requirements
Every document must have:
```yaml
---
title: "Document Title"
version: 1.0
status: "Draft|Active|Deprecated"
owner: "Responsible party"
last_updated: "YYYY-MM-DDTHH:MM:SS-TZ:00"
parent_charter: "path/to/charter.md"
tags: ["relevant", "tags"]
---
```

### ID Formats
- Signals: `SIG-YYYY-MM-DD-NNN`
- Briefs: `BRIEF-YYYY-MM-DD-NNN`
- Decisions: `DEC-YYYY-MM-DD-NNN`

## Current State & Challenges

### What's Implemented
- Complete charter hierarchy and governance structure
- All core rules (knowledge, service, repository, decision, signal, brief, validation)
- Templates for all document types
- Signal Intelligence System ready for use
- Decision records system operational
- Validation system rules and integration with Rules Service
- First critical signal captured (system complexity)

### Current Critical Challenge
**Signal SIG-2025-07-14-001**: System complexity exceeding manual maintenance capacity
- Need automation for validation, link checking, document generation
- Transitioning from Stage 0 to Stage 1 (automated services)
- Requires v0 hexagonal architecture implementation

### Next Steps
1. Synthesize automation infrastructure brief from critical signal
2. Implement core validation services (linters, schema checkers)
3. Build graph maintenance tools (link checking, dependency tracking)
4. Create document generation APIs
5. Establish continuous monitoring

## Navigation Guide

### For Understanding Vision
Start with: `/os/domains/charters/data/company-os.charter.md`

### For Operational Rules
Check: `/os/domains/rules/data/`

### For Current Work
Look in: `/work/domains/projects/data/`

### For System Intelligence
Review: `/work/domains/signals/data/` and `/work/domains/briefs/data/`

### For Learning the Process
Study: `/os/domains/processes/data/synapse.methodology.md`

## Key Principles to Remember

1. **Git as Source of Truth**: Everything is version-controlled
2. **Explicit Over Implicit**: Capture all knowledge explicitly
3. **Evolution on Demand**: Only add complexity when friction demands it
4. **Charter Alignment**: All work must align with governing charters
5. **Evidence-Based**: Decisions based on signals, not opinions
6. **Self-Improving**: The system captures its own improvement needs

## Working with the System

### Creating New Documents
1. Verify timestamp with `date` command
2. Use appropriate template from service `/data/` directory
3. Follow naming convention and ID format
4. Include complete frontmatter
5. Link to related documents
6. Place in correct service domain

### Capturing Signals
- Use signal template for any friction, opportunity, or insight
- Be specific with examples and evidence
- Tag with appropriate severity
- Link to related context

### Making Decisions
- Use decision template for significant choices
- Include all options considered
- Document complete rationale
- Define success metrics
- Plan for review cycles

## Practical Examples

### Example Signal Creation
```markdown
---
title: "Signal: Difficulty Finding Related Documents"
signal_id: "SIG-2025-07-15-001"
signal_type: "friction"
severity: "medium"
status: "new"
parent_charter: "os/domains/charters/data/knowledge-architecture.charter.md"
---
```

### Example Charter Reference
```markdown
This aligns with the Knowledge Architecture Charter's principle of 
"making implicit knowledge explicit" by ensuring all context is captured.
```

### Example Cross-Reference
```markdown
See [Decision DEC-2025-07-14-001](../decisions/data/DEC-2025-07-14-001-decision-record-structure.decision.md) 
for the rationale behind this structure.
```

## Common Tasks & Patterns

### When to Create a Signal
- You experience repeated friction
- You see an opportunity for improvement
- You learn something that others should know
- A process fails or produces unexpected results
- You have an idea for a new feature or capability

### When to Create a Brief
- Multiple signals point to the same issue
- A pattern emerges from signal analysis
- Quarterly synthesis review identifies themes
- Critical severity signals demand action

### When to Create a Decision Record
- Choosing between multiple viable options
- Making architectural or design choices
- Changing established processes
- Investing significant resources
- Setting precedents for future work

## Anti-Patterns to Avoid

1. **Implicit Knowledge**: Never assume context - document everything
2. **Premature Automation**: Don't build tools before defining processes
3. **Opinion-Based Evolution**: Always base changes on measured signals
4. **Skipping the Meta Loop**: Don't just execute - capture learnings
5. **Breaking Charter Alignment**: All work must trace to a charter
6. **Ignoring Timestamps**: Always verify current time before creating documents

## The Company OS Manifesto

"We believe in a future where organizations operate as intelligent, self-improving systems. Where every decision is traceable, every process is explicit, and every improvement is measured. Where humans and AI work as true partners, each contributing their unique strengths. This is not just about efficiency - it's about creating organizations that learn, adapt, and evolve as living systems. The Company OS is our commitment to making this future real, one signal at a time."

## Repository URL
https://github.com/Christian-Blank/the-company-os

---

*This document serves as a complete context guide for AI agents working with the Company OS. Copy and paste this entire document when starting a new chat session to provide full context. The system is designed for continuous evolution through captured intelligence and systematic improvement.*
