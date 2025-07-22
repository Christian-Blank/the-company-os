---
title: "Repo Guardian Activities"
parent: "../README.md"
tags: ["activities", "temporal", "repo-guardian"]
---

# Repo Guardian Activities

This directory contains Temporal activity implementations for the Repo Guardian service.

## Overview

Activities are the building blocks that perform actual work in Temporal workflows. They handle all I/O operations, external API calls, and non-deterministic operations.

## Activity Modules

### repository.py
Repository operations:
- `clone_repository`: Safely clone a git repository
- `get_repository_diff`: Generate diffs between commits
- `cleanup_repository`: Remove cloned repositories

### analysis.py
Code analysis operations:
- `analyze_code_structure`: Analyze repository structure
- `validate_against_patterns`: Check adherence to patterns
- `identify_complexity_issues`: Find complexity hotspots

### llm.py
AI integration operations:
- `generate_structured_issues`: Create actionable issues from analysis
- `summarize_changes`: Generate change summaries
- `suggest_improvements`: AI-powered improvement suggestions

## Activity Patterns

### Error Handling
```python
@activity.defn
async def my_activity(input: InputModel) -> OutputModel:
    try:
        # Activity logic
        return result
    except TemporaryError as e:
        # Let Temporal retry
        raise
    except PermanentError as e:
        # Don't retry
        raise ApplicationError("Permanent failure", non_retryable=True)
```

### Retry Policies
Activities use configured retry policies:
- Default: 3 attempts with exponential backoff
- Network operations: 5 attempts
- AI operations: 2 attempts (cost consideration)

### Timeouts
- Start-to-close: 5 minutes (default)
- Repository operations: 10 minutes
- AI operations: 2 minutes

## Development Guidelines

1. **Idempotency**: Activities should be idempotent when possible
2. **Error Types**: Use appropriate error types for retry behavior
3. **Logging**: Use structured logging for debugging
4. **Metrics**: Emit metrics for monitoring
5. **Resource Cleanup**: Always clean up resources

## Testing

Activities can be tested independently:
- Unit tests with mocked dependencies
- Integration tests with real services
- Property-based tests for edge cases

See `/tests/activities/` for examples.

---

*Part of the Repo Guardian service following Temporal activity best practices.*
