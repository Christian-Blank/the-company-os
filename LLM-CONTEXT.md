# Company OS - LLM Context Guide

*This document provides comprehensive context for AI agents (ChatGPT, Claude, Gemini, etc.) to understand and assist with the Company OS project. This document focuses on essential orientation and references to canonical sources.*

## Project Overview

**The Company OS** is a self-evolving, intelligent operating system that acts as a living partner for organizations. It navigates the natural tension between universal entropy and our drive to create order, providing a framework for building coherent, meaningful systems in a complex world.

### Core Vision: The Symbiotic Partner

To create a self-evolving, intelligent operating system that acts as a living partner for our organization. The OS learns with us, adapts to us, and evolves as we grow, making processes adaptive, knowledge queryable, and collaboration seamless. Over time, it becomes an extension of our collective mind—an engine for translating intent into action and unlocking potential that was previously unimaginable.

## Essential Documents to Read

### Governance and Vision
- **Company Charter**: `company_os/domains/charters/data/company-os.charter.md` - Root vision and principles
- **Service Architecture**: `company_os/domains/charters/data/service-architecture.charter.md` - Technical governance
- **Knowledge Architecture**: `company_os/domains/charters/data/knowledge-architecture.charter.md` - Information management principles

### Operational Rules
- **All Rules**: `company_os/domains/rules/data/` - Complete operational rule set
- **Developer Workflow**: `DEVELOPER_WORKFLOW.md` - Complete development guide
- **Synapse Methodology**: `company_os/domains/processes/data/synapse.methodology.md` - Core development process

### Service Documentation
- **Service Registry**: `company_os/domains/registry/data/services.registry.md` - All active services
- **Rules Service**: `company_os/domains/rules_service/README.md` - Document validation and rule management
- **Source Truth Enforcement**: `company_os/domains/source_truth_enforcement/README.md` - Repository consistency validation
- **Repo Guardian**: `src/company_os/services/repo_guardian/README.md` - AI-powered repository analysis

## Current State & Recent Achievements

### ✅ Production Services (2025-07-22)

**Source Truth Enforcement Service v1.0** - COMPLETED
- **Registry-driven validation** of repository-wide consistency
- **Comprehensive CLI** with rich reporting and auto-fix capabilities
- **Pre-commit integration** preventing consistency violations
- **Production deployment** at `company_os/domains/source_truth_enforcement/`

**Rules Service v0** - COMPLETED
- **11 comprehensive test suites** with 100% pass rate
- **Production-ready CLI** with rich interface and error handling
- **Working pre-commit integration** with automatic validation and sync
- **Complete validation engine** with auto-fix capabilities
- **Signal intelligence framework** for continuous improvement

**Repo Guardian Service Phase 2 Step 2** - IN PROGRESS
- **Temporal workflow orchestration** infrastructure established
- **Hexagonal architecture** with clear service boundaries implemented
- **GitHub API integration** with repository analysis capabilities
- **Docker Compose configuration** for local Temporal development
- **Current status**: Implementing AI analysis pipeline

### ✅ Infrastructure Achievements (2025-07-22)

**Bazel Build System** - FULLY OPERATIONAL
- **Clean dependency resolution** with PyYAML replacing ruamel.yaml
- **Hermetic builds** for all services without dependency conflicts
- **Working CLI tools** via Bazel for all services
- **Complete test suite integration** with 85+ tests passing
- **Pre-commit hooks** using reliable Bazel commands

**Enhanced Pre-commit Validation** - JUST COMPLETED
- **Source Truth Enforcement** checks on every commit
- **Rules Service** validation and sync
- **Code quality** via ruff (formatting and linting)
- **Type checking** via mypy
- **All test suites** running on pre-commit
- **Comprehensive quality gates** preventing issues before commit

## System Architecture

### Service Boundaries
```
company_os/domains/          - Core system services (charters, rules, processes)
work/domains/               - Execution services (projects, signals, briefs, decisions)
src/company_os/services/    - Advanced services (repo_guardian)
shared/                     - Cross-cutting resources (schemas, libraries, MCP servers)
infrastructure/             - Deployment and operational support
```

### Key Active Services
- **Rules Service**: Document validation and rule synchronization
- **Source Truth Enforcement**: Repository consistency validation
- **Repo Guardian**: AI-powered repository quality analysis (Temporal-based)
- **Signal Intelligence**: Friction and opportunity capture system
- **Decision Records**: Comprehensive decision documentation

## Mental Models & Patterns

