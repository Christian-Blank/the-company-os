---
title: "Contributing to Company OS"
type: "guide"
audience: ["developers"]
last_updated: "2025-07-16T15:42:00-07:00"
tags: ["contributing", "development", "setup", "workflow"]
---

# Contributing to Company OS

This guide helps you set up your development environment and contribute effectively to Company OS.

## Development Setup

### Prerequisites
- **Python 3.8+** with pip
- **Bazel 6.0+** - Build system
- **Git** - Version control
- **Pre-commit** - Code quality hooks

### Environment Setup
```bash
# Clone the repository
git clone git@github.com:Christian-Blank/the-company-os.git
cd the-company-os

# Install Python dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Verify setup
bazel build //...
bazel test //company_os/domains/rules_service/tests:test_cli
```

### IDE Configuration

#### VS Code
Recommended extensions:
- **Python** - Python language support
- **Bazel** - Bazel build system support
- **Pre-commit** - Git hooks integration
- **Markdown All in One** - Markdown editing

#### PyCharm
- Configure Bazel plugin
- Set up Python interpreter
- Configure code formatting to match project standards

## Development Workflow

### 1. Start Development Session
```bash
# Navigate to project
cd the-company-os

# Update rules for AI assistants
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules sync

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes
Follow the established patterns:
- **Service architecture** - Hexagonal architecture with clear boundaries
- **Testing patterns** - Comprehensive unit and integration tests
- **Documentation patterns** - Update docs with code changes
- **Code quality** - Follow Python PEP 8 and project conventions

### 3. Test Your Changes
```bash
# Build affected services
bazel build //company_os/domains/affected_service/...

# Run service tests
bazel test //company_os/domains/affected_service/tests:all_tests

# Run integration tests
bazel test //company_os/domains/rules_service/tests:test_integration

# Run full test suite (for major changes)
bazel test //...
```

### 4. Update Documentation
```bash
# Update service documentation
# Edit /company_os/domains/service_name/docs/README.md

# Update global documentation if needed
# Edit /docs/ files

# Validate documentation
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- validate validate *.md
```

### 5. Commit Changes
```bash
# Stage changes
git add -A

# Commit with descriptive message
git commit -m "feat: add new service feature

- Implement core functionality
- Add comprehensive tests
- Update documentation
- Follow established patterns"
```

Pre-commit hooks will automatically:
- Sync rules to agent folders
- Validate markdown files
- Fix trailing whitespace
- Check for large files and merge conflicts

## Code Standards

### Python Code Style
- Follow **PEP 8** style guide
- Use **type hints** for all function signatures
- Maximum line length: **88 characters** (Black formatter)
- Use **docstrings** for all public functions and classes

### Project Structure
Follow the hexagonal architecture pattern:
```
/company_os/domains/service_name/
├── src/                    # Core domain logic
│   ├── __init__.py
│   ├── models.py          # Domain models
│   ├── service.py         # Business logic
│   └── config.py          # Configuration
├── adapters/              # External interfaces
│   ├── cli/               # Command-line interface
│   ├── api/               # REST API (future)
│   └── infrastructure/    # External dependencies
├── tests/                 # All test files
│   ├── test_service.py    # Unit tests
│   ├── test_integration.py # Integration tests
│   └── BUILD.bazel        # Test build config
├── docs/                  # Service documentation
│   ├── README.md          # Service overview
│   ├── api.md             # API documentation
│   └── implementation.md  # Implementation details
└── BUILD.bazel            # Build configuration
```

### Testing Standards
- **Unit tests** - Test individual components in isolation
- **Integration tests** - Test service interactions
- **End-to-end tests** - Test complete workflows
- **Performance tests** - Benchmark critical operations
- **Coverage target** - Focus on critical paths, not arbitrary percentages

### Documentation Standards
- **Service README** - Overview, quick start, and navigation
- **API documentation** - Complete parameter and return descriptions
- **Implementation guides** - Architecture and design decisions
- **Working examples** - All examples must be tested and current

## Testing Patterns

### Unit Tests
```python
"""Test individual components in isolation."""
import pytest
from unittest.mock import Mock, patch
from company_os.domains.service_name.src.service import ServiceClass

