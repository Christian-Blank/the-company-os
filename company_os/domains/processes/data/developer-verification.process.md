---
title: "Developer Verification Process - Complete System Validation"
version: 1.0
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-22T19:19:00-07:00"
parent_charter: "os/domains/charters/data/company-os.charter.md"
tags: ["process", "verification", "quality-assurance", "testing", "build-validation"]
---

# **Developer Verification Process - Complete System Validation**

**MANDATORY PROCESS**: This document defines the exact step-by-step verification process that MUST be followed after every development change to ensure system integrity and prevent quality regression.

**Source of Truth**: This process is the definitive guide for all development verification activities. All other documentation must reference this process.

---

## **Process Overview**

This verification process consists of 8 mandatory stages that must be executed in order. Each stage has specific pass/fail criteria and includes exact command-line instructions with expected outputs.

### **When to Execute This Process**
- ✅ **After every code change** (minimum: stages 1-3)
- ✅ **After structural changes** (minimum: stages 1-5)
- ✅ **Before committing code** (all stages 1-7)
- ✅ **Before merging branches** (all stages 1-8)
- ✅ **After environment changes** (all stages 1-8)

---

## **Stage 1: Environment Setup Verification**

**Purpose**: Ensure development environment meets exact system requirements

### **1.1 Python Version Verification (CRITICAL)**

**The Problem**: We discovered Python version mismatches causing dependency issues and test failures.

```bash
# Step 1: Check .python-version file
cat .python-version
# Expected Output: 3.12.0
# Source: Repository root .python-version file

# Step 2: Check pyenv configuration
pyenv version
# Expected Output: 3.12.0 (set by /Users/[user]/src/the-company-os/.python-version)

# Step 3: Check system Python version
python --version
# Expected Output: Python 3.12.0 (or 3.12.x)
# CRITICAL: Must match .python-version file

# Step 4: Check which Python is being used
which python
# Expected Output: /Users/[user]/.pyenv/shims/python (if using pyenv)
# OR: python: aliased to python3 (acceptable if python3 is 3.12.x)

# FAILURE INDICATORS:
# - python --version shows 3.11.x, 3.10.x, or lower
# - Version mismatch between .python-version and actual python
# - "command not found" for python

# RESOLUTION STEPS:
# If pyenv is installed but wrong version:
pyenv install 3.12.0
pyenv local 3.12.0
python --version  # Verify now shows 3.12.0

# If pyenv not installed:
# macOS: brew install pyenv
# Add to shell profile: eval "$(pyenv init -)"
# Restart shell, then: pyenv install 3.12.0 && pyenv local 3.12.0

# If system Python is wrong:
# macOS: brew install python@3.12
# Ubuntu: sudo apt install python3.12
# Windows: Download from python.org

# VERIFICATION:
python --version | grep -E "Python 3\.12\.[0-9]+"
echo $?  # Must return 0 (success)
```

### **1.2 Virtual Environment Setup and Verification**

**Using Standard Python venv** (Not uv - verified from repository evidence)

```bash
# CRITICAL: Remove existing venv if Python version is wrong
source venv/bin/activate 2>/dev/null && python --version | grep -q "3\.12" || {
    echo "❌ Virtual environment has wrong Python version, recreating..."
    deactivate 2>/dev/null || true
    rm -rf venv
}

# Step 1: Create virtual environment with correct Python
python -m venv venv
# Expected: No errors, venv/ directory created

# Step 2: Activate virtual environment
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate     # Windows

# Expected Output: (venv) appears in prompt

# Step 3: Verify virtual environment Python version
python --version
# Expected: Python 3.12.x (MUST match system Python)

# Step 4: Verify virtual environment location
which python
# Expected: /path/to/repo/venv/bin/python

# FAILURE INDICATORS:
# - Virtual environment Python version doesn't match system
# - (venv) doesn't appear in prompt
# - which python doesn't point to venv/bin/python

# RESOLUTION:
# Always recreate venv if version is wrong:
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
python --version  # Verify correct version
```

### **1.3 Dependency Installation and Verification**

