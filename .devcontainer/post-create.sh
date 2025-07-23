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
bazel version | head -1
git --version

# Create UV virtual environment
echo "🐍 Setting up Python virtual environment..."
uv venv .venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source .venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
uv pip sync requirements_lock.txt

# Verify core dependencies
echo "🔍 Verifying core dependencies..."
python -c "import pydantic, temporalio, pytest; print('✅ Core dependencies available')"

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

# Add .venv/bin to PATH when activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    export PATH="$VIRTUAL_ENV/bin:$PATH"
fi
EOF

# Source the new aliases
source ~/.bashrc

# Run a quick verification to ensure everything works
echo "🧪 Running quick verification..."
python --version | grep "3.12" || { echo "❌ Python version issue"; exit 1; }
uv pip check || { echo "❌ Dependency check failed"; exit 1; }
bazel version | grep -q "release 8\." || { echo "❌ Bazel version issue"; exit 1; }

echo ""
echo "🎉 Dev container setup complete!"
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
echo "✨ Happy coding!"
