"""Tests for the Rules Service CLI commands."""

import tempfile
import pytest
import yaml
from pathlib import Path
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock

from company_os.domains.rules_service.adapters.cli.__main__ import app
from company_os.domains.rules_service.src.models import RuleDocument, EnforcementLevel
from company_os.domains.rules_service.src.validation import ValidationResult, ValidationIssue

# Test runner
runner = CliRunner()


class TestMainCLI:
    """Test main CLI application."""
    
    def test_help_command(self):
        """Test main help command."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Company OS Rules Service CLI" in result.stdout
        assert "rules" in result.stdout
        assert "validate" in result.stdout
        assert "version" in result.stdout
    
    def test_version_command(self):
        """Test version command."""
        result = runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "Rules Service v0.1.0" in result.stdout


class TestRulesCommands:
    """Test rules command group."""
    
    def test_rules_help(self):
        """Test rules help command."""
        result = runner.invoke(app, ["rules", "--help"])
        assert result.exit_code == 0
        assert "Rules Service commands" in result.stdout
        assert "init" in result.stdout
        assert "sync" in result.stdout
        assert "query" in result.stdout
    
    def test_rules_init_creates_config(self):
        """Test rules init creates configuration file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / "test-config.yaml"
            
            result = runner.invoke(app, [
                "rules", "init", 
                "--config", str(config_path)
            ])
            
            assert result.exit_code == 0
            assert config_path.exists()
            assert "Configuration initialized" in result.stdout
            
            # Verify config content
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            assert config["version"] == "1.0"
            assert "rules_service" in config
            assert "agent_folders" in config["rules_service"]
            assert len(config["rules_service"]["agent_folders"]) == 4
    
    def test_rules_init_overwrite_prompt(self):
        """Test rules init overwrite prompt."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / "existing-config.yaml"
            
            # Create existing config
            config_path.write_text("existing: config")
            
            # Test declining overwrite
            result = runner.invoke(app, [
                "rules", "init", 
                "--config", str(config_path)
            ], input="n\n")
            
            assert result.exit_code == 0
            assert "Configuration file already exists" in result.stdout
            assert "Initialization cancelled" in result.stdout
            assert config_path.read_text() == "existing: config"
    
    def test_rules_init_overwrite_accept(self):
        """Test rules init overwrite accepted."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / "existing-config.yaml"
            
            # Create existing config
            config_path.write_text("existing: config")
            
            # Test accepting overwrite
            result = runner.invoke(app, [
                "rules", "init", 
                "--config", str(config_path)
            ], input="y\n")
            
            assert result.exit_code == 0
            assert "Configuration initialized" in result.stdout
            
            # Verify config was overwritten
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            assert config["version"] == "1.0"
    
    @patch('company_os.domains.rules_service.adapters.cli.commands.rules.SyncService')
    def test_rules_sync_default_config(self, mock_sync_service):
        """Test rules sync with default configuration."""
        mock_sync_instance = MagicMock()
        mock_sync_service.return_value = mock_sync_instance
        
        # Mock sync result
        mock_result = MagicMock()
        mock_result.files_added = 5
        mock_result.files_updated = 2
        mock_result.files_deleted = 1
        mock_result.files_skipped = 0
        mock_sync_instance.sync_rules.return_value = mock_result
        
        result = runner.invoke(app, ["rules", "sync"])
        
        assert result.exit_code == 0
        assert "Starting rules synchronization" in result.stdout
        assert "Added: 5 files" in result.stdout
        assert "Updated: 2 files" in result.stdout
        assert "Deleted: 1 files" in result.stdout
        assert "Synchronization complete: 8 operations" in result.stdout
        
        mock_sync_instance.sync_rules.assert_called_once_with(dry_run=False)
    
    @patch('company_os.domains.rules_service.adapters.cli.commands.rules.SyncService')
    def test_rules_sync_dry_run(self, mock_sync_service):
        """Test rules sync with dry run."""
        mock_sync_instance = MagicMock()
        mock_sync_service.return_value = mock_sync_instance
        
        # Mock sync result
        mock_result = MagicMock()
        mock_result.files_added = 3
        mock_result.files_updated = 0
        mock_result.files_deleted = 0
        mock_result.files_skipped = 0
        mock_sync_instance.sync_rules.return_value = mock_result
        
        result = runner.invoke(app, ["rules", "sync", "--dry-run"])
        
        assert result.exit_code == 0
        assert "DRY RUN MODE - No files will be modified" in result.stdout
        assert "Added: 3 files" in result.stdout
        
        mock_sync_instance.sync_rules.assert_called_once_with(dry_run=True)
    
    @patch('company_os.domains.rules_service.adapters.cli.commands.rules.SyncService')
    def test_rules_sync_no_changes(self, mock_sync_service):
        """Test rules sync when no changes needed."""
        mock_sync_instance = MagicMock()
        mock_sync_service.return_value = mock_sync_instance
        
        # Mock sync result with no changes
        mock_result = MagicMock()
        mock_result.files_added = 0
        mock_result.files_updated = 0
        mock_result.files_deleted = 0
        mock_result.files_skipped = 0
        mock_sync_instance.sync_rules.return_value = mock_result
        
        result = runner.invoke(app, ["rules", "sync"])
        
        assert result.exit_code == 0
        assert "All rules are up to date" in result.stdout
    
    @patch('company_os.domains.rules_service.adapters.cli.commands.rules.RuleDiscoveryService')
    def test_rules_query_all_rules(self, mock_discovery_service):
        """Test rules query without filters."""
        mock_discovery_instance = MagicMock()
        mock_discovery_service.return_value = mock_discovery_instance
        
        # Mock rules
        mock_rules = [
            RuleDocument(
                title="Test Rule 1",
                version="1.0",
                status="active",
                owner="test",
                last_updated="2025-01-01T00:00:00Z",
                parent_charter="test.charter.md",
                tags=["validation", "test"],
                enforcement_level=EnforcementLevel.STRICT,
                applies_to=[".md"]
            ),
            RuleDocument(
                title="Test Rule 2",
                version="1.0",
                status="active",
                owner="test",
                last_updated="2025-01-01T00:00:00Z",
                parent_charter="another.charter.md",
                tags=["sync"],
                enforcement_level=EnforcementLevel.ADVISORY,
                applies_to=[".decision.md"]
            )
        ]
        mock_discovery_instance.discover_rules.return_value = mock_rules
        
        result = runner.invoke(app, ["rules", "query"])
        
        assert result.exit_code == 0
        assert "Rules Query Results (2 found)" in result.stdout
        assert "Test Rule 1" in result.stdout
        assert "Test Rule 2" in result.stdout
        assert "strict" in result.stdout
        assert "advisory" in result.stdout
    
    @patch('company_os.domains.rules_service.adapters.cli.commands.rules.RuleDiscoveryService')
    def test_rules_query_with_filters(self, mock_discovery_service):
        """Test rules query with filters."""
        mock_discovery_instance = MagicMock()
        mock_discovery_service.return_value = mock_discovery_instance
        
        # Mock rules (one will be filtered out)
        mock_rules = [
            RuleDocument(
                title="Validation Rule",
                version="1.0",
                status="active",
                owner="test",
                last_updated="2025-01-01T00:00:00Z",
                parent_charter="test.charter.md",
                tags=["validation"],
                enforcement_level=EnforcementLevel.STRICT,
                applies_to=[".md"]
            )
        ]
        mock_discovery_instance.discover_rules.return_value = mock_rules
        
        result = runner.invoke(app, [
            "rules", "query", 
            "--tag", "validation",
            "--enforcement", "strict",
            "--limit", "10"
        ])
        
        assert result.exit_code == 0
        assert "Rules Query Results (1 found)" in result.stdout
        assert "Validation Rule" in result.stdout
    
    @patch('company_os.domains.rules_service.adapters.cli.commands.rules.RuleDiscoveryService')
    def test_rules_query_no_results(self, mock_discovery_service):
        """Test rules query with no matching results."""
        mock_discovery_instance = MagicMock()
        mock_discovery_service.return_value = mock_discovery_instance
        
        # Mock empty results
        mock_discovery_instance.discover_rules.return_value = []
        
        result = runner.invoke(app, ["rules", "query", "--tag", "nonexistent"])
        
        assert result.exit_code == 0
        assert "No rules found matching the criteria" in result.stdout
    
    @patch('company_os.domains.rules_service.adapters.cli.commands.rules.SyncService')
    def test_rules_sync_error_handling(self, mock_sync_service):
        """Test rules sync error handling."""
        mock_sync_service.side_effect = Exception("Sync failed")
        
        result = runner.invoke(app, ["rules", "sync"])
        
        assert result.exit_code == 1
        assert "Synchronization failed: Sync failed" in result.stdout
    
    @patch('company_os.domains.rules_service.adapters.cli.commands.rules.RuleDiscoveryService')
    def test_rules_query_error_handling(self, mock_discovery_service):
        """Test rules query error handling."""
        mock_discovery_service.side_effect = Exception("Query failed")
        
        result = runner.invoke(app, ["rules", "query"])
        
        assert result.exit_code == 1
        assert "Query failed: Query failed" in result.stdout


