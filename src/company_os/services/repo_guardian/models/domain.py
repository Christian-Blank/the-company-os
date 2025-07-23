"""
Domain models for Repo Guardian service.

This module contains the data models used throughout the service.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, validator, ConfigDict


class AnalysisDepth(str, Enum):
    """Analysis depth levels."""
    LIGHT = "light"
    STANDARD = "standard"
    DEEP = "deep"


class IssueSeverity(str, Enum):
    """Severity levels for issues."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class WorkflowStatus(str, Enum):
    """Workflow execution status."""
    STARTED = "started"
    ANALYZING = "analyzing"
    GENERATING_ISSUES = "generating_issues"
    CREATING_ISSUES = "creating_issues"
    COMPLETED = "completed"
    FAILED = "failed"


# Core Workflow Models
class WorkflowInput(BaseModel):
    """Input parameters for the Repo Guardian workflow."""
    repository_url: str = Field(..., description="GitHub repository URL")
    branch: str = Field(default="main", description="Branch to analyze")
    since_commit: Optional[str] = Field(None, description="Starting commit SHA for incremental analysis")
    analysis_depth: AnalysisDepth = Field(default=AnalysisDepth.STANDARD, description="Analysis thoroughness")
    create_issues: bool = Field(default=False, description="Whether to create GitHub issues")
    issue_labels: List[str] = Field(default_factory=lambda: ["repo-guardian", "automated"], description="Labels for created issues")
    max_issues_per_run: int = Field(default=5, description="Maximum issues to create in one run")

    @validator('repository_url')
    def validate_repository_url(cls, v):
        if not v.startswith(('https://github.com/', 'git@github.com:')):
            raise ValueError('Only GitHub repositories are supported')
        return v


class WorkflowOutput(BaseModel):
    """Output from the Repo Guardian workflow."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    workflow_id: str
    repository_url: str
    branch: str
    status: WorkflowStatus
    analysis_completed: bool
    issues_found: int = 0
    issues_created: int = 0
    execution_time_seconds: float
    timestamp: datetime
    error_message: Optional[str] = None
    metrics: Dict[str, Any] = Field(default_factory=dict)


class WorkflowConfig(BaseModel):
    """Configuration for workflow execution."""
    temporal_namespace: str = Field(default="default", description="Temporal namespace")
    task_queue: str = Field(default="repo-guardian-task-queue", description="Temporal task queue")
    activity_timeout_seconds: int = Field(default=300, description="Default activity timeout")
    workflow_timeout_seconds: int = Field(default=3600, description="Total workflow timeout")
    github_token_secret_name: str = Field(default="GITHUB_TOKEN", description="GitHub token environment variable")
    openai_api_key_secret_name: str = Field(default="OPENAI_API_KEY", description="OpenAI API key environment variable")
    anthropic_api_key_secret_name: str = Field(default="ANTHROPIC_API_KEY", description="Anthropic API key environment variable")


# Analysis Models
class RepositoryInfo(BaseModel):
    """Basic repository information."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    url: str
    full_name: str
    branch: str
    commit_sha: str
    default_branch: str
    language: Optional[str]
    size_kb: int
    updated_at: datetime


class AnalysisMetrics(BaseModel):
    """Metrics from repository analysis."""
    files_analyzed: int = 0
    lines_of_code: int = 0
    complexity_score: float = 0.0
    test_coverage_percent: Optional[float] = None
    documentation_score: float = 0.0
    security_score: float = 0.0
    maintainability_score: float = 0.0


class Issue(BaseModel):
    """Represents an issue found during analysis."""
    title: str
    description: str
    severity: IssueSeverity
    category: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    suggestion: Optional[str] = None
    labels: List[str] = Field(default_factory=list)


class AnalysisResult(BaseModel):
    """Complete analysis result."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    repository_info: RepositoryInfo
    metrics: AnalysisMetrics
    issues: List[Issue] = Field(default_factory=list)
    overall_score: float = Field(ge=0.0, le=10.0, description="Overall quality score 0-10")
    analysis_duration_seconds: float
    llm_tokens_used: int = 0
    llm_cost_usd: float = 0.0
    timestamp: datetime