```bash
# PREREQUISITE: Virtual environment must be activated
echo $VIRTUAL_ENV | grep -q venv || {
    echo "❌ Virtual environment not activated"
    exit 1
}

# Step 1: Upgrade pip to latest version
pip install --upgrade pip
# Expected: Successfully upgraded pip

# Step 2: Install dependencies from lock file
pip install -r requirements_lock.txt
# Expected: Successfully installed [package list]
# Expected: No dependency conflicts
# Expected: No compilation errors

# Step 3: Verify no broken dependencies
pip check
# Expected Output: No broken requirements found.

# Step 4: Verify core dependencies are present
pip list | grep -E "(pydantic|temporalio|pytest|bazel)" || {
    echo "❌ Core dependencies missing"
    pip list
    exit 1
}

# Step 5: Verify dependency versions match lock file
pip list --format=freeze > current_deps.txt
diff requirements_lock.txt current_deps.txt || {
    echo "⚠️ Dependencies don't match lock file"
    echo "Consider running: uv pip compile requirements.in --generate-hashes -o requirements_lock.txt"
}
rm -f current_deps.txt

# FAILURE RESOLUTION:
# If dependency conflicts:
pip install --force-reinstall -r requirements_lock.txt
pip check

# If missing dependencies:
pip install -r requirements_lock.txt
pip check
```

### **1.4 Tool Version Verification**

```bash
# Bazel Version Check
bazel version
# Expected Output: Bazel release 8.x.x
# Source: https://bazel.build/install

bazel version | grep -q "release 8\." || {
    echo "❌ Bazel version must be 8.x.x"
    echo "Install: https://bazel.build/install"
    exit 1
}

# Git Version Check
git --version
# Expected: git version 2.x.x (any recent version)

# Git Repository Verification
git rev-parse --is-inside-work-tree
# Expected: true

git remote get-url origin
# Expected: git@github.com:Christian-Blank/the-company-os.git
# Source: Repository configuration
```

**Stage 1 Pass Criteria**: ✅ All commands return expected outputs with exit code 0

---

## **Stage 2: Repository State Verification**

**Purpose**: Establish known-good baseline before making changes

### **2.1 Repository Cleanliness Check**

```bash
# Step 1: Check working directory status
git status --porcelain
# Expected Output (Clean State): (no output)
# Expected Output (With Changes): Only expected modifications

# Step 2: Check for untracked files that might cause issues
git ls-files --others --exclude-standard | grep -v -E "\.(log|tmp|cache)$" | head -10
# Expected: No unexpected untracked files

# Step 3: Verify we're on the correct branch
git branch --show-current
# Expected: Your intended working branch

# Step 4: Check commit history
git log --oneline -5
# Review recent commits for context
```

### **2.2 Pre-commit Hook Verification**

```bash
# Step 1: Run pre-commit on all files
pre-commit run --all-files

# Expected Output (Success):
# Rules Service - Sync.....................................................Passed
# Rules Service - Validate.................................................Passed
# trim trailing whitespace.................................................Passed
# fix end of files.........................................................Passed
# check yaml...............................................................Passed
# check for added large files..............................................Passed
# check for merge conflicts................................................Passed

# FAILURE INDICATORS:
# - Any hook shows "Failed"
# - Exit code non-zero

# RESOLUTION:
# Fix any failing hooks before proceeding
# Some hooks auto-fix issues - review changes with git diff
```

**Stage 2 Pass Criteria**: ✅ Clean repository state, pre-commit hooks pass

---

## **Stage 3: Build System Verification**

**Purpose**: Ensure all build targets compile successfully

### **3.1 Bazel Build Verification**

```bash
# Step 1: Clean previous build artifacts
bazel clean

# Step 2: Build all Repo Guardian components
bazel build //src/company_os/services/repo_guardian/...
# Expected: INFO: Build completed successfully

# Step 3: Build Rules Service components
bazel build //company_os/domains/rules_service/...
# Known Issue: May fail with ruamel_yaml_clib errors
# Document status in verification log

# Step 4: Build core libraries
bazel build //shared/libraries/company_os_core/...
# Expected: INFO: Build completed successfully

# EXPECTED OUTPUTS:
# ✅ Repo Guardian: Build completed successfully
# ❌ Rules Service: Currently failing (document in Stage 8)
# ✅ Core Libraries: Build completed successfully

# FAILURE DIAGNOSIS:
# Common errors and solutions:
# 1. "ruamel_yaml_clib" missing: Known issue with Rules Service
# 2. Import errors: Check Python path configuration
# 3. Missing dependencies: Verify Stage 1 completed successfully
```

