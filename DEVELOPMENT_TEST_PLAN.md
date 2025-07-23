# Company OS Development Test Plan

**Purpose**: Comprehensive command validation to ensure all development operations work consistently across environments.

**Methodology**: Execute each command, document actual vs expected output, note failures and resolutions.

---

## Test Matrix Overview

| Category | Total Commands | Status |
|----------|----------------|--------|
| Environment Setup | 12 | 🔄 |
| Build Operations | 15 | 🔄 |
| Test Execution | 10 | 🔄 |
| Code Quality | 8 | 🔄 |
| Service Operations | 12 | 🔄 |
| CI/CD | 5 | 🔄 |
| **TOTAL** | **62** | **🔄** |

**Status Legend**:
- ✅ Working as expected
- ⚠️ Working with issues/warnings
- ❌ Not working
- 🔄 Not tested yet

---

## 1. Environment Setup Commands

### 1.1 Python Version Check
```bash
python3 --version
```
**Expected**: `Python 3.12.x`
**Status**: 🔄
**Notes**: 

### 1.2 Check .python-version File
```bash
cat .python-version
```
**Expected**: `3.12.0`
**Status**: 🔄
**Notes**: 

### 1.3 UV Installation Check
```bash
uv --version
```
**Expected**: `uv 0.x.x`
**Status**: 🔄
**Notes**: 

### 1.4 Install UV (if needed)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
**Expected**: Successful installation
**Status**: 🔄
**Notes**: 

### 1.5 Bazel Version Check
```bash
bazel version
```
**Expected**: `Bazel release 8.x.x`
**Status**: 🔄
**Notes**: 

### 1.6 Create UV Virtual Environment
```bash
uv venv .venv
```
**Expected**: Creates .venv directory
**Status**: 🔄
**Notes**: 

### 1.7 Activate Virtual Environment
```bash
source .venv/bin/activate
```
**Expected**: `(.venv)` in prompt
**Status**: 🔄
**Notes**: 

### 1.8 Sync Dependencies with UV
```bash
uv pip sync requirements_lock.txt
```
**Expected**: All packages installed with correct versions
**Status**: 🔄
**Notes**: 

### 1.9 Check Dependencies
```bash
uv pip check
```
**Expected**: `No broken requirements found.`
**Status**: 🔄
**Notes**: 

### 1.10 Update Dependencies (if needed)
```bash
uv pip compile requirements.in --generate-hashes -o requirements_lock.txt
```
**Expected**: Updated lock file
**Status**: 🔄
**Notes**: 

### 1.11 Verify Core Imports
```bash
python -c "import pydantic, temporalio, pytest, ruff, mypy"
```
**Expected**: No errors
**Status**: 🔄
**Notes**: 

### 1.12 Pre-commit Installation
```bash
pre-commit install
```
**Expected**: Pre-commit hooks installed
**Status**: 🔄
**Notes**: 

---

## 2. Build Operations

### 2.1 Build All Targets
```bash
bazel build //...
```
**Expected**: All targets build (some known failures OK)
**Status**: 🔄
**Notes**: 

### 2.2 Build Repo Guardian
```bash
bazel build //src/company_os/services/repo_guardian:worker
```
**Expected**: `INFO: Build completed successfully`
**Status**: 🔄
**Notes**: 

### 2.3 Build Source Truth Enforcement
```bash
bazel build //company_os/domains/source_truth_enforcement/...
```
**Expected**: `INFO: Build completed successfully`
**Status**: 🔄
**Notes**: 

### 2.4 Build Rules Service
```bash
bazel build //company_os/domains/rules_service/...
```
**Expected**: May fail with ruamel_yaml issues
**Status**: 🔄
**Notes**: 

### 2.5 Build Specific Library
```bash
bazel build //company_os/domains/rules_service/src:rules_service_lib
```
**Expected**: `INFO: Build completed successfully`
**Status**: 🔄
**Notes**: 

### 2.6 Build CLI Tools
```bash
bazel build //company_os/domains/rules_service/adapters/cli:rules_cli
```
**Expected**: Creates executable
**Status**: 🔄
**Notes**: 

### 2.7 Clean Bazel Cache
```bash
bazel clean
```
**Expected**: Cache cleaned
**Status**: 🔄
**Notes**: 

### 2.8 Deep Clean Bazel
```bash
bazel clean --expunge
```
**Expected**: Complete clean
**Status**: 🔄
**Notes**: 

### 2.9 Query Build Targets
```bash
bazel query //...
```
**Expected**: List of all targets
**Status**: 🔄
**Notes**: 

### 2.10 Query Dependencies
```bash
bazel query "deps(//src/company_os/services/repo_guardian:worker)"
```
**Expected**: Dependency tree
**Status**: 🔄
**Notes**: 

