# Developer Workflow Guide

## Overview

This document provides step-by-step instructions for setting up, building, and testing the Company OS rules_service. All commands should be run from the repository root directory.

## Prerequisites

- Python 3.12+
- Bazel 8.x
- Git

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/Christian-Blank/the-company-os
cd the-company-os

# Verify Python version
python --version  # Should be 3.12+

# Verify Bazel version
bazel version  # Should be 8.x
```

### 2. Build the Service

```bash
# Build all rules_service components
bazel build //company_os/domains/rules_service/...

# Build specific components
bazel build //company_os/domains/rules_service/src:rules_service_lib
bazel build //company_os/domains/rules_service:rules_service
```

### 3. Run Tests

```bash
# Run all rules_service tests
bazel test //company_os/domains/rules_service/tests:all_tests

# Run specific test suites
bazel test //company_os/domains/rules_service/tests:test_validation
bazel test //company_os/domains/rules_service/tests:test_validation_human_input
bazel test //company_os/domains/rules_service/tests:test_sync
bazel test //company_os/domains/rules_service/tests:test_config
bazel test //company_os/domains/rules_service/tests:test_integration
bazel test //company_os/domains/rules_service/tests:test_performance
```

### 4. Alternative: Run with pytest (Development Mode)

```bash
# Install dependencies (if not using Bazel)
pip install -r requirements.txt

# Run tests with pytest
python -m pytest company_os/domains/rules_service/tests/test_validation.py -v
python -m pytest company_os/domains/rules_service/tests/test_validation_human_input.py -v
```

## Detailed Build System Information

### Dependencies Management

**Bazel Approach (Recommended):**
- Dependencies are managed in `WORKSPACE` file
- Python packages are resolved via `pip_parse`
- No manual virtual environment needed
- All dependencies are hermetic and reproducible

**Manual Approach (Development Only):**
- Use `requirements.txt` for manual dependency installation
- Create virtual environment: `python -m venv .venv && source .venv/bin/activate`
- Install: `pip install -r requirements.txt`

### Build Artifacts

```bash
# Build Python wheel (if configured)
bazel build //company_os/domains/rules_service:rules_service_wheel

# Build CLI adapter
bazel build //company_os/domains/rules_service/adapters/cli:cli

# Build pre-commit hooks
bazel build //company_os/domains/rules_service/adapters/pre_commit:pre_commit
```

### Development Workflow

1. **Make Changes:** Edit source files in `company_os/domains/rules_service/src/`
2. **Run Tests:** `bazel test //company_os/domains/rules_service/tests:all_tests`
3. **Build:** `bazel build //company_os/domains/rules_service/...`
4. **Commit:** Only commit if tests pass

### Troubleshooting

**Common Issues:**
- Bazel cache issues: `bazel clean --expunge`
- Python import errors: Check `__init__.py` files exist
- Test failures: Check absolute imports are used

**Directory Structure:**
```
company_os/domains/rules_service/
├── src/                    # Core implementation
│   ├── validation.py       # Validation engine
│   ├── models.py          # Data models
│   ├── sync.py            # Sync service
│   └── config.py          # Configuration
├── tests/                 # Test suites
├── adapters/              # Interface adapters
│   ├── cli/              # CLI interface
│   └── pre_commit/       # Pre-commit hooks
└── docs/                 # Documentation
```

## Testing Commands Status

<!-- This section will be updated as we test each command -->

### Command Test Results

**Status Legend:**
- ✅ Working as expected
- ⚠️ Working with issues/warnings
- ❌ Not working
- 🔄 In progress

| Command | Status | Notes |
|---------|--------|-------|
| `bazel build //company_os/domains/rules_service/...` | ❌ | WORKSPACE file disabled by default in Bazel 8. Error: No repository visible as '@rules_python' from main repository. Requires Bzlmod migration. |
| `bazel build //company_os/domains/rules_service/... --enable_workspace` | ❌ | PyInfo/PyRuntimeInfo not defined in rules_python. Bazel 8 compatibility issue with rules_python 0.36.0. |
| `bazel build //company_os/domains/rules_service/src:rules_service_lib --enable_workspace` | ❌ | Updated to rules_python 1.5.1 but pip_parse not resolving transitive dependencies properly. Missing typing_extensions, ruamel.yaml.clib repos. |
| `bazel test //company_os/domains/rules_service/tests:all_tests` | ❌ | Bazel 8 + rules_python 1.5.1 compatibility issues with transitive dependencies |
| `python -m pytest company_os/domains/rules_service/tests/test_validation.py -v` | ✅ | 40 tests pass |
| `python -m pytest company_os/domains/rules_service/tests/test_validation_human_input.py -v` | ✅ | 11 tests pass |
| `python -m pytest company_os/domains/rules_service/tests/test_sync.py -v` | ✅ | 13 tests pass |
| `python -m pytest company_os/domains/rules_service/tests/ -v` | ✅ | 85 tests pass, 1 skipped |

