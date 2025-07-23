---
title: "Analysis: Python and Bazel Build System Standards - Definitive Guide"
version: 1.0
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-22T18:48:00-07:00"
parent_charter: "os/domains/charters/data/service-architecture.charter.md"
related_signals: ["SIG-2025-07-14-001-system-complexity-automation-need.signal.md"]
related_decisions: ["DEC-2025-07-15-001-core-adapter-architecture.decision.md"]
related_projects: ["rules-service-v0", "repo-guardian-workflow.vision.md"]
tags: ["analysis", "python", "bazel", "build-system", "standards", "development-workflow"]
---

# **Analysis: Python and Bazel Build System Standards - Definitive Guide**

**Status**: Active
**Version**: 1.0
**Owner**: OS Core Team
**Last Updated**: 2025-07-22T18:48:00-07:00

---

## **Executive Summary**

This document establishes the definitive standards for Python development and Bazel build system usage in the Company OS. It addresses recurring issues with Python environments, dependency management, and build system integration by providing clear decision trees, standard workflows, and troubleshooting guides.

### **Key Findings**
- **Dual-Path Approach**: Both Bazel (production) and venv (development) approaches are valid for different use cases
- **UV Package Manager**: Modern dependency management with lockfiles prevents version conflicts
- **Bazel 8 + bzlmod**: Modern configuration provides hermetic, reproducible builds
- **Clear Standards Needed**: Recurring issues stem from unclear guidance on when to use which approach

### **Recommendations**
- **Immediate**: Adopt standardized workflows for all Python development
- **Short-term**: Create decision trees for environment and build tool selection
- **Long-term**: Establish automated tooling to prevent common configuration errors

---

## **Context**

### **Background**
The Company OS has experienced recurring Python and Bazel issues including dependency conflicts, import path problems, build failures, and environment setup confusion. These issues slow development and create frustration for both human and AI developers.

### **Scope**
This analysis covers the complete Python development lifecycle in the Company OS:
- Environment setup (venv vs Bazel)
- Dependency management (UV, requirements files, Bazel integration)
- Build system configuration (MODULE.bazel, BUILD files)
- Development workflows (testing, building, running)
- Common issues and prevention strategies

### **Methodology**
Based on analysis of:
- Historical build system issues and resolutions
- Current working configurations (Rules Service, Repo Guardian)
- Industry best practices for monorepo Python development
- Bazel 8 modern patterns and bzlmod migration

---

## **Analysis**

### **Current State Assessment**

#### **Strengths**
1. **Working Bazel Configuration**: Successfully migrated to Bazel 8 + bzlmod
2. **UV Integration**: Modern dependency management with lockfiles
3. **Successful Services**: Rules Service v0 and Repo Guardian demonstrate working patterns
4. **Hermetic Builds**: Bazel provides reproducible, isolated builds

#### **Weaknesses**
1. **Unclear Guidance**: No clear decision tree for when to use venv vs Bazel
2. **Recurring Issues**: Same problems (import paths, dependencies) appear repeatedly
3. **Tool Confusion**: Developers unsure when to use which tools
4. **Documentation Gaps**: Missing comprehensive setup and troubleshooting guides

#### **Opportunities**
1. **Standardization**: Establish clear patterns for all Python development
2. **Automation**: Create tools to prevent common configuration errors
3. **Knowledge Transfer**: Document all solutions for common issues
4. **Developer Experience**: Streamline workflows for faster development

#### **Threats/Risks**
1. **Technical Debt**: Inconsistent patterns create maintenance burden
2. **Development Friction**: Unclear standards slow feature development
3. **Onboarding Difficulty**: New developers struggle with setup complexity
4. **AI Agent Confusion**: Inconsistent patterns confuse AI development partners

---

## **Detailed Analysis**

### **1. Python Environment Management**

#### **The Dual-Path Approach**

We support **two valid approaches** based on use case:

