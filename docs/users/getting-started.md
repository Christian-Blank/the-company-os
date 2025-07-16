---
title: "Getting Started with Company OS"
type: "guide"
audience: ["users"]
last_updated: "2025-07-16T15:41:00-07:00"
tags: ["getting-started", "installation", "setup", "users"]
---

# Getting Started with Company OS

This guide will help you get up and running with Company OS quickly and efficiently.

## Prerequisites

### Required Software
- **Python 3.8+** - Required for all services
- **Bazel 6.0+** - Build system
- **Git** - Version control

### Optional but Recommended
- **Pre-commit** - Git hooks for quality control
- **IDE with Python support** - VS Code, PyCharm, etc.

## Installation

### 1. Clone the Repository
```bash
git clone git@github.com:Christian-Blank/the-company-os.git
cd the-company-os
```

### 2. Install Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install
```

### 3. Verify Installation
```bash
# Test the build system
bazel build //...

# Run basic tests
bazel test //company_os/domains/rules_service/tests:test_cli
```

## First Steps

### 1. Initialize Rules Service
The Rules Service helps maintain document quality and consistency:

```bash
# Initialize configuration
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules init

# Sync rules to your editor
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules sync
```

### 2. Validate Your First Document
```bash
# Create a test document
echo "# Test Document" > test.md

# Validate it
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- validate validate test.md
```

### 3. Set Up Your Editor
Company OS supports multiple editors through rule synchronization:

#### VS Code
Rules are automatically synced to `.vscode/rules/` for Cline and other AI assistants.

#### Cursor
Rules are automatically synced to `.cursor/rules/` for AI assistance.

#### Other Editors
Rules are synced to `.cline/rules/` and `.claude/rules/` for various AI tools.

## Key Concepts

### Service-Oriented Architecture
Company OS is organized as independent services:
- **Rules Service** - Document validation and rule management
- **Configuration Service** - System configuration management
- **Infrastructure Services** - Build, testing, and deployment

### Documentation as Code
All documentation lives alongside code and evolves with the system:
- Service-specific documentation in `/service/docs/`
- Global documentation in `/docs/`
- LLM-optimized context for AI collaboration

### Hexagonal Architecture
Services follow hexagonal architecture patterns:
- **Core Domain** - Business logic
- **Adapters** - External interfaces (CLI, API, etc.)
- **Infrastructure** - External dependencies

## Common Workflows

### Daily Development
```bash
# Start development session
cd the-company-os

# Update rules for AI assistants
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules sync

# Make changes to code/documentation
# ... edit files ...

# Validate changes
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- validate validate *.md

# Run tests
bazel test //...

# Commit changes (pre-commit hooks run automatically)
git add -A && git commit -m "Your commit message"
```

### Document Creation
```bash
# Create new documentation
# Follow the templates in /docs/templates/

# Validate new documentation
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- validate validate new-doc.md

# Update cross-references as needed
# Use the global documentation hub for navigation
```

### Service Development
```bash
# Create new service following patterns
# See /docs/developers/service-creation.md

# Build service
bazel build //company_os/domains/new_service/...

# Run service tests
bazel test //company_os/domains/new_service/tests:all_tests

# Update documentation
# Create service docs in /company_os/domains/new_service/docs/
```

## Troubleshooting

### Common Issues

#### Build Errors
```bash
# Clear build cache
bazel clean

# Rebuild with verbose output
bazel build //... --verbose_failures
```

#### Import Errors
```bash
# Verify Python path
python -c "import sys; print(sys.path)"

# Check Bazel Python configuration
bazel info python_path
```

#### Pre-commit Issues
```bash
# Reinstall pre-commit hooks
pre-commit uninstall
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### Getting Help

#### Documentation
- **[CLI Reference](cli-reference.md)** - Complete command documentation
- **[Developer Guide](../developers/contributing.md)** - Development setup and patterns
- **[Architecture Overview](../architecture/overview.md)** - System understanding

#### Support Channels
- **GitHub Issues** - Bug reports and feature requests
- **Development Team** - Internal support for contributors
- **Documentation** - Self-service through comprehensive guides

## Next Steps

### For Users
1. **[Explore CLI Reference](cli-reference.md)** - Learn all available commands
2. **[Review Common Workflows](workflows/)** - Step-by-step task guides
3. **[Set Up Your Environment](../developers/contributing.md)** - Optimize for your workflow

### For Developers
1. **[Read Contributing Guide](../developers/contributing.md)** - Development setup
2. **[Understand Architecture](../architecture/overview.md)** - System design
3. **[Follow Testing Patterns](../developers/testing-patterns.md)** - Quality standards

### For AI Collaboration
1. **[Review LLM Context](../llm/context-complete.md)** - Full system understanding
2. **[Use Service Contexts](../llm/service-contexts/)** - Focused development
3. **[Maintain Context Consistency](../llm/context-maintenance.md)** - Session management

## Configuration

### Rules Service Configuration
Create `.rules-service.yaml` in your project root:

```yaml
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
    - name: "cline"
      path: ".cline/rules"
      enabled: true
  sync:
    conflict_resolution: "overwrite"
    cleanup_orphaned_files: true
    include_patterns: ["*.md"]
    exclude_patterns: ["**/node_modules/**", "**/.git/**"]
```

### Editor Configuration
Company OS works with various editors through rule synchronization:

- **VS Code**: Uses `.vscode/rules/` for AI assistants
- **Cursor**: Uses `.cursor/rules/` for AI assistance
- **Other editors**: Generic `.cline/rules/` and `.claude/rules/`

## Success Metrics

You'll know you're successful when:
- ✅ Build system works without errors
- ✅ Pre-commit hooks pass consistently
- ✅ Documentation is automatically validated
- ✅ AI assistants have up-to-date context
- ✅ Development workflow is smooth and efficient

---

*This guide is maintained by the OS Core Team. For questions or improvements, see the [Contributing Guide](../developers/contributing.md).*
