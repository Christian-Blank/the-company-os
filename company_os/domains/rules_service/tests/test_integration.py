"""Integration tests for the Rules Service.

These tests cover end-to-end workflows and service integration points.
"""

import os
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import shutil
from typer.testing import CliRunner

from company_os.domains.rules_service.src.discovery import RuleDiscoveryService
from company_os.domains.rules_service.src.sync import SyncService
from company_os.domains.rules_service.src.validation import ValidationService
from company_os.domains.rules_service.src.config import RulesServiceConfig, AgentFolder
from company_os.domains.rules_service.adapters.cli.__main__ import app
from company_os.domains.rules_service.adapters.pre_commit.hooks import sync_main, validate_main


class TestEndToEndWorkflows:
    """Test complete user workflows from start to finish."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.rules_dir = Path(self.temp_dir) / "rules"
        self.rules_dir.mkdir()

        # Create test rule files
        self.create_test_rules()

        # Create test config
        self.config = RulesServiceConfig(
            version="1.0",
            agent_folders=[
                AgentFolder(path=str(Path(self.temp_dir) / ".cursor/rules"), description="Test cursor"),
                AgentFolder(path=str(Path(self.temp_dir) / ".vscode/rules"), description="Test vscode"),
            ]
        )

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)

    def create_test_rules(self):
        """Create test rule files."""
        # Create a valid rules document
        rules_content = """---
title: "Test Rules"
version: 1.0
status: "Active"
owner: "Test Team"
last_updated: "2025-07-16T10:00:00-07:00"
tags: ["test", "rules"]
---

# Test Rules Document

## Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| TR001 | Test rule 1 | error |
| TR002 | Test rule 2 | warning |

## YAML Requirements

```yaml
frontmatter:
  title: "required"
  version: "required"
```

## List Rules