| Approach | When to Use | Advantages | Disadvantages |
|----------|-------------|------------|---------------|
| **Bazel Hermetic** | Production builds, CI/CD, reproducible environments | Fully reproducible, no environment pollution, scales to large teams | Slower iteration, more complex setup |
| **venv Development** | Rapid development, debugging, IDE integration | Fast iteration, familiar tools, IDE support | Environment drift, not reproducible |

#### **Decision Tree: Environment Selection**

```
Are you...
├─ Building for production/CI? → Use Bazel
├─ Running tests in CI? → Use Bazel
├─ Need reproducible builds? → Use Bazel
├─ Debugging or rapid iteration? → Use venv
├─ IDE development with breakpoints? → Use venv
└─ Unsure? → Start with venv, migrate to Bazel for CI
```

#### **Environment Setup Standards**

**For venv Development:**
```bash
# 1. Create and activate venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 2. Install from lockfile (NEVER from requirements.in directly)
pip install -r requirements_lock.txt

# 3. Verify installation
python -c "import company_os; print('✅ Package imports work')"
```

**For Bazel Hermetic:**
```bash
# 1. Verify Bazel version
bazel version  # Must be 8.x+

# 2. Build and test
bazel build //your/target/...
bazel test //your/target/tests:all_tests

# 3. Run applications
bazel run //your/target:app
```

### **2. Dependency Management with UV**

#### **The UV Workflow**

```
requirements.in → (UV compile) → requirements_lock.txt → (Bazel) → hermetic build
             ↘                                      ↗
               (pip install) → venv development
```

#### **Standard Dependency Workflow**

**Adding New Dependencies:**
```bash
# 1. Add to requirements.in (high-level constraints)
echo "fastapi==0.104.1" >> requirements.in

# 2. Regenerate lockfile with UV
uv pip compile requirements.in --generate-hashes -o requirements_lock.txt

# 3. Update BUILD.bazel files
# Add "@pypi//fastapi" to deps list

# 4. Clear Bazel cache and test
bazel clean --expunge
bazel test //your/target/tests:all_tests

# 5. Commit both files together
git add requirements.in requirements_lock.txt
git commit -m "Add fastapi dependency"
```

**Updating Dependencies:**
```bash
# 1. Update version in requirements.in
sed -i 's/fastapi==0.104.1/fastapi==0.105.0/' requirements.in

# 2. Regenerate lockfile
uv pip compile requirements.in --generate-hashes -o requirements_lock.txt

# 3. Test and commit
bazel test //your/target/tests:all_tests
git add requirements.in requirements_lock.txt
git commit -m "Update fastapi to 0.105.0"
```

#### **Dependency Management Rules**

1. **Single Source of Truth**: Only modify `requirements.in`
2. **Never Manual Edit**: Never manually edit `requirements_lock.txt`
3. **Always Regenerate**: Use UV to regenerate lockfile after any change
4. **Test After Changes**: Run full test suite after dependency updates
5. **Commit Together**: Always commit both files in the same commit

### **3. Bazel Build System Configuration**

#### **Modern Bazel 8 + bzlmod Setup**

**MODULE.bazel (Project Root):**
```starlark
module(
    name = "the_company_os",
    version = "0.1.0",
)

# Python rules - use latest stable versions
bazel_dep(name = "rules_python", version = "1.5.1")
bazel_dep(name = "aspect_rules_py", version = "1.6.0")

# Python toolchain
python = use_extension("@rules_python//python/extensions:python.bzl", "python")
python.toolchain(
    python_version = "3.12",
)

# Pip dependencies - single source of truth
pip = use_extension("@rules_python//python/extensions:pip.bzl", "pip")
pip.parse(
    hub_name = "pypi",
    python_version = "3.12",
    requirements_lock = "//:requirements_lock.txt",  # Points to lockfile
)
use_repo(pip, "pypi")
```

**Standard .bazelrc Configuration:**
```
# Disable legacy WORKSPACE
common --noenable_workspace

# Build settings
build --verbose_failures
build --sandbox_default_allow_network=false

# Test settings
test --test_output=errors
test --test_summary=short

# Python specific - CRITICAL: No PYTHONPATH manipulation!
test --action_env=PYTEST_CURRENT_TEST

# Development helpers
build --show_progress_rate_limit=5
build --curses=yes
build --color=yes
```

