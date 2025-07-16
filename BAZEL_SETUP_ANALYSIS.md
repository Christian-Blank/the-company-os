# Bazel Setup Analysis Report

## Executive Summary

This report documents our analysis of the Bazel build system setup for the Company OS Rules Service, including issues encountered, solutions implemented, and recommendations for maintaining packages and services.

## Current State (As of 2025-07-16)

### ✅ What's Working

1. **Bazel 8 with Bzlmod**: Successfully migrated from deprecated WORKSPACE to MODULE.bazel
2. **Python Dependencies**: Using rules_python with pip.parse for dependency management
3. **Build System**: All rules_service components build successfully
4. **Testing**: All 6 test suites pass via Bazel (85 tests total)
5. **CLI Binary**: Successfully builds and runs (with updated typer 0.16.0)

### Key Components

- **Bazel Version**: 8.3.1
- **rules_python**: 1.5.1
- **aspect_rules_py**: 1.6.0
- **Python Version**: 3.12

## Issues Encountered and Solutions

### 1. WORKSPACE Deprecation (Bazel 8)

**Issue**: Bazel 8 deprecated WORKSPACE files by default
```
ERROR: No repository visible as '@rules_python' from main repository
```

**Solution**: Migrated to MODULE.bazel (bzlmod)
```starlark
module(
    name = "the_company_os",
    version = "0.1.0",
)
```

### 2. rules_uv Compatibility

**Issue**: rules_uv version 0.81.0 doesn't exist
```
ERROR: Error loading '@@rules_uv+//uv:extensions.bzl'
```

**Solution**: Removed rules_uv, used standard rules_python pip.parse instead

### 3. Missing Dependencies

**Issue**: ruamel.yaml import error in tests
```
ModuleNotFoundError: No module named 'ruamel'
```

**Solution**: Added ruamel.yaml==0.18.6 to requirements.in

### 4. Typer/Click Compatibility

**Issue**: TypeError with typer 0.9.0 and click
```
TypeError: Parameter.make_metavar() missing 1 required positional argument: 'ctx'
```

**Solution**: Updated to typer==0.16.0 (latest available)

### 5. py_binary Main Attribute

**Issue**: CLI binary couldn't find __main__.py
```
Error in fail: could not find '__main__.py' as specified by 'main' attribute
```

**Solution**: Added srcs parameter to py_binary
```starlark
py_binary(
    name = "rules_cli",
    srcs = ["__main__.py"],
    main = "__main__.py",
    imports = ["../../../.."],
    deps = [...],
)
```

## Final Working Configuration

### 1. MODULE.bazel
```starlark
module(
    name = "the_company_os",
    version = "0.1.0",
)

# Python rules
bazel_dep(name = "rules_python", version = "1.5.1")
bazel_dep(name = "aspect_rules_py", version = "1.6.0")

# Python toolchain registration
python = use_extension("@rules_python//python/extensions:python.bzl", "python")
python.toolchain(
    python_version = "3.12",
)

# Pip dependencies
pip = use_extension("@rules_python//python/extensions:pip.bzl", "pip")
pip.parse(
    hub_name = "pypi",
    python_version = "3.12",
    requirements_lock = "//:requirements_lock.txt",
)
use_repo(pip, "pypi")
```

### 2. .bazelrc
```
# Disable legacy WORKSPACE
common --noenable_workspace

# Build settings
build --verbose_failures
build --sandbox_default_allow_network=false

# Test settings
test --test_output=errors
test --test_summary=short

# Python specific - NO PYTHONPATH!
test --action_env=PYTEST_CURRENT_TEST
```

### 3. Key BUILD.bazel Patterns

**Library Pattern**:
```starlark
load("@aspect_rules_py//py:defs.bzl", "py_library")

py_library(
    name = "rules_service_lib",
    srcs = glob(["*.py"]),
    imports = ["../../../.."],  # Critical for imports
    visibility = ["//visibility:public"],
    deps = [
        "//shared/libraries/company_os_core",
        "@pypi//pydantic",
        "@pypi//pyyaml",
        "@pypi//ruamel_yaml",
        "@pypi//mistune",
    ],
)
```

**Test Pattern**:
```starlark
load("@aspect_rules_py//py:defs.bzl", "py_test")

[
    py_test(
        name = test_file[:-3],  # Remove .py extension
        srcs = [test_file],
        deps = [
            "//company_os/domains/rules_service/src:rules_service_lib",
            "@pypi//pytest",
            "@pypi//pytest_bazel",
        ],
    )
    for test_file in glob(["test_*.py"])
]

# Test suite
test_suite(
    name = "all_tests",
    tests = [test_file[:-3] for test_file in glob(["test_*.py"])],
)
```

