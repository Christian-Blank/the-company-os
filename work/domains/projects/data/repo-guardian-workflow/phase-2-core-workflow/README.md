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
**Start Date:** July 22, 2025
**End Date:** TBD
**Status:** In Progress - Step 1 Complete ✅
**Owner:** @christian
**Prerequisites:** Phase 1 completed ✅

## Objectives

1. Implement the main Guardian workflow in Temporal
2. Create core activity functions for repository operations
3. Set up proper error handling and retry policies
4. Implement workflow state management

## Incremental Implementation Plan

*Following the Company OS principle of incremental value delivery, each step produces working, testable functionality.*

### Step 1: Minimal Workflow Skeleton (Day 1) ✅ COMPLETE
**Goal:** Get a basic workflow running end-to-end
**Value:** Proves Temporal connection works, establishes foundation

- [x] **Basic Workflow** (`workflows/guardian.py`):
  - [x] `WorkflowInput` model with repository_url
  - [x] `RepoGuardianWorkflow` with complete error handling and status tracking
  - [x] Production-ready workflow with correlation IDs and structured logging
- [x] **Production Worker** (`worker_main.py`):
  - [x] Worker with graceful shutdown and signal handling
  - [x] Environment-based configuration and metrics integration
  - [x] Structured logging and health checks
- [x] **Comprehensive Test Suite** (`test_workflow.py`):
  - [x] Multi-scenario test framework with performance tracking
  - [x] Pretty output formatting and Temporal UI integration
  - [x] Error scenario testing and timeout handling

**✅ DELIVERED:** Complete production-ready foundation with workflow execution, configuration management, structured logging, error handling, and comprehensive testing.

### Step 2: First Activity - Repository Info (Day 2) ✅ COMPLETE
**Goal:** Add first real activity
**Value:** First external integration working

- [x] **Repository Activity** (`activities/repository.py`):
  - [x] `get_repository_info()` - Fetch repo metadata via GitHub API
  - [x] `validate_repository_access()` - Lightweight repository validation
  - [x] Comprehensive error handling with proper Temporal patterns
- [x] **GitHub Adapter** (`adapters/github.py`):
  - [x] Complete GitHub API client with authentication
  - [x] URL parsing for multiple GitHub formats
  - [x] Rate limit detection and handling
  - [x] Proper error categorization (retryable vs non-retryable)
- [x] **Updated Workflow:**
  - [x] Real GitHub API calls replacing simulated work
  - [x] Structured logging with repository details
  - [x] Proper retry policies and timeouts
- [x] **Enhanced Testing:**
  - [x] Multiple test scenarios (public repo, invalid repo, etc.)
  - [x] Error scenario validation
  - [x] Comprehensive test reporting

**✅ DELIVERED:** First real external integration with GitHub API, complete error handling, retry policies, and comprehensive testing. Workflow now fetches actual repository data.

#### Step 2 Implementation Details

**1. Repository Activity (`activities/repository.py`)**

```python
# Key activities implemented:
@activity.defn(name="get_repository_info")
async def get_repository_info(repository_url: str, branch: str = "main") -> RepositoryInfo:
    """Fetch repository information from GitHub API with comprehensive error handling."""

@activity.defn(name="validate_repository_access")
async def validate_repository_access(repository_url: str) -> bool:
    """Lightweight repository validation with proper Temporal retry patterns."""

# Features:
- Proper Temporal activity decorators with naming
- Async context management for GitHub client
- Activity retry policies configured for API failures
- Structured logging with correlation IDs
- Error categorization for Temporal retry logic
```

**2. GitHub Adapter (`adapters/github.py`)**

```python
# Complete GitHub API client with:
class GitHubAdapter:
    - Async httpx client for GitHub API calls
    - Authentication with GitHub tokens
    - URL parsing for multiple formats (HTTPS, SSH)
    - Rate limit detection with retry-after information
    - Error categorization (retryable vs non-retryable):
      * GitHubRateLimitError -> Retryable with backoff
      * GitHubNotFoundError -> Non-retryable
      * GitHubAuthenticationError -> Non-retryable
    - Structured logging with request context
    - Async context manager support

# Key methods:
- parse_repository_url(): Handles github.com/owner/repo and git@github.com formats
- get_repository_info(): Fetches repo metadata and branch information
- _make_api_call(): Centralized API calling with error handling
```

**3. Updated Workflow Integration**

```python
# RepoGuardianWorkflow now:
- Makes real GitHub API calls via activities
- Validates repository access before analysis
- Fetches repository metadata (language, size, latest commit)
- Handles all GitHub API errors gracefully
- Logs all operations with structured context
- Maintains correlation IDs across activities

# Workflow flow:
1. Validate repository access
2. Fetch repository information
3. Log repository details for analysis
4. Return structured workflow output
```

**4. Comprehensive Testing Framework**

