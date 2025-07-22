# Rules Service Pre-commit Hook Issues and Fixes

## Executive Summary

During the implementation of pre-commit hooks for the Rules Service, we encountered several issues that revealed a fundamental problem: the Rules Service was never properly initialized in the repository. This led to architectural violations where we added workarounds in the hooks instead of addressing the root cause.

## Issues Encountered

### 1. Initial Bazel Dependency Issues

**Problem**: The original Bazel-based hooks failed with module import errors:
```
ModuleNotFoundError: No module named 'rich.console'
ModuleNotFoundError: No module named 'typer._types'
```

**Root Cause**: Bazel's isolated Python environment wasn't properly resolving transitive dependencies.

**Temporary Fix Applied**: Created direct Python hooks (`direct_hooks.py`) that bypass Bazel and import modules directly.

**Proper Fix**: Should use Bazel's `py_binary` with proper dependency management or ensure the CLI tool is properly installed in the environment.

### 2. Missing Configuration File

**Problem**: `RulesServiceConfig()` initialization failed with:
```
ValidationError: 2 validation errors for RulesServiceConfig
version: Field required
agent_folders: Field required
```

**Root Cause**: No `.rules-service.yaml` configuration file exists in the repository.

**Temporary Fix Applied**: Hardcoded configuration directly in the hooks:
```python
config_dict = {
    "version": "1.0",
    "agent_folders": [
        {"path": ".cursor/rules/", "description": "Cursor AI rules", "enabled": True},
        # ... other folders
    ]
}
config = RulesServiceConfig(**config_dict)
```

**Proper Fix**: Run `rules init` command to create proper configuration file.

### 3. Incorrect Rules Directory Path

**Problem**: No rule files found in `/os/domains/rules/data/`

**Root Cause**: Wrong path - rules actually exist at `/company_os/domains/rules/data/` not `/os/domains/rules/data/`. The repository contains 9 rule files:
- brief-system.rules.md
- code-factorization.rules.md
- decision-system.rules.md
- knowledge-system.rules.md
- repository-system.rules.md
- service-system.rules.md
- signal-system.rules.md
- tech-stack.rules.md
- validation-system.rules.md

**Temporary Fix Applied**: Hardcoded incorrect path, so validation runs without finding any rules.

**Proper Fix**: Use correct path: `company_os/domains/rules/data/`

### 4. Import Path Issues

**Problem**: `ValidationEngine` class not found, should be `ValidationService`

**Root Cause**: Incorrect class name used in import statements.

**Temporary Fix Applied**: Updated imports to use correct class names.

**Proper Fix**: This was the correct fix - no further action needed.

### 5. Missing SyncService Parameters

**Problem**: `SyncService` requires `root_path` parameter but hooks only provided `config`

**Root Cause**: Incomplete understanding of service initialization requirements.

**Temporary Fix Applied**: Added `project_root` as second parameter.

**Proper Fix**: This was the correct fix - no further action needed.

## Architecture Violations

### 1. Code Duplication
- Configuration is hardcoded in hooks instead of using shared configuration
- Rules discovery logic duplicated instead of using `RuleDiscoveryService`

### 2. Silent Failures
- Hooks don't notify users about missing initialization
- No helpful error messages when service isn't set up

### 3. Divergent Code Paths
- CLI uses `RulesServiceConfig.from_file()`
- Hooks use hardcoded dictionary
- This leads to different behavior and maintenance issues

## Proper Solution Architecture

### 1. Service Initialization Check

The hooks should first check if the service is initialized:

```python
def check_service_initialized() -> bool:
    """Check if Rules Service is properly initialized."""
    config_path = Path(".rules-service.yaml")
    rules_dir = Path("os/domains/rules/data")

    if not config_path.exists():
        console.print("[red]❌ Rules Service not initialized![/red]")
        console.print("[yellow]Run: bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules init[/yellow]")
        return False

    if not list(rules_dir.glob("*.rules.md")):
        console.print("[yellow]⚠️  No rule files found in {rules_dir}[/yellow]")
        console.print("[dim]The service will run but won't validate against any rules.[/dim]")

    return True
```

### 2. Shared Configuration Loading

Use the same configuration loading as the CLI:

```python
def load_config() -> Optional[RulesServiceConfig]:
    """Load configuration using the same method as CLI."""
    config_path = Path(".rules-service.yaml")

    if config_path.exists():
        return RulesServiceConfig.from_file(config_path)
    else:
        return None
```

### 3. Proper Service Integration

```python
def validate_main() -> int:
    # Check initialization first
    if not check_service_initialized():
        return 3  # Configuration error

    # Load config properly
    config = load_config()
    if not config:
        console.print("[red]❌ Failed to load configuration[/red]")
        return 3

    # Use RuleDiscoveryService like the CLI
    discovery_service = RuleDiscoveryService(".")
    rules = discovery_service.discover_rules()

    # Continue with validation...
```

## Implementation Steps

### 1. Initialize the Service Properly
```bash
# Create configuration
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules init

# Verify configuration
cat .rules-service.yaml
```

### 2. Create Rule Files
Create actual rule documents in `/os/domains/rules/data/`:
- `knowledge.rules.md`
- `decision.rules.md`
- `signal.rules.md`
- etc.

### 3. Update Hooks to Use Proper Architecture
- Remove hardcoded configurations
- Add initialization checks
- Use shared code paths with CLI
- Provide helpful error messages

### 4. Test Complete Workflow
```bash
# Initialize
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules init

# Sync rules
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules sync

# Test pre-commit hooks
pre-commit run --all-files
```

## Lessons Learned

1. **Always check service initialization** before implementing workarounds
2. **Maintain single source of truth** for configuration and behavior
3. **Provide clear error messages** that guide users to solutions
4. **Use existing service abstractions** instead of reimplementing logic
5. **Test the complete workflow** from initialization to execution

## Current State

As of now:
- ❌ Service is NOT properly initialized
- ❌ No configuration file exists
- ✅ Rule files DO exist (9 files in `/company_os/domains/rules/data/`)
- ⚠️  Hooks work but with hardcoded config and wrong path
- ⚠️  Validation passes but doesn't find rules due to incorrect path

## Next Actions

1. Initialize Rules Service properly
2. Fix path to rules directory in hooks
3. Refactor hooks to use proper architecture
4. Remove all hardcoded configurations
5. Add proper error handling and user guidance

---

*This document serves as a record of technical debt incurred during rapid implementation and the proper path forward to resolve it.*
