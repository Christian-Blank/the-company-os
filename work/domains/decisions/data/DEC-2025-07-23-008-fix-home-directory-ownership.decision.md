---
title: "Decision: Fix Home Directory Ownership in Dev Container User Rename"
type: "decision"
decision_id: "DEC-2025-07-23-008"
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
tags: ["development", "environment", "docker", "users", "permissions", "home-directory", "ubuntu", "devcontainer", "vscode", "ownership"]
---

# **Decision: Fix Home Directory Ownership in Dev Container User Rename**

**Status**: accepted
**Decision ID**: DEC-2025-07-23-008
**Date Decided**: 2025-07-23
**Deciders**: Cline AI Agent, Christian Blank

---

## **Context**

### **Problem Statement**
The dev container was building successfully but failing when VS Code attempted to install its server components. The error was:
```
mkdir: cannot create directory '/home/vscode/.vscode-server': Permission denied
```

Root cause analysis revealed that when renaming the existing Ubuntu user (uid=1000, name='ubuntu') to 'vscode', the home directory ownership was not properly handled:
1. The home directory remained at `/home/ubuntu` instead of moving to `/home/vscode`
2. Even when moved, the directory ownership remained with root instead of the vscode user
3. VS Code requires write access to `/home/vscode/.vscode-server` but was denied due to incorrect permissions

### **Triggering Signals**
This decision was made after implementing DEC-2025-07-23-007 (race condition fix) when the container built successfully but VS Code failed to start with permission errors. The issue occurred specifically in the user rename scenario where Ubuntu 24.04's default 'ubuntu' user needed to be renamed to 'vscode'.

### **Constraints**
- **Technical**: Must maintain all user creation scenarios while fixing home directory ownership
- **Resource**: VS Code must be able to write to user's home directory
- **Business**: Developer environment must work immediately after container startup
- **Philosophical**: Must handle all edge cases robustly without breaking existing functionality

### **Assumptions**
- Home directory ownership is critical for VS Code server installation
- The `-m` flag with usermod will properly move and re-own the home directory
- Explicit `chown -R` provides a safety net for any ownership issues
- The solution should work for both user creation and user rename scenarios

### **Environment State**
- **System Version**: Ubuntu 24.04 LTS with UID 1000 assigned to 'ubuntu' user
- **Team Composition**: Development team blocked by VS Code server installation failures
- **External Factors**: VS Code dev containers extension requirements for home directory access
- **Dependencies**: File system permissions, user/group management commands

---

## **Options Considered**

### **Option A**: Fix Home Directory Movement and Ownership (Recommended)
**Description**: Use usermod with `-m -d` flags and add explicit ownership fix

**Pros**:
- Addresses root cause of permission issues
- Maintains all existing functionality
- Provides comprehensive solution for both scenarios (create/rename)
- Follows Unix best practices for user management

**Cons**:
- Slightly more complex usermod command
- Requires understanding of home directory movement

**Estimated Effort**: 10 minutes to implement and test
**Risk Assessment**: Very low - well-established Unix user management practices

### **Option B**: Create New User and Delete Old
**Description**: Delete the existing ubuntu user and create vscode user fresh

**Pros**:
- Clean slate approach
- No home directory movement complexity

**Cons**:
- Destructive operation could lose system configuration
- More complex logic to handle existing files
- Could break system functionality that depends on ubuntu user
- Not idempotent

**Estimated Effort**: 30 minutes to implement safely
**Risk Assessment**: High - destructive operations with potential system impact

### **Option C**: Use Different UID to Avoid Conflict
**Description**: Use UID 1001 or other value to avoid the ubuntu user entirely

**Pros**:
- Simple solution that sidesteps the conflict
- No user renaming needed

**Cons**:
- Breaks dev container conventions (UID 1000)
- Could cause file permission issues with mounted volumes
- Doesn't solve the fundamental robustness problem
- May conflict with other system users

**Estimated Effort**: 5 minutes to change UID
**Risk Assessment**: Medium - avoids immediate issue but creates new problems

### **Option D**: Fix Permissions Post-Creation
**Description**: Create user normally then fix permissions with separate commands

**Pros**:
- Separates concerns between user creation and permission fixing
- Clear intent of permission operations

**Cons**:
- More complex multi-step process
- Doesn't address the fundamental home directory movement issue
- Could still have race conditions between steps

**Estimated Effort**: 20 minutes to implement multi-step process
**Risk Assessment**: Medium - addresses symptoms but not root cause

---

## **Decision**

### **Selected Option**: Option A - Fix Home Directory Movement and Ownership

### **Rationale**
The decision to fix home directory movement and ownership was made because:

1. **Root Cause Solution**: Addresses the fundamental issue of home directory ownership during user rename
2. **Comprehensive Fix**: Handles both user creation and user rename scenarios properly
3. **Unix Best Practices**: Uses standard usermod flags (`-m -d`) designed for this exact purpose
4. **Safety Net**: Explicit `chown -R` ensures ownership is correct regardless of usermod behavior
5. **VS Code Compatibility**: Ensures VS Code server can install and run properly

The implementation uses three key improvements:
- `usermod -l ... -d /home/vscode -m`: Renames user, sets new home path, and moves directory
- `chown -R vscode:vscode /home/vscode`: Guarantees correct ownership after all operations
- Maintains existing logic for user creation scenario

### **Charter Alignment**
This decision aligns with Company OS service architecture charter principles:
- **Explicit over Implicit**: Explicitly handles home directory movement and ownership
- **Quality Gates**: Ensures VS Code can install and function properly
- **Robustness**: Provides comprehensive solution for all user creation scenarios
- **Standards Compliance**: Follows Unix user management best practices