class TestServiceClass:
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_dependency = Mock()
        self.service = ServiceClass(self.mock_dependency)

    def test_service_method(self):
        """Test service method behavior."""
        # Arrange
        self.mock_dependency.method.return_value = "expected"

        # Act
        result = self.service.method()

        # Assert
        assert result == "expected"
        self.mock_dependency.method.assert_called_once()
```

### Integration Tests
```python
"""Test service integration points."""
import tempfile
import pytest
from pathlib import Path
from company_os.domains.service_name.src.service import ServiceClass

class TestServiceIntegration:
    def setup_method(self):
        """Set up integration test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.service = ServiceClass(config_path=self.temp_dir)

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)

    def test_end_to_end_workflow(self):
        """Test complete service workflow."""
        # Test full workflow from input to output
        result = self.service.process_workflow(test_input)
        assert result.success
        assert result.output_matches_expected()
```

### Performance Tests
```python
"""Test performance benchmarks."""
import time
import pytest
from company_os.domains.service_name.src.service import ServiceClass

class TestServicePerformance:
    def test_operation_performance(self):
        """Test operation completes within time limit."""
        service = ServiceClass()

        start_time = time.time()
        result = service.expensive_operation()
        end_time = time.time()

        assert result.success
        assert (end_time - start_time) < 5.0  # 5 second limit
```

## Service Creation Guide

### 1. Create Service Structure
```bash
# Create service directory
mkdir -p company_os/domains/new_service/{src,adapters,tests,docs}

# Create basic files
touch company_os/domains/new_service/src/{__init__.py,models.py,service.py,config.py}
touch company_os/domains/new_service/adapters/{__init__.py}
touch company_os/domains/new_service/tests/{__init__.py,test_service.py}
touch company_os/domains/new_service/docs/{README.md,api.md,implementation.md}
```

### 2. Create Build Configuration
```python
# company_os/domains/new_service/BUILD.bazel
load("@aspect_rules_py//py:defs.bzl", "py_library")

py_library(
    name = "new_service_lib",
    srcs = glob(["src/**/*.py"]),
    deps = [
        # Add dependencies here
    ],
    visibility = ["//visibility:public"],
)
```

### 3. Implement Core Service
```python
# company_os/domains/new_service/src/service.py
"""Core service implementation."""

from typing import List, Optional
from .models import ServiceModel
from .config import ServiceConfig

class NewService:
    """Main service class following hexagonal architecture."""

    def __init__(self, config: ServiceConfig):
        self.config = config

    def process(self, input_data: str) -> ServiceModel:
        """Process input according to service logic."""
        # Implement business logic here
        return ServiceModel(result="processed")
```

### 4. Create Tests
```python
# company_os/domains/new_service/tests/test_service.py
"""Test suite for new service."""
import pytest
from company_os.domains.new_service.src.service import NewService
from company_os.domains.new_service.src.config import ServiceConfig

class TestNewService:
    def test_service_creation(self):
        """Test service can be created."""
        config = ServiceConfig()
        service = NewService(config)
        assert service is not None
```

### 5. Create Documentation
```markdown
# company_os/domains/new_service/docs/README.md
---
title: "New Service Documentation"
type: "overview"
service: "new_service"
audience: ["users", "developers", "llm"]
last_updated: "2025-07-16T15:42:00-07:00"
tags: ["new-service", "documentation"]
---

# New Service Documentation

Brief description of what this service does.

## Quick Start
[Installation and basic usage instructions]

## Core Concepts
[Key concepts and terminology]

## API Reference
[Link to api.md]

## Implementation Details
[Link to implementation.md]
```

## Build System

### Bazel Basics
```bash
# Build specific target
bazel build //company_os/domains/service_name:target

# Build all targets in package
bazel build //company_os/domains/service_name/...

# Run tests
bazel test //company_os/domains/service_name/tests:all_tests

# Clean build cache
bazel clean
```

### Adding Dependencies
```python
# In BUILD.bazel file
py_library(
    name = "library_name",
    srcs = ["source.py"],
    deps = [
        "//company_os/domains/other_service:other_service_lib",
        "@pypi//requests",  # External dependency
    ],
)
```

### Common Build Patterns
```python
# Python library
py_library(
    name = "lib",
    srcs = glob(["src/**/*.py"]),
    deps = [...],
)

# Python binary
py_binary(
    name = "cli",
    srcs = ["cli.py"],
    deps = [":lib"],
)

# Python test
py_test(
    name = "test",
    srcs = ["test.py"],
    deps = [":lib", "@pypi//pytest"],
)
```

## Git Workflow

### Branch Naming
- **Feature branches**: `feature/description`
- **Bug fixes**: `fix/description`
- **Documentation**: `docs/description`
- **Refactoring**: `refactor/description`

### Commit Messages
Follow conventional commits format:
```
type(scope): description

- Detailed explanation of changes
- Include context and reasoning
- Reference issues if applicable

Co-authored-by: Name <email@example.com>
```

Types:
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **refactor**: Code refactoring
- **test**: Test additions or changes
- **chore**: Maintenance tasks

### Pull Request Process
1. Create feature branch
2. Make changes following standards
3. Add tests and documentation
4. Ensure all tests pass
5. Create pull request with clear description
6. Address review feedback
7. Merge after approval

## Code Review Guidelines

### For Authors
- **Test your changes** - All tests must pass
- **Update documentation** - Keep docs current with code
- **Follow standards** - Consistent with project patterns
- **Provide context** - Clear PR description and commit messages

### For Reviewers
- **Check functionality** - Does it work as intended?
- **Review tests** - Are they comprehensive and correct?
- **Verify documentation** - Is it accurate and helpful?
- **Consider maintainability** - Will future developers understand this?

## Debugging

### Common Issues
```bash
# Build failures
bazel build //... --verbose_failures

# Import errors
python -c "import sys; print(sys.path)"

# Test failures
bazel test //path/to:test --test_output=all

# Pre-commit issues
pre-commit run --all-files
```

### Debug Tools
- **Python debugger** - Use `pdb` or IDE debugger
- **Logging** - Add debug logging to understand flow
- **Bazel query** - Understand build dependencies
- **Git bisect** - Find when issues were introduced

## Performance Considerations

### Profiling
```python
# Profile code performance
import cProfile
cProfile.run('your_function()')

# Memory profiling
import memory_profiler
@memory_profiler.profile
def your_function():
    pass
```

### Optimization
- **Measure first** - Profile before optimizing
- **Focus on hot paths** - Optimize critical code paths
- **Use appropriate data structures** - Choose efficient algorithms
- **Cache when appropriate** - Avoid repeated expensive operations

## Release Process

### Version Management
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Update version in relevant files
- Tag releases in git
- Update changelog

### Documentation Updates
- Update API documentation
- Refresh examples and guides
- Update LLM context files
- Verify all links work

## Contributing Guidelines

### Before Contributing
1. Read this guide thoroughly
2. Set up development environment
3. Understand the codebase architecture
4. Review existing issues and PRs

### Quality Standards
- All tests must pass
- Documentation must be updated
- Code must follow style guidelines
- Changes must be backward compatible (unless breaking change is justified)

### Communication
- Use GitHub issues for bugs and feature requests
- Discuss major changes before implementation
- Be respectful and constructive in reviews
- Help maintain a positive development environment

---

*This guide is maintained by the OS Core Team. For questions or suggestions, create an issue or discuss in development channels.*
