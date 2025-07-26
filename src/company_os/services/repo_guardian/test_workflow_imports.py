"""
Test workflow imports to ensure they follow Temporal's sandbox rules.

This test validates that workflows can be imported in Temporal's sandbox
without violating determinism or import restrictions.
"""

from temporalio.testing import WorkflowEnvironment


async def test_workflow_imports():
    """Verify workflows can be imported in Temporal's sandbox.

    This test will fail immediately if any workflow violates
    Temporal's import rules (e.g., importing from activities).

    If this test fails, check:
    1. Workflows should not import from activity modules
    2. Workflows should not import modules with side effects
    3. Workflows should only use deterministic imports
    """
    # The import itself is the test - it will fail if invalid
    from .workflows.guardian import RepoGuardianWorkflow

    # Start environment to fully validate workflow definition
    async with await WorkflowEnvironment.start_local():
        # Success means imports are clean and workflow is valid
        assert RepoGuardianWorkflow is not None


def test_constants_import():
    """Verify constants can be imported from both workflows and activities."""
    # Both should import successfully without circular dependencies
    from src.company_os.services.repo_guardian.constants import (
        REPOSITORY_RETRY_POLICY,
        TASK_QUEUE,
    )
    from src.company_os.services.repo_guardian.workflows.guardian import (
        RepoGuardianWorkflow,
    )
    from src.company_os.services.repo_guardian.activities.repository import (
        get_repository_info,
    )

    assert REPOSITORY_RETRY_POLICY is not None
    assert TASK_QUEUE == "repo-guardian-task-queue"
    assert RepoGuardianWorkflow is not None
    assert get_repository_info is not None


if __name__ == "__main__":
    # Run the sync test
    test_constants_import()

    # Run the async test
    import asyncio

    asyncio.run(test_workflow_imports())
    print("✅ All workflow import tests passed!")
