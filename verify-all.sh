#!/bin/bash
set -e

echo "🔍 Company OS Developer Verification Process v1.0"
echo "================================================="

# Stage 1: Environment
echo "📋 Stage 1: Environment Verification"
echo "Checking Python version..."
python --version | grep -q "3\.12" || {
    echo "❌ Python version must be 3.12.x (found: $(python --version))"
    echo "Expected: 3.12.0 (per .python-version file)"
    echo "Run: pyenv install 3.12.0 && pyenv local 3.12.0"
    exit 1
}

echo "Checking virtual environment..."
source venv/bin/activate 2>/dev/null || {
    echo "❌ Virtual environment not found"
    echo "Run: python -m venv venv && source venv/bin/activate"
    exit 1
}

python --version | grep -q "3\.12" || {
    echo "❌ Virtual environment has wrong Python version: $(python --version)"
    echo "Expected: Python 3.12.x"
    echo "Run: rm -rf venv && python -m venv venv && source venv/bin/activate"
    exit 1
}

echo "Checking dependencies..."
pip check || {
    echo "❌ Dependency conflicts detected"
    echo "Run: pip install --force-reinstall -r requirements_lock.txt"
    exit 1
}

echo "✅ Stage 1 passed: Environment verified"

# Stage 2: Repository
echo ""
echo "📋 Stage 2: Repository State"
echo "Running pre-commit hooks..."
pre-commit run --all-files || {
    echo "❌ Pre-commit hooks failed"
    echo "Fix issues and try again"
    exit 1
}
echo "✅ Stage 2 passed: Repository state clean"

# Stage 3: Builds
echo ""
echo "📋 Stage 3: Build Verification"
echo "Building Repo Guardian..."
bazel build //src/company_os/services/repo_guardian:worker || {
    echo "❌ Repo Guardian build failed"
    exit 1
}

echo "Building shared libraries..."
bazel build //shared/libraries/company_os_core/... || {
    echo "❌ Shared libraries build failed"
    exit 1
}

echo "✅ Stage 3 passed: Critical builds successful"

# Stage 4: Tests
echo ""
echo "📋 Stage 4: Core Tests"
echo "Running core validation tests..."
python -m pytest company_os/domains/rules_service/tests/test_validation.py -q || {
    echo "❌ Core validation tests failed"
    exit 1
}

echo "Running sync tests..."
python -m pytest company_os/domains/rules_service/tests/test_sync.py -q || {
    echo "❌ Sync tests failed"
    exit 1
}

echo "✅ Stage 4 passed: Core tests successful"

# Summary
echo ""
echo "🎉 Verification completed successfully!"
echo "================================================="
echo "✅ Environment: Python 3.12.x with correct venv"
echo "✅ Repository: Clean state, pre-commit hooks pass"
echo "✅ Builds: Critical services build successfully"
echo "✅ Tests: Core functionality tests pass"
echo ""
echo "📖 Full process documented in:"
echo "   company_os/domains/processes/data/developer-verification.process.md"
