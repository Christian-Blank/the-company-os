"""
Test worker that tests each incremental workflow to identify the failing import.
"""

import asyncio
import sys
from temporalio.client import Client
from temporalio.worker import Worker


async def test_workflow_step(workflow_class, step_name):
    """Test a single workflow step."""
    print(f"\n🔍 Testing {step_name} with {workflow_class.__name__}...")

    try:
        # Connect to Temporal
        client = await Client.connect("localhost:7233")

        # Create worker with this workflow only
        worker = Worker(
            client,
            task_queue=f"test-{step_name.lower()}-queue",
            workflows=[workflow_class],
            activities=[],
        )

        print(f"  ✅ Worker created successfully")

        # Test validation by starting worker briefly
        try:
            await asyncio.wait_for(worker.run(), timeout=2.0)
        except asyncio.TimeoutError:
            print(f"  ✅ {step_name} validation PASSED")
            return True

    except Exception as e:
        print(f"  ❌ {step_name} validation FAILED: {e}")
        return False


async def main():
    """Test all workflow steps."""
    print("Testing incremental workflow imports...")

    # Import the test workflows
    try:
        from .test_incremental_workflow import TEST_WORKFLOWS
        print(f"Available workflows: {[name for name, _ in TEST_WORKFLOWS]}")
    except Exception as e:
        print(f"Failed to import test workflows: {e}")
        return False

    # Test each workflow step
    all_passed = True
    for step_name, workflow_class in TEST_WORKFLOWS:
        passed = await test_workflow_step(workflow_class, step_name)
        if not passed:
            print(f"\n🎯 FOUND THE CULPRIT: {step_name} failed validation!")
            all_passed = False
            break

    if all_passed:
        print(f"\n✅ All {len(TEST_WORKFLOWS)} workflow steps passed validation")
        print("The issue might be in how imports combine, not individual imports")

    return all_passed


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)
