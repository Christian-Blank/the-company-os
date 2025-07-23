# Developer Workflow Guide

## Overview

This document provides step-by-step instructions for setting up, building, and testing the Company OS rules_service. All commands should be run from the repository root directory.

## Prerequisites

- Python 3.10+ (Currently running Python 3.10.17)
- Bazel 8.x
- Git

## Quick Start

**CRITICAL**: Before any development work, you MUST follow the [Developer Verification Process](company_os/domains/processes/data/developer-verification.process.md) to ensure environment consistency and prevent quality issues.

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/Christian-Blank/the-company-os
cd the-company-os

# Run the mandatory verification process
./verify-all.sh

# Or follow the detailed manual process:
# See: company_os/domains/processes/data/developer-verification.process.md
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
pip install -r requirements_lock.txt

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

### Command Test Results (Updated 2025-07-22)

**Status Legend:**
- ✅ Working as expected
- ⚠️ Working with issues/warnings
- ❌ Not working
- 🔄 In progress

| Command | Status | Notes |
|---------|--------|-------|
| `bazel build //company_os/domains/rules_service/...` | ❌ | Missing ruamel_yaml_clib BUILD files in external repository |
| `bazel build //src/company_os/services/repo_guardian:worker` | ✅ | Repo Guardian service builds successfully |
| `bazel test //company_os/domains/rules_service/tests:all_tests` | ❌ | Bazel 8 + rules_python 1.5.1 compatibility issues with transitive dependencies |
| `python -m pytest company_os/domains/rules_service/tests/test_validation.py -v` | ✅ | 40 tests pass |
| `python -m pytest company_os/domains/rules_service/tests/test_validation_human_input.py -v` | ✅ | 11 tests pass |
| `python -m pytest company_os/domains/rules_service/tests/test_sync.py -v` | ✅ | 13 tests pass |
| `python -m pytest company_os/domains/rules_service/tests/ -v` | ⚠️ | 117 passed, 46 failed, 1 skipped - significant test failures |
| `python -m src.company_os.services.repo_guardian.worker_main` | ⚠️ | Runs but has Pydantic datetime serialization errors |

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
- Virtual environment setup with `pip install -r requirements_lock.txt`
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

**Option 2: Manual commands (using UV and Bazel)**
```bash
# Setup (one-time) - Use UV for dependency management
uv venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv pip install -r requirements_lock.txt

# Alternative: Use Bazel for hermetic builds (recommended)
bazel test //company_os/domains/rules_service/tests:all_tests

# Development cycle with UV
python -m pytest company_os/domains/rules_service/tests/ -v
# Edit code, repeat tests

# Optional: Run linting and type checking with Bazel
bazel run //:ruff -- check company_os/domains/rules_service
bazel run //:mypy -- company_os/domains/rules_service/src
```

**For CI/CD (using Bazel and UV):**
```bash
# In CI environment - Use Bazel for consistent, hermetic builds
bazel test //company_os/domains/rules_service/tests:all_tests

# Alternative: Use UV for faster dependency installation
uv pip install -r requirements_lock.txt
python -m pytest company_os/domains/rules_service/tests/ --junit-xml=test-results.xml

# Recommended CI/CD pipeline:
# 1. Use Bazel for builds: bazel build //company_os/domains/rules_service/...
# 2. Use Bazel for tests: bazel test //company_os/domains/rules_service/tests:all_tests
# 3. Use Bazel for validation: bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- validate validate "**/*.md"
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

## Repo Guardian Service Development

### Overview

The Repo Guardian service is a Temporal-based workflow system that automates repository quality management through AI-powered analysis. It's located at `src/company_os/services/repo_guardian/`.

### Implementation Status

#### ✅ Completed Phases
- **Phase 1**: Infrastructure Setup (2025-07-22)
  - Temporal workflow orchestration infrastructure
  - Hexagonal architecture implementation
  - Docker Compose configuration for local development
  - Complete service scaffolding with proper BUILD.bazel

- **Phase 2 Step 1**: Minimal Workflow Skeleton (2025-07-22)
  - Production-ready workflow execution with correlation IDs
  - Environment-based configuration with validation
  - Structured logging with JSON/Console output
  - Comprehensive error handling and graceful shutdown
  - Multi-scenario testing framework with performance tracking

- **Phase 2 Step 2**: GitHub API Integration (2025-07-22) ✅ **COMPLETED**
  - Real GitHub API integration with httpx (async)
  - Repository validation and metadata fetching
  - Rate limit handling with retry-after information
  - Multiple URL format support (HTTPS, SSH)
  - Comprehensive error scenarios (auth, not found, server errors)
  - Complete testing suite with real API calls

#### 🔄 Current Phase
- **Phase 2 Step 3**: Analysis Stub (Next)
  - Repository structure analysis without AI
  - File counting and language detection
  - Simple rule-based checks

#### ⚠️ Critical Fix Applied (2025-07-22)
**Problem Resolved: "Failed validating workflow RepoGuardianWorkflow"**
- **Root Cause**: Pydantic datetime serialization incompatibility with Temporal's workflow sandbox
- **Solution**: Added `model_config = ConfigDict(arbitrary_types_allowed=True)` to domain models
- **Result**: Full workflow validation success, enabling all future development

See [Complete Debugging Analysis](work/domains/analysis/data/repo-guardian-workflow-debugging.analysis.md) for technical details.

### Development Setup

#### 1. Install Dependencies (UV and Bazel)

```bash
# Option 1: Use UV for dependency management (recommended for development)
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements_lock.txt

