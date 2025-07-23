"""
Minimal workflow for testing Temporal validation.
"""

from temporalio import workflow


@workflow.defn
class MinimalWorkflow:
    """Absolutely minimal workflow with no external imports."""

    @workflow.run
    async def run(self, message: str) -> str:
        """Simple workflow that returns a message."""
        workflow.logger.info(f"Minimal workflow received: {message}")
        return f"Processed: {message}"
