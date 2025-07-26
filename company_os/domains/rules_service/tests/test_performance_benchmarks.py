"""Performance benchmarks for the Rules Service.

This module provides standardized performance benchmarks for critical operations
and establishes baselines for performance regression detection.
"""

import shutil
import tempfile
import time
from pathlib import Path
from typing import List
from unittest.mock import MagicMock

import pytest

from company_os.domains.rules_service.src.config import AgentFolder, RulesServiceConfig
from company_os.domains.rules_service.src.discovery import RuleDiscoveryService
from company_os.domains.rules_service.src.sync import SyncService
from company_os.domains.rules_service.src.validation import ValidationService


class TestPerformanceBenchmarks:
    """Performance benchmarks for critical operations."""

    def setup_method(self):
        """Set up benchmark environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.rules_dir = Path(self.temp_dir) / "rules"
        self.rules_dir.mkdir()

        # Create test config
        self.config = RulesServiceConfig(
            version="1.0",
            agent_folders=[
                AgentFolder(
                    path=str(Path(self.temp_dir) / f".folder_{i}/rules"),
                    description=f"Folder {i}",
                )
                for i in range(3)
            ],
        )

    def teardown_method(self):
        """Clean up benchmark environment."""
        shutil.rmtree(self.temp_dir)

    def create_rule_files(self, count: int) -> List[Path]:
        """Create test rule files for benchmarking."""
        files = []
        for i in range(count):
            rule_file = self.rules_dir / f"rule_{i:03d}.rules.md"
            rule_file.write_text(f"""---
title: "Performance Test Rule {i}"
version: 1.0
status: "Active"
owner: "Performance Test"
last_updated: "2025-07-16T15:44:00-07:00"
tags: ["performance", "test", "benchmark"]
---

# Performance Test Rule {i}

This is a test rule for performance benchmarking.

## Rules Table

| Rule ID | Description | Severity |
|---------|-------------|----------|
| PR{i:03d}001 | Rule {i} first requirement | error |
| PR{i:03d}002 | Rule {i} second requirement | warning |
| PR{i:03d}003 | Rule {i} third requirement | info |

## YAML Requirements

```yaml
frontmatter:
  title: "required"
  version: "required"
  status: "required"
```

## List Rules

- **MUST** follow performance rule {i}
- **SHOULD** include performance metrics
- **MAY** include benchmark data
""")
            files.append(rule_file)
        return files

    @pytest.mark.performance
    def test_discovery_performance_baseline(self, benchmark):
        """Benchmark rules discovery performance."""
        # Create 10 rule files
        self.create_rule_files(10)

        discovery_service = RuleDiscoveryService(str(self.rules_dir))

        # Benchmark discovery operation
        rules = benchmark(discovery_service.discover_rules)

        # Verify results
        assert len(rules) == 10
        assert all(rule.title for rule in rules)

        # Performance baseline: should complete in under 5 seconds
        assert benchmark.stats.mean < 5.0

    @pytest.mark.performance
    def test_sync_performance_baseline(self, benchmark):
        """Benchmark sync operation performance."""
        # Create 5 rule files
        self.create_rule_files(5)

        # Create rule documents
        discovery_service = RuleDiscoveryService(str(self.rules_dir))
        rules = discovery_service.discover_rules()

        sync_service = SyncService(self.config, Path(self.temp_dir))

        # Benchmark sync operation
        result = benchmark(sync_service.sync_rules, rules)

        # Verify results
        assert result.added == 15  # 5 rules × 3 folders
        assert result.total_changes == 15

        # Performance baseline: should complete in under 3 seconds
        assert benchmark.stats.mean < 3.0

    @pytest.mark.performance
    def test_validation_performance_baseline(self, benchmark):
        """Benchmark validation performance."""
        # Create a test document
        test_doc = Path(self.temp_dir) / "test.md"
        test_doc.write_text("""---
title: "Test Document"
version: 1.0
status: "Active"
owner: "Test"
last_updated: "2025-07-16T15:44:00-07:00"
tags: ["test"]
---