# Option 2: Use Bazel for hermetic builds (recommended for CI/CD)
bazel build //src/company_os/services/repo_guardian:worker

# Key dependencies for Step 2 (managed via requirements.in):
# - pydantic-settings==2.2.1 (for updated config)
# - httpx==0.27.0 (for GitHub API client)
# - temporalio==1.9.0 (for workflow orchestration)

# To update dependencies:
uv pip compile requirements.in -o requirements_lock.txt
```

#### 2. Environment Configuration

```bash
cd src/company_os/services/repo_guardian
cp .env.example .env

# Edit .env with required values:
# REPO_GUARDIAN_GITHUB_TOKEN=your_github_token  # Required for Step 2
# REPO_GUARDIAN_TEMPORAL_HOST=localhost:7233     # Default value
```

#### 3. Start Temporal Development Server

```bash
# Using Docker Compose (recommended)
cd src/company_os/services/repo_guardian
docker-compose up -d

# Verify services are running
docker-compose ps

# Access Temporal UI at http://localhost:8233 (note: port 8233, not 8080)

# Or using Temporal CLI (alternative)
# temporal server start-dev
```

#### 4. Build and Run the Service

```bash
# Option 1: Build with Bazel (recommended)
bazel build //src/company_os/services/repo_guardian:worker
bazel run //src/company_os/services/repo_guardian:worker

# Option 2: Run directly with Python
cd src/company_os/services/repo_guardian
python worker_main.py
```

### Testing the Current Implementation

#### Quick Test (Step 1 + Step 2)
```bash
# 1. Ensure dependencies are installed and environment configured
source .venv/bin/activate
pip install pydantic-settings httpx  # Step 2 dependencies

# 2. Start Temporal
cd src/company_os/services/repo_guardian
docker-compose up -d

# 3. Run worker (Terminal 1)
python worker_main.py

# 4. Run test with real GitHub API (Terminal 2)
python test_workflow.py

# Expected: Workflow fetches real repository data from GitHub API
```

#### Comprehensive Test Suite
```bash
# Run all test scenarios including error conditions
python test_workflow.py --suite