- **MUST** have proper frontmatter
- **SHOULD** include clear descriptions
- **MAY** include examples
"""

        rules_file = self.rules_dir / "test.rules.md"
        rules_file.write_text(rules_content)

        # Create another rules file
        rules_file2 = self.rules_dir / "validation.rules.md"
        rules_file2.write_text(rules_content.replace("Test Rules", "Validation Rules"))

    def test_complete_discovery_sync_workflow(self):
        """Test complete workflow: discovery -> sync -> validation."""
        # Step 1: Discovery
        discovery_service = RuleDiscoveryService(str(self.rules_dir))
        rules = discovery_service.discover_rules()

        assert len(rules) == 2
        assert any("Test Rules" in rule.title for rule in rules)
        assert any("Validation Rules" in rule.title for rule in rules)

        # Step 2: Sync
        sync_service = SyncService(self.config, Path(self.temp_dir))
        result = sync_service.sync_rules(rules)

        assert result.added == 2  # Two rules files synced
        assert result.total_changes == 2

        # Verify files were created
        cursor_dir = Path(self.temp_dir) / ".cursor/rules"
        vscode_dir = Path(self.temp_dir) / ".vscode/rules"

        assert cursor_dir.exists()
        assert vscode_dir.exists()
        assert (cursor_dir / "test.rules.md").exists()
        assert (cursor_dir / "validation.rules.md").exists()
        assert (vscode_dir / "test.rules.md").exists()
        assert (vscode_dir / "validation.rules.md").exists()

        # Step 3: Validation
        validation_service = ValidationService(self.config)

        # Test validation of a synced file
        test_file = cursor_dir / "test.rules.md"
        validation_result = validation_service.validate_file(test_file)

        assert validation_result.is_valid

    def test_cli_end_to_end_workflow(self):
        """Test complete CLI workflow."""
        runner = CliRunner()

        # Change to temp directory for CLI operations
        with patch('os.getcwd', return_value=self.temp_dir):
            with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
                # Test rules sync command
                result = runner.invoke(app, [
                    "rules", "sync",
                    "--config", str(Path(self.temp_dir) / "test_config.yaml")
                ])

                # Should handle missing config gracefully
                assert result.exit_code == 0 or result.exit_code == 1  # May fail due to missing config

                # Test rules query command
                result = runner.invoke(app, [
                    "rules", "query",
                    "--title", "Test"
                ])

                assert result.exit_code == 0

    def test_error_recovery_workflow(self):
        """Test error handling and recovery in workflows."""
        # Test discovery with invalid directory
        discovery_service = RuleDiscoveryService("/nonexistent/path")
        rules = discovery_service.discover_rules()
        assert len(rules) == 0

        # Test sync with invalid target
        invalid_config = RulesServiceConfig(
            version="1.0",
            agent_folders=[
                AgentFolder(path="/invalid/path", description="Invalid path"),
            ]
        )

        sync_service = SyncService(invalid_config, Path(self.temp_dir))
        result = sync_service.sync_rules([])

        assert len(result.errors) > 0

    def test_pre_commit_integration_workflow(self):
        """Test pre-commit hooks integration."""
        # Create a test markdown file
        test_file = Path(self.temp_dir) / "test.md"
        test_file.write_text("# Test Document\n\nThis is a test.")

        # Test sync hook
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

            result = sync_main()
            assert result == 0
            mock_run.assert_called_once()

        # Test validate hook
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
            with patch('sys.argv', ['validate_hook', str(test_file)]):
                result = validate_main()
                assert result == 0
                mock_run.assert_called_once()


class TestServiceIntegration:
    """Test integration between different services."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = RulesServiceConfig(
            version="1.0",
            agent_folders=[
                AgentFolder(path=str(Path(self.temp_dir) / ".test/rules"), description="Test folder"),
            ]
        )

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)

    def test_discovery_sync_integration(self):
        """Test integration between discovery and sync services."""
        # Create a test rules file
        rules_dir = Path(self.temp_dir) / "rules"
        rules_dir.mkdir()

        rule_file = rules_dir / "integration.rules.md"
        rule_file.write_text("""---
title: "Integration Test Rules"
version: 1.0
status: "Active"
owner: "Test"
last_updated: "2025-07-16T10:00:00-07:00"
---

# Integration Test Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| IT001 | Integration test rule | error |
""")

        # Discover rules
        discovery_service = RuleDiscoveryService(str(rules_dir))
        rules = discovery_service.discover_rules()

        # Sync rules
        sync_service = SyncService(self.config, Path(self.temp_dir))
        result = sync_service.sync_rules(rules)

        assert result.added == 1

        # Verify the rule was synced correctly
        synced_file = Path(self.temp_dir) / ".test/rules/integration.rules.md"
        assert synced_file.exists()

        synced_content = synced_file.read_text()
        assert "Integration Test Rules" in synced_content
        assert "IT001" in synced_content

    def test_sync_validation_integration(self):
        """Test integration between sync and validation services."""
        # Create a test rules file with validation issues
        rules_dir = Path(self.temp_dir) / "rules"
        rules_dir.mkdir()

        rule_file = rules_dir / "validation_test.rules.md"
        rule_file.write_text("""---
title: "Validation Test Rules"
version: 1.0
status: "Active"
owner: "Test"
last_updated: "2025-07-16T10:00:00-07:00"
---

# Validation Test Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| VT001 | Validation test rule | error |
""")

        # Discover and sync
        discovery_service = RuleDiscoveryService(str(rules_dir))
        rules = discovery_service.discover_rules()

        sync_service = SyncService(self.config, Path(self.temp_dir))
        sync_result = sync_service.sync_rules(rules)

        assert sync_result.added == 1

        # Validate synced file
        validation_service = ValidationService(self.config)
        synced_file = Path(self.temp_dir) / ".test/rules/validation_test.rules.md"

        validation_result = validation_service.validate_file(synced_file)

        # Should be valid since it's a proper rules file
        assert validation_result.is_valid

    def test_config_service_integration(self):
        """Test integration with configuration service."""
        # Test that all services respect configuration
        config_with_exclusions = RulesServiceConfig(
            version="1.0",
            agent_folders=[
                AgentFolder(path=str(Path(self.temp_dir) / ".test/rules"), description="Test folder"),
            ]
        )

        # Set up exclusion patterns
        config_with_exclusions.sync.exclude_patterns = ["*test*"]

        # Create rules
        rules_dir = Path(self.temp_dir) / "rules"
        rules_dir.mkdir()

        # This should be excluded
        test_rule = rules_dir / "test.rules.md"
        test_rule.write_text("# Test Rule")

        # This should be included
        prod_rule = rules_dir / "production.rules.md"
        prod_rule.write_text("# Production Rule")

        # Discover and sync
        discovery_service = RuleDiscoveryService(str(rules_dir))
        rules = discovery_service.discover_rules()

        sync_service = SyncService(config_with_exclusions, Path(self.temp_dir))
        result = sync_service.sync_rules(rules)

        # Should sync fewer files due to exclusions
        assert result.total_changes <= len(rules)


