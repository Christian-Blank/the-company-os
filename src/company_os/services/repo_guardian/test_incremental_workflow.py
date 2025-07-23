"""
Test workflow that incrementally adds imports to identify the culprit.
"""

from temporalio import workflow

# Test 1: Just datetime and RetryPolicy from temporalio
from datetime import timedelta
from temporalio.common import RetryPolicy

@workflow.defn
class TestStep1Workflow:
    """Test with basic imports only."""

    @workflow.run
    async def run(self, message: str) -> str:
        return f"Step 1: {message}"


# Test 2: Add constants import
try:
    from src.company_os.services.repo_guardian.constants import REPOSITORY_RETRY_POLICY, REPOSITORY_FETCH_TIMEOUT

    @workflow.defn
    class TestStep2Workflow:
        """Test with constants import."""

        @workflow.run
        async def run(self, message: str) -> str:
            return f"Step 2: {message}"

    constants_import_ok = True
except Exception as e:
    print(f"Constants import failed: {e}")
    constants_import_ok = False


# Test 3: Add domain models import
try:
    from src.company_os.services.repo_guardian.models.domain import WorkflowInput, WorkflowOutput, WorkflowStatus, RepositoryInfo

    @workflow.defn
    class TestStep3Workflow:
        """Test with domain models import."""

        @workflow.run
        async def run(self, input: WorkflowInput) -> WorkflowOutput:
            return WorkflowOutput(
                workflow_id="test",
                repository_url=input.repository_url,
                branch=input.branch,
                status=WorkflowStatus.COMPLETED,
                analysis_completed=True,
                execution_time_seconds=0.1,
                timestamp=workflow.now()
            )

    domain_import_ok = True
except Exception as e:
    print(f"Domain models import failed: {e}")
    domain_import_ok = False


# List of workflows to test
TEST_WORKFLOWS = []

# Always add the basic workflow
TEST_WORKFLOWS.append(("Step1", TestStep1Workflow))

if constants_import_ok:
    TEST_WORKFLOWS.append(("Step2", TestStep2Workflow))

if domain_import_ok:
    TEST_WORKFLOWS.append(("Step3", TestStep3Workflow))

print(f"Available test workflows: {[name for name, _ in TEST_WORKFLOWS]}")
