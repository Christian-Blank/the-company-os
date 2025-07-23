---
title: "Phase 2: Core Workflow Development"
phase_number: 2
status: "Not Started"
duration: "2 weeks"
parent_project: "../../repo-guardian-workflow.vision.md"
last_updated: "2025-07-22T13:47:00-07:00"
tags: ["phase", "workflow", "temporal", "development"]
---

# Phase 2: Core Workflow Development

Build the Temporal workflow and core activities with proper error handling and state management.

## Phase Overview

**Duration:** 2 weeks
**Start Date:** TBD
**End Date:** TBD
**Status:** Not Started
**Owner:** @christian
**Prerequisites:** Phase 1 completed

## Objectives

1. Implement the main Guardian workflow in Temporal
2. Create core activity functions for repository operations
3. Set up proper error handling and retry policies
4. Implement workflow state management

## Task Checklist

### Workflow Implementation
- [ ] **Guardian Workflow (`workflows/guardian.py`)**
  - [ ] Define workflow interface and parameters
  - [ ] Implement main workflow logic:
    - [ ] Clone/update repository
    - [ ] Analyze repository changes
    - [ ] Generate issues if needed
    - [ ] Emit metrics
  - [ ] Add proper error handling
  - [ ] Configure retry policies
  - [ ] Implement workflow versioning

### Core Activities
- [ ] **Repository Activities (`activities/repository.py`)**
  - [ ] `clone_repository` - Clone repo to sandboxed location
  - [ ] `get_repository_diff` - Get changes since last run
  - [ ] `cleanup_repository` - Clean up cloned repo
  - [ ] Add activity timeouts and retries
  - [ ] Implement sandboxing for security

- [ ] **Analysis Activities (`activities/analysis.py`)**
  - [ ] `analyze_code_structure` - Check complexity metrics
  - [ ] `validate_patterns` - Verify architectural patterns
  - [ ] `check_documentation` - Validate docs quality
  - [ ] Return structured analysis results
  - [ ] Handle large file analysis efficiently

- [ ] **LLM Activities (`activities/llm.py`)**
  - [ ] `analyze_with_llm` - Generic LLM analysis
  - [ ] `generate_issue_content` - Create issue descriptions
  - [ ] `summarize_findings` - Summarize analysis results
  - [ ] Implement token counting and limits
  - [ ] Add fallback for API failures

### Domain Models
- [ ] **Data Models (`models/domain.py`)**
  - [ ] `RepositoryAnalysis` - Analysis results
  - [ ] `Issue` - GitHub issue representation
  - [ ] `WorkflowConfig` - Configuration model
  - [ ] `AnalysisMetrics` - Metrics data
  - [ ] Use Pydantic for validation

### Worker Implementation
- [ ] **Temporal Worker (`worker_main.py`)**
  - [ ] Set up worker configuration
  - [ ] Register workflows and activities
  - [ ] Configure task queues
  - [ ] Add graceful shutdown handling
  - [ ] Implement health checks

### Error Handling & Reliability
- [ ] **Retry Policies**
  - [ ] Define activity retry policies
  - [ ] Configure workflow retry behavior
  - [ ] Set appropriate timeouts
  - [ ] Handle non-retryable errors

- [ ] **State Management**
  - [ ] Track last analyzed commit
  - [ ] Store analysis history
  - [ ] Handle workflow restarts
  - [ ] Implement idempotency

### Testing
- [ ] **Unit Tests**
  - [ ] Test individual activities
  - [ ] Test workflow logic
  - [ ] Mock external dependencies
  - [ ] Test error scenarios

- [ ] **Integration Tests**
  - [ ] Test workflow with real Temporal
  - [ ] Test activity orchestration
  - [ ] Verify retry behavior
  - [ ] Test state persistence

## Deliverables

1. **Working Temporal Workflow** - Guardian workflow runs end-to-end
2. **Core Activities** - All activities implemented and tested
3. **Domain Models** - Data structures defined and validated
4. **Worker Process** - Temporal worker runs reliably
5. **Test Suite** - Unit and integration tests passing

## Success Criteria

- [ ] Workflow successfully analyzes a test repository
- [ ] All activities have proper error handling
- [ ] Retry policies work as expected
- [ ] Worker handles graceful shutdown
- [ ] 80%+ test coverage achieved

## Technical Decisions

### Workflow Design
- Single workflow handles complete analysis cycle
- Activities are atomic and idempotent
- State stored in workflow execution history

### Activity Boundaries
- Each activity does one thing well
- External calls isolated in activities
- Pure business logic in workflow

### Error Strategy
- Transient errors: Retry with exponential backoff
- API limits: Pause and retry later
- Fatal errors: Fail workflow with clear message

## Next Phase

Upon completion, proceed to [Phase 3: AI Integration](../phase-3-ai-integration/README.md)

---

*Core workflow development follows hexagonal architecture: domain logic separate from external integrations.*
