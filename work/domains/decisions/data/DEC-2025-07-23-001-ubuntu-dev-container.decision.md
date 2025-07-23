---
title: "Decision: Implement Ubuntu 24 LTS Development Container"
type: "decision"
decision_id: "DEC-2025-07-23-001"
status: "accepted"
date_proposed: "2025-07-23"
date_decided: "2025-07-23"
deciders: ["Cline AI Agent", "Christian Blank"]
parent_charter: "company_os/domains/charters/data/service-architecture.charter.md"
related_signals: []
related_brief: ""
related_project: ""
supersedes: ""
superseded_by: ""
tags: ["development", "environment", "consistency", "containerization", "ubuntu", "devcontainer"]
---

# **Decision: Implement Ubuntu 24 LTS Development Container**

**Status**: accepted
**Decision ID**: DEC-2025-07-23-001
**Date Decided**: 2025-07-23
**Deciders**: Cline AI Agent, Christian Blank

---

## **Context**

### **Problem Statement**
After standardizing the development workflow to use Bazel + UV exclusively, we need to ensure perfect consistency across all developer environments. Currently, developers may have different:
- Operating systems (macOS, Windows, Linux)
- Python versions and installation methods
- Tool versions (Bazel, UV, Docker)
- System dependencies and configurations

This leads to "works on my machine" problems that waste development time and create friction for new contributors.

### **Triggering Signals**
This decision follows the completion of:
- Updated `developer-verification.process.md` (v2.0) to use Bazel + UV only
- Created `verify-all.sh` script for consistent verification
- Created comprehensive `DEVELOPMENT_TEST_PLAN.md` with 62 commands to test

The natural next step is to provide a consistent environment where all these commands work identically for every developer.

### **Constraints**
- **Technical**: Must support Bazel 8.x, Python 3.12, UV, Docker-in-Docker
- **Resource**: Should be fast to set up and not resource-intensive
- **Business**: Must work with existing VSCode dev container ecosystem
- **Philosophical**: Aligns with Company OS principle of "explicit over implicit" by making environment deterministic

### **Assumptions**
- Developers use VSCode or compatible editors that support dev containers
- Docker Desktop or equivalent is available on developer machines
- Internet connectivity is available for initial container setup
- Ubuntu 24 LTS provides stable, long-term supported base environment

### **Environment State**
- **System Version**: Company OS with Bazel 8.x + bzlmod, Python 3.12, UV workflow
- **Team Composition**: Multi-platform development team (macOS, Windows, Linux)
- **External Factors**: VSCode dev containers are industry standard for environment consistency
- **Dependencies**: Docker ecosystem, VSCode dev containers extension

---

## **Options Considered**

### **Option A**: No Containerization (Status Quo)
**Description**: Continue with current approach of documented environment setup per platform

**Pros**:
- No additional tooling required
- Uses native OS performance
- Familiar to developers who prefer local development

**Cons**:
- "Works on my machine" problems persist
- Complex platform-specific setup instructions
- Difficult to maintain consistency across team
- New developer onboarding friction
- Different behavior across macOS/Windows/Linux

**Estimated Effort**: Ongoing maintenance burden
**Risk Assessment**: High - continued inconsistency issues

### **Option B**: Ubuntu 24 LTS Dev Container
**Description**: Create VSCode dev container with Ubuntu 24 LTS base, pre-configured with all required tools

**Pros**:
- Perfect environment consistency across all developers
- Fast onboarding - "Open in Container" and start coding
- Isolated from host system - no pollution
- Can test exact same environment in CI/CD
- Long-term support from Ubuntu 24 LTS
- Industry standard approach

**Cons**:
- Requires Docker Desktop
- Slight performance overhead vs native
- Learning curve for developers new to containers
- Storage space for container image

**Estimated Effort**: 4-6 hours initial setup, minimal ongoing maintenance
**Risk Assessment**: Low - well-established technology with good ecosystem support

### **Option C**: Alternative Base Images (Alpine, Debian, etc.)
**Description**: Use different Linux distribution as base

**Pros**:
- Potentially smaller image size (Alpine)
- Different package managers available

**Cons**:
- Less familiar to most developers
- May require more customization
- Ubuntu has better tool support and documentation
- Shorter support cycles for non-LTS versions

**Estimated Effort**: Similar to Option B but with more customization
**Risk Assessment**: Medium - less standard choice

---

## **Decision**

### **Selected Option**: Option B - Ubuntu 24 LTS Dev Container

### **Rationale**
Ubuntu 24 LTS dev container was selected because:

1. **Perfect Consistency**: Every developer gets identical environment, eliminating "works on my machine" issues
2. **Industry Standard**: VSCode dev containers are widely adopted best practice
3. **Long-term Stability**: Ubuntu 24 LTS provides 5-year support lifecycle
4. **CI/CD Parity**: Can use same container image in GitHub Actions
5. **Developer Experience**: One-click setup with "Open in Container"
6. **Isolation**: No pollution of developer's host system
7. **Tool Support**: Excellent support for Python, Bazel, UV, Docker-in-Docker

