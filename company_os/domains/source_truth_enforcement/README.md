---
title: "Source Truth Enforcement Service"
version: 1.1
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-22T21:07:00-07:00"
parent_charter: "os/domains/charters/data/service-architecture.charter.md"
tags: ["service", "validation", "consistency", "source-truth"]
---

# Source Truth Enforcement Service

A comprehensive service that validates consistency across the Company OS repository by checking that all technical specifications align with their authoritative sources as defined in the source truth registry.

## Overview

The Source Truth Enforcement Service ensures repository-wide consistency by:

- **Registry-driven validation**: Central registry defines authoritative sources for all specifications
- **Automated scanning**: Scans files for violations using configurable patterns
- **Rich reporting**: Provides detailed reports with suggestions for fixes
- **CI/CD integration**: Returns appropriate exit codes for build pipelines
- **Extensible architecture**: Easy to add new validation rules and patterns

## Architecture

This service follows the Company OS hexagonal architecture pattern:

```
company_os/domains/source_truth_enforcement/
├── src/                    # Core domain logic
│   ├── models.py          # Data models (Violation, Report, etc.)
│   ├── registry.py        # Registry loader and parser
│   ├── checker.py         # Main consistency checker
│   └── __init__.py        # Public API exports
├── adapters/              # External interfaces
│   └── cli/               # Command-line interface
│       ├── source_truth_cli.py  # CLI implementation
│       └── BUILD.bazel    # CLI build configuration
├── data/                  # Service data
│   └── source_truth_registry.yaml  # The registry file
└── BUILD.bazel           # Service build configuration
```

## Usage

### Command Line Interface

The service provides a rich CLI for checking consistency:

```bash
# Check all source of truth definitions
bazel run //company_os/domains/source_truth_enforcement/adapters/cli:source_truth_cli -- check --all

# Check specific areas
bazel run //company_os/domains/source_truth_enforcement/adapters/cli:source_truth_cli -- check --python-version
bazel run //company_os/domains/source_truth_enforcement/adapters/cli:source_truth_cli -- check --dependencies
bazel run //company_os/domains/source_truth_enforcement/adapters/cli:source_truth_cli -- check --forbidden-files

# Get service information
bazel run //company_os/domains/source_truth_enforcement/adapters/cli:source_truth_cli -- info

# Output options
bazel run //company_os/domains/source_truth_enforcement/adapters/cli:source_truth_cli -- check --all --format json
bazel run //company_os/domains/source_truth_enforcement/adapters/cli:source_truth_cli -- check --all --verbose --debug
```

### Exit Codes

The CLI returns standard exit codes for CI/CD integration:

- `0` - Success: No violations found
- `1` - Warnings: Low or medium severity violations found
- `2` - Errors: High severity violations found
- `3` - Failure: System error (configuration issue, registry not found, etc.)

### Python API

```python
from company_os.domains.source_truth_enforcement import SourceTruthChecker, CheckerConfig

# Create configuration
config = CheckerConfig(
    registry_path="path/to/registry.yaml",
    repository_root=".",
    verbose=True
)

# Initialize checker
checker = SourceTruthChecker(config)

# Check all definitions
report = checker.check_all()

# Check specific definition
report = checker.check_definition("python_version")

# Analyze results
if not report.success:
    for violation in report.violations:
        print(f"{violation.severity}: {violation.message}")
```

## Registry Configuration

The source truth registry (`data/source_truth_registry.yaml`) defines all consistency rules:

### Registry Structure

```yaml
version: "1.0"
metadata:
  description: "Central registry of source of truth definitions"
  owner: "OS Core Team"

registry:
  python_version:
    description: "Canonical Python version for the entire repository"
    source: ".python-version"          # File containing authoritative value
    type: "exact_version"              # Validation type
    severity: "high"                   # Violation severity
    scan_patterns:                     # Regex patterns to find violations
      - "Python 3\\.\\d+(\\.\\d+)?"
    scan_file_types:                   # File types to scan
      - "*.md"
      - "*.py"
    auto_fix: true                     # Whether auto-fix is supported
```

