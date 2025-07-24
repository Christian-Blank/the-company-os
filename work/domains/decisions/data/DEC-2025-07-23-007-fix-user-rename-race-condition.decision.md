---
title: "Decision: Fix Race Condition in User Rename Logic for Dev Container"
type: "decision"
decision_id: "DEC-2025-07-23-007"
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
tags: ["development", "environment", "docker", "users", "groups", "ubuntu", "devcontainer", "race-condition", "bugfix"]
---

# **Decision: Fix Race Condition in User Rename Logic for Dev Container**

**Status**: accepted
**Decision ID**: DEC-2025-07-23-007
**Date Decided**: 2025-07-23
**Deciders**: Cline AI Agent, Christian Blank

---

## **Context**

### **Problem Statement**
The dev container build was failing with a race condition error during user renaming:
```
id: 'ubuntu': no such user
groupmod: group '' does not exist
```

This occurred in the user rename path of DEC-2025-07-23-006's comprehensive user creation solution. The race condition happens when:
1. We identify a user with UID 1000 (named 'ubuntu')
2. We rename the user from 'ubuntu' to 'vscode' using `usermod`
3. We attempt to get the group of the old username with `id -gn "${CURRENT_USER}"`
4. But the old username no longer exists after the rename, causing `id -gn` to fail

### **Triggering Signals**
This decision was made immediately after implementing DEC-2025-07-23-006 when the container build failed during testing. The error occurred specifically in the user rename branch where UID 1000 existed but had a different name than 'vscode'.

### **Constraints**
- **Technical**: Must maintain all functionality from comprehensive user creation solution
- **Resource**: Must fix the race condition without breaking idempotency
- **Business**: Cannot delay development environment availability
- **Philosophical**: Must be robust and debuggable

### **Assumptions**
- The race condition only affects the rename path, not user creation path
- Capturing group information before rename operations will prevent the race
- The solution should maintain all existing robustness guarantees
- Better debugging output will help with future issues

### **Environment State**
- **System Version**: Ubuntu 24.04 LTS with UID 1000 assigned to 'ubuntu' user
- **Team Composition**: Development team waiting for working dev container
- **External Factors**: Docker build process and shell command execution order
- **Dependencies**: User/group modification commands (usermod, groupmod)

---

## **Options Considered**

### **Option A**: Capture Group Before Rename (Recommended)
**Description**: Capture both OLD_USER and OLD_GROUP before any rename operations

**Pros**:
- Fixes the race condition at its root cause
- Maintains all existing functionality
- Simple and clean solution
- Adds better debugging with `set -eux`

**Cons**:
- Requires updating the script logic
- Slightly more verbose variable management

**Estimated Effort**: 5 minutes to implement and test
**Risk Assessment**: Very low - surgical fix to specific race condition

### **Option B**: Use Different Group Management Strategy
**Description**: Avoid groupmod entirely and handle group management differently

**Pros**:
- Could avoid the race condition
- Might be more robust

**Cons**:
- More complex change with higher risk
- Could break existing group permission logic
- Doesn't address the fundamental timing issue

**Estimated Effort**: 30 minutes to redesign and test
**Risk Assessment**: Medium - broader changes with unknown side effects

### **Option C**: Add Sleep/Retry Logic
**Description**: Add delays or retry mechanisms around the problematic commands

**Pros**:
- Minimal code changes
- Could work around timing issues

**Cons**:
- Doesn't fix the root cause
- Unreliable workaround
- Adds unnecessary build time
- Could still fail under load

**Estimated Effort**: 10 minutes to add retry logic
**Risk Assessment**: High - unreliable band-aid solution

### **Option D**: Revert to Simpler User Creation
**Description**: Go back to a simpler approach that doesn't handle the rename case

**Pros**:
- Would avoid the complex rename path
- Simpler logic

**Cons**:
- Loses the comprehensive Ubuntu 24.04 compatibility
- Doesn't solve the fundamental UID 1000 conflict issue
- Step backwards in robustness

**Estimated Effort**: 15 minutes to simplify
**Risk Assessment**: High - loses production-ready capabilities

---

## **Decision**

### **Selected Option**: Option A - Capture Group Before Rename

### **Rationale**
The decision to capture the group before rename was made because:

1. **Root Cause Fix**: Addresses the race condition at its source rather than working around it
2. **Minimal Impact**: Requires only a small change to the existing logic
3. **Maintains Robustness**: Preserves all the comprehensive user creation capabilities
4. **Better Debugging**: Adding `set -eux` provides immediate error identification
5. **Industry Standard**: This pattern is commonly used in production shell scripts

The fix captures both `OLD_USER` and `OLD_GROUP` before any modifications, ensuring all information needed for rename operations is available throughout the process.

### **Charter Alignment**
This decision aligns with Company OS service architecture charter principles:
- **Explicit over Implicit**: Explicitly captures required information before operations
- **Quality Gates**: Ensures container builds succeed reliably without race conditions
- **Robustness**: Maintains all edge case handling while fixing the timing issue
- **Maintainability**: Adds debugging capabilities for future troubleshooting