### **3.2 Import Verification**

```bash
# Step 1: Test core imports
python -c "
import sys
sys.path.insert(0, '.')
try:
    from src.company_os.services.repo_guardian.models.domain import WorkflowInput
    print('✅ Repo Guardian imports working')
except Exception as e:
    print(f'❌ Repo Guardian import failed: {e}')
    sys.exit(1)
"

# Step 2: Test Rules Service imports
python -c "
import sys
sys.path.insert(0, '.')
try:
    from company_os.domains.rules_service.src.validation import ValidationService
    print('✅ Rules Service imports working')
except Exception as e:
    print(f'❌ Rules Service import failed: {e}')
    # Note: This may fail due to known dependency issues
"
```

**Stage 3 Pass Criteria**: ✅ Critical builds pass, import errors documented

---

## **Stage 4: Test Suite Verification**

**Purpose**: Ensure all tests run and document failure patterns

### **4.1 Rules Service Test Execution**

```bash
# Step 1: Run Rules Service validation tests
python -m pytest company_os/domains/rules_service/tests/test_validation.py -v
# Expected: 40 tests should pass

# Step 2: Run Rules Service sync tests
python -m pytest company_os/domains/rules_service/tests/test_sync.py -v
# Expected: 13 tests should pass

# Step 3: Run full Rules Service test suite
python -m pytest company_os/domains/rules_service/tests/ -v --tb=short
# Document results: Expected ~117 passed, ~46 failed
# Known failure rate: ~28% (document specific failures)

# CRITICAL: Record test results
python -m pytest company_os/domains/rules_service/tests/ --tb=no -q | tee test_results.log
echo "Test results logged to test_results.log"
```

### **4.2 Repo Guardian Test Verification**

```bash
# Step 1: Test Temporal workflow imports
cd src/company_os/services/repo_guardian
python -c "
try:
    from workflows.guardian import RepoGuardianWorkflow
    from models.domain import WorkflowInput
    print('✅ Temporal imports successful')
except Exception as e:
    print(f'❌ Temporal import failed: {e}')
    exit(1)
"
cd ../../..

# Step 2: Test basic workflow structure
# Note: Full runtime testing requires Temporal server
```

**Stage 4 Pass Criteria**: ✅ Core tests pass, failure patterns documented

---

## **Stage 5: Runtime Verification**

**Purpose**: Test actual service execution and runtime behavior

### **5.1 Temporal Service Runtime Test**

```bash
# PREREQUISITE: Docker or Temporal CLI must be available

# Step 1: Check if Temporal server is available
curl -f http://localhost:7233/api/v1/namespaces/default 2>/dev/null || {
    echo "⚠️ Temporal server not running"
    echo "Start with: cd src/company_os/services/repo_guardian && docker-compose up -d"
    echo "Or: temporal server start-dev"
}

# Step 2: Test workflow registration (if Temporal is running)
cd src/company_os/services/repo_guardian
timeout 10 python worker_main.py || {
    echo "⚠️ Worker failed to start or has runtime issues"
    echo "Known issue: Pydantic datetime serialization error"
    echo "Status: Under investigation"
}
cd ../../..
```

### **5.2 CLI Command Verification**

```bash
# Step 1: Test Rules Service CLI (if available)
python -m company_os.domains.rules_service.adapters.cli.main --help 2>/dev/null || {
    echo "⚠️ Rules Service CLI not accessible via Python module"
    echo "Known issue: Module path configuration"
}

# Step 2: Test basic Python module structure
python -c "
import sys
sys.path.insert(0, '.')
try:
    import company_os
    print('✅ Company OS module accessible')
except Exception as e:
    print(f'❌ Module import failed: {e}')
"
```

