"""Integration tests for the Rules Service sync functionality."""

import tempfile
from pathlib import Path
import pytest
import yaml

from company_os.domains.rules_service.src.sync import SyncService
from company_os.domains.rules_service.src.config import RulesServiceConfig
from company_os.domains.rules_service.src.discovery import RuleDiscoveryService


class TestSyncIntegration:
    """Integration tests for the complete sync workflow."""

    @pytest.fixture
    def workspace(self):
        """Create a complete test workspace with rules and config."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace_path = Path(tmp_dir)

            # Create directory structure
            rules_dir = workspace_path / "os/domains/rules/data"
            rules_dir.mkdir(parents=True)

            # Create sample rule files with proper frontmatter
            rule1_content = """---
title: "Test Rule 1"
version: 1.0
status: "active"
owner: "test"
last_updated: "2025-01-01T00:00:00Z"
parent_charter: "test.charter.md"
tags: ["test", "validation"]
---

# Test Rule 1

This is a test rule for validation.
"""
            (rules_dir / "test.rules.md").write_text(rule1_content)

            rule2_content = """---
title: "Another Rule"
version: 1.0
status: "active"
owner: "test"
last_updated: "2025-01-01T00:00:00Z"
parent_charter: "another.charter.md"
tags: ["test", "sync"]
---

# Another Rule

This rule tests synchronization.
"""
            (rules_dir / "another.rules.md").write_text(rule2_content)

            draft_rule_content = """---
title: "Draft Rule"
version: 0.1
status: "draft"
owner: "test"
last_updated: "2025-01-01T00:00:00Z"
parent_charter: "test.charter.md"
tags: ["draft"]
---

# Draft Rule

