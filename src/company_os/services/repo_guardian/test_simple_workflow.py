"""
Simple workflow test to isolate import issues.
"""

from datetime import timedelta
from temporalio import workflow


@workflow.defn
class SimpleTestWorkflow:
    """Minimal workflow for testing imports."""

    @workflow.run
    async def run(self, message: str) -> str:
        """Simple workflow that just returns a message."""
        workflow.logger.info(f"Simple workflow received: {message}")
        await workflow.sleep(0.1)  # Minimal processing
        return f"Processed: {message}"


if __name__ == "__main__":
    print("Simple workflow definition created successfully")
