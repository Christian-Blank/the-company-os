---
title: "Decision: Delay User Switch Until After Setup in Dev Container Dockerfile"
type: "decision"
decision_id: "DEC-2025-07-23-004"
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
tags: ["development", "environment", "docker", "users", "permissions", "ubuntu", "devcontainer", "setup"]
---

# **Decision: Delay User Switch Until After Setup in Dev Container Dockerfile**

**Status**: accepted
**Decision ID**: DEC-2025-07-23-004
**Date Decided**: 2025-07-23
**Deciders**: Cline AI Agent, Christian Blank

---

## **Context**

### **Problem Statement**
The dev container build was failing with the error:
```
unable to find user vscode: no matching entries in passwd file
```

This occurred during the git configuration step, which was running as the vscode user after a `USER $USERNAME` directive, but the user context wasn't properly established for subsequent commands.

### **Triggering Signals**
This decision was made during implementation of DEC-2025-07-23-001 (Ubuntu Dev Container) immediately after resolving DEC-2025-07-23-003 (robust user creation). The error occurred when trying to run `git config --global --add safe.directory` as the vscode user.

### **Constraints**
- **Technical**: Docker USER directive changes context for all subsequent RUN commands
- **Resource**: Container build must complete successfully
- **Business**: Cannot delay development environment availability
- **Philosophical**: Setup commands should run with appropriate privileges

### **Assumptions**
- Setup commands (git config, directory creation) need consistent execution context
- User switching should happen only after all setup is complete
- Root privileges are needed for system configuration during build
- The vscode user should only be active for the final runtime environment

### **Environment State**
- **System Version**: Ubuntu 24.04 LTS with multi-stage Dockerfile
- **Team Composition**: Development team using VSCode dev containers
- **External Factors**: Docker build process and user context switching
- **Dependencies**: User creation, git configuration, directory setup

---

## **Options Considered**

### **Option A**: Move USER Directive After All Setup Commands
**Description**: Keep all setup commands running as root, switch to vscode user only at the very end

**Pros**:
- Clear separation between setup (root) and runtime (vscode) contexts
- Ensures all setup commands have consistent execution environment
- Follows Docker best practices for multi-stage builds
- Simplifies troubleshooting by reducing context switches

**Cons**:
- Requires careful review of which commands need root vs user privileges
- Directory permissions need to be set explicitly

**Estimated Effort**: 10 minutes to reorganize Dockerfile
**Risk Assessment**: Low - standard Docker pattern

### **Option B**: Run Git Config as Root with Explicit User
**Description**: Keep USER directive but run git config with explicit user specification

**Pros**:
- Minimal change to current structure
- Could solve immediate issue

**Cons**:
- Doesn't address fundamental context switching problem
- More complex command with user specification
- Other setup commands might have similar issues
- Not a scalable solution

**Estimated Effort**: 5 minutes to modify command
**Risk Assessment**: Medium - doesn't solve root cause

### **Option C**: Create Directories and Configs Before User Creation
**Description**: Rearrange commands to do all system setup before creating users

**Pros**:
- Could avoid user context issues
- Might work for current case

**Cons**:
- Complex dependency management
- Some configs might need user to exist first
- Doesn't address fundamental USER directive timing issue
- Could create permission problems

**Estimated Effort**: 20 minutes to reorganize and test
**Risk Assessment**: High - complex dependencies

### **Option D**: Use Multiple USER Directives
**Description**: Switch back and forth between root and vscode user as needed

**Pros**:
- Fine-grained control over execution context
- Could handle specific command requirements

**Cons**:
- Makes Dockerfile complex and hard to follow
- Error-prone with multiple context switches
- Violates principle of clear separation
- Debugging becomes difficult

**Estimated Effort**: 15 minutes to implement switches
**Risk Assessment**: High - complex and error-prone

---

## **Decision**

### **Selected Option**: Option A - Move USER Directive After All Setup Commands

### **Rationale**
The decision to delay the user switch was made because:

