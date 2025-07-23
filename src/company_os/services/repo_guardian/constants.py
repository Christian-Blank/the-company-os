"""
Shared constants for Repo Guardian service.

This module contains only deterministic objects that can be safely
imported by both workflows and activities. No I/O, no logging, no side effects.
"""
from datetime import timedelta
from temporalio.common import RetryPolicy

# Retry policy for repository operations
REPOSITORY_RETRY_POLICY = RetryPolicy(
    initial_interval=timedelta(seconds=1),
    backoff_coefficient=2.0,
    maximum_interval=timedelta(seconds=60),
    maximum_attempts=5,
    non_retryable_error_types=["ApplicationError"]  # Matches temporalio.exceptions.ApplicationError.__name__
)

# Task queue configuration
TASK_QUEUE = "repo-guardian-task-queue"

# Timeout constants (no magic numbers in code!)
DEFAULT_ACTIVITY_TIMEOUT = timedelta(seconds=300)
DEFAULT_WORKFLOW_TIMEOUT = timedelta(seconds=3600)
REPOSITORY_FETCH_TIMEOUT = timedelta(seconds=30)
