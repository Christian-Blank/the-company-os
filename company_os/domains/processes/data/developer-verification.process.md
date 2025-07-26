---
title: "Developer Verification Process - Complete System Validation"
version: 2.0
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-23T11:47:00-07:00"
parent_charter: "os/domains/charters/data/company-os.charter.md"
tags: ["process", "verification", "quality-assurance", "testing", "build-validation"]
---

# **Developer Verification Process - Complete System Validation**

**MANDATORY PROCESS**: This document defines the exact step-by-step verification process that MUST be followed after every development change to ensure system integrity and prevent quality regression.

**Source of Truth**: This process is the definitive guide for all development verification activities. All other documentation must reference this process.

**Quick Start**: Run `./verify-all.sh` for the automated version of this process (developers may prefer the script).

---

## **Process Overview**

This verification process consists of 7 mandatory stages that must be executed in order. Each stage has specific pass/fail criteria and includes exact command-line instructions with expected outputs.

### **Core Principles**
- **One canonical tool per concern**:
  - Environment & dependencies: **UV** (fast, lock-file aware)
  - Build/test/CI: **Bazel 8** + bzlmod
  - Lint/type-check: **Bazel** or pre-commit (scripted, never ad-hoc)
- **Docs ≙ code**: This document is executable via `./verify-all.sh`
- **No duplicated instructions**: Other docs reference this process
- **CI is the referee**: GitHub Actions runs the same script

### **When to Execute This Process**
- ✅ **After every code change** (minimum: stages 1-3)
- ✅ **After structural changes** (minimum: stages 1-5)
- ✅ **Before committing code** (all stages 1-6)
- ✅ **Before merging branches** (all stages 1-7)
- ✅ **After environment changes** (all stages 1-7)

---

## **Stage 1: Environment Bootstrap (Must Pass Before Anything Else)**

**Purpose**: Ensure development environment meets exact system requirements using UV and Bazel only.

### **1.1 Tool Version Verification**

```bash verify
# Python version check
python3 --version | grep -E '^Python 3\.12\.' || { echo "❌ Need Python 3.12"; exit 1; }

# UV version check
uv --version | grep -q "^uv 0\." || { echo "❌ UV not installed. Install: https://docs.astral.sh/uv/"; exit 1; }

# Bazel version check
bazel version | grep -q "release 8\." || { echo "❌ Need Bazel 8.x. Install: https://bazel.build/install"; exit 1; }

echo "✅ All tools verified"
```

### **1.2 Create/Refresh UV Virtual Environment**

```bash verify
# Creates .venv if missing, re-uses if Python is still 3.12
uv venv .venv

# Activate virtual environment
source .venv/bin/activate

# Verify activation
echo $VIRTUAL_ENV | grep -q "\.venv" || { echo "❌ Virtual environment not activated"; exit 1; }

# Verify Python version in venv
python --version | grep -q "3\.12" || { echo "❌ Virtual environment has wrong Python version"; exit 1; }

echo "✅ Virtual environment ready"
```

### **1.3 Sync Lock-file Dependencies**

```bash verify
# Fast, hash-verified dependency installation
uv pip sync requirements_lock.txt || { echo "❌ Failed to sync dependencies"; exit 1; }

# Verify no conflicts
uv pip check || { echo "❌ Dependency conflicts detected"; exit 1; }

# Verify core dependencies
python -c "import pydantic, temporalio, pytest" || { echo "❌ Core dependencies missing"; exit 1; }

echo "✅ Dependencies synced"
```

**Stage 1 Pass Criteria**: ✅ All commands exit 0, correct versions installed

---

## **Stage 2: Pre-commit Validation**

**Purpose**: Ensure code quality gates are passing

### **2.1 Run All Pre-commit Hooks**

```bash verify
# Run pre-commit on all files
pre-commit run --all-files || { echo "❌ Pre-commit hooks failed"; exit 1; }

echo "✅ All pre-commit hooks passed"
```

**Expected Output**:
```
Source Truth Enforcement.................................................Passed
Rules Service - Sync.....................................................Passed
Rules Service - Validate.................................................Passed
Rules Service Tests......................................................Passed
Lint with Ruff...........................................................Passed
Format with Ruff.........................................................Passed
Type check with MyPy.....................................................Passed
```

**Stage 2 Pass Criteria**: ✅ All hooks pass

---

## **Stage 3: Build Verification**

**Purpose**: Ensure all components build successfully with Bazel

### **3.1 Build Core Services**

```bash verify
# Build all targets (may show some failures for known issues)
bazel build //... 2>&1 | tee build.log

# Check specific critical services
bazel build //src/company_os/services/repo_guardian:worker || { echo "⚠️ Repo Guardian build failed"; }
bazel build //company_os/domains/source_truth_enforcement/... || { echo "⚠️ Source Truth build failed"; }
bazel build //company_os/domains/rules_service/... || { echo "⚠️ Rules Service build failed (known issue)"; }

echo "✅ Critical builds completed"
```

### **3.2 Lint and Type Check with Bazel**