### Core Principles (Non-Negotiable)
1. **Shared, Explicit Memory** - All context explicitly documented
2. **Fluid Co-Development** - Human-AI partnership with role exchange
3. **Process-First, Tools-Second** - Define process before automation
4. **Context Over Compliance** - Understand why, not just what
5. **Self-Evolution via Double Learning Loop** - Continuous improvement
6. **Effectiveness is Truth** - Measurable outcomes guide decisions

*For complete details, see: `company_os/domains/charters/data/company-os.charter.md`*

### File Naming Convention
`name.type.md` where type indicates document purpose:
- `.charter.md` - Vision and governance
- `.rules.md` - Operational rules
- `.methodology.md` - Process definitions
- `.signal.md` - Captured signals
- `.brief.md` - Opportunity briefs
- `.decision.md` - Decision records
- `.vision.md` - Project visions

*Complete naming rules: `company_os/domains/rules/data/knowledge.rules.md`*

### ID Formats
- Signals: `SIG-YYYY-MM-DD-NNN`
- Briefs: `BRIEF-YYYY-MM-DD-NNN`
- Decisions: `DEC-YYYY-MM-DD-NNN`

*Complete ID rules: `company_os/domains/rules/data/signal.rules.md`*

## Development Workflow

### Getting Started
1. **Read this document** for orientation
2. **Review key charters** in `company_os/domains/charters/data/`
3. **Check current rules** in `company_os/domains/rules/data/`
4. **Follow developer workflow** in `DEVELOPER_WORKFLOW.md`
5. **Use Synapse methodology** for all development work

### Quality Assurance
Every commit automatically runs:
- Source Truth Enforcement (consistency validation)
- Rules Service (document validation and sync)
- Code formatting and linting (ruff)
- Type checking (mypy)
- All test suites (85+ tests)

### Service Development
- **Follow hexagonal architecture** as defined in service architecture charter
- **Use Bazel** for hermetic builds and dependency management
- **Write comprehensive tests** following established patterns
- **Document everything** according to knowledge architecture charter

## Navigation Guide

### For Understanding Vision
- Start: `company_os/domains/charters/data/company-os.charter.md`
- Architecture: `company_os/domains/charters/data/service-architecture.charter.md`

### For Current Work
- Active Projects: `work/domains/projects/data/`
- System Signals: `work/domains/signals/data/`
- Opportunity Briefs: `work/domains/briefs/data/`

### For Development
- Rules: `company_os/domains/rules/data/`
- Process: `company_os/domains/processes/data/synapse.methodology.md`
- Developer Guide: `DEVELOPER_WORKFLOW.md`

### For Service Information
- Registry: `company_os/domains/registry/data/services.registry.md`
- Individual service READMEs in their respective directories

## Key Principles for AI Agents

1. **Git as Source of Truth** - Everything is version-controlled
2. **Explicit Over Implicit** - Always capture context and rationale
3. **Charter Alignment** - All work must trace to governing charters
4. **Evidence-Based** - Base decisions on signals and measurable outcomes
5. **Double Learning Loop** - Separate doing work from improving work
6. **Quality Gates** - Use pre-commit hooks and validation services

## Current Capabilities (2025-07-22)

1. **Automatic Rule Sync** - Agent folders stay synchronized with canonical rules
2. **Document Validation** - Real-time validation with auto-fix capabilities
3. **Source Truth Enforcement** - Repository-wide consistency validation
4. **Quality Gates** - Comprehensive pre-commit validation preventing issues
5. **AI-Powered Analysis** - Repo Guardian service for intelligent repository insights
6. **Signal Intelligence** - Continuous capture of friction and opportunities
7. **Hermetic Builds** - Reliable Bazel-based build system for all services

## Anti-Patterns to Avoid

1. **Implicit Knowledge** - Never assume context exists - document everything
2. **Premature Automation** - Define clear processes before building tools
3. **Opinion-Based Evolution** - Always base changes on measured signals
4. **Skipping the Meta Loop** - Don't just execute - capture learnings and improvements
5. **Breaking Charter Alignment** - All work must trace to a governing charter
6. **Ignoring Quality Gates** - Always use validation services and pre-commit hooks

## Repository Information

- **URL**: https://github.com/Christian-Blank/the-company-os
- **Primary Branch**: main
- **Python Version**: 3.12 (see `.python-version`)
- **Build System**: Bazel 8+ with MODULE.bazel (bzlmod)
- **Dependency Management**: requirements.in → requirements_lock.txt

---

*This document serves as orientation for AI agents working with the Company OS. For detailed information, always reference the canonical documents linked throughout this guide. The system is designed for continuous evolution through captured intelligence and systematic improvement.*

*Last Updated: 2025-07-22 - Added Source Truth Enforcement, enhanced pre-commit configuration, and Bazel dependency fixes*