1. **Clear Separation**: Establishes a clean boundary between setup (root) and runtime (user) contexts
2. **Docker Best Practice**: Follows standard pattern of doing system setup as root, then switching to non-root user for runtime
3. **Consistency**: All setup commands run in the same context, reducing complexity
4. **Reliability**: Eliminates user context issues during build process
5. **Maintainability**: Easier to understand and debug with clear phase separation

The approach creates two distinct phases:
- **Setup Phase (root)**: User creation, system configuration, directory setup
- **Runtime Phase (vscode)**: Final environment for development

### **Charter Alignment**
This decision aligns with Company OS service architecture charter principles:
- **Explicit over Implicit**: Clearly separates setup and runtime phases
- **Quality Gates**: Ensures container builds succeed reliably
- **Maintainability**: Creates understandable, debuggable container structure
- **Robustness**: Reduces complexity and potential failure points

---

## **Consequences**

### **Immediate Impact**
- Dev container builds successfully without user context errors
- Clear separation between setup and runtime phases
- All setup commands run with consistent root privileges
- Directory permissions set explicitly where needed

### **Long-term Effects**
- **Enables**: Reliable container builds with predictable execution contexts
- **Prevents**: User context confusion during build process
- **Creates**: Standard pattern for future container modifications
- **Maintains**: Security by switching to non-root user for runtime

### **Success Metrics**
- **Container Build Success**: 100% successful builds
- **Setup Reliability**: All setup commands execute correctly
- **Runtime Security**: Container runs as non-root user

### **Risk Mitigation**
- **Risk**: Directory permission issues → **Mitigation**: Explicitly set ownership where needed
- **Risk**: Commands requiring user context → **Mitigation**: Identify and handle in runtime phase

---

## **Implementation**

### **Action Items**

1. **Reorganize Dockerfile User Context**
   - **Owner**: Cline AI Agent
   - **Timeline**: Immediate
   - **Dependencies**: None

2. **Test Container Build Process**
   - **Owner**: Christian Blank
   - **Timeline**: After Dockerfile update
   - **Dependencies**: Item 1 complete

3. **Verify Directory Permissions**
   - **Owner**: Development team
   - **Timeline**: During first container use
   - **Dependencies**: Item 2 complete

### **Implementation Path**
1. Move `USER $USERNAME` directive to just before final `CMD` instruction
2. Ensure all setup commands (git config, directory creation) run as root
3. Explicitly set directory ownership where needed for vscode user access
4. Test build to ensure successful completion
5. Verify runtime behavior with vscode user

### **Rollback Plan**
- **Conditions**: If directory permissions or runtime access issues occur
- **Steps**: Revert USER directive placement and investigate specific command requirements
- **Preservation**: No data preservation needed for build-time changes

---

## **Review**

### **Review Triggers**
- **Time-based**: Review during major container architecture changes
- **Event-based**: Review if build context issues arise
- **Metric-based**: Review if build success rate drops below 95%

### **Review Process**
1. **Data gathering**: Monitor build success rates and user context issues
2. **Analysis**: Assess if the setup/runtime separation continues to be effective
3. **Decision**: Maintain approach or investigate newer container user patterns

---

## **Learning Capture**

### **Expected Outcomes**
- Container builds work reliably with clear phase separation
- No more user context errors during build
- Better understanding of Docker USER directive behavior
- Foundation for other container build patterns

### **Monitoring Plan**
- **Data to collect**: Container build success rates, user context errors, permission issues
- **Frequency**: Every container build
- **Responsible**: Platform team and container maintainers

### **Signal Generation**
- **Positive outcomes**: Generate signals about successful container build patterns
- **Negative outcomes**: Generate signals if user context or permission issues arise
- **Unexpected consequences**: Monitor for runtime behavior changes

---

## **Notes**

This decision reflects the fundamental Docker principle of separating build-time setup from runtime execution. The USER directive in Docker affects all subsequent RUN, CMD, and ENTRYPOINT instructions, so its placement is critical.

The pattern we're implementing:
1. **Build Phase**: All setup as root with system privileges
2. **Runtime Phase**: Switch to non-root user for security

This is the standard approach used in most production Docker containers and provides the best balance of functionality and security.