# Test Document

This is a test document for validation benchmarking.

## Content

Some content here.
""")

        validation_service = ValidationService(self.config)

        # Benchmark validation operation
        result = benchmark(validation_service.validate_file, test_doc)

        # Verify results
        assert result is not None

        # Performance baseline: should complete in under 2 seconds
        assert benchmark.stats.mean < 2.0

    @pytest.mark.performance
    def test_large_repository_simulation(self, benchmark):
        """Benchmark performance with large repository simulation."""
        # Create 50 rule files to simulate large repository
        self.create_rule_files(50)

        discovery_service = RuleDiscoveryService(str(self.rules_dir))

        def full_discovery_cycle():
            """Full discovery cycle including rule extraction."""
            rules = discovery_service.discover_rules()
            # Simulate some processing
            processed = []
            for rule in rules:
                if rule.title and rule.document_type:
                    processed.append(rule)
            return processed

        # Benchmark full discovery cycle
        processed_rules = benchmark(full_discovery_cycle)

        # Verify results
        assert len(processed_rules) == 50

        # Performance baseline: should complete in under 10 seconds
        assert benchmark.stats.mean < 10.0

    @pytest.mark.performance
    def test_concurrent_operations_performance(self, benchmark):
        """Benchmark concurrent operations performance."""
        from concurrent.futures import ThreadPoolExecutor

        # Create 20 rule files
        self.create_rule_files(20)

        discovery_service = RuleDiscoveryService(str(self.rules_dir))
        rules = discovery_service.discover_rules()

        # Create multiple sync services for concurrent test
        sync_services = [
            SyncService(
                RulesServiceConfig(
                    version="1.0",
                    agent_folders=[
                        AgentFolder(
                            path=str(Path(self.temp_dir) / f".concurrent_{i}/rules"),
                            description=f"Concurrent {i}",
                        )
                    ],
                ),
                Path(self.temp_dir),
            )
            for i in range(5)
        ]

        def concurrent_sync():
            """Perform concurrent sync operations."""
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [
                    executor.submit(service.sync_rules, rules)
                    for service in sync_services
                ]
                results = [future.result() for future in futures]
            return results

        # Benchmark concurrent operations
        results = benchmark(concurrent_sync)

        # Verify results
        assert len(results) == 5
        assert all(result.added == 20 for result in results)

        # Performance baseline: should complete in under 8 seconds
        assert benchmark.stats.mean < 8.0


class TestPerformanceRegression:
    """Performance regression tests to catch performance degradation."""

    def setup_method(self):
        """Set up regression test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.baseline_file = Path(self.temp_dir) / "performance_baseline.json"

    def teardown_method(self):
        """Clean up regression test environment."""
        shutil.rmtree(self.temp_dir)

    def save_baseline(self, operation: str, duration: float):
        """Save performance baseline for regression detection."""
        import json

        baselines = {}
        if self.baseline_file.exists():
            with open(self.baseline_file, "r") as f:
                baselines = json.load(f)

        baselines[operation] = duration

        with open(self.baseline_file, "w") as f:
            json.dump(baselines, f, indent=2)

    def check_regression(self, operation: str, duration: float, tolerance: float = 0.5):
        """Check if performance has regressed beyond tolerance."""
        import json

        if not self.baseline_file.exists():
            # No baseline, save current as baseline
            self.save_baseline(operation, duration)
            return True

        with open(self.baseline_file, "r") as f:
            baselines = json.load(f)

        if operation not in baselines:
            self.save_baseline(operation, duration)
            return True

        baseline = baselines[operation]
        regression_threshold = baseline * (1 + tolerance)

        if duration > regression_threshold:
            pytest.fail(
                f"Performance regression detected for {operation}!\n"
                f"Baseline: {baseline:.3f}s\n"
                f"Current: {duration:.3f}s\n"
                f"Threshold: {regression_threshold:.3f}s\n"
                f"Regression: {((duration - baseline) / baseline * 100):.1f}%"
            )

        return True

    @pytest.mark.regression
    def test_discovery_regression(self):
        """Test for performance regression in discovery operations."""
        temp_rules_dir = Path(self.temp_dir) / "rules"
        temp_rules_dir.mkdir()

        # Create consistent test data
        for i in range(10):
            rule_file = temp_rules_dir / f"rule_{i}.rules.md"
            rule_file.write_text(f"# Rule {i}\n\nContent for rule {i}")

        discovery_service = RuleDiscoveryService(str(temp_rules_dir))

        # Measure discovery time
        start_time = time.time()
        rules = discovery_service.discover_rules()
        end_time = time.time()

        duration = end_time - start_time

        # Check for regression
        self.check_regression("discovery_10_files", duration)

        # Verify functionality
        assert len(rules) == 10

    @pytest.mark.regression
    def test_sync_regression(self):
        """Test for performance regression in sync operations."""
        temp_rules_dir = Path(self.temp_dir) / "rules"
        temp_rules_dir.mkdir()

        # Create test rules
        rules = []
        for i in range(5):
            rule_file = temp_rules_dir / f"sync_rule_{i}.rules.md"
            rule_file.write_text(f"# Sync Rule {i}")

            # Create mock rule document
            rule_doc = MagicMock()
            rule_doc.file_path = str(rule_file)
            rule_doc.title = f"Sync Rule {i}"
            rules.append(rule_doc)

        config = RulesServiceConfig(
            version="1.0",
            agent_folders=[
                AgentFolder(
                    path=str(Path(self.temp_dir) / ".test/rules"), description="Test"
                )
            ],
        )

        sync_service = SyncService(config, Path(self.temp_dir))

        # Measure sync time
        start_time = time.time()
        result = sync_service.sync_rules(rules)
        end_time = time.time()

        duration = end_time - start_time

        # Check for regression
        self.check_regression("sync_5_files", duration)

        # Verify functionality
        assert result.added == 5