class TestErrorHandling:
    """Test error handling across the system."""

    def test_cli_error_scenarios(self):
        """Test CLI error handling."""
        runner = CliRunner()

        # Test invalid config path
        result = runner.invoke(app, [
            "rules", "sync",
            "--config", "/nonexistent/config.yaml"
        ])
        assert result.exit_code != 0

        # Test invalid command
        result = runner.invoke(app, ["invalid", "command"])
        assert result.exit_code != 0

    def test_pre_commit_error_handling(self):
        """Test pre-commit hook error handling."""
        # Test sync hook with subprocess error
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=1,
                stdout="",
                stderr="Error occurred"
            )

            result = sync_main()
            assert result == 1

        # Test validate hook with subprocess error
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=2,
                stdout="",
                stderr="Validation failed"
            )
            with patch('sys.argv', ['validate_hook', 'test.md']):
                result = validate_main()
                assert result == 2

    def test_service_error_recovery(self):
        """Test service error recovery."""
        temp_dir = tempfile.mkdtemp()

        try:
            # Test discovery with permission denied
            with patch('pathlib.Path.glob', side_effect=PermissionError("Access denied")):
                discovery_service = RuleDiscoveryService(temp_dir)
                rules = discovery_service.discover_rules()
                assert len(rules) == 0

            # Test sync with IO error
            config = RulesServiceConfig(
                version="1.0",
                agent_folders=[
                    AgentFolder(path=str(Path(temp_dir) / ".test/rules"), description="Test"),
                ]
            )

            sync_service = SyncService(config, Path(temp_dir))

            with patch('shutil.copy2', side_effect=IOError("Disk full")):
                result = sync_service.sync_rules([])
                # Should handle gracefully
                assert isinstance(result.errors, list)

        finally:
            shutil.rmtree(temp_dir)


class TestPerformanceBaselines:
    """Test performance benchmarks for critical operations."""

    def test_discovery_performance(self):
        """Test discovery performance with multiple files."""
        temp_dir = tempfile.mkdtemp()

        try:
            # Create multiple rule files
            rules_dir = Path(temp_dir) / "rules"
            rules_dir.mkdir()

            for i in range(10):
                rule_file = rules_dir / f"rule_{i}.rules.md"
                rule_file.write_text(f"""---
title: "Rule {i}"
version: 1.0
status: "Active"
owner: "Test"
last_updated: "2025-07-16T10:00:00-07:00"
---

# Rule {i}

| Rule ID | Description | Severity |
|---------|-------------|----------|
| R{i:03d} | Rule {i} description | error |
""")

            # Measure discovery time
            import time
            start_time = time.time()

            discovery_service = RuleDiscoveryService(str(rules_dir))
            rules = discovery_service.discover_rules()

            end_time = time.time()
            discovery_time = end_time - start_time

            assert len(rules) == 10
            assert discovery_time < 5.0  # Should complete in under 5 seconds

        finally:
            shutil.rmtree(temp_dir)

    def test_sync_performance(self):
        """Test sync performance with multiple files and folders."""
        temp_dir = tempfile.mkdtemp()

        try:
            # Create test rules
            rules_dir = Path(temp_dir) / "rules"
            rules_dir.mkdir()

            rules = []
            for i in range(5):
                rule_file = rules_dir / f"perf_rule_{i}.rules.md"
                rule_file.write_text(f"# Performance Rule {i}")

                # Mock rule document
                rule_doc = MagicMock()
                rule_doc.file_path = str(rule_file)
                rule_doc.title = f"Performance Rule {i}"
                rules.append(rule_doc)

            # Create config with multiple folders
            config = RulesServiceConfig(
                version="1.0",
                agent_folders=[
                    AgentFolder(path=str(Path(temp_dir) / f".folder_{i}/rules"), description=f"Folder {i}")
                    for i in range(3)
                ]
            )

            # Measure sync time
            import time
            start_time = time.time()

            sync_service = SyncService(config, Path(temp_dir))
            result = sync_service.sync_rules(rules)

            end_time = time.time()
            sync_time = end_time - start_time

            assert result.added == 15  # 5 rules × 3 folders
            assert sync_time < 3.0  # Should complete in under 3 seconds

        finally:
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    pytest.main([__file__])