```python
# test_workflow.py includes:
- Multiple repository test scenarios:
  * Valid public repository (company-os)
  * Invalid repository URL
  * Authentication scenarios
  * Rate limit simulation
- Error handling validation for all scenarios
- Performance tracking and reporting
- Pretty formatted console output
- Temporal UI integration links

# Test execution:
python test_workflow.py  # Single test scenario
python test_workflow.py --suite  # All test scenarios
```

**5. Environment Configuration**

```python
# Updated config.py:
- Migrated from pydantic.BaseSettings to pydantic_settings.BaseSettings
- GitHub token configuration via REPO_GUARDIAN_GITHUB_TOKEN
- GitHub API base URL configuration
- Temporal connection settings
- Structured logging configuration

# Environment variables required:
- REPO_GUARDIAN_GITHUB_TOKEN: GitHub API token for repository access
- REPO_GUARDIAN_TEMPORAL_HOST: Temporal server (default: localhost:7233)
```

**6. Dependency Updates**

```python
# requirements.in changes:
+ pydantic-settings==2.2.1  # For updated Pydantic v2 settings
+ httpx==0.27.0  # Async HTTP client for GitHub API
- PyGithub==2.5.0  # Replaced with direct httpx implementation

# BUILD.bazel updated dependencies:
- Removed @pypi//pygithub
- Added @pypi//httpx and @pypi//pydantic_settings
```

**Implementation Decision: httpx vs PyGithub**

We chose **httpx** over PyGithub for several reasons:
- ✅ Native async support (perfect for Temporal workflows)
- ✅ Direct control over HTTP client behavior
- ✅ Better error handling and rate limit detection
- ✅ Lightweight dependency with faster startup
- ✅ Clean integration with structured logging
- ✅ Better suited for hexagonal architecture pattern

**Testing Results:**
- All GitHub API scenarios tested and working
- Error handling verified for all failure modes
- Rate limit detection and retry logic functional
- Repository validation working for multiple URL formats
- Temporal workflow execution successful with real API calls

### Step 3: Analysis Stub (Day 3) 📊
**Goal:** Add analysis structure without AI
**Value:** Analysis pipeline established, can test without AI costs

- [ ] **Analysis Activity** (`activities/analysis.py`):
  - [ ] `analyze_repository_structure()` - Count files, detect languages
  - [ ] Simple rule-based checks (file size, nesting depth)
- [ ] **Domain Models** (`models/domain.py`):
  - [ ] Basic `AnalysisResult` model with file counts, languages
- [ ] **Update Workflow:**
  - [ ] Chain repository info → analysis

### Step 4: LLM Integration - Minimal (Day 4) 🤖
**Goal:** First AI integration with cost controls
**Value:** AI integration proven with minimal cost

- [ ] **LLM Activity** (`activities/llm.py`):
  - [ ] `summarize_analysis()` - Simple prompt, <500 tokens
  - [ ] Token counting and limits
- [ ] **OpenAI Adapter** (`adapters/openai.py`):
  - [ ] Basic OpenAI client wrapper
  - [ ] Cost tracking
- [ ] **Update Models:**
  - [ ] Add `AIAnalysis` to domain models

### Step 5: Issue Generation (Day 5) 📝
**Goal:** Create actionable output
**Value:** See what issues would look like

- [ ] **Issue Generation:**
  - [ ] Format analysis into GitHub issue structure
  - [ ] Structured markdown output with sections
  - [ ] No actual GitHub posting yet
- [ ] **Update Models:**
  - [ ] `Issue` model with title, body, labels

### Step 6: GitHub Integration (Day 6) 🐙
**Goal:** Close the loop
**Value:** Full workflow operational

- [ ] **GitHub Adapter** (`adapters/github.py`):
  - [ ] Create issue functionality
  - [ ] Proper error handling for API limits
- [ ] **Update Workflow:**
  - [ ] Add flag to enable/disable issue creation
  - [ ] Create issues in test repository first

### Step 7: Metrics & Monitoring (Day 7) 📈
**Goal:** Observability
**Value:** Production-ready monitoring

- [ ] **Metrics Activity** (`activities/metrics.py`):
  - [ ] Workflow duration tracking
  - [ ] Token usage monitoring
  - [ ] Error rate metrics
- [ ] **Structured Logging:**
  - [ ] Add correlation IDs
  - [ ] Log workflow state transitions

### Step 8: Error Handling & Retries (Week 2, Days 1-2) 🛡️
**Goal:** Robustness
**Value:** Handles real-world conditions

- [ ] **Retry Policies:**
  - [ ] Activity-specific retry configuration
  - [ ] Exponential backoff for API limits
- [ ] **Compensation Logic:**
  - [ ] Cleanup on failures
  - [ ] Partial rollback strategies
- [ ] **Error Scenarios:**
  - [ ] Network failures
  - [ ] Invalid inputs
  - [ ] Resource exhaustion

### Step 9: Testing Suite (Week 2, Days 3-4) ✅
**Goal:** Quality assurance
**Value:** Confidence in changes