---

## **Consequences**

### **Immediate Impact**
- VS Code server installs successfully without permission errors
- Home directory ownership is correct for both creation and rename scenarios
- Dev container becomes fully functional for development work
- No functional changes to user capabilities or permissions

### **Long-term Effects**
- **Enables**: Full VS Code dev container functionality across all Ubuntu 24.04 variants
- **Prevents**: Home directory permission issues in user management
- **Creates**: Robust pattern for handling user directory ownership
- **Maintains**: All existing user creation and rename capabilities

### **Success Metrics**
- **VS Code Installation**: 100% successful VS Code server installation
- **Home Directory Access**: Full read/write access to user home directory
- **Container Functionality**: Complete dev container feature set works properly

### **Risk Mitigation**
- **Risk**: Home directory movement failures → **Mitigation**: Explicit chown provides safety net
- **Risk**: Complex usermod command errors → **Mitigation**: Use well-documented standard flags
- **Risk**: Permission edge cases → **Mitigation**: Comprehensive ownership fix covers all scenarios

---

## **Implementation**

### **Action Items**

1. **Update User Creation Logic with Home Directory Fix**
   - **Owner**: Cline AI Agent
   - **Timeline**: Immediate
   - **Dependencies**: None

2. **Test VS Code Server Installation**
   - **Owner**: Christian Blank
   - **Timeline**: After Dockerfile update
   - **Dependencies**: Item 1 complete

3. **Validate All User Scenarios**
   - **Owner**: Development team
   - **Timeline**: During testing
   - **Dependencies**: Item 2 complete

### **Implementation Path**
1. Update the user creation RUN block with proper home directory handling:
   ```dockerfile
   RUN set -eux; \
       # ensure group
       if ! getent group "${USER_GID}" >/dev/null; then
           groupadd --gid "${USER_GID}" "${USERNAME}";
       fi; \
       # create user or rename existing uid=1000
       if id -u "${USER_UID}" >/dev/null 2>&1; then
           OLD_USER="$(getent passwd "${USER_UID}" | cut -d: -f1)"; \
           if [ "${OLD_USER}" != "${USERNAME}" ]; then
               OLD_GROUP="$(id -gn "${OLD_USER}")"; \
               usermod -l "${USERNAME}" \
                       -d "/home/${USERNAME}" -m \
                       "${OLD_USER}"; \
               groupmod -n "${USERNAME}" "${OLD_GROUP}";
           fi; \
       else
           useradd --uid  "${USER_UID}" \
                   --gid  "${USER_GID}" \
                   --create-home --shell /bin/bash "${USERNAME}";
       fi; \
       # guarantee ownership of the home hierarchy
       chown -R "${USERNAME}:${USERNAME}" "/home/${USERNAME}"; \
       # password-less sudo
       echo "${USERNAME} ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME}; \
       chmod 0440 /etc/sudoers.d/${USERNAME}
   ```

2. Test container build and VS Code server installation
3. Verify all development tools work properly
4. Document the complete solution

### **Rollback Plan**
- **Conditions**: If home directory operations cause issues (very unlikely)
- **Steps**: Revert to DEC-2025-07-23-007 implementation and investigate alternatives
- **Preservation**: No data preservation needed for build-time changes

---

## **Review**

### **Review Triggers**
- **Time-based**: Review if similar permission issues occur elsewhere
- **Event-based**: Review if VS Code server installation fails
- **Metric-based**: Review if dev container adoption drops below expected levels

### **Review Process**
1. **Data gathering**: Monitor VS Code installation success rates and permission errors
2. **Analysis**: Assess if the home directory solution continues to be effective
3. **Decision**: Maintain approach or investigate newer user management patterns

---

## **Learning Capture**

### **Expected Outcomes**
- 100% successful VS Code server installations in dev containers
- Proper home directory ownership across all user creation scenarios
- Deep understanding of Unix user management in containerized environments
- Reusable pattern for robust user directory handling

### **Monitoring Plan**
- **Data to collect**: VS Code installation success rates, permission errors, home directory ownership
- **Frequency**: Every container build and startup
- **Responsible**: Platform team and container maintainers

### **Signal Generation**
- **Positive outcomes**: Generate signals about successful home directory management patterns
- **Negative outcomes**: Generate signals if permission issues occur elsewhere
- **Unexpected consequences**: Monitor for any side effects of home directory operations

---

## **Notes**

This decision represents the final piece of the comprehensive user creation solution for Ubuntu 24.04 dev containers. The home directory ownership issue is a classic Unix systems administration challenge that occurs when renaming users without properly handling their file ownership.

### **Technical Details**
The key usermod flags:
- `-l newname`: Changes the login name
- `-d /new/home/path`: Sets the new home directory path
- `-m`: Moves the contents of the old home directory to the new location

The explicit `chown -R` serves as a safety net because:
1. It ensures ownership is correct regardless of usermod behavior
2. It handles any files that might have been created by root during the build process
3. It provides a clear, explicit ownership guarantee

### **Unix User Management Best Practices**
This solution demonstrates several Unix user management best practices:
- Always move home directories when renaming users
- Explicitly set ownership after user operations
- Use standard tools (usermod, chown) rather than custom scripts
- Handle both creation and modification scenarios in the same logic

### **Dev Container Standards**
This ensures compliance with VS Code dev container expectations:
- User has full control over their home directory
- VS Code server can install and run properly
- Development tools have proper file system access
- Container behaves like a native development environment
