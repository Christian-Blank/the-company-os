"""Performance benchmark tests for the Sync Service."""

import time
import tempfile
from pathlib import Path
import pytest

from company_os.domains.rules_service.src.sync import SyncService
from company_os.domains.rules_service.src.config import RulesServiceConfig, AgentFolder
from company_os.domains.rules_service.src.models import RuleDocument


class TestSyncPerformance:
    """Performance tests to verify sync completes in <2s."""

    @pytest.fixture
    def large_rule_set(self):
        """Create a large set of rule documents for performance testing."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            rules_dir = tmp_path / "rules"
            rules_dir.mkdir()

            # Create 50 rule files (typical large repository)
            rules = []
            for i in range(50):
                rule_file = rules_dir / f"rule-{i:03d}.rules.md"
                rule_file.write_text(f"# Rule {i}\n\nThis is rule number {i}." * 10)

                rules.append(RuleDocument(
                    title=f"Rule {i}",
                    version="1.0",
                    status="active",
                    owner="test",
                    last_updated="2025-01-01T00:00:00Z",
                    parent_charter="test.charter.md",
                    file_path=str(rule_file),
                    tags=["test", f"category-{i % 5}"]
                ))

            yield tmp_path, rules

    @pytest.fixture
    def performance_config(self):
        """Create a performance-oriented configuration."""
        return RulesServiceConfig(
            version="1.0",
            agent_folders=[
                AgentFolder(path=".clinerules/", description="CLI rules", enabled=True),
                AgentFolder(path=".cursor/rules/", description="Cursor rules", enabled=True),
                AgentFolder(path=".vscode/rules/", description="VSCode rules", enabled=True),
            ],
            sync={
                "conflict_strategy": "overwrite",
                "include_patterns": ["*.rules.md"],
                "exclude_patterns": [],
                "create_directories": True,
                "clean_orphaned": True,
            },
            performance={
                "max_parallel_operations": 10,
                "use_checksums": True,
                "checksum_algorithm": "sha256",
            }
        )

    def test_initial_sync_performance(self, large_rule_set, performance_config):
        """Test that initial sync completes in <2s for typical repository."""
        workspace, rules = large_rule_set
        sync_service = SyncService(performance_config, workspace)

        # Measure initial sync time
        start_time = time.time()
        result = sync_service.sync_rules(rules)
        end_time = time.time()

        sync_duration = end_time - start_time

        # Verify performance requirement
        assert sync_duration < 2.0, f"Initial sync took {sync_duration:.2f}s, expected <2s"

        # Verify correctness
        assert result.errors == []
        assert result.added == 150  # 50 rules * 3 folders
        assert result.updated == 0
        assert result.deleted == 0

        print(f"Initial sync performance: {sync_duration:.3f}s for {len(rules)} rules")

    def test_incremental_sync_performance(self, large_rule_set, performance_config):
        """Test that incremental sync is fast (<0.5s) when few files change."""
        workspace, rules = large_rule_set
        sync_service = SyncService(performance_config, workspace)

        # Initial sync
        sync_service.sync_rules(rules)

        # Modify 5 rules (10% change)
        for i in range(5):
            rule_path = Path(rules[i].file_path)
            rule_path.write_text(f"# Modified Rule {i}\n\nThis rule was updated.")

        # Measure incremental sync time
        start_time = time.time()
        result = sync_service.sync_rules(rules)
        end_time = time.time()

        sync_duration = end_time - start_time

        # Incremental sync should be much faster
        assert sync_duration < 0.5, f"Incremental sync took {sync_duration:.2f}s, expected <0.5s"

        # Verify only changed files were updated
        assert result.added == 0
        assert result.updated == 15  # 5 rules * 3 folders
        assert result.skipped == 135  # 45 unchanged rules * 3 folders

        print(f"Incremental sync performance: {sync_duration:.3f}s for 5 changed rules")

    def test_dry_run_performance(self, large_rule_set, performance_config):
        """Test that dry run is fast since it doesn't write files."""
        workspace, rules = large_rule_set
        sync_service = SyncService(performance_config, workspace)

        # Measure dry run time
        start_time = time.time()
        result = sync_service.sync_rules(rules, dry_run=True)
        end_time = time.time()

        sync_duration = end_time - start_time

        # Dry run should be very fast
        assert sync_duration < 0.5, f"Dry run took {sync_duration:.2f}s, expected <0.5s"

        # Verify no files were created
        assert not (workspace / ".clinerules").exists()
        assert result.added == 150  # Would add 50 rules * 3 folders

        print(f"Dry run performance: {sync_duration:.3f}s")

    def test_parallel_operations_scaling(self, large_rule_set, performance_config):
        """Test performance impact of parallel operations setting."""
        workspace, rules = large_rule_set

        results = {}

        for max_parallel in [1, 5, 10, 20]:
            # Update config
            performance_config.performance.max_parallel_operations = max_parallel
            sync_service = SyncService(performance_config, workspace)

            # Clean workspace
            for folder in [".clinerules", ".cursor", ".vscode"]:
                folder_path = workspace / folder
                if folder_path.exists():
                    import shutil
                    shutil.rmtree(folder_path)

            # Measure sync time
            start_time = time.time()
            sync_service.sync_rules(rules)
            end_time = time.time()

            duration = end_time - start_time
            results[max_parallel] = duration

            print(f"Parallel ops={max_parallel}: {duration:.3f}s")

        # Verify parallel operations improve performance
        assert results[10] < results[1], "Parallel operations should improve performance"
        assert results[10] < 2.0, "Even with parallel ops, should meet <2s requirement"

    @pytest.mark.skip(reason="Benchmark tests only run with --benchmark flag")
    def test_stress_performance(self, performance_config):
        """Stress test with very large rule set (200+ rules)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            rules_dir = tmp_path / "rules"
            rules_dir.mkdir()

            # Create 200 rule files
            rules = []
            for i in range(200):
                rule_file = rules_dir / f"stress-rule-{i:03d}.rules.md"
                rule_file.write_text(f"# Stress Test Rule {i}\n" * 50)

                rules.append(RuleDocument(
                    title=f"Stress Rule {i}",
                    version="1.0",
                    status="active",
                    owner="test",
                    last_updated="2025-01-01T00:00:00Z",
                    parent_charter="test.charter.md",
                    file_path=str(rule_file),
                    tags=["stress-test"]
                ))

            sync_service = SyncService(performance_config, tmp_path)

            start_time = time.time()
            result = sync_service.sync_rules(rules)
            end_time = time.time()

            sync_duration = end_time - start_time

            print(f"Stress test: {sync_duration:.3f}s for {len(rules)} rules")
            print(f"Rate: {len(rules) / sync_duration:.1f} rules/second")

            # Even with 200 rules, should complete reasonably fast
            assert sync_duration < 10.0, f"Stress test took too long: {sync_duration:.2f}s"
            assert result.errors == []