class TestValidateCommands:
    """Test validate command group."""
    
    def test_validate_help(self):
        """Test validate help command."""
        result = runner.invoke(app, ["validate", "--help"])
        assert result.exit_code == 0
        assert "Document validation commands" in result.stdout
        assert "validate" in result.stdout
    
    def test_validate_command_help(self):
        """Test validate validate command help."""
        result = runner.invoke(app, ["validate", "validate", "--help"])
        assert result.exit_code == 0
        assert "Validate markdown files against rules" in result.stdout
        assert "--auto-fix" in result.stdout
        assert "--format" in result.stdout
        assert "--verbose" in result.stdout
    
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.RuleDiscoveryService')
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.ValidationService')
    def test_validate_single_file_success(self, mock_validation_service, mock_discovery_service):
        """Test validating a single file successfully."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file = Path(tmp_dir) / "test.md"
            test_file.write_text("# Test Document\n\nThis is a test.")
            
            # Mock services
            mock_discovery_instance = MagicMock()
            mock_discovery_service.return_value = mock_discovery_instance
            mock_discovery_instance.discover_rules.return_value = []
            
            mock_validation_instance = MagicMock()
            mock_validation_service.return_value = mock_validation_instance
            
            # Mock validation result - no issues
            mock_result = ValidationResult(
                file_path=test_file,
                issues=[],
                auto_fixes=[]
            )
            mock_validation_instance.validate_document.return_value = mock_result
            
            result = runner.invoke(app, ["validate", "validate", str(test_file)])
            
            assert result.exit_code == 0
            assert "Validating 1 files" in result.stdout
            assert "All files passed validation" in result.stdout
    
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.RuleDiscoveryService')
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.ValidationService')
    def test_validate_with_warnings(self, mock_validation_service, mock_discovery_service):
        """Test validation with warnings."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file = Path(tmp_dir) / "test.md"
            test_file.write_text("# Test Document\n\nThis is a test.")
            
            # Mock services
            mock_discovery_instance = MagicMock()
            mock_discovery_service.return_value = mock_discovery_instance
            mock_discovery_instance.discover_rules.return_value = []
            
            mock_validation_instance = MagicMock()
            mock_validation_service.return_value = mock_validation_instance
            
            # Mock validation result with warnings
            mock_result = ValidationResult(
                file_path=test_file,
                issues=[
                    ValidationIssue(
                        line_number=1,
                        rule_id="test-rule",
                        severity="warning",
                        message="Test warning"
                    )
                ],
                auto_fixes=[]
            )
            mock_validation_instance.validate_document.return_value = mock_result
            
            result = runner.invoke(app, ["validate", "validate", str(test_file)])
            
            assert result.exit_code == 1  # Exit code 1 for warnings
            assert "Found 1 validation issues" in result.stdout
            assert "1 warnings" in result.stdout
    
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.RuleDiscoveryService')
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.ValidationService')
    def test_validate_with_errors(self, mock_validation_service, mock_discovery_service):
        """Test validation with errors."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file = Path(tmp_dir) / "test.md"
            test_file.write_text("# Test Document\n\nThis is a test.")
            
            # Mock services
            mock_discovery_instance = MagicMock()
            mock_discovery_service.return_value = mock_discovery_instance
            mock_discovery_instance.discover_rules.return_value = []
            
            mock_validation_instance = MagicMock()
            mock_validation_service.return_value = mock_validation_instance
            
            # Mock validation result with errors
            mock_result = ValidationResult(
                file_path=test_file,
                issues=[
                    ValidationIssue(
                        line_number=1,
                        rule_id="test-rule",
                        severity="error",
                        message="Test error"
                    )
                ],
                auto_fixes=[]
            )
            mock_validation_instance.validate_document.return_value = mock_result
            
            result = runner.invoke(app, ["validate", "validate", str(test_file)])
            
            assert result.exit_code == 2  # Exit code 2 for errors
            assert "Found 1 validation issues" in result.stdout
            assert "1 errors" in result.stdout
    
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.RuleDiscoveryService')
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.ValidationService')
    def test_validate_with_auto_fix(self, mock_validation_service, mock_discovery_service):
        """Test validation with auto-fix enabled."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file = Path(tmp_dir) / "test.md"
            test_file.write_text("# Test Document\n\nThis is a test.")
            
            # Mock services
            mock_discovery_instance = MagicMock()
            mock_discovery_service.return_value = mock_discovery_instance
            mock_discovery_instance.discover_rules.return_value = []
            
            mock_validation_instance = MagicMock()
            mock_validation_service.return_value = mock_validation_instance
            
            # Mock auto-fix
            mock_fix = MagicMock()
            mock_fix.apply.return_value = "# Test Document\n\nThis is a fixed test."
            
            mock_result = ValidationResult(
                file_path=test_file,
                issues=[],
                auto_fixes=[mock_fix]
            )
            mock_validation_instance.validate_document.return_value = mock_result
            
            result = runner.invoke(app, ["validate", "validate", str(test_file), "--auto-fix"])
            
            assert result.exit_code == 0
            assert "Applied 1 automatic fixes" in result.stdout
    
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.RuleDiscoveryService')
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.ValidationService')
    def test_validate_json_format(self, mock_validation_service, mock_discovery_service):
        """Test validation with JSON output format."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file = Path(tmp_dir) / "test.md"
            test_file.write_text("# Test Document\n\nThis is a test.")
            
            # Mock services
            mock_discovery_instance = MagicMock()
            mock_discovery_service.return_value = mock_discovery_instance
            mock_discovery_instance.discover_rules.return_value = []
            
            mock_validation_instance = MagicMock()
            mock_validation_service.return_value = mock_validation_instance
            
            mock_result = ValidationResult(
                file_path=test_file,
                issues=[],
                auto_fixes=[]
            )
            mock_validation_instance.validate_document.return_value = mock_result
            
            result = runner.invoke(app, [
                "validate", "validate", str(test_file), "--format", "json"
            ])
            
            assert result.exit_code == 0
            assert "{" in result.stdout  # JSON output
            assert "issues" in result.stdout
    
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.RuleDiscoveryService')
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.ValidationService')
    def test_validate_summary_format(self, mock_validation_service, mock_discovery_service):
        """Test validation with summary output format."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file = Path(tmp_dir) / "test.md"
            test_file.write_text("# Test Document\n\nThis is a test.")
            
            # Mock services
            mock_discovery_instance = MagicMock()
            mock_discovery_service.return_value = mock_discovery_instance
            mock_discovery_instance.discover_rules.return_value = []
            
            mock_validation_instance = MagicMock()
            mock_validation_service.return_value = mock_validation_instance
            
            mock_result = ValidationResult(
                file_path=test_file,
                issues=[],
                auto_fixes=[]
            )
            mock_validation_instance.validate_document.return_value = mock_result
            
            result = runner.invoke(app, [
                "validate", "validate", str(test_file), "--format", "summary"
            ])
            
            assert result.exit_code == 0
            assert "Validation Summary" in result.stdout
            assert "Total files: 1" in result.stdout
            assert "Valid files: 1" in result.stdout
    
    def test_validate_nonexistent_file(self):
        """Test validation of nonexistent file."""
        result = runner.invoke(app, ["validate", "validate", "nonexistent.md"])
        
        assert result.exit_code == 1
        assert "File not found: nonexistent.md" in result.stdout
    
    def test_validate_no_files(self):
        """Test validation with no files provided."""
        result = runner.invoke(app, ["validate", "validate"])
        
        assert result.exit_code == 2  # Missing required argument
        assert "Missing argument" in result.stdout
    
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.RuleDiscoveryService')
    def test_validate_discovery_error(self, mock_discovery_service):
        """Test validation with discovery service error."""
        mock_discovery_service.side_effect = Exception("Discovery failed")
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file = Path(tmp_dir) / "test.md"
            test_file.write_text("# Test Document\n\nThis is a test.")
            
            result = runner.invoke(app, ["validate", "validate", str(test_file)])
            
            assert result.exit_code == 3  # General error
            assert "Validation failed: Discovery failed" in result.stdout
    
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.RuleDiscoveryService')
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.ValidationService')
    def test_validate_no_exit_on_error(self, mock_validation_service, mock_discovery_service):
        """Test validation with --no-exit-on-error option."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file = Path(tmp_dir) / "test.md"
            test_file.write_text("# Test Document\n\nThis is a test.")
            
            # Mock services
            mock_discovery_instance = MagicMock()
            mock_discovery_service.return_value = mock_discovery_instance
            mock_discovery_instance.discover_rules.return_value = []
            
            mock_validation_instance = MagicMock()
            mock_validation_service.return_value = mock_validation_instance
            
            # Mock validation result with errors
            mock_result = ValidationResult(
                file_path=test_file,
                issues=[
                    ValidationIssue(
                        line_number=1,
                        rule_id="test-rule",
                        severity="error",
                        message="Test error"
                    )
                ],
                auto_fixes=[]
            )
            mock_validation_instance.validate_document.return_value = mock_result
            
            result = runner.invoke(app, [
                "validate", "validate", str(test_file), "--no-exit-on-error"
            ])
            
            assert result.exit_code == 0  # Should not exit on error
            assert "Found 1 validation issues" in result.stdout