### 2.11 Build with Verbose Output
```bash
bazel build //src/company_os/services/repo_guardian:worker --verbose_failures
```
**Expected**: Detailed error messages if fails
**Status**: 🔄
**Notes**: 

### 2.12 Build Python Wheel
```bash
bazel build //company_os/domains/rules_service:rules_service_wheel
```
**Expected**: Creates .whl file (if configured)
**Status**: 🔄
**Notes**: 

### 2.13 Check Bazel Configuration
```bash
bazel info
```
**Expected**: Bazel workspace info
**Status**: 🔄
**Notes**: 

### 2.14 Verify MODULE.bazel
```bash
cat MODULE.bazel | head -20
```
**Expected**: Shows module configuration
**Status**: 🔄
**Notes**: 

### 2.15 Check Build Logs
```bash
ls -la bazel-out/
```
**Expected**: Build output directories
**Status**: 🔄
**Notes**: 

---

## 3. Test Execution

### 3.1 Run All Tests
```bash
bazel test //...
```
**Expected**: Test results (some failures expected)
**Status**: 🔄
**Notes**: 

### 3.2 Run with Test Output
```bash
bazel test //... --test_output=all
```
**Expected**: Detailed test output
**Status**: 🔄
**Notes**: 

### 3.3 Run Specific Test Suite
```bash
bazel test //company_os/domains/rules_service/tests:test_validation
```
**Expected**: 40 tests pass
**Status**: 🔄
**Notes**: 

### 3.4 Run All Rules Service Tests
```bash
bazel test //company_os/domains/rules_service/tests:all_tests
```
**Expected**: 85+ tests
**Status**: 🔄
**Notes**: 

### 3.5 Run Tests with Coverage
```bash
bazel coverage //company_os/domains/rules_service/tests:all_tests
```
**Expected**: Coverage report
**Status**: 🔄
**Notes**: 

### 3.6 Run Tests with Pytest Directly
```bash
python -m pytest company_os/domains/rules_service/tests/ -v
```
**Expected**: Detailed test output
**Status**: 🔄
**Notes**: 

### 3.7 Run Specific Test File
```bash
python -m pytest company_os/domains/rules_service/tests/test_validation.py -v
```
**Expected**: 40 tests pass
**Status**: 🔄
**Notes**: 

### 3.8 Run Tests with Markers
```bash
python -m pytest -m "not slow" company_os/
```
**Expected**: Fast tests only
**Status**: 🔄
**Notes**: 

### 3.9 Check Test Logs
```bash
cat bazel-testlogs/company_os/domains/rules_service/tests/test_validation/test.log
```
**Expected**: Detailed test log
**Status**: 🔄
**Notes**: 

### 3.10 List Available Tests
```bash
bazel query "tests(//...)"
```
**Expected**: All test targets
**Status**: 🔄
**Notes**: 

---

## 4. Code Quality Commands

### 4.1 Run All Pre-commit Hooks
```bash
pre-commit run --all-files
```
**Expected**: All hooks pass
**Status**: 🔄
**Notes**: 

### 4.2 Run Specific Hook
```bash
pre-commit run source-truth-check --all-files
```
**Expected**: Source truth check passes
**Status**: 🔄
**Notes**: 

### 4.3 Ruff Linting via Bazel
```bash
bazel run //:ruff -- check company_os/ src/
```
**Expected**: Linting results
**Status**: 🔄
**Notes**: 

### 4.4 Ruff Formatting via Bazel
```bash
bazel run //:ruff -- format company_os/ src/
```
**Expected**: Files formatted
**Status**: 🔄
**Notes**: 

### 4.5 MyPy Type Checking via Bazel
```bash
bazel run //:mypy -- company_os/ src/
```
**Expected**: Type check results
**Status**: 🔄
**Notes**: 

### 4.6 Direct Ruff Check
```bash
ruff check .
```
**Expected**: Linting results
**Status**: 🔄
**Notes**: 

### 4.7 Direct MyPy Check
```bash
mypy company_os/
```
**Expected**: Type check results
**Status**: 🔄
**Notes**: 

### 4.8 Update Pre-commit Hooks
```bash
pre-commit autoupdate
```
**Expected**: Hooks updated
**Status**: 🔄
**Notes**: 

---

## 5. Service-Specific Commands

### 5.1 Source Truth CLI - Check All
```bash
bazel run //company_os/domains/source_truth_enforcement/adapters/cli:source_truth_cli -- check --all
```
**Expected**: No violations
**Status**: 🔄
**Notes**: 

