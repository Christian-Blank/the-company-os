#!/usr/bin/env python3
"""Build script for The Company OS rules_service."""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and report results."""
    print(f"\n🔨 {description}...")
    print(f"   Command: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"   ✅ Success")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
    else:
        print(f"   ❌ Failed")
        if result.stderr:
            print(f"   Error: {result.stderr.strip()}")
        return False
    
    return True

def main():
    """Main build process."""
    print("The Company OS Build System")
    print("=" * 50)
    
    # Ensure we're in the right directory
    root_dir = Path(__file__).parent
    
    # Check Python version
    if not run_command([sys.executable, "--version"], "Checking Python version"):
        return 1
    
    # Install dependencies
    if not run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      "Installing dependencies"):
        return 1
    
    # Run linting
    if not run_command([sys.executable, "-m", "ruff", "check", "company_os/domains/rules_service"], 
                      "Running linter (ruff)"):
        print("   ⚠️  Linting failed - continuing anyway")
    
    # Run type checking
    if not run_command([sys.executable, "-m", "mypy", "company_os/domains/rules_service/src"], 
                      "Running type checker (mypy)"):
        print("   ⚠️  Type checking failed - continuing anyway")
    
    # Run tests
    if not run_command([sys.executable, "-m", "pytest", "company_os/domains/rules_service/tests/", "-v"], 
                      "Running tests"):
        return 1
    
    print("\n✨ Build completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())