<!-- Test findings will be added here as we progress -->

## Migration to Bzlmod

### Attempted Migration Steps

1. ✅ Created MODULE.bazel with rules_python 1.5.1
2. ✅ Updated all BUILD files to use @pypi repository
3. ✅ Renamed WORKSPACE to WORKSPACE.bzlmod to disable it
4. ✅ Generated requirements_lock.txt with pip-compile
5. ❌ Bazel build still fails due to transitive dependency issues

### Current Issues with Bazel 8 + rules_python

- pip.parse expects annotated_types package but can't find BUILD files
- Transitive dependencies not being resolved properly
- Complex dependency graph with pydantic-core causing issues

## Build System Analysis

### Current State Summary

**✅ What's Working:**
- Python absolute imports with `company_os.domains.rules_service` package structure
- All 85 tests passing via pytest (40 validation + 11 human input + 13 sync + 21 other)
- Virtual environment setup with `pip install -r requirements.txt`
- Manual dependency management via requirements.txt

**❌ What's Not Working:**
- Bazel build system due to Bazel 8 compatibility issues with rules_python
- WORKSPACE file deprecated in Bazel 8, requires bzlmod migration
- pip_parse not resolving transitive dependencies properly
- Hermetic builds not currently achievable

### Key Issues Identified

1. **Bazel Version Compatibility**:
   - Bazel 8.3.1 has deprecated WORKSPACE files
   - rules_python 1.5.1 (latest) has transitive dependency resolution issues
   - Need to migrate to MODULE.bazel (bzlmod) for Bazel 8+ compatibility

2. **Dependency Management**:
   - pip_parse fails to resolve typing_extensions, ruamel.yaml.clib
   - Manual requirements.txt works but not hermetic
   - Need to generate lock files for reproducible builds

3. **Test Infrastructure**:
   - pytest works perfectly from command line
   - Bazel py_test targets cannot build due to dependency issues
   - Mixed success with different build approaches

### Recommendations

**Short-term (Current Development):**
1. Continue using pytest for development and CI
2. Use virtual environments for dependency isolation
3. Keep requirements.txt updated and version-pinned

**Medium-term (Build System Migration):**
1. Migrate to MODULE.bazel for Bazel 8+ compatibility
2. Use pip-tools to generate requirements.lock for reproducible builds
3. Consider alternatives like Poetry or pipenv for dependency management

**Long-term (Scalability):**
1. Evaluate whether Bazel is the right choice for this Python project
2. Consider simpler build systems (setuptools, hatch, etc.)
3. Focus on developer experience and CI/CD pipeline reliability

### Current Developer Workflow

**Option 1: Using Python build script (Recommended)**
```bash
# Simple one-command build and test
./build.py

# This runs:
# - Dependency installation
# - Linting (ruff)
# - Type checking (mypy)
# - All tests (pytest)
```

**Option 2: Manual commands**
```bash
# Setup (one-time)
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Development cycle
python -m pytest company_os/domains/rules_service/tests/ -v
# Edit code, repeat tests

# Optional: Run linting and type checking
python -m ruff check company_os/domains/rules_service
python -m mypy company_os/domains/rules_service/src
```

**For CI/CD:**
```bash
# In CI environment
pip install -r requirements.txt
python -m pytest company_os/domains/rules_service/tests/ --junit-xml=test-results.xml
```

## Using the Rules Service CLI

### CLI Overview

The Rules Service CLI provides commands for managing rules, syncing them to agent folders, and validating documents. The Rules Service v0 is now **production-ready** and fully integrated into the Company OS workflow.

### Installation

```bash
# Build the CLI (recommended)
bazel build //company_os/domains/rules_service/adapters/cli:rules_cli

# Or install locally for development
pip install -e company_os/domains/rules_service
```

### Available Commands

#### 1. Initialize Configuration

```bash
# Create default configuration file
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules init

# Create configuration at custom location
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules init --config custom-config.yaml
```

