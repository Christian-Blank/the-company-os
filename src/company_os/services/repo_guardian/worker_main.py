"""
Repo Guardian Temporal Worker.

This module runs the Temporal worker that executes workflows and activities.
"""

import asyncio
import logging
from temporalio.client import Client
from temporalio.worker import Worker

from .workflows.guardian import RepoGuardianWorkflow
from .activities import repository, analysis, llm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Run the Temporal worker."""
    # Create client connected to server at the given address
    # In production, this would use environment variables
    client = await Client.connect("localhost:7233")

    # Run the worker
    worker = Worker(
        client,
        task_queue="repo-guardian-task-queue",
        workflows=[RepoGuardianWorkflow],
        activities=[
            # Repository activities
            repository.clone_repository,
            repository.get_diff,
            repository.cleanup_repository,
            # Analysis activities
            analysis.analyze_complexity,
            analysis.verify_patterns,
            analysis.check_documentation,
            # LLM activities
            llm.analyze_with_llm,
            llm.generate_issue_description,
        ],
    )

    logger.info("Starting Repo Guardian worker...")
    logger.info("Connected to Temporal at localhost:7233")
    logger.info("Listening on task queue: repo-guardian-task-queue")

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
