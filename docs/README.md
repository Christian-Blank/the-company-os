---
title: "Company OS Documentation Hub"
type: "overview"
audience: ["users", "developers", "llm"]
last_updated: "2025-07-16T15:37:00-07:00"
tags: ["documentation", "navigation", "overview"]
---

# Company OS Documentation Hub

Welcome to the Company OS documentation system. This hub provides organized access to all documentation across the system.

## Quick Start

### For Users
- **[Getting Started](users/getting-started.md)** - Install and start using Company OS
- **[CLI Reference](users/cli-reference.md)** - Complete command-line interface guide
- **[Common Workflows](users/workflows/)** - Step-by-step task guides

### For Developers
- **[Contributing Guide](developers/contributing.md)** - How to contribute to Company OS
- **[Service Creation](developers/service-creation.md)** - Creating new services
- **[Testing Patterns](developers/testing-patterns.md)** - Testing standards and examples
- **[Build System](developers/build-system.md)** - Bazel build system guide

### For LLM Collaboration
- **[Complete Context](llm/context-complete.md)** - Full system context for development
- **[Service Contexts](llm/service-contexts/)** - Individual service contexts

## System Overview

Company OS is organized as a collection of service domains, each owning its specific functionality and documentation:

### Core Services
- **[Rules Service](../company_os/domains/rules_service/docs/README.md)** - Document validation and rule management
- **[Configuration Service](../company_os/domains/config_service/docs/README.md)** - System configuration management

### Infrastructure Services
- **[Bazel Build System](../infrastructure/docs/README.md)** - Build and dependency management
- **[Testing Infrastructure](../infrastructure/testing/docs/README.md)** - Testing tools and patterns

## Architecture Documentation

### System Architecture
- **[Architecture Overview](architecture/overview.md)** - High-level system design
- **[Service Boundaries](architecture/service-boundaries.md)** - Service domain organization
- **[Integration Patterns](architecture/patterns/)** - Cross-service communication patterns

### Design Principles
- **[Hexagonal Architecture](architecture/hexagonal-architecture.md)** - Core architectural pattern
- **[Domain-Driven Design](architecture/domain-driven-design.md)** - Service boundary principles
- **[Testing Strategy](architecture/testing-strategy.md)** - System-wide testing approach

## Development Workflow

### Essential Commands
```bash
# Build entire system
bazel build //...

# Run all tests
bazel test //...

# Run specific service tests
bazel test //company_os/domains/rules_service/tests:all_tests

# Install and run CLI
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli
```

### Key Patterns
- **[Service Creation Pattern](developers/service-creation.md)** - Standard service structure
- **[Testing Pattern](developers/testing-patterns.md)** - Comprehensive testing approach
- **[Documentation Pattern](developers/documentation-patterns.md)** - Documentation standards

## Project Status

### Active Development
- **[Rules Service v0](../work/domains/projects/data/rules-service-v0/README.md)** - Document validation and rule management
- **[Knowledge Architecture v2](../company_os/domains/charters/data/knowledge-architecture.charter.md)** - Documentation system redesign

### Completed Features
- Hexagonal service architecture
- Bazel build system
- Pre-commit integration
- CLI interface patterns
- Comprehensive testing framework

## Navigation Tips

### Finding Information
1. **Start here** for overview and navigation
2. **Service-specific docs** for detailed implementation
3. **Architecture docs** for system understanding
4. **Developer docs** for contribution guidance

### Documentation Conventions
- **Purpose-driven organization** - Find by what you need to do
- **Audience-specific entry points** - Different paths for different needs
- **Working examples** - All examples are tested and current
- **Cross-references** - Links connect related information

## Contributing to Documentation

All documentation follows the **Documentation as Code** principle:

1. **Service documentation** lives with the service code
2. **Global documentation** lives in this `/docs/` directory
3. **Updates are part of development** - code changes include doc updates
4. **Quality is enforced** - documentation is reviewed with code

See [Contributing Guide](developers/contributing.md) for detailed contribution guidelines.

## Support and Feedback

### For Users
- Check [Common Workflows](users/workflows/) for step-by-step guidance
- Review [CLI Reference](users/cli-reference.md) for command details
- File issues for bugs or feature requests

### For Developers
- Review [Contributing Guide](developers/contributing.md) for development setup
- Check [Service Creation](developers/service-creation.md) for new service patterns
- Follow [Testing Patterns](developers/testing-patterns.md) for quality standards

### For LLM Sessions
- Use [Complete Context](llm/context-complete.md) for full system understanding
- Reference [Service Contexts](llm/service-contexts/) for focused development
- Maintain context consistency across development sessions

---

*This documentation hub is maintained by the OS Core Team and updated as part of the development workflow. Last updated: 2025-07-16T15:37:00-07:00*