#### **Standard BUILD.bazel Patterns**

**Library Pattern:**
```starlark
load("@aspect_rules_py//py:defs.bzl", "py_library")

py_library(
    name = "service_lib",
    srcs = glob(["*.py"]),
    imports = ["../../../.."],  # CRITICAL: Enables absolute imports
    visibility = ["//visibility:public"],
    deps = [
        "//shared/libraries/company_os_core",
        "@pypi//pydantic",
        "@pypi//httpx",
        # Always use @pypi// prefix for external deps
    ],
)
```

**Binary Pattern:**
```starlark
load("@aspect_rules_py//py:defs.bzl", "py_binary")

py_binary(
    name = "service",
    srcs = ["__main__.py"],
    main = "__main__.py",
    imports = ["../../../.."],
    deps = [
        ":service_lib",
        "@pypi//typer",
    ],
)
```

**Test Pattern:**
```starlark
load("@aspect_rules_py//py:defs.bzl", "py_test")

[
    py_test(
        name = test_file[:-3],  # Remove .py extension
        srcs = [test_file],
        imports = ["../../../.."],
        deps = [
            ":service_lib",
            "@pypi//pytest",
        ],
    )
    for test_file in glob(["test_*.py"])
]

# Group tests for easy execution
test_suite(
    name = "all_tests",
    tests = [test_file[:-3] for test_file in glob(["test_*.py"])],
)
```

### **4. Standard Development Workflows**

#### **Creating a New Service**

**Step 1: Directory Structure**
```bash
mkdir -p company_os/domains/new_service/{src,tests,adapters}
touch company_os/domains/new_service/{__init__.py,BUILD.bazel}
touch company_os/domains/new_service/src/{__init__.py,BUILD.bazel}
touch company_os/domains/new_service/tests/BUILD.bazel
```

**Step 2: Root BUILD.bazel**
```starlark
load("@aspect_rules_py//py:defs.bzl", "py_library")

py_library(
    name = "new_service",
    visibility = ["//visibility:public"],
    deps = [
        "//company_os/domains/new_service/src:new_service_lib",
    ],
)
```

**Step 3: Source BUILD.bazel**
```starlark
load("@aspect_rules_py//py:defs.bzl", "py_library")

py_library(
    name = "new_service_lib",
    srcs = glob(["*.py"]),
    imports = ["../../../.."],
    visibility = ["//visibility:public"],
    deps = [
        "//shared/libraries/company_os_core",
        # Add dependencies as needed
    ],
)
```

**Step 4: Test and Validate**
```bash
# Test the build
bazel build //company_os/domains/new_service/...

# Create a simple test
echo 'def test_import():
    import company_os.domains.new_service
    assert True' > company_os/domains/new_service/tests/test_basic.py

# Test the test
bazel test //company_os/domains/new_service/tests:test_basic
```

#### **Adding Dependencies to Existing Service**

**Step 1: Update requirements.in**
```bash
echo "new-package==1.0.0" >> requirements.in
```

**Step 2: Regenerate lockfile**
```bash
uv pip compile requirements.in --generate-hashes -o requirements_lock.txt
```

**Step 3: Update BUILD.bazel**
```starlark
deps = [
    "@pypi//new_package",  # Add this line
    # ... existing deps
]
```

**Step 4: Test and commit**
```bash
bazel clean --expunge  # Clear cache
bazel build //your/service/...
bazel test //your/service/tests:all_tests
git add requirements.in requirements_lock.txt your/service/BUILD.bazel
git commit -m "Add new-package dependency to service"
```

#### **Development Iteration Workflows**

**Fast Development (venv):**
```bash
# 1. Setup once
source venv/bin/activate
pip install -r requirements_lock.txt

# 2. Develop and test rapidly
python -m pytest your/service/tests/ -v
python your/service/main.py

# 3. Before committing, validate with Bazel
bazel test //your/service/tests:all_tests
```

**Production Validation (Bazel):**
```bash
# Always run before committing
bazel build //your/service/...
bazel test //your/service/tests:all_tests

# For deployment
bazel run //your/service:main
```

