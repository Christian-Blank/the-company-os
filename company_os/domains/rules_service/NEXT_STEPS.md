# Rules Service Pre-commit Hooks - Next Steps

## Summary

We've identified that the core issue with the pre-commit hooks was that the Rules Service was never properly initialized. This led to architectural violations where we hardcoded configurations and created diverging code paths.

## Files Created

1. **`ISSUES_AND_FIXES.md`** - Comprehensive documentation of all issues, temporary fixes, and proper solutions
2. **`hooks_proper.py`** - Proper implementation that follows service architecture
3. **`NEXT_STEPS.md`** - This file, outlining the path forward

## Immediate Actions Required

### 1. Initialize the Rules Service

```bash
# Create the configuration file
bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules init

# This will create .rules-service.yaml with proper configuration
```

### 2. Verify Rule Files

Rule files already exist in `/company_os/domains/rules/data/`:

```bash
# List existing rule files
ls -la company_os/domains/rules/data/*.rules.md

# Output shows 9 rule files:
# - brief-system.rules.md
# - code-factorization.rules.md
# - decision-system.rules.md
# - knowledge-system.rules.md
# - repository-system.rules.md
# - service-system.rules.md
# - signal-system.rules.md
# - tech-stack.rules.md
# - validation-system.rules.md
```

### 3. Test Proper Hooks

```bash
# Test with the proper implementation
python company_os/domains/rules_service/adapters/pre_commit/hooks_proper.py validate README.md

# If not initialized, you'll see:
# ❌ Rules Service not initialized!
# The Rules Service requires initialization before use.
#
# To initialize, run:
#   bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules init
```

### 4. Update Pre-commit Configuration

Once the service is properly initialized, update `.pre-commit-config.yaml` to use the proper hooks:

```yaml
# Rules Service Hooks (Local)
-   repo: local
    hooks:
    -   id: rules-sync
        name: Rules Service - Sync
        description: Synchronize rules to agent folders
        entry: python company_os/domains/rules_service/adapters/pre_commit/hooks_proper.py
        files: 'sync_hook'  # This makes the script run in sync mode
        language: system
        pass_filenames: false
        always_run: true
        stages: [pre-commit]
        verbose: false

    -   id: rules-validate
        name: Rules Service - Validate
        description: Validate markdown files against rules
        entry: python company_os/domains/rules_service/adapters/pre_commit/hooks_proper.py
        files: 'validate_hook'  # This makes the script run in validate mode
        language: system
        types: [markdown]
        stages: [pre-commit]
        verbose: false
```

### 5. Remove Technical Debt

After proper initialization:
1. Delete `direct_hooks.py` (the workaround implementation)
2. Delete `hooks_improved.py` (intermediate attempt)
3. Delete `validate_direct.py` and `sync_direct.py` (wrapper scripts)
4. Keep only `hooks_proper.py` as the canonical implementation

## Key Principles Going Forward

1. **Check initialization first** - Always verify service setup before use
2. **Use shared components** - Leverage existing service abstractions
3. **Provide helpful errors** - Guide users to solutions, don't just fail
4. **Maintain consistency** - CLI and hooks should behave identically
5. **Document assumptions** - Make requirements explicit

## Expected Behavior After Fixes

### When Service Not Initialized:
```
❌ Rules Service not initialized!
The Rules Service requires initialization before use.

To initialize, run:
  bazel run //company_os/domains/rules_service/adapters/cli:rules_cli -- rules init
```

### When No Rules Exist:
```
⚠️  No rule files found in os/domains/rules/data/
The service will run but won't validate against any rules.
Add .rules.md files to define validation rules.
```

### When Properly Set Up:
```
================================================================================
          RULES SERVICE VALIDATION - 3 file(s)
================================================================================

✓ Found 5 rule(s) to validate against

⠋ Validating README.md...

================================================================================
                   VALIDATION SUMMARY
================================================================================

┏━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Metric          ┃ Count ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ Files Processed │     3 │
│ Rules Applied   │     5 │
│ ⚠️  Warnings    │     2 │
└─────────────────┴───────┘

⚠️  Validation completed with warnings
```

## Timeline

1. **Immediate** (Today):
   - Initialize Rules Service
   - Create at least one rule file
   - Test proper hooks work

2. **Short-term** (This Week):
   - Create comprehensive rule files for all document types
   - Update pre-commit config to use proper hooks
   - Remove workaround implementations

3. **Long-term** (Next Sprint):
   - Add more sophisticated validation rules
   - Implement auto-fix for more issue types
   - Create rule authoring guide

---

*This plan ensures we fix the root cause rather than patching symptoms, leading to a maintainable and properly architected solution.*