The slight performance overhead is acceptable given the significant benefits in consistency and developer experience.

### **Charter Alignment**
This decision aligns with Company OS service architecture charter principles:
- **Explicit over Implicit**: Environment is completely specified and reproducible
- **Single Source of Truth**: One container definition for all environments
- **Quality Gates**: Ensures consistent testing environment
- **Developer Experience**: Removes friction from setup and onboarding

---

## **Consequences**

### **Immediate Impact**
- All developers can use identical development environment
- New contributors can start coding within minutes
- Environment setup becomes deterministic and testable
- Host system remains clean and unmodified

### **Long-term Effects**
- **Enables**:
  - Consistent CI/CD pipeline using same container
  - Reproducible builds across all environments
  - Easier debugging of environment-specific issues
  - Simplified documentation with single setup path
- **Prevents**:
  - Platform-specific environment issues
  - Version drift across developer machines
  - Complex multi-platform setup documentation
- **Creates**:
  - Dependency on Docker ecosystem
  - Container image to maintain and update

### **Success Metrics**
- **Setup Time**: New developer productive in < 5 minutes
- **Environment Issues**: Reduce environment-related issues to near zero
- **Build Consistency**: 100% success rate for `./verify-all.sh` in container
- **Developer Satisfaction**: Positive feedback on setup experience

### **Risk Mitigation**
- **Risk**: Docker not available → **Mitigation**: Maintain fallback documentation for local setup
- **Risk**: Container bloat → **Mitigation**: Regular cleanup and optimization of image layers
- **Risk**: Performance issues → **Mitigation**: Optimize container for development workflow

---

## **Implementation**

### **Action Items**

1. **Create `.devcontainer/` Directory Structure**
   - **Owner**: Cline AI Agent
   - **Timeline**: Immediate
   - **Dependencies**: None

2. **Create Dockerfile with Required Tools**
   - **Owner**: Cline AI Agent
   - **Timeline**: Immediate
   - **Dependencies**: Item 1 complete

3. **Configure devcontainer.json**
   - **Owner**: Cline AI Agent
   - **Timeline**: Immediate
   - **Dependencies**: Item 2 complete

4. **Create Post-Creation Setup Script**
   - **Owner**: Cline AI Agent
   - **Timeline**: Immediate
   - **Dependencies**: Item 3 complete

5. **Test Container with Complete Command Suite**
   - **Owner**: Christian Blank
   - **Timeline**: After implementation
   - **Dependencies**: Items 1-4 complete

6. **Update Documentation**
   - **Owner**: Cline AI Agent
   - **Timeline**: After testing
   - **Dependencies**: Item 5 complete

### **Implementation Path**
1. Create `.devcontainer/devcontainer.json` with VSCode configuration
2. Create `.devcontainer/Dockerfile` based on Ubuntu 24.04 with all tools
3. Create `.devcontainer/post-create.sh` for environment setup
4. Test container by running complete `DEVELOPMENT_TEST_PLAN.md` suite
5. Update `DEVELOPER_WORKFLOW.md` to mention dev container option
6. Update `README.md` with dev container quick start

### **Rollback Plan**
- **Conditions**: If container causes significant performance issues or developer resistance
- **Steps**: Simply remove `.devcontainer/` directory to return to previous state
- **Preservation**: No existing development workflow is changed - container is additive

---

## **Review**

### **Review Triggers**
- **Time-based**: Review after 3 months of usage
- **Event-based**: Review if container setup takes > 10 minutes or frequent issues reported
- **Metric-based**: Review if < 80% of developers adopt container approach

### **Review Process**
1. **Data gathering**: Survey developer satisfaction, measure setup times, count environment issues
2. **Analysis**: Compare metrics against success criteria, gather feedback
3. **Decision**: Maintain, optimize, or consider alternative approaches

---

## **Learning Capture**

### **Expected Outcomes**
- Developers report faster onboarding and fewer environment issues
- Build consistency improves significantly
- CI/CD pipeline reliability increases
- Documentation burden decreases

### **Monitoring Plan**
- **Data to collect**: Setup times, error rates, developer feedback, adoption rates
- **Frequency**: Weekly for first month, then monthly
- **Responsible**: Project maintainers

### **Signal Generation**
- **Positive outcomes**: Generate signals about successful practices for other projects
- **Negative outcomes**: Generate signals about container limitations or improvements needed
- **Unexpected consequences**: Monitor for performance impacts or workflow disruptions

---

## **Notes**

This decision represents a shift toward containerized development environments, following industry best practices. The Ubuntu 24 LTS base provides the stability needed for long-term development while ensuring all developers have access to the exact same toolchain and environment configuration.

The implementation will be validated by running the complete 62-command test suite from `DEVELOPMENT_TEST_PLAN.md` to ensure all development operations work correctly in the containerized environment.