---

## **Consequences**

### **Immediate Impact**
- Dev container builds successfully without race condition errors
- All comprehensive user creation scenarios continue to work
- Better debugging output for future container issues
- No changes to functionality or user experience

### **Long-term Effects**
- **Enables**: Reliable container builds in all Ubuntu 24.04 scenarios
- **Prevents**: Race conditions in user management operations
- **Creates**: More robust pattern for similar shell script operations
- **Maintains**: All existing capabilities and idempotency guarantees

### **Success Metrics**
- **Build Success Rate**: 100% across all Ubuntu 24.04 variations
- **Race Condition Elimination**: No more user/group rename timing errors
- **Functionality Preservation**: All user creation scenarios work as before

### **Risk Mitigation**
- **Risk**: Variable capture errors → **Mitigation**: Use `set -eux` for immediate error detection
- **Risk**: Logic complexity → **Mitigation**: Clear variable naming and comments

---

## **Implementation**

### **Action Items**

1. **Update User Creation Logic with Race Condition Fix**
   - **Owner**: Cline AI Agent
   - **Timeline**: Immediate
   - **Dependencies**: None

2. **Test Container Build Process**
   - **Owner**: Christian Blank
   - **Timeline**: After Dockerfile update
   - **Dependencies**: Item 1 complete

3. **Validate All User Creation Scenarios**
   - **Owner**: Development team
   - **Timeline**: During testing
   - **Dependencies**: Item 2 complete

### **Implementation Path**
1. Replace the user creation RUN block with race-condition-free version:
   ```dockerfile
   RUN set -eux; \
       # 1. create group if missing
       if ! getent group "${USER_GID}" >/dev/null; then
           groupadd --gid "${USER_GID}" "${USERNAME}";
       fi; \
       # 2. create user or rename existing UID-1000 user
       if id -u "${USER_UID}" >/dev/null 2>&1; then
           OLD_USER="$(getent passwd "${USER_UID}" | cut -d: -f1)"; \
           if [ "${OLD_USER}" != "${USERNAME}" ]; then
               OLD_GROUP="$(id -gn "${OLD_USER}")"; \
               usermod   --login "${USERNAME}" \
                         --home  "/home/${USERNAME}" \
                         "${OLD_USER}"; \
               groupmod  --new-name "${USERNAME}" "${OLD_GROUP}";
           fi; \
       else
           useradd --uid  "${USER_UID}" \
                   --gid  "${USER_GID}" \
                   --create-home --shell /bin/bash "${USERNAME}";
       fi; \
       # 3. sudo without password
       echo "${USERNAME} ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME}; \
       chmod 0440 /etc/sudoers.d/${USERNAME}
   ```

2. Test build to ensure race condition is eliminated
3. Verify all user creation scenarios work correctly
4. Update related documentation

### **Rollback Plan**
- **Conditions**: If the fix introduces other issues (unlikely)
- **Steps**: Revert to DEC-2025-07-23-006 implementation and investigate alternatives
- **Preservation**: No data preservation needed for build-time changes

---

## **Review**

### **Review Triggers**
- **Time-based**: Review if similar race conditions occur elsewhere
- **Event-based**: Review if any user creation issues arise
- **Metric-based**: Review if build success rate drops below 95%

### **Review Process**
1. **Data gathering**: Monitor build success rates and user creation logs
2. **Analysis**: Assess if the race condition fix continues to be effective
3. **Decision**: Maintain approach or investigate newer solutions

---

## **Learning Capture**

### **Expected Outcomes**
- 100% reliable container builds without race conditions
- Better understanding of shell script timing issues in Docker
- Improved debugging capabilities for future container issues
- Reusable pattern for similar operations requiring atomic captures

### **Monitoring Plan**
- **Data to collect**: Build success rates, user creation timing, error logs
- **Frequency**: Every container build
- **Responsible**: Platform team and container maintainers

### **Signal Generation**
- **Positive outcomes**: Generate signals about successful race condition prevention patterns
- **Negative outcomes**: Generate signals if timing issues occur elsewhere
- **Unexpected consequences**: Monitor for any side effects of the debugging additions

---

## **Notes**

This decision represents a classic example of fixing a race condition by ensuring atomic operations and proper information capture before state-changing operations.

### **Technical Details**
The race condition occurred because:
1. `usermod --login` changes the username immediately
2. `id -gn "${OLD_USERNAME}"` then fails because the old username no longer exists
3. `groupmod` receives an empty string, causing failure

The fix ensures:
1. All required information is captured before any state changes
2. Operations proceed with captured values rather than live lookups
3. `set -eux` provides immediate error detection and variable expansion visibility

### **Shell Script Best Practices**
This pattern demonstrates several shell scripting best practices:
- Capture all required information before state-changing operations
- Use `set -eux` for debugging and error detection
- Clear variable naming to indicate temporal relationships (OLD_USER, OLD_GROUP)
- Atomic operation grouping to prevent partial state changes
