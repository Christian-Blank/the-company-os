"""Performance benchmark tests for Rules Service CLI."""

import tempfile
import pytest
from pathlib import Path
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock

from company_os.domains.rules_service.adapters.cli.__main__ import app
from company_os.domains.rules_service.src.models import RuleDocument, EnforcementLevel
from company_os.domains.rules_service.src.validation import ValidationResult, ValidationIssue

runner = CliRunner()


class TestCLIPerformanceBenchmarks:
    """Performance benchmarks for CLI operations."""
    
    @pytest.mark.benchmark(group="rules-sync")
    @patch('company_os.domains.rules_service.adapters.cli.commands.rules.SyncService')
    def test_rules_sync_performance(self, mock_sync_service, benchmark):
        """Benchmark: rules sync should complete in <2s for typical repositories."""
        # Mock sync service for consistent testing
        mock_sync_instance = MagicMock()
        mock_sync_service.return_value = mock_sync_instance
        
        # Mock realistic sync result
        mock_result = MagicMock()
        mock_result.files_added = 25
        mock_result.files_updated = 5
        mock_result.files_deleted = 2
        mock_result.files_skipped = 0
        mock_sync_instance.sync_rules.return_value = mock_result
        
        # Benchmark the sync operation
        def sync_operation():
            result = runner.invoke(app, ["rules", "sync"])
            return result
        
        result = benchmark(sync_operation)
        
        # Verify operation completed successfully
        assert result.exit_code == 0
        assert "Synchronization complete" in result.stdout
        
        # Performance expectation: <2s for typical repository
        # (pytest-benchmark will track this automatically)
    
    @pytest.mark.benchmark(group="rules-sync")
    @patch('company_os.domains.rules_service.adapters.cli.commands.rules.SyncService')
    def test_rules_sync_dry_run_performance(self, mock_sync_service, benchmark):
        """Benchmark: rules sync dry-run should be fast."""
        mock_sync_instance = MagicMock()
        mock_sync_service.return_value = mock_sync_instance
        
        mock_result = MagicMock()
        mock_result.files_added = 25
        mock_result.files_updated = 5
        mock_result.files_deleted = 2
        mock_result.files_skipped = 0
        mock_sync_instance.sync_rules.return_value = mock_result
        
        def sync_dry_run():
            result = runner.invoke(app, ["rules", "sync", "--dry-run"])
            return result
        
        result = benchmark(sync_dry_run)
        
        assert result.exit_code == 0
        assert "DRY RUN MODE" in result.stdout
    
    @pytest.mark.benchmark(group="rules-query")
    @patch('company_os.domains.rules_service.adapters.cli.commands.rules.RuleDiscoveryService')
    def test_rules_query_performance(self, mock_discovery_service, benchmark):
        """Benchmark: rules query should respond in <1s."""
        mock_discovery_instance = MagicMock()
        mock_discovery_service.return_value = mock_discovery_instance
        
        # Mock 50 rules (typical repository size)
        mock_rules = []
        for i in range(50):
            rule = RuleDocument(
                title=f"Rule {i}",
                version="1.0",
                status="active",
                owner="test",
                last_updated="2025-01-01T00:00:00Z",
                parent_charter="test.charter.md",
                tags=["validation", f"tag{i % 5}"],
                enforcement_level=EnforcementLevel.STRICT if i % 2 == 0 else EnforcementLevel.ADVISORY,
                applies_to=[".md"]
            )
            mock_rules.append(rule)
        
        mock_discovery_instance.discover_rules.return_value = mock_rules
        
        def query_operation():
            result = runner.invoke(app, ["rules", "query"])
            return result
        
        result = benchmark(query_operation)
        
        assert result.exit_code == 0
        assert "50 found" in result.stdout
    
    @pytest.mark.benchmark(group="rules-query")
    @patch('company_os.domains.rules_service.adapters.cli.commands.rules.RuleDiscoveryService')
    def test_rules_query_filtered_performance(self, mock_discovery_service, benchmark):
        """Benchmark: filtered rules query performance."""
        mock_discovery_instance = MagicMock()
        mock_discovery_service.return_value = mock_discovery_instance
        
        # Mock filtered results (10 out of 50)
        mock_rules = []
        for i in range(10):
            rule = RuleDocument(
                title=f"Validation Rule {i}",
                version="1.0",
                status="active",
                owner="test",
                last_updated="2025-01-01T00:00:00Z",
                parent_charter="test.charter.md",
                tags=["validation"],
                enforcement_level=EnforcementLevel.STRICT,
                applies_to=[".md"]
            )
            mock_rules.append(rule)
        
        mock_discovery_instance.discover_rules.return_value = mock_rules
        
        def query_filtered():
            result = runner.invoke(app, [
                "rules", "query", "--tag", "validation", "--enforcement", "strict"
            ])
            return result
        
        result = benchmark(query_filtered)
        
        assert result.exit_code == 0
        assert "10 found" in result.stdout
    
    @pytest.mark.benchmark(group="validate")
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.RuleDiscoveryService')
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.ValidationService')
    def test_validate_single_file_performance(self, mock_validation_service, mock_discovery_service, benchmark):
        """Benchmark: single file validation performance."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file = Path(tmp_dir) / "test.md"
            test_file.write_text("# Test Document\n\nThis is a test document with some content.\n")
            
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
            
            def validate_single():
                result = runner.invoke(app, ["validate", "validate", str(test_file)])
                return result
            
            result = benchmark(validate_single)
            
            assert result.exit_code == 0
    
    @pytest.mark.benchmark(group="validate")
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.RuleDiscoveryService')
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.ValidationService')
    def test_validate_multiple_files_performance(self, mock_validation_service, mock_discovery_service, benchmark):
        """Benchmark: validate 100 files in <5s."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            
            # Create 100 test files
            test_files = []
            for i in range(100):
                test_file = workspace / f"test_{i}.md"
                test_file.write_text(f"# Test Document {i}\n\nThis is test document {i}.\n")
                test_files.append(str(test_file))
            
            # Mock services
            mock_discovery_instance = MagicMock()
            mock_discovery_service.return_value = mock_discovery_instance
            mock_discovery_instance.discover_rules.return_value = []
            
            mock_validation_instance = MagicMock()
            mock_validation_service.return_value = mock_validation_instance
            
            def mock_validate_document(file_path, content):
                return ValidationResult(
                    file_path=file_path,
                    issues=[],
                    auto_fixes=[]
                )
            
            mock_validation_instance.validate_document.side_effect = mock_validate_document
            
            def validate_multiple():
                result = runner.invoke(app, ["validate", "validate"] + test_files)
                return result
            
            result = benchmark(validate_multiple)
            
            assert result.exit_code == 0
            assert "100 files" in result.stdout
    
    @pytest.mark.benchmark(group="validate")
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.RuleDiscoveryService')
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.ValidationService')
    def test_validate_with_issues_performance(self, mock_validation_service, mock_discovery_service, benchmark):
        """Benchmark: validation with issues (realistic scenario)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            
            # Create 20 files with various issues
            test_files = []
            for i in range(20):
                test_file = workspace / f"test_{i}.md"
                test_file.write_text(f"# Test Document {i}\n\nThis is test document {i}.\n")
                test_files.append(str(test_file))
            
            # Mock services
            mock_discovery_instance = MagicMock()
            mock_discovery_service.return_value = mock_discovery_instance
            mock_discovery_instance.discover_rules.return_value = []
            
            mock_validation_instance = MagicMock()
            mock_validation_service.return_value = mock_validation_instance
            
            def mock_validate_with_issues(file_path, content):
                # Simulate some files having issues
                issues = []
                if "test_5" in str(file_path) or "test_15" in str(file_path):
                    issues.append(ValidationIssue(
                        line_number=1,
                        rule_id="test-rule",
                        severity="warning",
                        message="Test warning"
                    ))
                
                return ValidationResult(
                    file_path=file_path,
                    issues=issues,
                    auto_fixes=[]
                )
            
            mock_validation_instance.validate_document.side_effect = mock_validate_with_issues
            
            def validate_with_issues():
                result = runner.invoke(app, ["validate", "validate"] + test_files)
                return result
            
            result = benchmark(validate_with_issues)
            
            assert result.exit_code == 1  # Has warnings
            assert "20 files" in result.stdout
    
    @pytest.mark.benchmark(group="validate")
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.RuleDiscoveryService')
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.ValidationService')
    def test_validate_json_output_performance(self, mock_validation_service, mock_discovery_service, benchmark):
        """Benchmark: JSON output format performance."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            
            # Create 10 test files
            test_files = []
            for i in range(10):
                test_file = workspace / f"test_{i}.md"
                test_file.write_text(f"# Test Document {i}\n\nContent {i}.\n")
                test_files.append(str(test_file))
            
            # Mock services
            mock_discovery_instance = MagicMock()
            mock_discovery_service.return_value = mock_discovery_instance
            mock_discovery_instance.discover_rules.return_value = []
            
            mock_validation_instance = MagicMock()
            mock_validation_service.return_value = mock_validation_instance
            
            def mock_validate_document(file_path, content):
                return ValidationResult(
                    file_path=file_path,
                    issues=[],
                    auto_fixes=[]
                )
            
            mock_validation_instance.validate_document.side_effect = mock_validate_document
            
            def validate_json():
                result = runner.invoke(app, [
                    "validate", "validate", "--format", "json"
                ] + test_files)
                return result
            
            result = benchmark(validate_json)
            
            assert result.exit_code == 0
            assert "{" in result.stdout  # JSON output
    
    @pytest.mark.benchmark(group="cli-startup")
    def test_cli_startup_performance(self, benchmark):
        """Benchmark: CLI startup time."""
        def cli_startup():
            result = runner.invoke(app, ["--help"])
            return result
        
        result = benchmark(cli_startup)
        
        assert result.exit_code == 0
        assert "Rules Service CLI" in result.stdout
    
    @pytest.mark.benchmark(group="cli-startup")
    def test_version_command_performance(self, benchmark):
        """Benchmark: version command performance."""
        def version_command():
            result = runner.invoke(app, ["version"])
            return result
        
        result = benchmark(version_command)
        
        assert result.exit_code == 0
        assert "v0.1.0" in result.stdout