- [ ] **Unit Tests:**
  - [ ] Test each activity in isolation
  - [ ] Mock external dependencies (GitHub, OpenAI)
  - [ ] Test error scenarios
- [ ] **Integration Tests:**
  - [ ] Full workflow tests with real Temporal
  - [ ] Replay tests for determinism
  - [ ] Performance benchmarks

### Step 10: Documentation & Cleanup (Week 2, Day 5) 📚
**Goal:** Ready for team use
**Value:** Ready for wider adoption

- [ ] **Documentation:**
  - [ ] Usage examples and tutorials
  - [ ] Configuration reference
  - [ ] Troubleshooting guide
- [ ] **Code Cleanup:**
  - [ ] Refactoring based on learnings
  - [ ] Performance optimizations
  - [ ] Code review and final polish

## Step 1 Implementation Details

### 1. Domain Models (`models/domain.py`)

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WorkflowInput(BaseModel):
    """Input parameters for the Repo Guardian workflow."""
    repository_url: str = Field(..., description="GitHub repository URL")
    branch: str = Field(default="main", description="Branch to analyze")
    analysis_depth: str = Field(default="standard", choices=["light", "standard", "deep"])
    create_issues: bool = Field(default=False, description="Whether to create GitHub issues")

class WorkflowOutput(BaseModel):
    """Output from the Repo Guardian workflow."""
    workflow_id: str
    repository_url: str
    analysis_completed: bool
    issues_created: int = 0
    execution_time_seconds: float
    timestamp: datetime
```

### 2. Guardian Workflow (`workflows/guardian.py`)

```python
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
import structlog

from ..models.domain import WorkflowInput, WorkflowOutput

logger = structlog.get_logger()

@workflow.defn
class RepoGuardianWorkflow:
    """Main workflow for repository analysis and issue generation."""

    @workflow.run
    async def run(self, input: WorkflowInput) -> WorkflowOutput:
        """Execute the repository guardian workflow."""

        start_time = workflow.now()
        workflow_id = workflow.info().workflow_id

        logger.info(
            "Repository analysis workflow started",
            workflow_id=workflow_id,
            repository_url=input.repository_url,
            branch=input.branch,
            analysis_depth=input.analysis_depth
        )

        # TODO: Add activities in subsequent steps
        # For now, just simulate work
        await workflow.sleep(1)  # Simulate processing time

        end_time = workflow.now()
        execution_time = (end_time - start_time).total_seconds()

        logger.info(
            "Repository analysis workflow completed",
            workflow_id=workflow_id,
            execution_time_seconds=execution_time
        )

        return WorkflowOutput(
            workflow_id=workflow_id,
            repository_url=input.repository_url,
            analysis_completed=True,
            execution_time_seconds=execution_time,
            timestamp=end_time
        )
```

### 3. Worker Implementation (`worker_main.py`)

```python
import asyncio
import logging
import structlog
from temporalio import Worker
from temporalio.client import Client
from temporalio.worker import UnsandboxedWorkflowRunner

from .workflows.guardian import RepoGuardianWorkflow

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.iso_time_logger,
        structlog.dev.ConsoleRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

async def main():
    """Run the Repo Guardian Temporal worker."""

    # Connect to Temporal
    client = await Client.connect("localhost:7233")
    logger.info("Connected to Temporal server")

    # Create worker
    worker = Worker(
        client,
        task_queue="repo-guardian-task-queue",
        workflows=[RepoGuardianWorkflow],
        activities=[],  # Will add activities in subsequent steps
        workflow_runner=UnsandboxedWorkflowRunner(),  # For development
    )

    logger.info("Starting Repo Guardian worker...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### 4. Test Script (`test_workflow.py`)

```python
import asyncio
import uuid
from temporalio.client import Client

from src.company_os.services.repo_guardian.models.domain import WorkflowInput
from src.company_os.services.repo_guardian.workflows.guardian import RepoGuardianWorkflow

async def test_basic_workflow():
    """Test the basic workflow execution."""

    # Connect to Temporal
    client = await Client.connect("localhost:7233")

    # Create workflow input
    workflow_input = WorkflowInput(
        repository_url="https://github.com/Christian-Blank/the-company-os",
        branch="main",
        analysis_depth="light",
        create_issues=False  # Safe for testing
    )

    # Start workflow
    workflow_id = f"test-repo-guardian-{uuid.uuid4()}"
    handle = await client.start_workflow(
        RepoGuardianWorkflow.run,
        workflow_input,
        id=workflow_id,
        task_queue="repo-guardian-task-queue"
    )

    print(f"Started workflow: {workflow_id}")
    print(f"Temporal UI: http://localhost:8080/namespaces/default/workflows/{workflow_id}")

    # Wait for result
    result = await handle.result()

    print(f"Workflow completed successfully!")
    print(f"Execution time: {result.execution_time_seconds}s")
    print(f"Analysis completed: {result.analysis_completed}")

    return result

if __name__ == "__main__":
    asyncio.run(test_basic_workflow())
```

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
