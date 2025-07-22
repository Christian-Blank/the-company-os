"""
Repo Guardian Temporal Worker.

This module runs the Temporal worker that executes workflows and activities.
"""

import asyncio
import signal
import sys
from typing import Optional
from temporalio.client import Client
from temporalio.worker import Worker, UnsandboxedWorkflowRunner
from temporalio.runtime import Runtime, PrometheusConfig, TelemetryConfig

from .config import settings
from .utils.logging import setup_logging, get_logger
from .workflows.guardian import RepoGuardianWorkflow
from .activities.repository import REPOSITORY_ACTIVITIES

# Initialize logging
setup_logging()
logger = get_logger(__name__)


class WorkerManager:
    """Manages the Temporal worker lifecycle."""

    def __init__(self):
        self.worker: Optional[Worker] = None
        self.client: Optional[Client] = None
        self.shutdown_event = asyncio.Event()

    async def start(self) -> None:
        """Start the Temporal worker."""
        try:
            logger.info("Starting Repo Guardian worker",
                       temporal_host=settings.temporal_host,
                       task_queue=settings.task_queue,
                       log_level=settings.log_level,
                       development_mode=settings.development_mode)

            # Set up Temporal runtime with telemetry
            if settings.metrics_enabled:
                runtime = Runtime(telemetry=TelemetryConfig(
                    metrics=PrometheusConfig(bind_address=f"0.0.0.0:{settings.metrics_port}")
                ))
            else:
                runtime = None

            # Connect to Temporal
            self.client = await Client.connect(
                settings.temporal_host,
                namespace=settings.temporal_namespace,
                runtime=runtime
            )

            logger.info("Connected to Temporal server",
                       namespace=settings.temporal_namespace)

            # Create worker
            self.worker = Worker(
                self.client,
                task_queue=settings.task_queue,
                workflows=[RepoGuardianWorkflow],
                activities=REPOSITORY_ACTIVITIES,
                workflow_runner=UnsandboxedWorkflowRunner() if settings.development_mode else None,
            )

            logger.info("Worker configured successfully",
                       workflows=["RepoGuardianWorkflow"],
                       activities_count=len(REPOSITORY_ACTIVITIES))

            # Start worker
            logger.info("Worker starting - ready to process workflows")
            await self.worker.run()

        except Exception as e:
            logger.error("Failed to start worker", error=str(e))
            raise

    async def shutdown(self) -> None:
        """Gracefully shutdown the worker."""
        logger.info("Initiating graceful shutdown")

        if self.worker:
            logger.info("Shutting down worker")
            self.worker.shutdown()

        if self.client:
            logger.info("Closing Temporal client connection")
            await self.client.close()

        logger.info("Shutdown complete")


async def main() -> None:
    """Main entry point for the worker."""
    worker_manager = WorkerManager()

    def signal_handler(signum: int, frame) -> None:
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, initiating shutdown")
        asyncio.create_task(worker_manager.shutdown())

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        await worker_manager.start()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error("Worker failed", error=str(e))
        sys.exit(1)
    finally:
        await worker_manager.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
