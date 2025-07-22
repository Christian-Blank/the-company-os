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
- [x] **Draft Repo Guardian Charter** ✅
  - [x] Define vision and purpose aligned with Company OS Charter
  - [x] Establish principles for AI-human workflow orchestration
  - [x] Define service boundaries and responsibilities
  - [x] Set governance model for workflow evolution
  - [x] Create success metrics and quality standards
  - [x] File location: `company_os/domains/charters/data/repo-guardian.charter.md`

### Dependencies Setup
- [x] **Update Python Dependencies** ✅
  - [x] Add to `requirements.in`:
    - [x] `temporalio` - Temporal Python SDK
    - [x] `openai` - OpenAI API client
    - [x] `anthropic` - Claude API client
    - [x] `prometheus-client` - Metrics emission
    - [x] `structlog` - Structured logging
    - [x] `PyGithub` - GitHub API client (added)
  - [x] Run `pip-compile requirements.in -o requirements_lock.txt`
  - [x] Test dependency installation

- [x] **Update Bazel Configuration** ✅
  - [x] Update `MODULE.bazel` if needed (already configured)
  - [x] Ensure pip dependencies are accessible to Bazel
  - [x] Test Bazel build with new dependencies

### Project Structure
- [x] **Create Service Directory Structure** ✅
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

- [x] **Create Initial BUILD.bazel Files** ✅
  - [x] Main service BUILD file
  - [x] Define py_library for service
  - [x] Define py_binary for worker
  - [x] Set up proper dependencies

### Environment Configuration
- [x] **Local Development Setup** ✅
  - [x] Create `.env.example` with required variables:
    - [x] `TEMPORAL_ADDRESS`
    - [x] `OPENAI_API_KEY`
    - [x] `ANTHROPIC_API_KEY`
    - [x] `GITHUB_TOKEN`
  - [x] Document environment setup in README

- [x] **Temporal Development Environment** ✅
  - [x] Install Temporal CLI (`brew install temporal`)
  - [x] Create docker-compose.yml for local Temporal
  - [x] Test `docker-compose up --detach`
  - [x] Verify Temporal UI access at http://localhost:8080

### Documentation
- [x] **Create Service Documentation** ✅
  - [x] Service README in `src/company_os/services/repo_guardian/README.md`
  - [x] Architecture overview
  - [x] Development setup guide
  - [x] Configuration reference

- [ ] **Update Project Documentation**
  - [ ] Add service to registry: `company_os/domains/registry/data/services.registry.md`
  - [ ] Create initial evolution log
  - [ ] Document design decisions
  - [ ] Check that every major folder has a README.md and that it is up to date following company_os/domains/charters/data/knowledge-architecture.charter.md
  - [ ] Create ADRS, Signals, README.md files and other documents where required
  - [ ] Verify that everything is building and all documents are linting as expected
  - [ ] Commit all changes with a descriptive commit message
  - [ ] Create a pull request for the current phase with a descriptive message

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
