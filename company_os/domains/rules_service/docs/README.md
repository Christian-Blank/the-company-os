---
title: "Rules Service Documentation"
type: "overview"
service: "rules_service"
audience: ["users", "developers", "llm"]
last_updated: "2025-07-16T15:38:00-07:00"
tags: ["rules", "validation", "service", "documentation"]
---

# Rules Service Documentation

The Rules Service provides document validation and rule management capabilities for the Company OS. It discovers, syncs, and validates markdown documents against defined rules.

## Quick Start

### Installation
```bash
# Build the service
bazel build //company_os/domains/rules_service/...

# Run the CLI
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli
```

### Basic Usage
```bash
# Initialize configuration
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules init

# Sync rules to agent folders
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules sync

# Validate documents
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- validate validate README.md
```

### Pre-commit Integration
```yaml
# Add to .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: rules-sync
        name: Rules Service - Sync
        entry: bazel run //company_os/domains/rules_service/adapters/pre_commit:rules_sync_hook
        language: system
        always_run: true
        pass_filenames: false

      - id: rules-validate
        name: Rules Service - Validate
        entry: bazel run //company_os/domains/rules_service/adapters/pre_commit:rules_validate_hook
        language: system
        files: '\.md$'
```

## Core Concepts

### Rules Discovery
The service discovers rules from markdown files in configured directories:
- Extracts rules from tables, YAML blocks, and lists
- Detects document types automatically
- Organizes rules by category and severity

### Rules Synchronization
Distributes rules to agent folders for AI consumption:
- Configurable target directories (`.cursor/rules`, `.vscode/rules`, etc.)
- Conflict resolution strategies
- Atomic file operations

### Document Validation
Validates documents against applicable rules:
- Automatic rule application based on document type
- Severity-based classification (error, warning, info)
- Auto-fix capabilities for common issues
- Human-in-the-loop workflow for complex issues

## Service Architecture

The Rules Service follows hexagonal architecture principles:

```
┌─────────────────────────────────────────────────────────────┐
│                        Adapters                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │    CLI      │  │ Pre-commit  │  │     Future API      │  │
│  │  Interface  │  │   Hooks     │  │    (REST/GraphQL)   │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                      Core Domain                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Discovery  │  │    Sync     │  │     Validation      │  │
│  │   Service   │  │  Service    │  │      Service        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                   Infrastructure                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Config    │  │ File System │  │       Bazel         │  │
│  │ Management  │  │   Access    │  │   Build System      │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## API Reference

### CLI Commands
- **[CLI Reference](api.md#cli-commands)** - Complete command documentation
- **[Configuration](api.md#configuration)** - Configuration options
- **[Error Codes](api.md#error-codes)** - Exit codes and error handling

### Service APIs
- **[Discovery Service](api.md#discovery-service)** - Rule discovery APIs
- **[Sync Service](api.md#sync-service)** - Rule synchronization APIs
- **[Validation Service](api.md#validation-service)** - Document validation APIs

## Implementation Details

### Key Design Patterns
- **[Hexagonal Architecture](implementation.md#hexagonal-architecture)** - Service structure
- **[Domain-Driven Design](implementation.md#domain-driven-design)** - Domain modeling
- **[Dependency Injection](implementation.md#dependency-injection)** - Service composition

### Performance Considerations
- **[Concurrent Processing](implementation.md#concurrent-processing)** - Parallel rule processing
- **[File System Caching](implementation.md#caching)** - Hash-based change detection
- **[Benchmarking](implementation.md#benchmarking)** - Performance measurement

### Error Handling
- **[Exception Hierarchy](implementation.md#exception-hierarchy)** - Error classification
- **[Graceful Degradation](implementation.md#graceful-degradation)** - Fault tolerance
- **[Logging Strategy](implementation.md#logging-strategy)** - Observability

## Testing

### Test Organization
```
tests/
├── test_discovery.py          # Discovery service tests
├── test_sync.py               # Sync service tests
├── test_validation.py         # Validation service tests
├── test_cli.py                # CLI interface tests
├── test_pre_commit.py         # Pre-commit hook tests
├── test_integration.py        # End-to-end integration tests
└── test_performance.py        # Performance benchmarks
```

### Running Tests
```bash
# Run all tests
bazel test //company_os/domains/rules_service/tests:all_tests

# Run specific test suites
bazel test //company_os/domains/rules_service/tests:test_integration
bazel test //company_os/domains/rules_service/tests:test_cli

