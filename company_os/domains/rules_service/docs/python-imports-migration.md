# Python Imports Migration Guide

## Overview

This guide documents the migration from relative imports to absolute imports in the rules_service to resolve Python module conflicts and improve maintainability.

## Changes Made

### 1. Directory Structure

**Before:**
```
os/domains/rules_service/
```

**After:**
```
company_os/domains/rules_service/
```

**Reason:** The `os` directory name conflicted with Python's built-in `os` module, preventing absolute imports.

### 2. Import Statements

**Before (Relative Imports):**
```python
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.validation import ValidationService
from src.models import RuleDocument
```

**After (Absolute Imports):**
```python
from company_os.domains.rules_service.src.validation import ValidationService
from company_os.domains.rules_service.src.models import RuleDocument
```

### 3. Shared Library Imports

**Before:**
```python
from company_os_core.models import BaseDocument
```

**After:**
```python
from shared.libraries.company_os_core.models import BaseDocument
```

### 4. BUILD.bazel Files

**Before:**
```bazel
deps = [
    "//os/domains/rules_service/src:rules_service_lib",
]
imports = [".."]
```

**After:**
```bazel
deps = [
    "//company_os/domains/rules_service/src:rules_service_lib",
]
# imports = [".."] removed since using absolute imports
```

### 5. Package Structure

Added `__init__.py` files to create proper Python packages:
- `company_os/__init__.py`
- `company_os/domains/__init__.py`
- `company_os/domains/rules_service/__init__.py`
- `shared/__init__.py`
- `shared/libraries/__init__.py`

## Benefits

1. **No Module Conflicts:** Eliminated conflicts with Python's built-in `os` module
2. **Cleaner Imports:** No more `sys.path` manipulation in tests
3. **Better IDE Support:** IDEs can properly resolve absolute imports
4. **Explicit Dependencies:** Clear dependency graph in BUILD files
5. **Consistency:** All imports follow the same pattern

## Usage Examples

### Running Tests

**Before:**
```bash
# Required PYTHONPATH manipulation
PYTHONPATH=/path/to/repo:$PYTHONPATH python -m pytest tests/
```

**After:**
```bash
# Works from any directory
python -m pytest company_os/domains/rules_service/tests/
```

### Importing in Code

**Before:**
```python
# In tests/test_validation.py
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.validation import ValidationService
```

**After:**
```python
# In tests/test_validation.py
from company_os.domains.rules_service.src.validation import ValidationService
```

## Migration Checklist

When adding new modules or tests, ensure:

- [ ] Use absolute imports starting with `company_os.`
- [ ] No `sys.path` manipulation
- [ ] Proper `__init__.py` files in all package directories
- [ ] BUILD.bazel files use absolute paths for dependencies
- [ ] No `imports = [".."]` in BUILD files when using absolute imports

## Testing

All 51 validation tests pass with the new import structure:
- 40 core validation tests
- 11 human input validation tests

Run tests with:
```bash
python -m pytest company_os/domains/rules_service/tests/test_validation.py -v
python -m pytest company_os/domains/rules_service/tests/test_validation_human_input.py -v
```

## Future Considerations

1. **Bazel Migration:** Consider migrating from WORKSPACE to MODULE.bazel for Bazel 8 compatibility
2. **Import Aliases:** Could add import aliases for frequently used modules
3. **Package Restructuring:** Could move code from `src/` subdirectory to parent level

This migration establishes a solid foundation for the rules_service with clean, maintainable Python imports.