### **5. Import Path Management**

#### **The Import Path Problem**

Python imports in monorepos are complex. Our solution:

**Standard Pattern:**
```python
# ALWAYS use absolute imports from package root
from company_os.domains.rules_service.src import models
from company_os.services.repo_guardian.workflows import guardian

# NEVER use relative imports in library code
# from ..models import SomeModel  # ❌ Causes Bazel issues

# NEVER use sys.path manipulation
# sys.path.append("../../../")  # ❌ Breaks hermetic builds
```

**BUILD.bazel Configuration:**
```starlark
py_library(
    name = "lib",
    srcs = glob(["*.py"]),
    imports = ["../../../.."],  # This enables the absolute imports
    # ...
)
```

#### **Import Debugging Checklist**

When you get import errors:

1. **Check BUILD.bazel**: Does it have `imports = ["../../../.."]`?
2. **Check Import Style**: Are you using absolute imports?
3. **Check __init__.py**: Do all parent directories have `__init__.py`?
4. **Check Dependencies**: Is the imported module in `deps`?
5. **Clear Cache**: Run `bazel clean --expunge`

### **6. Common Issues and Solutions**

#### **Issue 1: "Module not found" in Bazel**

**Symptoms:**
```
ModuleNotFoundError: No module named 'company_os'
```

**Solutions:**
```starlark
# In BUILD.bazel, add imports parameter
py_library(
    name = "lib",
    imports = ["../../../.."],  # This line is critical
    # ...
)
```

#### **Issue 2: Dependency version conflicts**

**Symptoms:**
```
ERROR: Could not find a version that satisfies the requirement
```

**Solutions:**
```bash
# 1. Check for conflicting versions in requirements.in
grep -n "package-name" requirements.in

# 2. Regenerate lockfile
uv pip compile requirements.in --generate-hashes -o requirements_lock.txt

# 3. Clear Bazel cache
bazel clean --expunge
```

#### **Issue 3: Bazel build cache issues**

**Symptoms:**
```
ERROR: Analysis of target failed; build aborted
```

**Solutions:**
```bash
# Nuclear option - clear everything
bazel clean --expunge

# Rebuild from scratch
bazel build //your/target/...
```

#### **Issue 4: venv/Bazel environment conflicts**

**Symptoms:**
- Tests pass in venv but fail in Bazel
- Different behavior between environments

**Solutions:**
```bash
# 1. Ensure lockfile is up to date
uv pip compile requirements.in --generate-hashes -o requirements_lock.txt

# 2. Reinstall venv from lockfile
pip install -r requirements_lock.txt --force-reinstall

# 3. Test both environments
python -m pytest tests/
bazel test //tests:all_tests
```

#### **Issue 5: Pydantic + Temporal integration**

**Symptoms:**
```
Failed validating workflow
Unable to generate pydantic-core schema for <class 'datetime.datetime'>
```

**Solutions:**
```python
# Add to Pydantic models used in workflows
from pydantic import BaseModel, ConfigDict

class WorkflowModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    # ... rest of model
```

---

## **Decision Trees and Quick Reference**

### **"Which tool should I use?" Decision Tree**

```
What are you doing?
├─ Quick testing/debugging? → venv + pytest
├─ Building for production? → Bazel
├─ CI/CD pipeline? → Bazel
├─ Adding new dependencies? → UV + both environments
├─ IDE development? → venv (with Bazel validation before commit)
├─ Creating new service? → Follow standard service template
└─ Unsure? → Ask in #engineering-help
```

### **"Something's broken" Troubleshooting Tree**

```
What's the error?
├─ Import errors?
│   ├─ Check BUILD.bazel imports parameter
│   ├─ Use absolute imports
│   └─ Verify __init__.py files exist
├─ Dependency errors?
│   ├─ Regenerate requirements_lock.txt
│   ├─ Clear Bazel cache
│   └─ Check for version conflicts
├─ Build errors?
│   ├─ bazel clean --expunge
│   ├─ Check BUILD.bazel syntax
│   └─ Verify dependencies in deps list
└─ Environment differences?
    ├─ Ensure venv uses requirements_lock.txt
    ├─ Test both venv and Bazel
    └─ Check for side effects in imports
```