This is a draft rule that should be excluded.
"""
            (rules_dir / "draft-example.rules.md").write_text(draft_rule_content)

            # Create configuration file
            config_data = {
                "version": "1.0",
                "agent_folders": [
                    {
                        "path": ".clinerules/",
                        "description": "CLI agent rules",
                        "enabled": True
                    },
                    {
                        "path": ".cursor/rules/",
                        "description": "Cursor IDE rules",
                        "enabled": True
                    },
                    {
                        "path": ".vscode/rules/",
                        "description": "VSCode rules",
                        "enabled": False
                    }
                ],
                "sync": {
                    "conflict_strategy": "overwrite",
                    "include_patterns": ["*.rules.md"],
                    "exclude_patterns": ["*draft*.rules.md"],
                    "create_directories": True,
                    "clean_orphaned": True
                },
                "performance": {
                    "max_parallel_operations": 5,
                    "use_checksums": True,
                    "checksum_algorithm": "sha256"
                }
            }

            config_path = workspace_path / "rules-service.config.yaml"
            with open(config_path, 'w') as f:
                yaml.dump(config_data, f)

            yield workspace_path

    def test_full_sync_workflow(self, workspace):
        """Test the complete discovery and sync workflow."""
        # Load configuration
        config = RulesServiceConfig.from_file(workspace / "rules-service.config.yaml")

        # Discover rules
        discovery = RuleDiscoveryService(workspace)
        rules, errors = discovery.discover_rules()

        assert len(errors) == 0
        assert len(rules) == 3  # Including draft

        # Initialize sync service
        sync_service = SyncService(config, workspace)

        # Perform initial sync
        result = sync_service.sync_rules(rules)

        # Verify results
        assert result.added == 4  # 2 non-draft rules * 2 enabled folders
        assert result.updated == 0
        assert result.deleted == 0
        assert result.errors == []

        # Verify files exist in target folders
        assert (workspace / ".clinerules/test.rules.md").exists()
        assert (workspace / ".clinerules/another.rules.md").exists()
        assert not (workspace / ".clinerules/draft-example.rules.md").exists()

        assert (workspace / ".cursor/rules/test.rules.md").exists()
        assert (workspace / ".cursor/rules/another.rules.md").exists()

        # VSCode folder should not exist (disabled)
        assert not (workspace / ".vscode/rules").exists()

    def test_sync_with_updates(self, workspace):
        """Test sync behavior when files are updated."""
        config = RulesServiceConfig.from_file(workspace / "rules-service.config.yaml")
        discovery = RuleDiscoveryService(workspace)
        sync_service = SyncService(config, workspace)

        # Initial sync
        rules, _ = discovery.discover_rules()
        result1 = sync_service.sync_rules(rules)
        assert result1.added == 4

        # Modify a source rule
        rule_path = workspace / "os/domains/rules/data/test.rules.md"
        content = rule_path.read_text()
        rule_path.write_text(content.replace("This is a test rule", "This is an updated test rule"))

        # Re-discover and sync
        rules, _ = discovery.discover_rules(refresh_cache=True)
        result2 = sync_service.sync_rules(rules)

        assert result2.added == 0
        assert result2.updated == 2  # Updated in 2 folders
        assert result2.skipped == 2  # Other rule unchanged

        # Verify update was applied
        synced_content = (workspace / ".clinerules/test.rules.md").read_text()
        assert "This is an updated test rule" in synced_content

    def test_sync_with_orphaned_files(self, workspace):
        """Test cleanup of orphaned files."""
        config = RulesServiceConfig.from_file(workspace / "rules-service.config.yaml")
        discovery = RuleDiscoveryService(workspace)
        sync_service = SyncService(config, workspace)

        # Create orphaned files manually
        (workspace / ".clinerules").mkdir(parents=True)
        orphan1 = workspace / ".clinerules/orphan.rules.md"
        orphan1.write_text("# Orphaned rule")

        (workspace / ".cursor/rules").mkdir(parents=True)
        orphan2 = workspace / ".cursor/rules/old.rules.md"
        orphan2.write_text("# Old rule")

        # Sync
        rules, _ = discovery.discover_rules()
        result = sync_service.sync_rules(rules)

        # Check orphans were deleted
        assert not orphan1.exists()
        assert not orphan2.exists()
        assert result.deleted == 2
        assert result.added == 4  # Normal files still added

    def test_sync_status_reporting(self, workspace):
        """Test sync status functionality."""
        config = RulesServiceConfig.from_file(workspace / "rules-service.config.yaml")
        discovery = RuleDiscoveryService(workspace)
        sync_service = SyncService(config, workspace)

        rules, _ = discovery.discover_rules()

        # Check status before sync
        status_before = sync_service.get_sync_status(rules)
        assert status_before[".clinerules/"]["sync_state"] == "not_initialized"
        assert status_before[".cursor/rules/"]["sync_state"] == "not_initialized"

        # Sync
        sync_service.sync_rules(rules)

        # Check status after sync
        status_after = sync_service.get_sync_status(rules)
        assert status_after[".clinerules/"]["sync_state"] == "in_sync"
        assert status_after[".clinerules/"]["rule_count"] == "2"
        assert status_after[".cursor/rules/"]["sync_state"] == "in_sync"
        assert status_after[".cursor/rules/"]["rule_count"] == "2"

    def test_tag_based_sync(self, workspace):
        """Test syncing only rules with specific tags."""
        config = RulesServiceConfig.from_file(workspace / "rules-service.config.yaml")
        discovery = RuleDiscoveryService(workspace)
        sync_service = SyncService(config, workspace)

        # Discover all rules
        rules, _ = discovery.discover_rules()

        # Filter by tag
        validation_rules = discovery.query_by_tags(["validation"])
        assert len(validation_rules) == 1

        # Sync only validation rules
        result = sync_service.sync_rules(validation_rules)
        assert result.added == 2  # 1 rule * 2 folders

        # Verify only validation rule was synced
        assert (workspace / ".clinerules/test.rules.md").exists()
        assert not (workspace / ".clinerules/another.rules.md").exists()

    def test_dry_run_mode(self, workspace):
        """Test dry run doesn't make changes."""
        config = RulesServiceConfig.from_file(workspace / "rules-service.config.yaml")
        discovery = RuleDiscoveryService(workspace)
        sync_service = SyncService(config, workspace)

        rules, _ = discovery.discover_rules()

        # Dry run
        result = sync_service.sync_rules(rules, dry_run=True)

        # Check result shows what would be done
        assert result.added == 4
        assert result.errors == []

        # But no actual files created
        assert not (workspace / ".clinerules").exists()
        assert not (workspace / ".cursor").exists()

    def test_config_overrides(self, workspace):
        """Test configuration override functionality."""
        config = RulesServiceConfig.from_file(workspace / "rules-service.config.yaml")

        # Apply overrides
        overrides = {
            "sync.conflict_strategy": "skip",
            "sync.clean_orphaned": False
        }

        overridden_config = config.merge_with_overrides(overrides)

        discovery = RuleDiscoveryService(workspace)
        sync_service = SyncService(overridden_config, workspace)

        # Create an orphaned file
        (workspace / ".clinerules").mkdir(parents=True)
        orphan = workspace / ".clinerules/orphan.rules.md"
        orphan.write_text("# Should not be deleted")

        # Sync with overridden config
        rules, _ = discovery.discover_rules()
        result = sync_service.sync_rules(rules)

        # Orphan should NOT be deleted (clean_orphaned=False)
        assert orphan.exists()
        assert result.deleted == 0