#### 2. Query Rules

```bash
# List all rules
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules query

# Filter by tag
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules query --tag validation

# Filter by document type
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules query --type ".decision.md"

# Filter by enforcement level
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules query --enforcement strict

# Combine filters and limit results
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules query --tag formatting --type ".charter.md" --limit 10
```

#### 3. Sync Rules to Agent Folders

```bash
# Sync rules to all configured agent folders
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules sync

# Dry run to preview changes
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules sync --dry-run

# Use custom configuration
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules sync --config custom-config.yaml
```

#### 4. Validate Documents

```bash
# Validate a single file
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- validate validate README.md

# Validate multiple files
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- validate validate file1.md file2.md file3.md

# Validate using glob patterns
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- validate validate "**/*.charter.md"

# Validate entire directory
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- validate validate work/domains/briefs/

# Apply auto-fixes
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- validate validate README.md --auto-fix

# Use different output formats
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- validate validate *.md --format json
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- validate validate *.md --format summary

# Verbose output
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- validate validate *.md --verbose

# Continue on errors (don't exit on first error)
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- validate validate *.md --no-exit-on-error
```

### Exit Codes

The CLI uses specific exit codes to indicate different outcomes:

- `0`: Success - all operations completed successfully
- `1`: Warnings found during validation
- `2`: Errors found during validation
- `3`: General failure (configuration issues, file not found, etc.)

### Example Workflows

#### Initial Setup
```bash
# 1. Initialize configuration
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules init

# 2. Edit .rules-service.yaml to customize settings
vim .rules-service.yaml

# 3. Sync rules to agent folders
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules sync

# 4. Validate your documents
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- validate validate "**/*.md" --auto-fix
```

#### CI/CD Integration
```bash
# In your CI pipeline
bazel build //company_os/domains/rules_service/adapters/cli:rules_cli
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- validate validate "**/*.md" --format json > validation-results.json
```

#### Development Workflow
```bash
# Check rules before committing
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- validate validate $(git diff --name-only --cached | grep '\.md$')
```

### Configuration File Format

The `.rules-service.yaml` configuration file has the following structure:

```yaml
version: "1.0"
rules_service:
  repository_root: "."
  rules_directories:
    - "os/domains/rules/data"
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
    - name: "claude"
      path: ".claude/rules"
      enabled: true
  sync:
    conflict_resolution: "overwrite"  # or "skip", "ask"
    cleanup_orphaned_files: true
    include_patterns: ["*.md"]
    exclude_patterns: ["**/node_modules/**", "**/.git/**"]
```

## Conclusion

### Final Status

**Bazel Build System:**
- ✅ Successfully working with Bazel 8 using MODULE.bazel (bzlmod)
- ✅ All rules_service components build successfully
- ✅ All 6 test suites pass (85 tests total)
- ✅ CLI binary builds and runs correctly
- ✅ Proper dependency management with requirements_lock.txt

**Key Success Factors:**
- Migrated from deprecated WORKSPACE to MODULE.bazel
- Using aspect_rules_py for better Python support
- Proper import paths in BUILD files (`imports = ["../../../.."]`)
- Updated dependencies (typer 0.16.0, added ruamel.yaml)

### Working Commands

**Build:**
```bash
bazel build //company_os/domains/rules_service/src:rules_service_lib
bazel build //company_os/domains/rules_service/adapters/cli:rules_cli
bazel build //company_os/domains/rules_service/...
```

**Test:**
```bash
bazel test //company_os/domains/rules_service/tests:test_validation
bazel test //company_os/domains/rules_service/tests:all_tests
```

**Run:**
```bash
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- --help
```

### Recommendation

**Use Bazel for the Company OS project:**
1. Provides hermetic, reproducible builds
2. Excellent caching and incremental builds
3. Scales well for monorepo architecture
4. Now fully functional with Python 3.12

For detailed setup instructions and patterns, see `BAZEL_SETUP_ANALYSIS.md`.

## Next Steps

1. ✅ Analyze build system consistency - **COMPLETED**
2. ✅ Document findings and issues - **COMPLETED**
3. ✅ Successfully migrate to bzlmod - **COMPLETED**
4. ✅ Establish Bazel-based workflow - **COMPLETED**
5. ✅ Create comprehensive documentation - **COMPLETED** (see BAZEL_SETUP_ANALYSIS.md)

---

*Last updated: 2025-07-16 - All Bazel commands verified and working.*
