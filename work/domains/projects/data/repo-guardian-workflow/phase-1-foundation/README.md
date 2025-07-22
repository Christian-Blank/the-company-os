---
title: "Phase 1: Foundation & Setup"
phase_number: 1
status: "Not Started"
duration: "1 week"
parent_project: "../../repo-guardian-workflow.vision.md"
last_updated: "2025-07-22T13:45:00-07:00"
tags: ["phase", "foundation", "setup", "charter", "dependencies"]
---

# Phase 1: Foundation & Setup

Establish the charter, dependencies, and basic project structure for the Repo Guardian workflow.

## Phase Overview

**Duration:** 1 week
**Start Date:** TBD
**End Date:** TBD
**Status:** Not Started
**Owner:** @christian

## Objectives

1. Create the Repo Guardian charter document
2. Set up project dependencies (Temporal, OpenAI, Anthropic)
3. Establish the service directory structure
4. Configure development environment

## Task Checklist

### Charter Creation
- [ ] **Draft Repo Guardian Charter**
  - [ ] Define vision and purpose aligned with Company OS Charter
  - [ ] Establish principles for AI-human workflow orchestration
  - [ ] Define service boundaries and responsibilities
  - [ ] Set governance model for workflow evolution
  - [ ] Create success metrics and quality standards
  - [ ] File location: `company_os/domains/charters/data/repo-guardian.charter.md`

### Dependencies Setup
- [ ] **Update Python Dependencies**
  - [ ] Add to `requirements.in`:
    - [ ] `temporalio` - Temporal Python SDK
    - [ ] `openai` - OpenAI API client
    - [ ] `anthropic` - Claude API client
    - [ ] `prometheus-client` - Metrics emission
    - [ ] `structlog` - Structured logging
  - [ ] Run `pip-compile requirements.in -o requirements_lock.txt`
  - [ ] Test dependency installation

- [ ] **Update Bazel Configuration**
  - [ ] Update `MODULE.bazel` if needed
  - [ ] Ensure pip dependencies are accessible to Bazel
  - [ ] Test Bazel build with new dependencies

### Project Structure
- [ ] **Create Service Directory Structure**
  ```
  src/company_os/services/repo_guardian/
  ├── __init__.py
  ├── BUILD.bazel
  ├── workflows/
  │   ├── __init__.py
  │   └── guardian.py
  ├── activities/
  │   ├── __init__.py
  │   ├── repository.py
  │   ├── analysis.py
  │   └── llm.py
  ├── adapters/
  │   ├── __init__.py
  │   ├── github.py
  │   ├── openai.py
  │   └── claude.py
  ├── models/
  │   ├── __init__.py
  │   └── domain.py
  └── worker_main.py
  ```

- [ ] **Create Initial BUILD.bazel Files**
  - [ ] Main service BUILD file
  - [ ] Define py_library for service
  - [ ] Define py_binary for worker
  - [ ] Set up proper dependencies

### Environment Configuration
- [ ] **Local Development Setup**
  - [ ] Create `.env.example` with required variables:
    - [ ] `TEMPORAL_ADDRESS`
    - [ ] `OPENAI_API_KEY`
    - [ ] `ANTHROPIC_API_KEY`
    - [ ] `GITHUB_TOKEN`
  - [ ] Document environment setup in README

- [ ] **Temporal Development Environment**
  - [x] Install Temporal CLI (`brew install temporal`)
  - [ ] Create docker-compose.yml for local Temporal
  - [ ] Test `temporal server start-dev`
  - [ ] Verify Temporal UI access at http://localhost:8233

### Documentation
- [ ] **Create Service Documentation**
  - [ ] Service README in `src/company_os/services/repo_guardian/README.md`
  - [ ] Architecture overview
  - [ ] Development setup guide
  - [ ] Configuration reference

- [ ] **Update Project Documentation**
  - [ ] Add service to registry: `company_os/domains/registry/data/services.registry.md`
  - [ ] Create initial evolution log
  - [ ] Document design decisions

## Deliverables

1. **Repo Guardian Charter** - Complete governance document
2. **Updated Dependencies** - All required packages available
3. **Service Structure** - All directories and files created
4. **Development Environment** - Local Temporal running
5. **Documentation** - Service documented and registered

## Success Criteria

- [ ] Charter reviewed and approved by team
- [ ] All dependencies install without conflicts
- [ ] Bazel builds successfully with new dependencies
- [ ] Temporal server runs locally
- [ ] Basic project structure passes validation

## Next Phase

Upon completion, proceed to [Phase 2: Core Workflow Development](../phase-2-core-workflow/README.md)

---

*Foundation phase follows Company OS principle: "Process-First, Tools-Second" - Define clear governance before building.*