### **Quick Command Reference**

**Environment Setup:**
```bash
# venv setup
python -m venv venv && source venv/bin/activate
pip install -r requirements_lock.txt

# Verify Bazel setup
bazel version && bazel build //shared/libraries/company_os_core
```

**Dependency Management:**
```bash
# Add dependency
echo "package==1.0.0" >> requirements.in
uv pip compile requirements.in --generate-hashes -o requirements_lock.txt

# Update dependency
sed -i 's/package==1.0.0/package==1.1.0/' requirements.in
uv pip compile requirements.in --generate-hashes -o requirements_lock.txt
```

**Build and Test:**
```bash
# Build service
bazel build //company_os/domains/service/...

# Test service
bazel test //company_os/domains/service/tests:all_tests

# Run service
bazel run //company_os/domains/service:main
```

**Troubleshooting:**
```bash
# Clear cache
bazel clean --expunge

# Reinstall venv
pip install -r requirements_lock.txt --force-reinstall

# Debug imports
python -c "import company_os; print('✅ Imports work')"
```

---

## **Prevention Strategies**

### **1. Automated Validation**

**Pre-commit Hooks:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: bazel-build-test
        name: Bazel Build Test
        entry: bazel build //...
        language: system
        pass_filenames: false

      - id: requirements-lock-check
        name: Requirements Lock Check
        entry: bash -c 'uv pip compile requirements.in --generate-hashes --dry-run'
        language: system
        files: requirements.in
```

**CI/CD Validation:**
```yaml
# github-actions.yml
- name: Validate Build System
  run: |
    bazel build //...
    bazel test //...

- name: Validate venv compatibility
  run: |
    python -m venv test-venv
    source test-venv/bin/activate
    pip install -r requirements_lock.txt
    python -m pytest tests/ --tb=short
```

### **2. Standard Templates**

**Service Template Generator:**
```bash
# scripts/create-service.sh
#!/bin/bash
SERVICE_NAME=$1
SERVICE_PATH="company_os/domains/$SERVICE_NAME"