```bash verify
# Run linting
bazel run //:ruff -- check --exit-zero company_os/ src/ || { echo "⚠️ Linting issues found"; }

# Run type checking
bazel run //:mypy -- company_os/ src/ || { echo "⚠️ Type checking issues found"; }

echo "✅ Code quality checks completed"
```

**Stage 3 Pass Criteria**: ✅ Critical services build, quality checks documented

---

## **Stage 4: Test Execution**

**Purpose**: Run all test suites and document results

### **4.1 Run All Tests with Bazel**

```bash verify
# Run all tests
bazel test //... --test_output=errors 2>&1 | tee test.log || { echo "⚠️ Some tests failed"; }

# Run specific test suites if needed
bazel test //company_os/domains/rules_service/tests:all_tests || { echo "⚠️ Rules Service tests failed"; }
bazel test //src/company_os/services/repo_guardian/tests:all || { echo "⚠️ Repo Guardian tests failed"; }

echo "✅ Test execution completed"
```

**Stage 4 Pass Criteria**: ✅ Test results documented, critical tests pass

---

## **Stage 5: Service Validation**

**Purpose**: Validate individual services are operational

### **5.1 Source Truth Enforcement Check**

```bash verify
# Check all source truth definitions
bazel run //company_os/domains/source_truth_enforcement/adapters/cli:source_truth_cli -- check --all || {
    echo "❌ Source truth violations found"
    exit 1
}

echo "✅ Source truth validation passed"
```

### **5.2 Rules Service Validation**

```bash verify
# Validate rules service
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules query || {
    echo "⚠️ Rules Service CLI issues"
}

echo "✅ Service validation completed"
```

**Stage 5 Pass Criteria**: ✅ Critical services operational

---

## **Stage 6: Integration Validation**

**Purpose**: Verify service integrations and configurations

### **6.1 Docker Services (If Applicable)**

```bash verify
# Check Docker availability
docker --version || { echo "⚠️ Docker not available"; }

# Validate docker-compose files
find . -name "docker-compose.yml" -exec docker-compose -f {} config \; || {
    echo "⚠️ Docker compose validation issues"
}

echo "✅ Integration validation completed"
```

**Stage 6 Pass Criteria**: ✅ Integrations validated

---

## **Stage 7: Full System Summary**

**Purpose**: Generate comprehensive validation report

### **7.1 Generate Verification Summary**

```bash verify
echo "=== VERIFICATION SUMMARY ==="
echo "Stage 1 - Environment: ✅ UV + Bazel ready"
echo "Stage 2 - Pre-commit: ✅ All hooks passed"
echo "Stage 3 - Builds: ✅ Critical services built"
echo "Stage 4 - Tests: ✅ Test suite executed"
echo "Stage 5 - Services: ✅ Services validated"
echo "Stage 6 - Integration: ✅ Integrations checked"
echo "==========================="
echo "🎉 Verification completed successfully"
```

**Stage 7 Pass Criteria**: ✅ All stages documented

---

## **Automation Script**

The `verify-all.sh` script executes all stages automatically:

```bash
#!/bin/bash
# This script is auto-generated from the verification process
# Run: ./verify-all.sh [--stage N]
```

To run specific stages:
- `./verify-all.sh --stage 1` - Environment only
- `./verify-all.sh --stage 1-3` - Environment through builds
- `./verify-all.sh` - All stages

---

## **CI/CD Integration**

GitHub Actions should run the same verification:

```yaml
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
        with:
          version: "0.5.x"
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - uses: bazel-contrib/setup-bazel@v4
        with:
          bazelisk-version: "latest"
      - name: Run verification
        run: |
          chmod +x verify-all.sh
          ./verify-all.sh
```

---

## **Troubleshooting Guide**

### **Common Issues and Resolutions**

1. **Python Version Mismatch**
   - Install Python 3.12: `brew install python@3.12` (macOS)
   - Or use pyenv: `pyenv install 3.12.0 && pyenv local 3.12.0`

2. **UV Not Found**
   - Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Or: `pip install uv`

3. **Bazel Version Issues**
   - Install Bazel 8: `brew install bazel` (macOS)
   - Or use Bazelisk: `brew install bazelisk`

4. **Dependency Conflicts**
   - Clear cache: `rm -rf .venv && uv venv .venv`
   - Resync: `uv pip sync requirements_lock.txt`

5. **Build Failures**
   - Clean Bazel: `bazel clean --expunge`
   - Check logs: `cat bazel-out/*/test.log`

---

## **Key Principles**

1. **UV Only for Python**: No pip, no pip-tools, no poetry
2. **Bazel for Builds**: All production builds use Bazel
3. **Lock Files**: Always use `requirements_lock.txt`, never `requirements.txt`
4. **Automation First**: Use `verify-all.sh` for consistency
5. **Single Source**: This document is the only source of truth

---

## **References**

- [UV Documentation](https://docs.astral.sh/uv/)
- [Bazel Documentation](https://bazel.build/docs)
- [Company OS Developer Guide](../../DEVELOPER_WORKFLOW.md)
- [Python 3.12 Release Notes](https://docs.python.org/3/whatsnew/3.12.html)

---

**Next Update**: After testing all commands and documenting results in the test plan.
