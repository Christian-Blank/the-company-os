#!/usr/bin/env python3
"""
Pre-commit validate hook entry point.
"""

import sys
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(project_root))

from company_os.domains.rules_service.adapters.pre_commit.hooks import validate_main

if __name__ == "__main__":
    sys.exit(validate_main())
