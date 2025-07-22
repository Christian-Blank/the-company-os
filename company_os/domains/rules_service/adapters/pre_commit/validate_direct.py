#!/usr/bin/env python3
"""Direct validate hook wrapper."""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(project_root))

# Now we can import from the project
from company_os.domains.rules_service.adapters.pre_commit.direct_hooks import validate_main

if __name__ == "__main__":
    sys.exit(validate_main())
