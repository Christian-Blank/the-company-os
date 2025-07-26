# Development Workflow Update Summary

**Date**: July 23, 2025
**Purpose**: Standardize development workflow on Bazel + UV only

## Changes Made

### 1. Updated `company_os/domains/processes/data/developer-verification.process.md` (v2.0)
- ✅ Removed all references to pyenv, pip install, manual venv
- ✅ Replaced with UV commands throughout (`uv venv .venv`, `uv pip sync`)
- ✅ Added core principles section emphasizing UV + Bazel only
- ✅ Streamlined from 8 to 7 stages
- ✅ Added quick start: "Run `./verify-all.sh`"
- ✅ Added comprehensive troubleshooting guide
- ✅ Added CI/CD integration example

### 2. Simplified `DEVELOPER_WORKFLOW.md`
- ✅ Converted to orientation/reference document
- ✅ Removed all duplicated command listings
- ✅ Points to verification process as single source of truth
- ✅ Kept only TL;DR and quick reference

### 3. Created `verify-all.sh`
- ✅ Executable script implementing the verification process
- ✅ Supports stage selection: `--stage N` or `--stage N-M`
- ✅ Colored output for better visibility
- ✅ Tracks overall success/failure
- ✅ Matches documentation exactly

### 4. Created `DEVELOPMENT_TEST_PLAN.md`
- ✅ 62 commands across 6 categories
- ✅ Each command has expected output
- ✅ Space for test results and notes
- ✅ Common issues and resolutions included
- ✅ Ready for systematic testing

## Key Principles Enforced

1. **One canonical tool per concern**:
   - Environment & dependencies: **UV** only
   - Build/test/CI: **Bazel 8** only
   - No pip, pip-tools, poetry, or manual venv

2. **Docs ≙ code**: The verification process is executable

3. **No duplication**: Single source of truth in verification process

4. **CI is the referee**: Same script runs locally and in CI

## Next Steps

1. **Test the verification script**:
   ```bash
   ./verify-all.sh
   ```

2. **Work through test plan**:
   - Execute each command in `DEVELOPMENT_TEST_PLAN.md`
   - Document actual results
   - Note any failures or deviations

3. **Fix any issues found**:
   - Update commands that don't work
   - Document workarounds
   - Update CI configuration if needed

4. **Update pre-commit hooks**:
   - Ensure they align with new workflow
   - Consider adding UV/Bazel version checks

5. **Update CI/CD**:
   - Use the GitHub Actions config from verification process
   - Ensure it runs `./verify-all.sh`

## Benefits

1. **Consistency**: Everyone uses same tools and workflow
2. **Speed**: UV is much faster than pip
3. **Reliability**: Lock files ensure reproducible builds
4. **Simplicity**: One script to rule them all
5. **CI/CD Parity**: Local = CI environment

## Migration Guide

For developers currently using pip/venv:
```bash
# Clean up old environment
rm -rf venv/
rm -rf .venv/

# Start fresh with UV
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv .venv
source .venv/bin/activate
uv pip sync requirements_lock.txt

# Run verification
./verify-all.sh
```

---

This update eliminates the "works on my machine" problem by enforcing a single, standardized workflow for all development activities.