### 5.2 Source Truth CLI - Python Version
```bash
bazel run //company_os/domains/source_truth_enforcement/adapters/cli:source_truth_cli -- check --python-version
```
**Expected**: Python version consistency check
**Status**: 🔄
**Notes**: 

### 5.3 Source Truth CLI - Dependencies
```bash
bazel run //company_os/domains/source_truth_enforcement/adapters/cli:source_truth_cli -- check --dependencies
```
**Expected**: Dependency workflow check
**Status**: 🔄
**Notes**: 

### 5.4 Rules Service CLI - Init
```bash
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules init
```
**Expected**: Creates .rules-service.yaml
**Status**: 🔄
**Notes**: 

### 5.5 Rules Service CLI - Query
```bash
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules query
```
**Expected**: Lists all rules
**Status**: 🔄
**Notes**: 

### 5.6 Rules Service CLI - Sync
```bash
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules sync
```
**Expected**: Syncs rules to agent folders
**Status**: 🔄
**Notes**: 

### 5.7 Rules Service CLI - Validate
```bash
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- validate validate "*.md"
```
**Expected**: Validates markdown files
**Status**: 🔄
**Notes**: 

### 5.8 Repo Guardian Worker
```bash
bazel run //src/company_os/services/repo_guardian:worker
```
**Expected**: Worker starts (needs Temporal)
**Status**: 🔄
**Notes**: 

### 5.9 Start Temporal (Docker)
```bash
cd src/company_os/services/repo_guardian && docker-compose up -d
```
**Expected**: Temporal services start
**Status**: 🔄
**Notes**: 

### 5.10 Check Temporal Status
```bash
docker-compose ps
```
**Expected**: All services running
**Status**: 🔄
**Notes**: 

### 5.11 Run Repo Guardian Test
```bash
cd src/company_os/services/repo_guardian && python test_workflow.py
```
**Expected**: Test workflow executes
**Status**: 🔄
**Notes**: 

### 5.12 Stop Temporal
```bash
cd src/company_os/services/repo_guardian && docker-compose down
```
**Expected**: Services stop cleanly
**Status**: 🔄
**Notes**: 

---

## 6. CI/CD Commands

### 6.1 Run Verification Script
```bash
./verify-all.sh
```
**Expected**: All stages pass
**Status**: 🔄
**Notes**: 

### 6.2 Run Specific Stage
```bash
./verify-all.sh --stage 1
```
**Expected**: Stage 1 only
**Status**: 🔄
**Notes**: 

### 6.3 Run Stage Range
```bash
./verify-all.sh --stage 1-3
```
**Expected**: Stages 1-3
**Status**: 🔄
**Notes**: 

### 6.4 Check Git Status
```bash
git status --porcelain
```
**Expected**: Clean or expected changes
**Status**: 🔄
**Notes**: 

### 6.5 Simulate CI Environment
```bash
env -i HOME=$HOME PATH=$PATH bash -c './verify-all.sh'
```
**Expected**: Works in clean environment
**Status**: 🔄
**Notes**: 

---

## Common Issues & Resolutions

### Issue: Python Version Mismatch
**Symptom**: `Python 3.10.x` instead of `3.12.x`
**Resolution**:
```bash
# macOS
brew install python@3.12
# or
pyenv install 3.12.0 && pyenv local 3.12.0
```

### Issue: UV Not Found
**Symptom**: `uv: command not found`
**Resolution**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Add to PATH if needed
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
```

### Issue: Bazel Build Failures
**Symptom**: `ERROR: no such package`
**Resolution**:
```bash
bazel clean --expunge
bazel sync
```

### Issue: Dependency Conflicts
**Symptom**: `pip check` shows conflicts
**Resolution**:
```bash
rm -rf .venv
uv venv .venv
source .venv/bin/activate
uv pip sync requirements_lock.txt
```

### Issue: Pre-commit Failures
**Symptom**: Hooks fail on commit
**Resolution**:
```bash
pre-commit run --all-files
# Fix issues shown
git add -u
git commit
```

---

## Test Execution Log

### Date: _______________
### Tester: _______________
### Environment: _______________

| Command # | Status | Notes |
|-----------|--------|-------|
| 1.1 | 🔄 | |
| 1.2 | 🔄 | |
| ... | ... | ... |

---

## Summary

### Overall Results
- **Total Commands**: 62
- **Passed**: ___
- **Failed**: ___
- **Warnings**: ___
- **Not Applicable**: ___

### Critical Failures
1. 
2. 
3. 

### Recommendations
1. 
2. 
3. 

### Next Steps
1. Fix critical failures
2. Document workarounds
3. Update CI/CD configuration
4. Create automation for common fixes

---

**Last Updated**: Not tested yet
**Next Review**: After initial test run
