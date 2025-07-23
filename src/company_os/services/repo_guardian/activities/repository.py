"""
Repository-related activities for Repo Guardian service.

This module contains Temporal activities for repository operations.
"""

from temporalio import activity
from temporalio.exceptions import ApplicationError

from ..adapters.github import (
    GitHubAdapter,
    GitHubAPIError,
    GitHubRateLimitError,
    GitHubNotFoundError,
    GitHubAuthenticationError
)
from ..models.domain import RepositoryInfo
from ..utils.logging import get_logger
from ..constants import REPOSITORY_RETRY_POLICY

logger = get_logger(__name__)


@activity.defn(name="get_repository_info")
async def get_repository_info(repository_url: str, branch: str = "main") -> RepositoryInfo:
    """Fetch repository information from GitHub API.

    This activity retrieves basic repository metadata including the latest commit SHA,
    default branch, primary language, and other repository statistics.

    Args:
        repository_url: GitHub repository URL (supports various formats)
        branch: Branch to analyze (defaults to "main")

    Returns:
        RepositoryInfo: Complete repository information

    Raises:
        ApplicationError: For non-retryable errors (invalid URL, repo not found, auth failed)
        ActivityError: For retryable errors (rate limits, server errors)
    """
    activity_logger = logger.bind(
        activity="get_repository_info",
        repository_url=repository_url,
        branch=branch
    )

    activity_logger.info("Starting repository info fetch")

    try:
        async with GitHubAdapter() as github:
            repository_info = await github.get_repository_info(repository_url, branch)

            activity_logger.info(
                "Repository info fetch completed successfully",
                full_name=repository_info.full_name,
                commit_sha=repository_info.commit_sha[:8],
                language=repository_info.language,
                size_kb=repository_info.size_kb
            )

            return repository_info

    except GitHubNotFoundError as e:
        # Non-retryable: repository or branch doesn't exist
        error_msg = f"Repository not found: {str(e)}"
        activity_logger.error("Repository not found", error=error_msg)
        raise ApplicationError(error_msg, non_retryable=True)

    except GitHubAuthenticationError as e:
        # Non-retryable: authentication/authorization failed
        error_msg = f"GitHub authentication failed: {str(e)}"
        activity_logger.error("GitHub authentication failed", error=error_msg)
        raise ApplicationError(error_msg, non_retryable=True)

    except GitHubRateLimitError as e:
        # Retryable: rate limit exceeded, let Temporal retry
        activity_logger.warning(
            "GitHub rate limit exceeded, will retry",
            error=str(e),
            retry_after=getattr(e, 'retry_after', None)
        )
        raise  # Let Temporal handle the retry

    except GitHubAPIError as e:
        # Retryable: other API errors (server errors, timeouts, etc.)
        activity_logger.warning(
            "GitHub API error, will retry",
            error=str(e)
        )
        raise  # Let Temporal handle the retry

    except Exception as e:
        # Non-retryable: unexpected errors
        error_msg = f"Unexpected error fetching repository info: {str(e)}"
        activity_logger.error("Unexpected error", error=error_msg)
        raise ApplicationError(error_msg, non_retryable=True)


@activity.defn(name="validate_repository_access")
async def validate_repository_access(repository_url: str) -> bool:
    """Validate that we can access the specified repository.

    This is a lightweight check that can be used before starting
    more expensive operations.

    Args:
        repository_url: GitHub repository URL to validate

    Returns:
        bool: True if repository is accessible, False otherwise

    Raises:
        ApplicationError: For configuration or authentication issues
    """
    activity_logger = logger.bind(
        activity="validate_repository_access",
        repository_url=repository_url
    )

    activity_logger.info("Validating repository access")

    try:
        async with GitHubAdapter() as github:
            # Parse URL to validate format
            owner, repo = github.parse_repository_url(repository_url)

            # Try to fetch minimal repository info
            await github._make_api_call(f"/repos/{owner}/{repo}")

            activity_logger.info("Repository access validation successful")
            return True

    except GitHubNotFoundError:
        activity_logger.warning("Repository not found or not accessible")
        return False

    except GitHubAuthenticationError as e:
        # Authentication issues should be raised as non-retryable
        error_msg = f"GitHub authentication failed: {str(e)}"
        activity_logger.error("Authentication error during validation", error=error_msg)
        raise ApplicationError(error_msg, non_retryable=True)

    except (GitHubRateLimitError, GitHubAPIError):
        # For validation, we'll consider rate limits as temporary failures
        activity_logger.warning("API error during validation, treating as inaccessible")
        return False

    except Exception as e:
        error_msg = f"Unexpected error validating repository access: {str(e)}"
        activity_logger.error("Unexpected validation error", error=error_msg)
        raise ApplicationError(error_msg, non_retryable=True)


# Activity configuration for the worker
REPOSITORY_ACTIVITIES = [
    get_repository_info,
    validate_repository_access,
]
