"""
Repo Guardian Temporal Workflow.

This module contains the main workflow definition for the Repo Guardian service.
"""

from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

from ..models.domain import WorkflowInput, WorkflowOutput, WorkflowStatus, RepositoryInfo
from ..utils.logging import get_logger
from ..activities.repository import REPOSITORY_RETRY_POLICY

logger = get_logger(__name__)


@workflow.defn
class RepoGuardianWorkflow:
    """Main workflow for repository analysis and issue generation."""

    @workflow.run
    async def run(self, input: WorkflowInput) -> WorkflowOutput:
        """Execute the repository guardian workflow."""

        start_time = workflow.now()
        workflow_id = workflow.info().workflow_id
        correlation_id = f"repo-guardian-{workflow_id}"

        # Create structured logger with context
        wf_logger = logger.bind(
            workflow_id=workflow_id,
            correlation_id=correlation_id,
            repository_url=input.repository_url,
            branch=input.branch
        )

        try:
            wf_logger.info(
                "Repository analysis workflow started",
                analysis_depth=input.analysis_depth.value,
                create_issues=input.create_issues,
                max_issues=input.max_issues_per_run
            )

            # Phase 1: Fetch Repository Information
            wf_logger.info("Fetching repository information", status=WorkflowStatus.ANALYZING.value)
            
            repository_info = await workflow.execute_activity(
                "get_repository_info",
                args=[input.repository_url, input.branch],
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=REPOSITORY_RETRY_POLICY
            )
            
            wf_logger.info(
                "Repository information retrieved",
                full_name=repository_info.full_name,
                language=repository_info.language,
                size_kb=repository_info.size_kb,
                commit_sha=repository_info.commit_sha[:8]
            )

            # Phase 2: Additional processing based on analysis depth
            if input.analysis_depth.value in ["standard", "deep"]:
                wf_logger.info("Performing extended analysis")
                # Simulate additional processing for now
                await workflow.sleep(0.5 if input.analysis_depth.value == "standard" else 1.0)

            # Phase 3: Complete workflow
            end_time = workflow.now()
            execution_time = (end_time - start_time).total_seconds()

            wf_logger.info(
                "Repository analysis workflow completed successfully",
                execution_time_seconds=execution_time,
                status=WorkflowStatus.COMPLETED.value
            )

            return WorkflowOutput(
                workflow_id=workflow_id,
                repository_url=input.repository_url,
                branch=input.branch,
                status=WorkflowStatus.COMPLETED,
                analysis_completed=True,
                issues_found=0,  # Will be updated in subsequent steps
                issues_created=0,  # Will be updated when GitHub integration is added
                execution_time_seconds=execution_time,
                timestamp=end_time,
                metrics={
                    "correlation_id": correlation_id,
                    "analysis_depth": input.analysis_depth.value,
                    "workflow_version": "1.0.0"
                }
            )

        except Exception as e:
            end_time = workflow.now()
            execution_time = (end_time - start_time).total_seconds()

            error_msg = f"Workflow failed: {str(e)}"
            wf_logger.error(
                "Repository analysis workflow failed",
                error=error_msg,
                execution_time_seconds=execution_time,
                status=WorkflowStatus.FAILED.value
            )

            return WorkflowOutput(
                workflow_id=workflow_id,
                repository_url=input.repository_url,
                branch=input.branch,
                status=WorkflowStatus.FAILED,
                analysis_completed=False,
                execution_time_seconds=execution_time,
                timestamp=end_time,
                error_message=error_msg,
                metrics={
                    "correlation_id": correlation_id,
                    "workflow_version": "1.0.0"
                }
            )
