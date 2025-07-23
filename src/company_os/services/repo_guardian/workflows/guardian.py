"""
Repo Guardian Temporal Workflow.

This module contains the main workflow definition for the Repo Guardian service.
"""

from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

from ..models.domain import WorkflowInput, WorkflowOutput, WorkflowStatus, RepositoryInfo
from ..constants import REPOSITORY_RETRY_POLICY, REPOSITORY_FETCH_TIMEOUT


@workflow.defn
class RepoGuardianWorkflow:
    """Main workflow for repository analysis and issue generation."""

    @workflow.run
    async def run(self, input: WorkflowInput) -> WorkflowOutput:
        """Execute the repository guardian workflow."""

        start_time = workflow.now()
        workflow_id = workflow.info().workflow_id
        correlation_id = f"repo-guardian-{workflow_id}"

        # Use Temporal's built-in workflow logger
        workflow.logger.info(
            f"Repository analysis workflow started - "
            f"repository_url={input.repository_url}, "
            f"branch={input.branch}, "
            f"analysis_depth={input.analysis_depth.value}, "
            f"create_issues={input.create_issues}"
        )

        try:
            # Phase 1: Fetch Repository Information
            workflow.logger.info("Fetching repository information")

            repository_info = await workflow.execute_activity(
                "get_repository_info",
                args=[input.repository_url, input.branch],
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=REPOSITORY_RETRY_POLICY
            )

            workflow.logger.info(
                f"Repository information retrieved - "
                f"full_name={repository_info.full_name}, "
                f"language={repository_info.language}, "
                f"size_kb={repository_info.size_kb}, "
                f"commit_sha={repository_info.commit_sha[:8]}"
            )

            # Phase 2: Additional processing based on analysis depth
            if input.analysis_depth.value in ["standard", "deep"]:
                workflow.logger.info("Performing extended analysis")
                # Simulate additional processing for now
                await workflow.sleep(0.5 if input.analysis_depth.value == "standard" else 1.0)

            # Phase 3: Complete workflow
            end_time = workflow.now()
            execution_time = (end_time - start_time).total_seconds()

            workflow.logger.info(
                f"Repository analysis workflow completed successfully - "
                f"execution_time_seconds={execution_time}"
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
            workflow.logger.error(
                f"Repository analysis workflow failed - "
                f"error={error_msg}, "
                f"execution_time_seconds={execution_time}"
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