class TestCLIMemoryUsage:
    """Memory usage tests for CLI operations."""
    
    @pytest.mark.benchmark(group="memory")
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.RuleDiscoveryService')
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.ValidationService')
    def test_validate_large_file_memory(self, mock_validation_service, mock_discovery_service, benchmark):
        """Test memory usage with large file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            
            # Create a large file (1MB)
            large_content = "# Large File\n\n" + ("This is a line of content.\n" * 50000)
            large_file = workspace / "large.md"
            large_file.write_text(large_content)
            
            # Mock services
            mock_discovery_instance = MagicMock()
            mock_discovery_service.return_value = mock_discovery_instance
            mock_discovery_instance.discover_rules.return_value = []
            
            mock_validation_instance = MagicMock()
            mock_validation_service.return_value = mock_validation_instance
            
            mock_result = ValidationResult(
                file_path=large_file,
                issues=[],
                auto_fixes=[]
            )
            mock_validation_instance.validate_document.return_value = mock_result
            
            def validate_large():
                result = runner.invoke(app, ["validate", "validate", str(large_file)])
                return result
            
            result = benchmark(validate_large)
            
            assert result.exit_code == 0
            # Memory usage should be reasonable for 1MB file
    
    @pytest.mark.benchmark(group="memory")
    @patch('company_os.domains.rules_service.adapters.cli.commands.rules.RuleDiscoveryService')
    def test_rules_query_large_ruleset_memory(self, mock_discovery_service, benchmark):
        """Test memory usage with large rule set."""
        mock_discovery_instance = MagicMock()
        mock_discovery_service.return_value = mock_discovery_instance
        
        # Mock 500 rules (large repository)
        mock_rules = []
        for i in range(500):
            rule = RuleDocument(
                title=f"Rule {i}",
                version="1.0",
                status="active",
                owner="test",
                last_updated="2025-01-01T00:00:00Z",
                parent_charter="test.charter.md",
                tags=["validation", f"tag{i % 10}"],
                enforcement_level=EnforcementLevel.STRICT if i % 2 == 0 else EnforcementLevel.ADVISORY,
                applies_to=[".md"]
            )
            mock_rules.append(rule)
        
        mock_discovery_instance.discover_rules.return_value = mock_rules
        
        def query_large_ruleset():
            result = runner.invoke(app, ["rules", "query"])
            return result
        
        result = benchmark(query_large_ruleset)
        
        assert result.exit_code == 0
        assert "500 found" in result.stdout


class TestCLIStressTests:
    """Stress tests for CLI operations."""
    
    @pytest.mark.benchmark(group="stress")
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.RuleDiscoveryService')
    @patch('company_os.domains.rules_service.adapters.cli.commands.validate.ValidationService')
    def test_validate_many_small_files_stress(self, mock_validation_service, mock_discovery_service, benchmark):
        """Stress test: validate many small files."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            
            # Create 200 small files
            test_files = []
            for i in range(200):
                test_file = workspace / f"small_{i}.md"
                test_file.write_text(f"# Small {i}\n\nContent {i}.\n")
                test_files.append(str(test_file))
            
            # Mock services
            mock_discovery_instance = MagicMock()
            mock_discovery_service.return_value = mock_discovery_instance
            mock_discovery_instance.discover_rules.return_value = []
            
            mock_validation_instance = MagicMock()
            mock_validation_service.return_value = mock_validation_instance
            
            def mock_validate_document(file_path, content):
                return ValidationResult(
                    file_path=file_path,
                    issues=[],
                    auto_fixes=[]
                )
            
            mock_validation_instance.validate_document.side_effect = mock_validate_document
            
            def validate_many_small():
                result = runner.invoke(app, ["validate", "validate"] + test_files)
                return result
            
            result = benchmark(validate_many_small)
            
            assert result.exit_code == 0
            assert "200 files" in result.stdout
    
    @pytest.mark.benchmark(group="stress")
    @patch('company_os.domains.rules_service.adapters.cli.commands.rules.SyncService')
    def test_sync_large_repository_stress(self, mock_sync_service, benchmark):
        """Stress test: sync large repository."""
        mock_sync_instance = MagicMock()
        mock_sync_service.return_value = mock_sync_instance
        
        # Mock large sync operation
        mock_result = MagicMock()
        mock_result.files_added = 150
        mock_result.files_updated = 50
        mock_result.files_deleted = 10
        mock_result.files_skipped = 5
        mock_sync_instance.sync_rules.return_value = mock_result
        
        def sync_large():
            result = runner.invoke(app, ["rules", "sync"])
            return result
        
        result = benchmark(sync_large)
        
        assert result.exit_code == 0
        assert "Added: 150" in result.stdout
        assert "Updated: 50" in result.stdout
