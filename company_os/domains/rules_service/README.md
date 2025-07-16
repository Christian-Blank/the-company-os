# Rules Service

This service is responsible for managing and validating the rules of the Company OS.

## Overview

The Rules Service provides the following capabilities:

- **Rule Discovery**: Scans the repository for `.rules.md` files and parses their frontmatter
- **Synchronization**: Keeps agent-specific rule folders in sync with the canonical rules
- **Validation**: Validates markdown documents against the discovered rules (coming in Milestone 4)

## Current Status

### Completed Milestones
- ✅ **Milestone 1**: Project Foundation (Base models, Bazel setup)
- ✅ **Milestone 2**: Rules Discovery (File scanning, frontmatter parsing, tag queries)
- ✅ **Milestone 3**: Sync Engine (Agent folder sync, change detection, conflict resolution)

### Upcoming Milestones
- **Milestone 4**: Validation Core (Document validation engine)
- **Milestone 5**: CLI Interface (Command-line tools)
- **Milestone 6**: Pre-commit Integration (Git hooks)
- **Milestone 7**: Testing & Documentation

## Setup

### Prerequisites
- Python 3.13+ with type checking enabled
- Bazel for build management
- Git for version control

### Configuration

Create a `rules-service.config.yaml` file in your repository root:

```yaml
version: 1.0

agent_folders:
  - path: ".clinerules/"
    description: "Rules for CLI agents"
    enabled: true
  - path: ".cursor/rules/"
    description: "Rules for Cursor IDE"
    enabled: true

sync:
  conflict_strategy: "overwrite"
  include_patterns: ["*.rules.md"]
  exclude_patterns: ["*draft*.rules.md"]
```

## Architecture

The Rules Service follows the Hexagonal Architecture pattern:

```
/os/domains/rules_service/
├── src/                    # Core domain logic
│   ├── models.py          # Domain models
│   ├── discovery.py       # Rule discovery service
│   ├── sync.py           # Synchronization service
│   └── config.py         # Configuration handling
├── adapters/              # External interfaces
│   ├── cli/              # CLI adapter (future)
│   └── pre_commit/       # Git hooks (future)
├── tests/                 # Test suite
├── docs/                  # Documentation
└── data/                  # Stage 0 file storage
```

## Usage (Current Capabilities)

### Rule Discovery

```python
from pathlib import Path
from os.domains.rules_service.src.discovery import RuleDiscoveryService

# Initialize discovery service
discovery = RuleDiscoveryService(Path("/path/to/repo"))

# Discover all rules
rules, errors = discovery.discover_rules()

# Query rules by tags
validation_rules = discovery.query_by_tags(["validation"])
```

### Rule Synchronization

```python
from os.domains.rules_service.src.sync import SyncService
from os.domains.rules_service.src.config import RulesServiceConfig

# Load configuration
config = RulesServiceConfig.from_file(Path("rules-service.config.yaml"))

# Initialize sync service
sync_service = SyncService(config, Path("/path/to/repo"))

# Sync rules to agent folders
result = sync_service.sync_rules(rules)
print(f"Synced {result.added} new rules, updated {result.updated}")
```

## Development

### Running Tests

```bash
# Run all tests
bazel test //os/domains/rules_service/tests:all_tests

# Run specific test suite
bazel test //os/domains/rules_service/tests:test_sync
bazel test //os/domains/rules_service/tests:test_config
bazel test //os/domains/rules_service/tests:test_integration
```

### Building

```bash
# Build all packages
bazel build //os/domains/rules_service/...
```

## Documentation

- [Sync Engine Documentation](docs/sync-engine.md) - Detailed sync engine documentation
- [Service Boundaries](docs/boundaries.md) - Service boundary definitions
- [Evolution Log](docs/evolution-log.md) - Service evolution history

## Contributing

When contributing to the Rules Service:

1. Follow the Synapse Methodology for development
2. Ensure all tests pass before committing
3. Update documentation for any API changes
4. Use type hints for all Python code
5. Follow the established architectural patterns