# Run with coverage
bazel test //company_os/domains/rules_service/tests:all_tests --coverage

# Run performance benchmarks
bazel test //company_os/domains/rules_service/tests:test_performance
```

### Test Patterns
- **[Unit Testing](patterns.md#unit-testing)** - Service isolation and mocking
- **[Integration Testing](patterns.md#integration-testing)** - End-to-end workflows
- **[Performance Testing](patterns.md#performance-testing)** - Benchmarking patterns

## Examples

### Basic Rule Definition
```markdown
---
title: "Example Rules"
version: 1.0
status: "Active"
owner: "Documentation Team"
last_updated: "2025-07-16T15:38:00-07:00"
---

# Example Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| DOC001 | All documents must have frontmatter | error |
| DOC002 | Titles should be descriptive | warning |
| DOC003 | Include examples where applicable | info |
```

### Configuration Example
```yaml
# .rules-service.yaml
version: "1.0"
rules_service:
  repository_root: "."
  rules_directories:
    - "company_os/domains/rules/data"
  agent_folders:
    - name: "cursor"
      path: ".cursor/rules"
      enabled: true
    - name: "vscode"
      path: ".vscode/rules"
      enabled: true
  sync:
    conflict_resolution: "overwrite"
    cleanup_orphaned_files: true
```

### Validation Workflow
```python
from company_os.domains.rules_service.src.validation import ValidationService
from company_os.domains.rules_service.src.config import RulesServiceConfig

# Initialize service
config = RulesServiceConfig.from_file(".rules-service.yaml")
validator = ValidationService(config)

# Validate a document
result = validator.validate_file("README.md")
if not result.is_valid:
    for issue in result.issues:
        print(f"{issue.severity}: {issue.message}")
```

## Development

### Contributing
1. **[Setup Development Environment](../../docs/developers/contributing.md)**
2. **[Follow Service Patterns](patterns.md)**
3. **[Write Tests](patterns.md#testing-patterns)**
4. **[Update Documentation](patterns.md#documentation-patterns)**

### Building
```bash
# Build service
bazel build //company_os/domains/rules_service/...

# Build CLI
bazel build //company_os/domains/rules_service/adapters/cli:rules_cli

# Build pre-commit hooks
bazel build //company_os/domains/rules_service/adapters/pre_commit:all
```

### Debugging
```bash
# Debug CLI with verbose output
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- --verbose rules sync

# Debug tests
bazel test //company_os/domains/rules_service/tests:test_cli --test_output=all

# Debug build issues
bazel build //company_os/domains/rules_service/... --verbose_failures
```

## Troubleshooting

### Common Issues
- **[Import Errors](troubleshooting.md#import-errors)** - Module import issues
- **[Configuration Issues](troubleshooting.md#configuration-issues)** - Config file problems
- **[Performance Issues](troubleshooting.md#performance-issues)** - Slow operations

### Debugging Tips
- **[Enable Logging](troubleshooting.md#logging)** - Debug output
- **[Check Configuration](troubleshooting.md#configuration-validation)** - Validate settings
- **[Verify File Permissions](troubleshooting.md#file-permissions)** - Access issues

## Roadmap

### Completed (v0.1)
- ✅ Core discovery, sync, and validation services
- ✅ CLI interface with comprehensive commands
- ✅ Pre-commit integration
- ✅ Comprehensive test suite
- ✅ Performance benchmarking

### Planned (v0.2)
- 🔄 REST API for external integration
- 🔄 Web dashboard for rule management
- 🔄 Advanced rule types (regex, custom validators)
- 🔄 Real-time validation in editors

### Future (v1.0)
- 📋 Rule authoring assistance
- 📋 Advanced analytics and reporting
- 📋 Multi-repository support
- 📋 Plugin system for custom rules

## Related Documentation

- **[Global Documentation Hub](../../../docs/README.md)** - System overview
- **[Knowledge Architecture](../../charters/data/knowledge-architecture.charter.md)** - Documentation principles
- **[Service Architecture](../../charters/data/service-architecture.charter.md)** - Service design patterns
- **[Development Workflow](../../../DEVELOPER_WORKFLOW.md)** - Development process

---

*This documentation is maintained by the Rules Service team and updated as part of the development workflow. For questions or contributions, see the [Contributing Guide](../../../docs/developers/contributing.md).*