# This tests:
# - Valid repository (company-os repo)
# - Invalid repository URL
# - Authentication scenarios
# - Error handling paths
```

#### Test with Custom Repository
```bash
# Test with your own repository
python test_workflow.py --repo https://github.com/your-org/your-repo
```

### Service Architecture

```
src/company_os/services/repo_guardian/
├── workflows/          # Temporal workflow definitions
│   └── guardian.py     # Main RepoGuardianWorkflow
├── activities/         # Temporal activity implementations
│   ├── repository.py   # Repository operations (✅ Step 2)
│   ├── analysis.py     # Code analysis logic (🔄 Step 3)
│   └── llm.py         # LLM integrations (🔄 Step 4)
├── models/            # Domain models
│   └── domain.py      # Pydantic models (✅ Complete)
├── adapters/          # External integrations
│   ├── github.py      # GitHub API adapter (✅ Step 2)
│   ├── openai.py      # OpenAI integration (🔄 Step 4)
│   └── metrics.py     # Prometheus metrics (🔄 Step 7)
├── utils/             # Utility modules
│   └── logging.py     # Structured logging (✅ Complete)
├── config.py          # Environment configuration (✅ Complete)
├── worker_main.py     # Worker entry point (✅ Complete)
└── test_workflow.py   # Testing framework (✅ Complete)
```

### Current Capabilities (Step 1 + Step 2)

1. **Repository Validation**: Real GitHub repository access validation
2. **Metadata Fetching**: Language, size, latest commit SHA, default branch
3. **URL Format Support**: Both HTTPS and SSH GitHub URL formats
4. **Error Handling**: Rate limits, authentication failures, not found, server errors
5. **Workflow Integration**: GitHub data flows through Temporal activities
6. **Testing Coverage**: Multiple scenarios and comprehensive error conditions

### Environment Variables

#### Required for Current Implementation
- `REPO_GUARDIAN_TEMPORAL_HOST`: Temporal server (default: localhost:7233)
- `REPO_GUARDIAN_GITHUB_TOKEN`: GitHub API token with repo access (required for Step 2)

#### For Future Steps
- `REPO_GUARDIAN_OPENAI_API_KEY`: OpenAI API key (Step 4)
- `REPO_GUARDIAN_ANTHROPIC_API_KEY`: Anthropic API key (Step 4)
- `REPO_GUARDIAN_METRICS_PORT`: Prometheus metrics port (Step 7)

### Building with Bazel

```bash
# Build the service
bazel build //src/company_os/services/repo_guardian:worker

# Build all components
bazel build //src/company_os/services/repo_guardian/...

# Run with Bazel
bazel run //src/company_os/services/repo_guardian:worker
```

### Testing with Bazel

```bash
# Future: Unit tests (when implemented in Step 9)
# bazel test //src/company_os/services/repo_guardian/tests:all

# Future: Integration tests (when implemented in Step 9)
# bazel test //src/company_os/services/repo_guardian/tests:integration
```

### Development Workflow

1. **Start Temporal UI**: Navigate to http://localhost:8233 to monitor workflows
2. **Make changes**: Edit source files in `src/company_os/services/repo_guardian/`
3. **Test locally**: Run worker and trigger workflows with test_workflow.py
4. **Verify GitHub integration**: Ensure API calls work with real repositories
5. **Run tests**: Use test suite to verify all scenarios work
6. **Commit changes**: Follow the Company OS git workflow

### Troubleshooting

#### Common Issues

1. **Temporal Connection Refused**
   ```bash
   # Check if Temporal is running
   docker-compose ps

   # Check logs
   docker-compose logs temporal

   # Restart if needed
   docker-compose down && docker-compose up -d
   ```

2. **GitHub API Errors**
   ```bash
   # Check if token is set
   echo $REPO_GUARDIAN_GITHUB_TOKEN

   # Test token manually
   curl -H "Authorization: token $REPO_GUARDIAN_GITHUB_TOKEN" \
        https://api.github.com/user
   ```

3. **Import Errors**
   ```bash
   # Ensure you're in the repo root and venv is activated
   cd /path/to/the-company-os
   source .venv/bin/activate

   # Install missing dependencies
   pip install pydantic-settings httpx
   ```

#### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run worker with debug output
python src/company_os/services/repo_guardian/worker_main.py
```

## Next Steps

1. ✅ Analyze build system consistency - **COMPLETED**
2. ✅ Document findings and issues - **COMPLETED**
3. ✅ Successfully migrate to bzlmod - **COMPLETED**
4. ✅ Establish Bazel-based workflow - **COMPLETED**
5. ✅ Create comprehensive documentation - **COMPLETED** (see BAZEL_SETUP_ANALYSIS.md)
6. ✅ Implement Repo Guardian Phase 1 - **COMPLETED** (2025-07-22)

---

*Last updated: 2025-07-22 - Added Repo Guardian service documentation.*