class TestPerformanceUtilities:
    """Utilities for performance testing and benchmarking."""

    @staticmethod
    def create_performance_report(benchmark_results: dict) -> str:
        """Create a formatted performance report."""
        report = "# Performance Benchmark Report\n\n"
        report += f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        report += "## Benchmark Results\n\n"
        for operation, stats in benchmark_results.items():
            report += f"### {operation}\n"
            report += f"- Mean: {stats['mean']:.3f}s\n"
            report += f"- Min: {stats['min']:.3f}s\n"
            report += f"- Max: {stats['max']:.3f}s\n"
            report += f"- Std Dev: {stats['stddev']:.3f}s\n\n"

        return report

    @staticmethod
    def profile_operation(operation_func, *args, **kwargs):
        """Profile an operation and return timing statistics."""
        import cProfile
        import io
        import pstats

        profiler = cProfile.Profile()
        profiler.enable()

        start_time = time.time()
        result = operation_func(*args, **kwargs)
        end_time = time.time()

        profiler.disable()

        # Get profiling stats
        stats_stream = io.StringIO()
        ps = pstats.Stats(profiler, stream=stats_stream)
        ps.sort_stats("cumulative").print_stats(20)

        return {
            "result": result,
            "duration": end_time - start_time,
            "profile": stats_stream.getvalue(),
        }

    @staticmethod
    def memory_profile_operation(operation_func, *args, **kwargs):
        """Profile memory usage of an operation."""
        import tracemalloc

        tracemalloc.start()

        start_time = time.time()
        result = operation_func(*args, **kwargs)
        end_time = time.time()

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return {
            "result": result,
            "duration": end_time - start_time,
            "memory_current": current,
            "memory_peak": peak,
        }


if __name__ == "__main__":
    # Run benchmarks directly
    pytest.main(
        [
            __file__,
            "-v",
            "-m",
            "performance",
            "--benchmark-only",
            "--benchmark-sort=mean",
        ]
    )
