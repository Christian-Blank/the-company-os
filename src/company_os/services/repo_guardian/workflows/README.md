---
title: "Repo Guardian Workflows"
parent: "../README.md"
tags: ["workflows", "temporal", "repo-guardian"]
---

# Repo Guardian Workflows

This directory contains Temporal workflow definitions for the Repo Guardian service.

## Overview

Workflows orchestrate the execution of activities to accomplish complex, long-running tasks. They are deterministic, fault-tolerant, and replayable.

## Workflow Structure

### guardian.py
The main workflow that coordinates repository analysis:
- `RepoGuardianWorkflow`: Main workflow class
  - Clones repository
  - Analyzes code changes
  - Generates structured issues
  - Emits metrics
  - Creates GitHub issues (when enabled)

## Workflow Patterns

### Error Handling
- Activities have automatic retry policies
- Workflows handle activity failures gracefully
- Compensation logic for cleanup operations

### State Management
- Workflow state is automatically persisted by Temporal
- Can query workflow state at any time
- Support for long-running operations (days/weeks)

## Development Guidelines

1. **Deterministic Code**: Workflows must be deterministic
   - No random numbers
   - No system time (use workflow time)
   - No direct I/O operations

2. **Activity Isolation**: All external operations in activities
   - File I/O
   - Network calls
   - Database operations

3. **Versioning**: Use Temporal's versioning for updates
   - Maintain backward compatibility
   - Use workflow.get_version() for changes

## Testing

Workflows can be tested using:
- Unit tests with mocked activities
- Workflow replay tests
- Integration tests with real Temporal

See `/tests/workflows/` for examples.

---

*Part of the Repo Guardian service following Temporal best practices.*