**Stage 5 Pass Criteria**: ✅ Runtime issues documented, basic services accessible

---

## **Stage 6: Integration Verification**

**Purpose**: Test service integration points and dependencies

### **6.1 Docker Integration Test**

```bash
# Step 1: Verify Docker is available
docker --version || {
    echo "❌ Docker not available"
    echo "Install: https://docs.docker.com/get-docker/"
    exit 1
}

# Step 2: Test Repo Guardian Docker Compose
cd src/company_os/services/repo_guardian
docker-compose config || {
    echo "❌ Docker Compose configuration invalid"
    exit 1
}

# Optional: Start services for integration test
# docker-compose up -d
# docker-compose ps
# docker-compose down

cd ../../..
```

### **6.2 Environment Configuration Test**

```bash
# Step 1: Check required environment variables
echo "Checking Repo Guardian environment configuration..."
cd src/company_os/services/repo_guardian

# Check if .env.example exists
test -f .env.example || {
    echo "❌ .env.example missing"
    exit 1
}

# Check if .env exists (optional but recommended)
test -f .env || echo "⚠️ .env file not configured (copy from .env.example)"

cd ../../..
```

**Stage 6 Pass Criteria**: ✅ Integration points tested, configuration verified

---

## **Stage 7: Full System Verification**

**Purpose**: Complete end-to-end system validation

### **7.1 Complete Build Suite**

```bash
# Step 1: Build all available targets
echo "Building all available Bazel targets..."

# Build Repo Guardian (should succeed)
bazel build //src/company_os/services/repo_guardian:worker
echo "Repo Guardian build: $?"

# Attempt Rules Service build (may fail - document)
bazel build //company_os/domains/rules_service/... 2>&1 | tee rules_service_build.log
echo "Rules Service build: $? (see rules_service_build.log)"

# Build shared libraries
bazel build //shared/libraries/company_os_core/...
echo "Shared libraries build: $?"
```

### **7.2 Documentation Consistency Check**

```bash
# Step 1: Verify Python version consistency
echo "Checking Python version consistency..."
PYTHON_VERSION_FILE=$(cat .python-version)
PYTHON_ACTUAL=$(python --version | cut -d' ' -f2)

echo "Required (per .python-version): $PYTHON_VERSION_FILE"
echo "Actual (python --version): $PYTHON_ACTUAL"

echo "$PYTHON_ACTUAL" | grep -q "^$PYTHON_VERSION_FILE" || {
    echo "❌ CRITICAL: Python version mismatch detected"
    echo "This was the root cause of many issues"
    exit 1
}
```

### **7.3 Quality Gate Summary**

```bash
# Generate verification summary
echo "=== VERIFICATION SUMMARY ==="
echo "Stage 1 - Environment: $(python --version | grep -q '3\.12' && echo '✅ PASS' || echo '❌ FAIL')"
echo "Stage 3 - Builds: Mixed (Repo Guardian ✅, Rules Service ❌)"
echo "Stage 4 - Tests: Mixed (~72% pass rate documented)"
echo "Stage 5 - Runtime: Temporal issues documented"
echo "Stage 7 - Documentation: Python version consistency critical"
echo "=========================="
```

**Stage 7 Pass Criteria**: ✅ System state documented, critical issues identified

---

## **Stage 8: Automation and Documentation**

**Purpose**: Create reusable verification scripts and update documentation

### **8.1 Create Verification Scripts**

