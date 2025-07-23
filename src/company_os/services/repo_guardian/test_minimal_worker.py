"""
Test worker with minimal workflow to isolate validation issues.
"""

import asyncio
import sys
from temporalio.client import Client
from temporalio.worker import Worker
from .minimal_workflow import MinimalWorkflow


async def test_minimal_worker():
    """Test if a minimal workflow validates successfully."""
    print("Testing minimal workflow validation...")

    try:
        # Connect to Temporal
        client = await Client.connect("localhost:7233")
        print("✅ Connected to Temporal server")

        # Create worker with minimal workflow only
        worker = Worker(
            client,
            task_queue="test-minimal-queue",
            workflows=[MinimalWorkflow],
            activities=[],  # No activities
        )
        print("✅ Worker created successfully")

        print("🔍 Starting worker (this tests validation)...")
        # This will fail at validation if there's still an issue
        await asyncio.wait_for(worker.run(), timeout=5.0)

    except asyncio.TimeoutError:
        print("✅ Worker started successfully (timeout expected)")
        return True
    except Exception as e:
        print(f"❌ Worker failed: {e}")
        return False
    finally:
        print("🛑 Test complete")


if __name__ == "__main__":
    result = asyncio.run(test_minimal_worker())
    sys.exit(0 if result else 1)
