# Developer Workflow Guide

## TL;DR

1. **Clone repo**: `git clone https://github.com/Christian-Blank/the-company-os`
2. **Run verification**: `./verify-all.sh` → ensures env, build and tests pass
3. **Hack on code**: Make your changes
4. **Test before push**: `bazel test //...` or `./verify-all.sh`
5. **Open a PR**: Follow standard GitHub flow

## Complete Process

For the complete, authoritative development process, see:
→ **[Developer Verification Process](company_os/domains/processes/data/developer-verification.process.md)**

## Quick Reference

### Environment Setup
- **Python**: 3.12 (check `.python-version`)
- **Dependencies**: UV (`uv pip sync requirements_lock.txt`)
- **Build System**: Bazel 8.x with bzlmod

### Key Commands
```bash
# One-command verification
./verify-all.sh

# Quick builds
bazel build //...

# Quick tests
bazel test //...

# Pre-commit checks
pre-commit run --all-files
```

### Project Structure
```
company_os/domains/         - Core system services
work/domains/              - Execution services
src/company_os/services/   - Advanced services
shared/                    - Cross-cutting resources
infrastructure/            - Deployment support
```

## CI/CD

All pull requests automatically run the same `./verify-all.sh` script. If it fails locally, it will fail in CI.

## Getting Help

- **Build Issues**: See troubleshooting in verification process
- **Test Failures**: Check `bazel-testlogs/` for details
- **Dependency Issues**: `rm -rf .venv && uv venv .venv && uv pip sync requirements_lock.txt`

---

*This is an orientation document. All commands and detailed processes are maintained in the [Developer Verification Process](company_os/domains/processes/data/developer-verification.process.md).*
