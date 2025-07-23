"""
Test script for Repo Guardian workflows.

This script provides comprehensive testing capabilities for the Repo Guardian service.
"""

import asyncio
import uuid
import time
from datetime import datetime
from typing import Dict, Any, List
from temporalio.client import Client, WorkflowHandle

from src.company_os.services.repo_guardian.config import settings
from src.company_os.services.repo_guardian.utils.logging import setup_logging, get_logger
from src.company_os.services.repo_guardian.models.domain import WorkflowInput, WorkflowOutput, AnalysisDepth
from src.company_os.services.repo_guardian.workflows.guardian import RepoGuardianWorkflow

# Initialize logging
setup_logging()
logger = get_logger(__name__)


class WorkflowTester:
    """Comprehensive workflow testing utility."""

    def __init__(self):
        self.client: Client = None
        self.results: List[Dict[str, Any]] = []

    async def connect(self) -> None:
        """Connect to Temporal server."""
        self.client = await Client.connect(
            settings.temporal_host,
            namespace=settings.temporal_namespace
        )
        logger.info("Connected to Temporal server",
                   host=settings.temporal_host,
                   namespace=settings.temporal_namespace)

    async def disconnect(self) -> None:
        """Disconnect from Temporal server."""
        if self.client:
            await self.client.close()
            logger.info("Disconnected from Temporal server")

    async def run_single_test(
        self,
        test_name: str,
        workflow_input: WorkflowInput,
        expected_success: bool = True
    ) -> Dict[str, Any]:
        """Run a single workflow test."""
        workflow_id = f"test-repo-guardian-{test_name}-{uuid.uuid4()}"

        logger.info(f"Starting test: {test_name}",
                   workflow_id=workflow_id,
                   repository_url=workflow_input.repository_url)

        start_time = time.time()

        try:
            # Start workflow
            handle: WorkflowHandle = await self.client.start_workflow(
                RepoGuardianWorkflow.run,
                workflow_input,
                id=workflow_id,
                task_queue=settings.task_queue
            )

            logger.info(f"Workflow started: {workflow_id}")
            print(f"🚀 Started workflow: {workflow_id}")
            print(f"   📊 Temporal UI: http://localhost:8080/namespaces/{settings.temporal_namespace}/workflows/{workflow_id}")

            # Wait for result with timeout
            result: WorkflowOutput = await asyncio.wait_for(
                handle.result(),
                timeout=30.0  # 30 second timeout for tests
            )

            execution_time = time.time() - start_time

            # Analyze results
            success = result.analysis_completed and not result.error_message

            test_result = {
                "test_name": test_name,
                "workflow_id": workflow_id,
                "success": success,
                "expected_success": expected_success,
                "passed": success == expected_success,
                "execution_time": execution_time,
                "workflow_result": result.dict(),
                "error": None
            }

            if success:
                logger.info(f"Test {test_name} completed successfully",
                           execution_time=execution_time,
                           workflow_execution_time=result.execution_time_seconds)
                print(f"✅ Test '{test_name}' PASSED")
                print(f"   ⏱️  Execution time: {execution_time:.2f}s")
                print(f"   📈 Workflow time: {result.execution_time_seconds:.2f}s")
                print(f"   📊 Status: {result.status.value}")
            else:
                logger.warning(f"Test {test_name} failed",
                              error=result.error_message)
                print(f"❌ Test '{test_name}' FAILED")
                print(f"   💥 Error: {result.error_message}")

        except asyncio.TimeoutError:
            execution_time = time.time() - start_time
            test_result = {
                "test_name": test_name,
                "workflow_id": workflow_id,
                "success": False,
                "expected_success": expected_success,
                "passed": False,
                "execution_time": execution_time,
                "workflow_result": None,
                "error": "Workflow timeout after 30 seconds"
            }
            logger.error(f"Test {test_name} timed out", timeout=30.0)
            print(f"⏰ Test '{test_name}' TIMED OUT")

        except Exception as e:
            execution_time = time.time() - start_time
            test_result = {
                "test_name": test_name,
                "workflow_id": workflow_id,
                "success": False,
                "expected_success": expected_success,
                "passed": False,
                "execution_time": execution_time,
                "workflow_result": None,
                "error": str(e)
            }
            logger.error(f"Test {test_name} failed with exception", error=str(e))
            print(f"💥 Test '{test_name}' ERROR: {str(e)}")

        self.results.append(test_result)
        print()  # Empty line for readability
        return test_result

    async def run_test_suite(self) -> Dict[str, Any]:
        """Run the complete test suite."""
        print("🧪 Starting Repo Guardian Test Suite")
        print("=" * 50)

        # Test cases
        test_cases = [
            {
                "name": "basic-success",
                "input": WorkflowInput(
                    repository_url="https://github.com/octocat/Hello-World",
                    branch="master",  # This repo uses master
                    analysis_depth=AnalysisDepth.LIGHT,
                    create_issues=False
                ),
                "expected_success": True
            },
            {
                "name": "company-os-repo",
                "input": WorkflowInput(
                    repository_url="https://github.com/Christian-Blank/the-company-os",
                    branch="main",
                    analysis_depth=AnalysisDepth.STANDARD,
                    create_issues=False
                ),
                "expected_success": True  # Will succeed if token provided, fail gracefully without
            },
            {
                "name": "different-branch",
                "input": WorkflowInput(
                    repository_url="https://github.com/octocat/Hello-World",
                    branch="nonexistent-branch",  # Should fallback to default
                    analysis_depth=AnalysisDepth.LIGHT,
                    create_issues=False
                ),
                "expected_success": True  # Should fallback to master branch
            },
            {
                "name": "deep-analysis",
                "input": WorkflowInput(
                    repository_url="https://github.com/octocat/Hello-World",
                    branch="master",
                    analysis_depth=AnalysisDepth.DEEP,
                    create_issues=False
                ),
                "expected_success": True
            },
            {
                "name": "invalid-repo",
                "input": WorkflowInput(
                    repository_url="https://github.com/nonexistent-user/nonexistent-repo",
                    branch="main",
                    analysis_depth=AnalysisDepth.LIGHT,
                    create_issues=False
                ),
                "expected_success": False
            },
            {
                "name": "invalid-url-format",
                "input": WorkflowInput(
                    repository_url="https://invalid-url-format-not-github",
                    branch="main",
                    analysis_depth=AnalysisDepth.LIGHT,
                    create_issues=False
                ),
                "expected_success": False
            }
        ]

        # Run all tests
        for test_case in test_cases:
            await self.run_single_test(
                test_case["name"],
                test_case["input"],
                test_case["expected_success"]
            )

        # Generate summary
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["passed"])
        failed_tests = total_tests - passed_tests

        print("📊 Test Suite Results")
        print("=" * 30)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")

        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.results:
                if not result["passed"]:
                    print(f"  - {result['test_name']}: {result['error']}")

        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests/total_tests)*100,
            "results": self.results
        }