mkdir -p $SERVICE_PATH/{src,tests,adapters}
# ... generate standard BUILD.bazel files
# ... generate standard __init__.py files
# ... generate standard test templates
```

### **3. Documentation Standards**

**Every Service Must Have:**
1. **README.md** with build and test instructions
2. **BUILD.bazel** files following standard patterns
3. **Test suite** with both venv and Bazel validation
4. **Dependency documentation** explaining why each dependency is needed

### **4. Regular Maintenance**

**Monthly Tasks:**
- Review and update dependencies
- Clean up unused dependencies
- Validate all services build and test successfully
- Update this standards document based on new learnings

---

## **Conclusions**

### **Summary of Standards**

1. **Dual-Path Approach**: Support both venv (development) and Bazel (production) workflows
2. **UV Dependency Management**: Single source of truth with lockfiles
3. **Bazel 8 + bzlmod**: Modern, hermetic build system
4. **Standard Patterns**: Consistent BUILD.bazel and import patterns across all services
5. **Clear Decision Trees**: Guidance for when to use which tools

### **Implications**

- **Faster Development**: Clear standards reduce setup time and confusion
- **Fewer Issues**: Prevention strategies eliminate common problems
- **Better Onboarding**: New developers (human and AI) can follow clear patterns
- **Maintainable Codebase**: Consistent patterns reduce maintenance burden

### **Success Metrics**

- **Reduction in Build Issues**: Track build failures and dependency conflicts
- **Faster Onboarding**: Measure time from zero to first contribution
- **Developer Satisfaction**: Survey feedback on development experience
- **AI Agent Effectiveness**: Track successful task completion rates

---

## **Recommendations**

### **Immediate Actions**

1. **Adopt These Standards**: Begin using standardized workflows for all development
   - **Owner**: All developers
   - **Timeline**: Immediately
   - **Resources**: Reference this document

2. **Create Service Templates**: Build automated service generation tools
   - **Owner**: Infrastructure Team
   - **Timeline**: This sprint
   - **Resources**: 1 day development

### **Medium-term Actions**

1. **Implement Automated Validation**: Add pre-commit hooks and CI checks
   - **Owner**: Infrastructure Team
   - **Timeline**: Next sprint
   - **Dependencies**: Template creation

2. **Training and Documentation**: Create video guides and examples
   - **Owner**: OS Core Team
   - **Timeline**: Next month
   - **Dependencies**: Standards adoption

### **Long-term Actions**

1. **IDE Integration**: Create plugins/extensions for popular IDEs
   - **Owner**: Tools Team
   - **Timeline**: Next quarter
   - **Strategic Impact**: Improved developer experience

2. **Advanced Tooling**: Build custom tools for dependency management and conflict resolution
   - **Owner**: Infrastructure Team
   - **Timeline**: Next quarter
   - **Strategic Impact**: Elimination of manual dependency management

---

## **Implementation Considerations**

### **Resource Requirements**

- **Human Resources**: 0.5 FTE for template creation, 0.25 FTE for maintenance
- **Financial Resources**: No additional tooling costs (UV and Bazel are free)
- **Technical Resources**: CI/CD pipeline updates, pre-commit hook setup

### **Change Management**

- **Stakeholder Impact**: All developers must adopt new standards
- **Communication Strategy**: Share examples and success stories
- **Training Needs**: Hands-on workshops for complex scenarios

### **Success Metrics**

- **Quantitative**: Build failure rate, dependency conflict frequency, setup time
- **Qualitative**: Developer satisfaction scores, ease of onboarding feedback
- **Timeline**: Measure improvements over 6 months

---

## **Next Steps**

### **Week 1: Immediate Implementation**
1. Begin using standardized BUILD.bazel patterns for all new development
2. Adopt UV workflow for all dependency changes
3. Use decision trees for tool selection

### **Week 2-4: Tooling and Automation**
1. Create service templates and generation scripts
2. Implement pre-commit hooks for validation
3. Update CI/CD pipelines with build validation

### **Month 2-3: Training and Refinement**
1. Conduct training sessions on new standards
2. Gather feedback and refine processes
3. Create advanced tooling for complex scenarios

### **Ongoing: Maintenance and Evolution**
- Monthly dependency reviews and updates
- Quarterly standards review and updates
- Continuous improvement based on developer feedback

---

## **Appendices**

### **Appendix A: Complete Working Examples**

**Minimal Service Example:**
```
company_os/domains/example_service/
├── __init__.py
├── BUILD.bazel                 # Root library aggregator
├── src/
│   ├── __init__.py
│   ├── BUILD.bazel             # Main library with proper imports
│   ├── models.py               # Pydantic models
│   └── service.py              # Core logic
└── tests/
    ├── BUILD.bazel             # Test configuration
    ├── test_models.py          # Model tests
    └── test_service.py         # Service tests
```

### **Appendix B: Troubleshooting Flowcharts**

[Detailed flowcharts for common issue resolution - would be included as diagrams in a real document]

### **Appendix C: Tool Version Matrix**

| Tool | Version | Reason |
|------|---------|--------|
| Python | 3.12+ | Latest stable with good performance |
| Bazel | 8.x | Modern bzlmod support |
| rules_python | 1.5.1+ | Bazel 8 compatibility |
| aspect_rules_py | 1.6.0+ | Better Python support |
| UV | Latest | Fastest dependency resolution |

---

## **References**

- [Bazel Python Rules Documentation](https://github.com/bazelbuild/rules_python)
- [UV Package Manager](https://github.com/astral-sh/uv)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)
- [Company OS Service Architecture Charter](os/domains/charters/data/service-architecture.charter.md)
- [Existing Bazel Setup Analysis](work/domains/analysis/data/bazel_setup.analysis.md)

---

**This document serves as the single source of truth for Python development and Bazel build system usage in the Company OS. All developers should bookmark and refer to this guide for consistent, reliable development practices.**