### Supported Validation Types

1. **exact_version**: Ensures all references match exactly (e.g., Python version)
2. **file_existence_and_workflow**: Validates file patterns and workflows
3. **minimum_version**: Checks minimum version requirements
4. **configuration_validation**: Validates configuration patterns
5. **directory_structure_validation**: Checks service locations
6. **reporting_standards**: Validates status reporting formats
7. **reference_validation**: Checks documentation references

### Current Definitions

The registry currently validates:

- **Python Version**: Consistency with `.python-version` file
- **Dependencies**: Proper use of `requirements.in` → `requirements_lock.txt` workflow
- **Bazel Configuration**: MODULE.bazel vs deprecated WORKSPACE
- **Service Locations**: Correct import paths and service structure
- **Documentation Standards**: Reference accuracy and timestamp formats

## Ignore Comments

The Source Truth Enforcement Service supports ESLint-style ignore comments to suppress violations in specific contexts. This is useful for configuration files, documentation examples, and legitimate exceptions.

### Ignore Comment Syntax

#### Single Line Ignore
```yaml
# source-truth-ignore-next-line <rule-name> -- <reason>
forbidden_patterns:
  - "requirements.txt"  # This line would be ignored
```

#### Block Ignore
```yaml
# source-truth-ignore-start <rule-name> -- <reason>
forbidden_patterns:
  - "requirements.txt"
  - "pip-compile"
  - "pip install -r requirements.txt"
# source-truth-ignore-end <rule-name>
```

#### File-wide Ignore
```yaml
# source-truth-ignore-file <rule-name> -- <reason>
# This ignores the entire file for the specified rule
```

### Rules for Ignore Comments

1. **Reason Required**: Every ignore directive must include `-- <reason>` explaining why
2. **Valid Rule Names**: Rule name must match a definition in the registry
3. **Block Closure**: Every `ignore-start` must have a matching `ignore-end`
4. **No Empty Reasons**: The reason cannot be empty or just whitespace

### Examples

#### Registry Configuration (Self-Documentation)
```yaml
# The registry file itself uses ignore comments to prevent self-detection
dependencies:
  description: "Canonical dependency management workflow"

  # source-truth-ignore-start dependencies -- These patterns define what violations to detect
  forbidden_patterns:
    - "pip install -r requirements\\.txt"
    - "pip-compile\\s+"
    - "requirements\\.txt"
  # source-truth-ignore-end dependencies
```

#### Documentation Examples
```markdown
<!-- source-truth-ignore-next-line python_version -- This is an example of what NOT to do -->
Install Python 3.8+ for this legacy project.

The correct approach is to use Python 3.12.0 as specified in `.python-version`.
```

#### Legitimate Exceptions
```yaml
# source-truth-ignore-next-line dependencies -- Legacy system compatibility requirement
- name: Install old requirements
  command: pip install -r requirements.txt
```

### Verbose Reporting

When using `--verbose`, the service reports on ignored violations:

```bash
ℹ️ Ignored Violations:
┏━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Rule        ┃ Count ┃ Reasons                                                                     ┃
┡━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ dependencies │   8   │ These patterns define what violations to detect                         │
│ bazel_version│   4   │ These patterns identify outdated Bazel configurations                  │
└─────────────┴───────┴─────────────────────────────────────────────────────────────────────────┘

Total ignored: 12
```

### Best Practices

1. **Use Sparingly**: Fix the underlying issue rather than ignoring it when possible
2. **Clear Reasons**: Explain why the ignore is necessary and legitimate
3. **Review Regularly**: Periodically review ignored violations to see if they can be resolved
4. **Prefer Specific Rules**: Ignore specific rules rather than using broad file ignores
5. **Document Context**: In configuration files, add comments explaining the ignore purpose