## Build and Test Commands

### Building
```bash
# Build library
bazel build //company_os/domains/rules_service/src:rules_service_lib

# Build CLI
bazel build //company_os/domains/rules_service/adapters/cli:rules_cli

# Build everything
bazel build //company_os/domains/rules_service/...
```

### Testing
```bash
# Run single test
bazel test //company_os/domains/rules_service/tests:test_validation

# Run all tests
bazel test //company_os/domains/rules_service/tests:all_tests

# Run with verbose output
bazel test //company_os/domains/rules_service/tests:all_tests --test_output=all
```

### Running
```bash
# Run CLI
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- --help
```

## How to Add New Components

### Adding a New Package

1. **Create directory structure**:
```
company_os/domains/new_service/
├── __init__.py
├── BUILD.bazel
├── src/
│   ├── __init__.py
│   ├── BUILD.bazel
│   └── models.py
└── tests/
    ├── BUILD.bazel
    └── test_models.py
```

2. **Create root BUILD.bazel**:
```starlark
load("@aspect_rules_py//py:defs.bzl", "py_library")

py_library(
    name = "new_service",
    visibility = ["//visibility:public"],
    deps = [
        "//company_os/domains/new_service/src:new_service_lib",
    ],
)
```

3. **Create src/BUILD.bazel**:
```starlark
load("@aspect_rules_py//py:defs.bzl", "py_library")

py_library(
    name = "new_service_lib",
    srcs = glob(["*.py"]),
    imports = ["../../../.."],
    visibility = ["//visibility:public"],
    deps = [
        # Add dependencies
    ],
)
```

### Adding a New Service

1. **Update requirements.in** if new dependencies needed:
```
# New service dependencies
httpx==0.24.1
```

2. **Regenerate lock file**:
```bash
uv pip compile requirements.in --generate-hashes -o requirements_lock.txt
```

3. **Add to BUILD file deps**:
```starlark
deps = [
    "@pypi//httpx",
]
```

### Adding Tests

1. **Create test file** following naming convention `test_*.py`

2. **Tests are automatically discovered** by glob pattern

3. **Run specific test**:
```bash
bazel test //company_os/domains/new_service/tests:test_models
```

## Best Practices

### 1. Import Management
- Always use absolute imports: `from company_os.domains.rules_service.src import models`
- Set `imports = ["../../../.."]` in py_library rules
- Never use PYTHONPATH manipulation

### 2. Dependency Management
- Pin all versions in requirements.in
- Use `uv pip compile` for deterministic lock files
- Always include `--generate-hashes` for security

### 3. Test Organization
- One test file per module
- Use test_suite for grouping
- Follow pytest conventions

### 4. Build Performance
- Use glob patterns for source files
- Leverage Bazel's caching
- Run `bazel clean --expunge` only when necessary

## Troubleshooting

### Common Issues

1. **Import errors**: Check `imports` parameter in BUILD files
2. **Missing dependencies**: Verify requirements_lock.txt is up to date
3. **Test discovery**: Ensure test files start with `test_`
4. **Cache issues**: Run `bazel clean` or `bazel clean --expunge`

### Debug Commands

```bash
# Show build graph
bazel query --notool_deps --noimplicit_deps "deps(//company_os/domains/rules_service/...)"

# Show why a target depends on another
bazel query "somepath(//company_os/domains/rules_service/tests:all_tests, @pypi//pydantic)"

# Clean cache
bazel clean --expunge
```

## Recommendations

### Short-term
1. ✅ Continue using current Bazel 8 + bzlmod setup
2. ✅ Maintain locked dependencies with uv
3. ✅ Follow established BUILD patterns

### Medium-term
1. Add pre-commit hooks for Bazel formatting (buildifier)
2. Create BUILD file generator for new services
3. Add CI/CD integration with Bazel remote cache

### Long-term
1. Evaluate Bazel remote execution for faster builds
2. Consider custom Starlark macros for common patterns
3. Implement automated dependency updates

## Conclusion

The Bazel setup is now fully functional with:
- Modern Bazel 8 + bzlmod configuration
- Proper Python 3.12 support
- All tests passing
- CLI tools building correctly
- Clear patterns for adding new components

The key insight is that Bazel 8's migration to bzlmod requires careful attention to:
1. MODULE.bazel configuration
2. Proper import paths in BUILD files
3. Dependency management through requirements_lock.txt

This setup provides a solid foundation for the Company OS rules service and can be extended to other services following the documented patterns.