async def test_basic_workflow() -> None:
    """Test a single basic workflow."""
    print("🧪 Testing Basic Workflow")
    print("=" * 30)

    tester = WorkflowTester()

    try:
        await tester.connect()

        workflow_input = WorkflowInput(
            repository_url="https://github.com/Christian-Blank/the-company-os",
            branch="main",
            analysis_depth=AnalysisDepth.STANDARD,
            create_issues=False  # Safe for testing
        )

        result = await tester.run_single_test("basic-test", workflow_input)

        if result["passed"]:
            print("🎉 Basic workflow test completed successfully!")
        else:
            print("💥 Basic workflow test failed!")
            return 1

    finally:
        await tester.disconnect()

    return 0


async def test_comprehensive_suite() -> int:
    """Run the comprehensive test suite."""
    tester = WorkflowTester()

    try:
        await tester.connect()
        summary = await tester.run_test_suite()

        # Return appropriate exit code
        return 0 if summary["failed_tests"] == 0 else 1

    finally:
        await tester.disconnect()


async def main() -> None:
    """Main entry point for testing."""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--suite":
        exit_code = await test_comprehensive_suite()
    else:
        exit_code = await test_basic_workflow()

    sys.exit(exit_code)


if __name__ == "__main__":
    asyncio.run(main())
