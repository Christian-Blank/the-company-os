"""
Domain models for Repo Guardian service.

This module contains the data models used throughout the service.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from enum import Enum


class IssueSeverity(Enum):
    """Severity levels for issues."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class FileAnalysis:
    """Analysis results for a single file."""
    path: str
    complexity_score: float
    issues: List[dict]
    recommendations: List[str]


@dataclass
class RepositoryState:
    """State of a repository at analysis time."""
    url: str
    branch: str
    commit_sha: str
    analyzed_at: datetime
    files_count: int
    total_lines: int


@dataclass
class Issue:
    """Represents an issue found during analysis."""
    title: str
    description: str
    severity: IssueSeverity
    file_path: Optional[str]
    line_number: Optional[int]
    category: str
    suggestion: Optional[str]


@dataclass
class AnalysisResult:
    """Complete analysis result."""
    repository_state: RepositoryState
    overall_score: float
    issues: List[Issue]
    metrics: dict
    execution_time_seconds: float
    llm_tokens_used: int
    llm_cost_usd: float


@dataclass
class WorkflowInput:
    """Input parameters for the Repo Guardian workflow."""
    repository_url: str
    branch: str = "main"
    since_commit: Optional[str] = None
    analysis_depth: str = "standard"  # light, standard, deep
    create_issues: bool = True
    issue_labels: List[str] = None

    def __post_init__(self):
        if self.issue_labels is None:
            self.issue_labels = ["repo-guardian", "automated"]
