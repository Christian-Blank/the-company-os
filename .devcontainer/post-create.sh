#!/bin/bash
#
# Company OS Dev Container Post-Creation Setup
# This script runs after the dev container is created to set up the development environment
#

set -euo pipefail

echo "🚀 Setting up Company OS development environment..."

# Ensure we're in the right directory
cd /workspaces/the-company-os

# Verify tools are available
echo "📋 Checking tool versions..."
python3 --version
uv --version
# Show Bazel release without tripping pipefail
bazel --version
git --version

# Verify pipx-installed CLI tools
echo "🔧 Checking pipx-installed CLI tools..."
pre-commit --version
ruff --version
mypy --version

# Create UV virtual environment (idempotent)
echo "🐍 Setting up Python virtual environment..."
uv venv .venv

# Install Python dependencies using UV
echo "📦 Installing Python dependencies..."
uv pip sync requirements_lock.txt

# Verify core dependencies in the project venv
echo "🔍 Verifying core dependencies..."
.venv/bin/python -c "import pydantic, temporalio, pytest; print('✅ Core dependencies available')"

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
pre-commit install

# Make verification script executable
echo "🔨 Making verification script executable..."
chmod +x verify-all.sh

# Set up git configuration for container
echo "⚙️  Configuring git for container..."
git config --global --add safe.directory /workspaces/the-company-os
git config --global init.defaultBranch main

# Create useful aliases
echo "📝 Setting up shell aliases..."
cat >> ~/.bashrc << 'EOF'

# Company OS development aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'

# Python/UV aliases
alias py='python'
alias pyi='python -i'
alias activate='source .venv/bin/activate'

# Bazel aliases
alias bb='bazel build'
alias bt='bazel test'
alias br='bazel run'
alias bc='bazel clean'

# Company OS specific
alias verify='./verify-all.sh'
alias verify-env='./verify-all.sh --stage 1'
alias verify-build='./verify-all.sh --stage 1-3'

# Enable color output
export CLICOLOR=1
export LSCOLORS=ExFxBxDxCxegedabagacad

# Ensure VIRTUAL_ENV is set
export VIRTUAL_ENV=/workspaces/the-company-os/.venv
export PATH="$VIRTUAL_ENV/bin:$PATH"
EOF

# Source the new aliases
source ~/.bashrc

# Run a quick verification to ensure everything works
echo "🧪 Running quick verification..."
python --version | grep "3.12" || { echo "❌ Python version issue"; exit 1; }
uv pip check || { echo "❌ Dependency check failed"; exit 1; }

# Fail if we're not on major 8.x
if ! bazel --version | grep -qE '^bazel 8\.'; then
    echo "❌ Bazel major version is not 8.x"
    exit 1
fi

# Verify pipx tools are accessible
echo "🔍 Verifying pipx CLI tools..."
which pre-commit > /dev/null || { echo "❌ pre-commit not in PATH"; exit 1; }
which ruff > /dev/null || { echo "❌ ruff not in PATH"; exit 1; }
which mypy > /dev/null || { echo "❌ mypy not in PATH"; exit 1; }

echo ""
echo "🎉 Dev container setup complete!"
echo ""
echo "🔧 Tool Architecture Overview:"
echo "   • Project dependencies: UV-managed .venv/ (pydantic, temporalio, pytest, etc.)"
echo "   • CLI tools: pipx-managed isolation (pre-commit, ruff, mypy)"
echo "   • Build system: Bazel 8.x via Bazelisk"
echo ""
echo "🔧 Available commands:"
echo "   ./verify-all.sh          - Run complete verification"
echo "   ./verify-all.sh --stage 1 - Check environment only"
echo "   bazel build //...        - Build all targets"
echo "   bazel test //...         - Run all tests"
echo "   pre-commit run --all-files - Run all quality checks"
echo ""
echo "📚 Documentation:"
echo "   DEVELOPER_WORKFLOW.md    - Quick reference"
echo "   DEVELOPMENT_TEST_PLAN.md - Complete command reference"
echo "   company_os/domains/processes/data/developer-verification.process.md - Detailed process"
echo ""
echo "✨ Happy coding! The environment respects PEP 668 and Ubuntu 24.04 best practices."