### Validation

The service validates ignore comments and will warn about:

- **Missing Reasons**: Ignore directives without `-- <reason>`
- **Unknown Rules**: References to non-existent rule names
- **Unclosed Blocks**: `ignore-start` without matching `ignore-end`
- **Unused Ignores**: Ignore directives that don't affect any violations (with `--verbose`)

## Development

### Building the Service

```bash
# Build all components
bazel build //company_os/domains/source_truth_enforcement/...

# Build just the CLI
bazel build //company_os/domains/source_truth_enforcement/adapters/cli:source_truth_cli

# Run tests (when implemented)
bazel test //company_os/domains/source_truth_enforcement/tests:all
```

### Adding New Validation Rules

1. **Define in Registry**: Add new definition to `data/source_truth_registry.yaml`
2. **Update Models**: Add any new fields to `src/models.py` if needed
3. **Implement Logic**: Add validation logic to `src/checker.py`
4. **Test**: Verify the rule works with test cases

Example new rule:

```yaml
registry:
  new_rule:
    description: "Description of what this validates"
    source: "path/to/source/file"     # Optional: source of truth file
    type: "exact_version"             # Choose appropriate type
    severity: "medium"                # high|medium|low
    scan_patterns:
      - "pattern1"
      - "pattern2"
    scan_file_types:
      - "*.ext"
    forbidden_patterns:              # Optional: patterns that should not exist
      - "bad_pattern"
```

### Performance Configuration

The service supports parallel processing and caching:

```yaml
global_config:
  performance:
    max_file_size_mb: 10
    parallel_processing: true
    max_workers: 4
    cache_enabled: true
    cache_duration_hours: 24
```

## Integration

### Pre-commit Hooks

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: source-truth-check
        name: Source Truth Consistency Check
        entry: bazel run //company_os/domains/source_truth_enforcement/adapters/cli:source_truth_cli -- check --all
        language: system
        pass_filenames: false
```

### CI/CD Pipelines

GitHub Actions example:

```yaml
- name: Check Source Truth Consistency
  run: |
    bazel run //company_os/domains/source_truth_enforcement/adapters/cli:source_truth_cli -- check --all --format json > violations.json
    if [ $? -ne 0 ]; then
      echo "Source truth violations found"
      cat violations.json
      exit 1
    fi
```

## Troubleshooting

### Common Issues

**Registry not found**:
```bash
❌ Error: Registry file not found: /path/to/registry.yaml
```
- Solution: Ensure the registry file exists or specify custom path with `--registry`

**No files scanned**:
```
Files Scanned: 0
```
- Check that scan patterns match existing files
- Verify working directory is repository root
- Enable `--debug` to see detailed path resolution

**Permission errors**:
- Ensure read access to all scanned directories
- Check file sizes don't exceed `max_file_size_mb` limit

### Debug Mode

Enable verbose debugging:

```bash
bazel run //company_os/domains/source_truth_enforcement/adapters/cli:source_truth_cli -- check --all --debug --verbose
```

This shows:
- Registry loading details
- File discovery process
- Pattern matching results
- Performance metrics

## Related Services

- **Rules Service**: Document validation and rule synchronization
- **Repo Guardian**: AI-powered repository quality analysis
- **Knowledge Service**: Documentation and knowledge management

## Status

- **Version**: 1.1.0
- **Stage**: 0 (File-based)
- **Status**: Active and production-ready
- **Owner**: OS Core Team
- **Last Updated**: 2025-07-22
- **Latest Feature**: ESLint-style ignore comments for suppressing violations

## Future Enhancements

- **Stage 1**: MCP server for external tool integration
- **Stage 2**: Database caching for large repositories
- **Stage 3**: Auto-fix capabilities for supported violations
- **Stage 4**: Integration with external code quality tools

---

*This service is part of the Company OS ecosystem. For more information, see the [Service Registry](../registry/data/services.registry.md).*
