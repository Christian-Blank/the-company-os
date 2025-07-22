"""
Configuration for Repo Guardian service.

This module handles environment configuration and settings.
"""

import os
from typing import Optional
from pydantic import BaseSettings, Field


class RepoGuardianSettings(BaseSettings):
    """Settings for the Repo Guardian service."""

    # Temporal Configuration
    temporal_host: str = Field(default="localhost:7233", description="Temporal server address")
    temporal_namespace: str = Field(default="default", description="Temporal namespace")
    task_queue: str = Field(default="repo-guardian-task-queue", description="Temporal task queue")

    # Timeouts
    activity_timeout_seconds: int = Field(default=300, description="Default activity timeout")
    workflow_timeout_seconds: int = Field(default=3600, description="Total workflow timeout")

    # GitHub Configuration
    github_token: Optional[str] = Field(default=None, description="GitHub API token")
    github_api_base_url: str = Field(default="https://api.github.com", description="GitHub API base URL")

    # LLM Configuration
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API key")

    # Cost Controls
    max_tokens_per_request: int = Field(default=4000, description="Maximum tokens per LLM request")
    max_cost_per_workflow_usd: float = Field(default=1.0, description="Maximum cost per workflow run")

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format: json or console")

    # Metrics
    metrics_enabled: bool = Field(default=True, description="Enable metrics collection")
    metrics_port: int = Field(default=9090, description="Metrics HTTP port")

    # Health Check
    health_check_enabled: bool = Field(default=True, description="Enable health check endpoint")
    health_check_port: int = Field(default=8080, description="Health check HTTP port")

    # Development
    development_mode: bool = Field(default=False, description="Enable development mode features")
    mock_llm_responses: bool = Field(default=False, description="Use mock LLM responses for testing")

    class Config:
        env_prefix = "REPO_GUARDIAN_"
        case_sensitive = False
        env_file = ".env"


def get_settings() -> RepoGuardianSettings:
    """Get configuration settings."""
    return RepoGuardianSettings()


# Global settings instance
settings = get_settings()
