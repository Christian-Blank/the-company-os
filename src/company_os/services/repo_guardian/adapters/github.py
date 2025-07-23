"""
GitHub API adapter for Repo Guardian service.

This module provides a clean interface to GitHub API operations.
"""

import re
from datetime import datetime
from typing import Optional, Tuple
from urllib.parse import urlparse

import httpx
from temporalio.exceptions import ApplicationError

from src.company_os.services.repo_guardian.config import settings
from src.company_os.services.repo_guardian.utils.logging import get_logger
from src.company_os.services.repo_guardian.models.domain import RepositoryInfo

logger = get_logger(__name__)


class GitHubAPIError(Exception):
    """Base exception for GitHub API errors."""
    pass


class GitHubRateLimitError(GitHubAPIError):
    """Raised when GitHub API rate limit is exceeded."""
    def __init__(self, message: str, retry_after: Optional[int] = None):
        super().__init__(message)
        self.retry_after = retry_after


class GitHubNotFoundError(GitHubAPIError):
    """Raised when repository or resource is not found."""
    pass


class GitHubAuthenticationError(GitHubAPIError):
    """Raised when GitHub authentication fails."""
    pass


class GitHubAdapter:
    """GitHub API client adapter following hexagonal architecture."""

    def __init__(self, api_token: Optional[str] = None):
        """Initialize GitHub adapter with optional API token."""
        self.api_token = api_token or settings.github_token
        self.base_url = settings.github_api_base_url

        # Set up HTTP client with proper headers
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "CompanyOS-RepoGuardian/1.0"
        }

        if self.api_token:
            headers["Authorization"] = f"token {self.api_token}"

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            timeout=30.0
        )

        self.logger = logger.bind(component="github_adapter")

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    def parse_repository_url(self, repository_url: str) -> Tuple[str, str]:
        """Parse repository URL to extract owner and repository name.

        Args:
            repository_url: GitHub repository URL in various formats

        Returns:
            Tuple of (owner, repo_name)

        Raises:
            ValueError: If URL format is not recognized
        """
        # Support multiple URL formats
        patterns = [
            # HTTPS formats
            r'https://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$',
            # SSH format
            r'git@github\.com:([^/]+)/([^/]+?)(?:\.git)?$',
        ]

        for pattern in patterns:
            match = re.match(pattern, repository_url)
            if match:
                owner, repo = match.groups()
                return owner, repo

        raise ValueError(f"Invalid GitHub repository URL format: {repository_url}")

    async def get_repository_info(self, repository_url: str, branch: str = "main") -> RepositoryInfo:
        """Fetch repository information from GitHub API.

        Args:
            repository_url: GitHub repository URL
            branch: Branch name to analyze

        Returns:
            RepositoryInfo model with repository data

        Raises:
            GitHubNotFoundError: Repository not found
            GitHubAuthenticationError: Authentication failed
            GitHubRateLimitError: Rate limit exceeded
            GitHubAPIError: Other API errors
        """
        try:
            owner, repo = self.parse_repository_url(repository_url)
        except ValueError as e:
            raise ApplicationError(str(e), non_retryable=True)

        self.logger.info(
            "Fetching repository information",
            owner=owner,
            repo=repo,
            branch=branch
        )

        try:
            # Fetch repository data
            repo_response = await self._make_api_call(f"/repos/{owner}/{repo}")

            # Fetch branch data for latest commit
            try:
                branch_response = await self._make_api_call(f"/repos/{owner}/{repo}/branches/{branch}")
                commit_sha = branch_response["commit"]["sha"]
            except GitHubNotFoundError:
                # Branch not found, use default branch
                branch = repo_response["default_branch"]
                branch_response = await self._make_api_call(f"/repos/{owner}/{repo}/branches/{branch}")
                commit_sha = branch_response["commit"]["sha"]

            # Map API response to domain model
            repository_info = RepositoryInfo(
                url=repository_url,
                full_name=repo_response["full_name"],
                branch=branch,
                commit_sha=commit_sha,
                default_branch=repo_response["default_branch"],
                language=repo_response.get("language"),
                size_kb=repo_response["size"],
                updated_at=datetime.fromisoformat(repo_response["updated_at"].replace('Z', '+00:00'))
            )

            self.logger.info(
                "Successfully fetched repository information",
                full_name=repository_info.full_name,
                commit_sha=commit_sha[:8],
                language=repository_info.language,
                size_kb=repository_info.size_kb
            )

            return repository_info

        except GitHubAPIError:
            # Re-raise GitHub-specific errors
            raise
        except Exception as e:
            self.logger.error("Unexpected error fetching repository info", error=str(e))
            raise GitHubAPIError(f"Unexpected error: {str(e)}")

    async def _make_api_call(self, endpoint: str) -> dict:
        """Make an authenticated API call to GitHub.

        Args:
            endpoint: API endpoint path

        Returns:
            JSON response as dictionary

        Raises:
            GitHubNotFoundError: Resource not found (404)
            GitHubAuthenticationError: Authentication failed (401, 403)
            GitHubRateLimitError: Rate limit exceeded
            GitHubAPIError: Other API errors
        """
        try:
            response = await self.client.get(endpoint)

            # Check for rate limiting
            if response.status_code == 403:
                rate_limit_remaining = response.headers.get("X-RateLimit-Remaining", "0")
                if rate_limit_remaining == "0":
                    rate_limit_reset = response.headers.get("X-RateLimit-Reset")
                    retry_after = None
                    if rate_limit_reset:
                        try:
                            reset_time = int(rate_limit_reset)
                            retry_after = reset_time - int(datetime.now().timestamp())
                            retry_after = max(0, retry_after)
                        except ValueError:
                            pass

                    error_msg = "GitHub API rate limit exceeded"
                    if retry_after:
                        error_msg += f" (retry after {retry_after} seconds)"

                    self.logger.warning(
                        "GitHub API rate limit exceeded",
                        retry_after=retry_after,
                        endpoint=endpoint
                    )

                    raise GitHubRateLimitError(error_msg, retry_after)

            # Handle different status codes
            if response.status_code == 401:
                raise GitHubAuthenticationError("GitHub API authentication failed - check token")
            elif response.status_code == 403:
                raise GitHubAuthenticationError("GitHub API access forbidden - insufficient permissions")
            elif response.status_code == 404:
                raise GitHubNotFoundError(f"GitHub resource not found: {endpoint}")
            elif response.status_code == 429:
                # Additional rate limiting (abuse detection)
                retry_after_header = response.headers.get("Retry-After")
                retry_after = int(retry_after_header) if retry_after_header else 60

                self.logger.warning(
                    "GitHub API secondary rate limit triggered",
                    retry_after=retry_after,
                    endpoint=endpoint
                )

                raise GitHubRateLimitError(
                    f"GitHub API secondary rate limit (retry after {retry_after}s)",
                    retry_after
                )
            elif response.status_code >= 500:
                raise GitHubAPIError(f"GitHub API server error: {response.status_code}")
            elif not response.is_success:
                raise GitHubAPIError(f"GitHub API error: {response.status_code} - {response.text}")

            # Log successful API call
            rate_limit_remaining = response.headers.get("X-RateLimit-Remaining")
            if rate_limit_remaining:
                self.logger.debug(
                    "GitHub API call successful",
                    endpoint=endpoint,
                    rate_limit_remaining=rate_limit_remaining
                )

            return response.json()

        except httpx.TimeoutException:
            self.logger.error("GitHub API request timed out", endpoint=endpoint)
            raise GitHubAPIError(f"GitHub API request timed out: {endpoint}")
        except httpx.RequestError as e:
            self.logger.error("GitHub API request failed", endpoint=endpoint, error=str(e))
            raise GitHubAPIError(f"GitHub API request failed: {str(e)}")

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