```bash
# Create automation script
cat > verify-all.sh << 'EOF'
#!/bin/bash
set -e

echo "Starting Company OS Developer Verification Process..."

# Stage 1: Environment
echo "Stage 1: Environment Verification"
python --version | grep -q "3\.12" || {
    echo "❌ Python version must be 3.12.x"
    exit 1
}

# Virtual environment check
source venv/bin/activate
python --version | grep -q "3\.12" || {
    echo "❌ Virtual environment has wrong Python version"
    exit 1
}

pip check || {
    echo "❌ Dependency conflicts detected"
    exit 1
}

echo "✅ Stage 1 passed"

# Stage 2: Repository
echo "Stage 2: Repository State"
pre-commit run --all-files || {
    echo "❌ Pre-commit hooks failed"
    exit 1
}
echo "✅ Stage 2 passed"

# Stage 3: Builds
echo "Stage 3: Build Verification"
bazel build //src/company_os/services/repo_guardian:worker || {
    echo "❌ Repo Guardian build failed"
    exit 1
}
echo "✅ Stage 3 critical builds passed"

# Stage 4: Tests
echo "Stage 4: Core Tests"
python -m pytest company_os/domains/rules_service/tests/test_validation.py -q || {
    echo "❌ Core validation tests failed"
    exit 1
}
echo "✅ Stage 4 core tests passed"

echo "🎉 Verification completed successfully"
EOF

chmod +x verify-all.sh
echo "Created verify-all.sh automation script"
```

### **8.2 Update Documentation References**

```bash
# Note: Links to be added to documentation:
echo "Documentation updates needed:"
echo "1. DEVELOPER_WORKFLOW.md - Reference this process"
echo "2. Service README files - Link to relevant sections"
echo "3. .python-version enforcement in CI/CD"
echo "4. Pre-commit hook improvements"
```

**Stage 8 Pass Criteria**: ✅ Automation created, documentation plan established

---

## **Critical Findings and Issues**

Based on verification testing on 2025-07-22:

### **Environment Issues**
1. **Python Version Mismatch**: `.python-version` specifies 3.12.0, but virtual environment uses 3.10.17
2. **Virtual Environment Tool**: Using standard Python `venv` (not uv venv)
3. **Dependency Management**: Using uv for dependency compilation with requirements.in → requirements_lock.txt (evidence-based)

### **Build Issues**
1. **Rules Service**: Bazel build fails with ruamel_yaml_clib missing BUILD files
2. **Repo Guardian**: Bazel build succeeds
3. **Import Paths**: Some services have module path configuration issues

### **Test Issues**
1. **Rules Service**: 28% failure rate (46 failed, 117 passed, 1 skipped)
2. **Test Types**: Core validation tests pass, CLI/integration tests fail significantly

### **Runtime Issues**
1. **Temporal Workflows**: Pydantic datetime serialization error prevents completion
2. **CLI Commands**: Module path issues prevent direct execution

### **Root Cause Analysis**
The Python version mismatch (3.12.0 expected, 3.10.17 actual) appears to be the root cause of many dependency and compatibility issues.

---

## **Resolution Protocol**

### **Immediate Actions Required**
1. **Fix Python Version**: Recreate virtual environment with Python 3.12.0
2. **Update Dependencies**: Reinstall all packages with correct Python version
3. **Verify Build Compatibility**: Test if Python 3.12 resolves build issues

### **Process Enforcement**
1. **Mandatory**: Run this verification process before any commits
2. **Automation**: Use `verify-all.sh` script for consistent verification
3. **Documentation**: Update all references to link to this process

### **Success Metrics**
- Python version consistency: 100%
- Core test pass rate: >95%
- Build success rate: Document and track improvements
- Documentation accuracy: 100% verified

---

## **References**

### **Evidence Sources**
- `.python-version` file: Contains "3.12.0"
- `pyenv version` output: "3.12.0 (set by .python-version)"
- `python --version` output: "Python 3.10.17" (mismatch identified)
- Directory listing: `venv/` directory exists (not `.venv/`)
- `.gitignore` patterns: Both `venv/` and `.venv/` included
- Test results: 28% failure rate documented from actual pytest run

### **Documentation Links**
- [Python Installation Guide](https://python.org/downloads/)
- [pyenv Installation](https://github.com/pyenv/pyenv#installation)
- [Bazel Installation](https://bazel.build/install)
- [Docker Installation](https://docs.docker.com/get-docker/)

---

**CRITICAL SUCCESS FACTOR**: This process MUST prevent Python version mismatches, which were identified as the root cause of multiple system issues including test failures, dependency conflicts, and runtime errors.

**Next Update**: After implementing Python 3.12 environment, re-run this verification process and update success criteria based on improved results.
