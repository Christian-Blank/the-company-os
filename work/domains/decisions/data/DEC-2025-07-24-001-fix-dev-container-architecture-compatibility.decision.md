---
title: "Decision: Fix Dev Container Architecture Compatibility for Multi-Platform Support"
type: "decision"
decision_id: "DEC-2025-07-24-001"
status: "accepted"
date_proposed: "2025-07-24"
date_decided: "2025-07-24"
deciders: ["Christian Blank", "Cline AI"]
parent_charter: "company_os/domains/charters/data/service-architecture.charter.md"
related_signals: []
related_brief: ""
related_project: ""
supersedes: ""
superseded_by: ""
tags: ["development", "environment", "docker", "architecture", "multi-platform", "bazel", "devcontainer", "compatibility"]
---

# **Decision: Fix Dev Container Architecture Compatibility for Multi-Platform Support**

**Status**: accepted
**Decision ID**: DEC-2025-07-24-001
**Date Decided**: 2025-07-24
**Deciders**: Christian Blank, Cline AI

---

## **Context**

### **Problem Statement**
The dev container post-creation script is failing with a Rosetta architecture compatibility error:
```
rosetta error: failed to open elf at /lib64/ld-linux-x86-64.so.2
```

Root cause analysis reveals that the Dockerfile is hardcoded to download x86_64 (amd64) versions of Bazelisk and Buildifier, but the container is running on ARM64 architecture (Apple Silicon Mac). This creates an architecture mismatch that prevents Bazel from executing properly during the development environment setup.

### **Triggering Signals**
This decision was made when the dev container build completed successfully but the post-creation command failed during Bazel version check. The error occurred specifically when Bazelisk attempted to download and execute Bazel binaries that were incompatible with the host architecture.

### **Constraints**
- **Technical**: Must support both x86_64 and ARM64 architectures transparently
- **Resource**: Container build must remain fast and reliable across platforms
- **Business**: Development team includes members using both Intel/AMD and Apple Silicon machines
- **Philosophical**: Must provide consistent development experience regardless of host architecture

### **Assumptions**
- Docker's TARGETPLATFORM argument provides reliable architecture detection
- Bazelisk and Buildifier releases include both amd64 and arm64 variants
- Architecture detection logic will work correctly in multi-platform builds
- The fix will not impact container build performance significantly

### **Environment State**
- **System Version**: Ubuntu 24.04 LTS dev container with hardcoded amd64 binary downloads
- **Team Composition**: Mixed development team using Intel/AMD and Apple Silicon hardware
- **External Factors**: Docker multi-platform support and GitHub release binary naming conventions
- **Dependencies**: Bazelisk v1.19.0, Buildtools v6.4.0, Docker buildx platform detection

---

## **Options Considered**

### **Option A**: Dynamic Architecture Detection with TARGETPLATFORM (Selected)
**Description**: Use Docker's built-in TARGETPLATFORM argument to detect architecture and download appropriate binaries

**Pros**:
- Uses Docker's native multi-platform support
- Transparent to users - works automatically
- Maintains current pinned versions for reproducibility
- Standard Docker best practice for multi-platform images
- No performance impact on container builds

**Cons**:
- Slightly more complex download logic
- Requires understanding of Docker platform detection

**Estimated Effort**: 15 minutes to implement and test
**Risk Assessment**: Very low - uses standard Docker multi-platform patterns

### **Option B**: Separate Dockerfiles for Each Architecture
**Description**: Create architecture-specific Dockerfiles (Dockerfile.amd64, Dockerfile.arm64)

**Pros**:
- Simple and explicit per-architecture
- No complex logic in individual Dockerfiles

**Cons**:
- Maintenance burden of multiple files
- Violates DRY principle
- Complex dev container configuration
- User must manually select appropriate file

**Estimated Effort**: 30 minutes to create and configure multiple files
**Risk Assessment**: Medium - maintenance complexity and user experience issues

### **Option C**: Runtime Architecture Detection
**Description**: Download correct binaries during container startup rather than build time

**Pros**:
- Could detect actual runtime architecture
- Single container image works everywhere

**Cons**:
- Slower container startup times
- Network dependency during startup
- More complex post-creation scripts
- Potential security implications of runtime downloads

**Estimated Effort**: 45 minutes to implement runtime detection
**Risk Assessment**: High - performance impact and complexity

### **Option D**: Use Multi-Architecture Base Images
**Description**: Rely on base image architecture detection rather than explicit binary downloads

**Pros**:
- Leverages existing multi-arch infrastructure
- No explicit architecture handling needed

**Cons**:
- Limited control over tool versions
- May not have pinned versions available
- Could break reproducible builds
- Doesn't solve the specific Bazelisk issue

**Estimated Effort**: Variable - depends on availability of suitable base images
**Risk Assessment**: High - loss of version control and reproducibility

---

## **Decision**

### **Selected Option**: Option A - Dynamic Architecture Detection with TARGETPLATFORM

### **Rationale**
The dynamic architecture detection approach was selected because:

1. **Docker Native Support**: Uses Docker's built-in TARGETPLATFORM argument, which is the standard approach for multi-platform container images
2. **Transparent Operation**: Works automatically without user intervention or configuration
3. **Maintains Reproducibility**: Preserves pinned version approach while adding architecture flexibility
4. **Standard Practice**: Follows established Docker multi-platform patterns used throughout the ecosystem
5. **Minimal Complexity**: Simple conditional logic that's easy to understand and maintain
6. **Future Proof**: Will work with Docker's evolving multi-platform support

The implementation detects whether the build platform is linux/amd64 or linux/arm64 and downloads the appropriate binary variant.

### **Charter Alignment**
This decision aligns with Company OS service architecture charter principles:
- **Explicit over Implicit**: Explicitly handles architecture differences rather than assuming x86_64
- **Quality Gates**: Ensures container works reliably across all developer platforms
- **Standards Compliance**: Follows Docker multi-platform best practices
- **Developer Experience**: Provides seamless experience regardless of hardware architecture

---

## **Consequences**

### **Immediate Impact**
- Dev container builds and runs successfully on both Intel/AMD and Apple Silicon machines
- Bazel and related tools execute correctly regardless of host architecture
- Post-creation script completes without architecture-related errors
- Development team has consistent experience across all hardware platforms

### **Long-term Effects**
- **Enables**: Full multi-platform development team support
- **Prevents**: Architecture-related failures in development environments
- **Creates**: Foundation for other multi-platform tool installations
- **Maintains**: Reproducible builds with pinned versions across architectures

### **Success Metrics**
- **Container Build Success**: 100% success rate across both x86_64 and ARM64 platforms
- **Tool Functionality**: Bazel, Buildifier work correctly on all architectures
- **Developer Experience**: No architecture-related setup issues reported

### **Risk Mitigation**
- **Risk**: Platform detection failure → **Mitigation**: Default to amd64 with clear error message
- **Risk**: Binary availability → **Mitigation**: Verify both architectures are available for pinned versions
- **Risk**: Build performance → **Mitigation**: Conditional logic has minimal overhead

---

## **Implementation**

### **Action Items**

1. **Update Dockerfile with Architecture Detection Logic**
   - **Owner**: Cline AI
   - **Timeline**: Immediate
   - **Dependencies**: None

2. **Test Container Build on Both Architectures**
   - **Owner**: Christian Blank
   - **Timeline**: After Dockerfile update
   - **Dependencies**: Item 1 complete

3. **Verify Tool Functionality Across Platforms**
   - **Owner**: Development team
   - **Timeline**: During testing
   - **Dependencies**: Item 2 complete

### **Implementation Path**
1. Add TARGETPLATFORM argument to Dockerfile
2. Implement architecture detection logic for Bazelisk download:
   - Extract architecture from TARGETPLATFORM
   - Map to appropriate binary naming convention
   - Download correct variant
3. Apply same logic to Buildifier download
4. Test build on both x86_64 and ARM64 systems
5. Verify all tools execute correctly

### **Rollback Plan**
- **Conditions**: If architecture detection causes build failures
- **Steps**: Revert to hardcoded amd64 downloads temporarily
- **Preservation**: Document architecture issues for alternative solution development

---

## **Review**

### **Review Triggers**
- **Time-based**: Review when Docker multi-platform support evolves significantly
- **Event-based**: Review if architecture detection fails for any platform
- **Metric-based**: Review if build success rate drops below 95% on any platform

### **Review Process**
1. **Data gathering**: Monitor build success rates across all platforms
2. **Analysis**: Assess effectiveness of architecture detection logic
3. **Decision**: Maintain approach or investigate newer multi-platform solutions

---

## **Learning Capture**

### **Expected Outcomes**
- Seamless multi-platform development environment support
- Better understanding of Docker multi-platform capabilities
- Reusable pattern for other architecture-dependent tool installations
- Improved developer onboarding experience regardless of hardware

### **Monitoring Plan**
- **Data to collect**: Build success rates by platform, tool execution success, developer feedback
- **Frequency**: Every container build and startup
- **Responsible**: Platform team and container maintainers

### **Signal Generation**
- **Positive outcomes**: Generate signals about successful multi-platform patterns
- **Negative outcomes**: Generate signals if platform detection issues arise
- **Unexpected consequences**: Monitor for performance impacts or edge cases

---

## **Notes**

This decision addresses a common challenge in multi-platform Docker development where tools must be architecture-aware. The solution leverages Docker's native multi-platform support rather than implementing custom detection logic.

### **Technical Details**
The TARGETPLATFORM argument format is:
- `linux/amd64` for Intel/AMD x86_64 systems
- `linux/arm64` for ARM64 systems (Apple Silicon, ARM servers)

Binary naming conventions for the affected tools:
- Bazelisk: `bazelisk-linux-amd64` and `bazelisk-linux-arm64`
- Buildifier: `buildifier-linux-amd64` and `buildifier-linux-arm64`

### **Docker Multi-Platform Best Practices**
This implementation follows Docker's recommended patterns:
- Use ARG TARGETPLATFORM for platform detection
- Parse platform string to extract architecture
- Conditional logic based on detected architecture
- Maintain same functionality across all platforms

### **Future Considerations**
This pattern can be extended to other architecture-dependent tools as the development environment evolves. The architecture detection logic is reusable and can be abstracted into helper functions if needed.
