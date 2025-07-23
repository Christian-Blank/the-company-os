# Company OS Development Container

This directory contains the VSCode development container configuration for the Company OS project, implementing [Decision DEC-2025-07-23-001](../work/domains/decisions/data/DEC-2025-07-23-001-ubuntu-dev-container.decision.md).

## Overview

The dev container provides a consistent Ubuntu 24.04 LTS environment with all required development tools pre-configured, eliminating "works on my machine" issues and enabling instant productivity for new contributors.

## Files

### `devcontainer.json`
VSCode dev container configuration that defines:
- Ubuntu 24.04 base image via Dockerfile
- VSCode extensions for Python, Bazel, Git, YAML, Markdown
- Port forwarding for Temporal (8080, 7233) and development servers
- Volume mounts for caching UV packages and Bazel artifacts
- Environment variables for Python and UV
- Post-creation setup script execution

### `Dockerfile`
Ubuntu 24.04 based container image with:
- **Python 3.12** (matching `.python-version`)
- **UV package manager** for fast dependency management
- **Bazel 8.x** via Bazelisk for hermetic builds
- **Buildifier** for Bazel code formatting
- **Pre-commit** framework for quality gates
- **Docker-in-Docker** support for Temporal services
- Essential build tools and system dependencies
- Non-root `vscode` user for security

### `post-create.sh`
Automated setup script that runs after container creation:
- Creates and activates UV virtual environment
- Installs Python dependencies from `requirements_lock.txt`
- Installs pre-commit hooks
- Configures git for container environment
- Sets up helpful shell aliases
- Runs verification checks
- Provides helpful onboarding messages

## Usage

### Prerequisites
- Docker Desktop or equivalent
- VSCode with "Dev Containers" extension installed

### Getting Started
1. **Clone repository**: `git clone https://github.com/Christian-Blank/the-company-os`
2. **Open in VSCode**: `code the-company-os`
3. **Reopen in Container**:
   - `Cmd/Ctrl+Shift+P` → "Dev Containers: Reopen in Container"
   - Or click "Reopen in Container" popup notification
4. **Wait for setup**: Post-creation script runs automatically
5. **Start coding**: Environment is fully configured

### First Run
The container will:
- Download Ubuntu 24.04 base image (~500MB)
- Build custom image with all tools (~1.5GB total)
- Run post-creation setup (~2-3 minutes)
- **Total time**: 5-10 minutes depending on internet speed

### Subsequent Runs
- Container reuse: ~30 seconds
- Cached volumes preserve UV packages and Bazel artifacts

## Included Tools & Versions

| Tool | Version | Purpose |
|------|---------|---------|
| Ubuntu | 24.04 LTS | Base OS (5-year support) |
| Python | 3.12 | Matches `.python-version` |
| UV | Latest | Fast dependency management |
| Bazel | 8.x | Hermetic builds via Bazelisk |
| Buildifier | Latest | Bazel code formatting |
| Pre-commit | Latest | Quality gates |
| Git | Latest | Version control |
| Docker | Latest | Docker-in-Docker for services |

## Pre-configured VSCode Extensions

- **Python Development**: Python, MyPy, Ruff
- **Bazel**: Bazel language support
- **Version Control**: GitLens, Git Graph
- **Documentation**: Markdown, YAML, spell check
- **General**: JSON, EditorConfig, Docker

## Environment Variables

- `PYTHONPATH=/workspaces/the-company-os`
- `UV_CACHE_DIR=/workspaces/the-company-os/.uv-cache`
- `BAZEL_CACHE_DIR=/home/vscode/.cache/bazel`

## Volume Mounts

- `company-os-uv-cache`: UV package cache
- `company-os-bazel-cache`: Bazel build artifacts
- `company-os-python-cache`: Python package cache

## Port Forwarding

| Port | Service | Purpose |
|------|---------|---------|
| 8080 | Temporal UI | Temporal dashboard |
| 8233 | Temporal UI | Alternative port |
| 7233 | Temporal gRPC | Temporal client connection |
| 9090 | Prometheus | Metrics collection |
| 3000, 8000 | Development | General web development |

## Shell Aliases

The container includes helpful aliases:
- `verify` → `./verify-all.sh`
- `verify-env` → `./verify-all.sh --stage 1`
- `bb` → `bazel build`
- `bt` → `bazel test`
- `br` → `bazel run`
- `py` → `python`
- `activate` → `source .venv/bin/activate`

## Verification Commands

After container setup, verify everything works:

```bash
# Complete verification (recommended)
./verify-all.sh

# Quick environment check
./verify-all.sh --stage 1

# Build verification
bazel build //...

# Test execution
bazel test //...
```

## Performance Considerations

### Optimizations
- **Volume caching**: UV and Bazel caches persist between container rebuilds
- **Layer optimization**: Dockerfile uses multi-stage approach for smaller images
- **Minimal base**: Ubuntu 24.04 LTS provides good balance of features vs size

### Resource Usage
- **RAM**: ~2GB recommended minimum
- **Storage**: ~2GB for image + caches
- **CPU**: Builds will use available cores

## Troubleshooting

### Container won't start
- Ensure Docker Desktop is running
- Check available disk space (need ~3GB)
- Try rebuilding: "Dev Containers: Rebuild Container"

### Post-creation script fails
- Check logs in VSCode terminal
- Common issues:
  - Network connectivity (UV download, git clone)
  - Permissions (should be handled automatically)
  - Missing `requirements_lock.txt` (ensure in repo root)

### Performance issues
- Close unnecessary applications to free RAM
- Enable Docker BuildKit for faster builds
- Consider increasing Docker memory limits

### Tools not found
- Restart terminal: `Cmd/Ctrl+Shift+P` → "Terminal: Create New Terminal"
- Check PATH: `echo $PATH`
- Rebuild container if needed

## Development Workflow

### Recommended workflow
1. **Open in container**: One-time setup
2. **Use integrated terminal**: All tools available
3. **Edit with VSCode**: Extensions pre-configured
4. **Run verification**: `./verify-all.sh` before commits
5. **Use aliases**: `bb //...`, `bt //...`, etc.

### Git configuration
The container automatically configures:
- Safe directory for workspace
- Default branch: `main`
- Container-specific settings

### External services
- **Temporal**: Use `docker-compose up -d` in service directory
- **Databases**: Consider additional containers via docker-compose

## CI/CD Parity

The dev container uses the same tools and versions as CI:
- Ubuntu 24.04 base
- Python 3.12
- UV for dependencies
- Bazel 8.x for builds
- Same verification script

This ensures "if it works in the container, it works in CI."

## Support

- **Issues**: Check `DEVELOPMENT_TEST_PLAN.md` for command verification
- **Process**: See `developer-verification.process.md` for detailed workflow
- **Decision rationale**: See `DEC-2025-07-23-001-ubuntu-dev-container.decision.md`

---

**Built for Company OS**: Explicit over implicit, single source of truth, quality gates, and human-AI partnership.
