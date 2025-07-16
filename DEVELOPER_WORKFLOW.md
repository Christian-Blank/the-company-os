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
git clone <repository-url>
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

**For Development:**
```bash
# Setup (one-time)
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Development cycle
python -m pytest company_os/domains/rules_service/tests/ -v
# Edit code, repeat tests
```

**For CI/CD:**
```bash
# In CI environment
pip install -r requirements.txt
python -m pytest company_os/domains/rules_service/tests/ --junit-xml=test-results.xml
```

## Next Steps

After verifying all commands work:
1. ✅ Analyze build system consistency - **COMPLETED**
2. ✅ Document findings and issues - **COMPLETED** 
3. Consider bzlmod migration for future Bazel compatibility
4. Establish standardized workflow for new services based on pytest approach

---

*This document will be updated as we test and verify each command.*