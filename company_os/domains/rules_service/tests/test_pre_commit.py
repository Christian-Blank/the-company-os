"""
Tests for pre-commit hooks.
"""

import sys
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import subprocess
import time

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from company_os.domains.rules_service.adapters.pre_commit.hooks import sync_main, validate_main


class TestPreCommitHooks:
    """Test pre-commit hook implementations."""

    def test_sync_main_success(self):
        """Test successful sync hook execution."""
        with patch('company_os.domains.rules_service.adapters.pre_commit.hooks.sync') as mock_sync:
            # Configure mock to simulate successful sync
            mock_sync.return_value = None

            # Run sync hook
            exit_code = sync_main()

            # Assert success
            assert exit_code == 0
            mock_sync.assert_called_once()

    def test_sync_main_failure(self):
        """Test sync hook execution with error."""
        with patch('company_os.domains.rules_service.adapters.pre_commit.hooks.sync') as mock_sync:
            # Configure mock to raise exception
            mock_sync.side_effect = Exception("Sync failed")

            # Run sync hook
            exit_code = sync_main()

            # Assert failure
            assert exit_code == 1

    def test_validate_main_no_files(self):
        """Test validate hook with no files."""
        # Mock sys.argv to have no files
        with patch.object(sys, 'argv', ['validate_hook']):
            exit_code = validate_main()
            assert exit_code == 0

    def test_validate_main_no_markdown_files(self):
        """Test validate hook with non-markdown files."""
        # Mock sys.argv with non-markdown files
        with patch.object(sys, 'argv', ['validate_hook', 'file.txt', 'script.py']):
            exit_code = validate_main()
            assert exit_code == 0

    def test_validate_main_with_markdown_files(self):
        """Test validate hook with markdown files."""
        # Mock sys.argv with markdown files
        with patch.object(sys, 'argv', ['validate_hook', 'README.md', 'docs/guide.md']):
            with patch('company_os.domains.rules_service.adapters.pre_commit.hooks.validate_command') as mock_validate:
                # Mock SystemExit to simulate validate command exit
                mock_validate.side_effect = SystemExit(0)

                exit_code = validate_main()
                assert exit_code == 0

                # Verify validate was called with correct files
                called_files = mock_validate.call_args[1]['files']
                assert len(called_files) == 2
                assert Path('README.md') in called_files
                assert Path('docs/guide.md') in called_files
                assert mock_validate.call_args[1]['auto_fix'] is True

    def test_validate_main_with_warnings(self):
        """Test validate hook with warnings."""
        with patch.object(sys, 'argv', ['validate_hook', 'test.md']):
            with patch('company_os.domains.rules_service.adapters.pre_commit.hooks.validate_command') as mock_validate:
                # Mock SystemExit with warning code
                mock_validate.side_effect = SystemExit(1)

                exit_code = validate_main()
                assert exit_code == 1

    def test_validate_main_with_errors(self):
        """Test validate hook with errors."""
        with patch.object(sys, 'argv', ['validate_hook', 'test.md']):
            with patch('company_os.domains.rules_service.adapters.pre_commit.hooks.validate_command') as mock_validate:
                # Mock SystemExit with error code
                mock_validate.side_effect = SystemExit(2)

                exit_code = validate_main()
                assert exit_code == 2

    def test_validate_main_unexpected_error(self):
        """Test validate hook with unexpected error."""
        with patch.object(sys, 'argv', ['validate_hook', 'test.md']):
            with patch('company_os.domains.rules_service.adapters.pre_commit.hooks.validate_command') as mock_validate:
                # Mock unexpected exception
                mock_validate.side_effect = Exception("Unexpected error")

                exit_code = validate_main()
                assert exit_code == 3


class TestPreCommitPerformance:
    """Test performance requirements for pre-commit hooks."""

    def test_sync_hook_performance(self):
        """Test that sync hook completes within performance requirements."""
        with patch('company_os.domains.rules_service.adapters.pre_commit.hooks.sync') as mock_sync:
            # Configure mock to simulate quick sync
            mock_sync.return_value = None

            start_time = time.time()
            exit_code = sync_main()
            duration = time.time() - start_time

            assert exit_code == 0
            # Hook overhead should be minimal (well under 2s requirement)
            assert duration < 0.5

    def test_validate_hook_performance_no_files(self):
        """Test validate hook performance with no files."""
        with patch.object(sys, 'argv', ['validate_hook']):
            start_time = time.time()
            exit_code = validate_main()
            duration = time.time() - start_time

            assert exit_code == 0
            # Should exit immediately
            assert duration < 0.1

    def test_validate_hook_performance_with_files(self):
        """Test validate hook performance with files."""
        # Create list of 10 markdown files
        files = [f'file{i}.md' for i in range(10)]

        with patch.object(sys, 'argv', ['validate_hook'] + files):
            with patch('company_os.domains.rules_service.adapters.pre_commit.hooks.validate_command') as mock_validate:
                # Mock quick validation
                mock_validate.side_effect = SystemExit(0)

                start_time = time.time()
                exit_code = validate_main()
                duration = time.time() - start_time

                assert exit_code == 0
                # Hook overhead should be minimal
                assert duration < 0.5


class TestPreCommitIntegration:
    """Integration tests for pre-commit hooks."""

    @pytest.mark.integration
    def test_bazel_build_hooks(self):
        """Test that hook binaries can be built with Bazel."""
        # Build sync hook
        result = subprocess.run(
            ['bazel', 'build', '//company_os/domains/rules_service/adapters/pre_commit:rules_sync_hook'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Build failed: {result.stderr}"

        # Build validate hook
        result = subprocess.run(
            ['bazel', 'build', '//company_os/domains/rules_service/adapters/pre_commit:rules_validate_hook'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Build failed: {result.stderr}"

    @pytest.mark.integration
    def test_pre_commit_config_valid(self):
        """Test that .pre-commit-config.yaml is valid."""
        # This would require pre-commit to be installed
        # For now, just check the file exists
        config_path = Path('.pre-commit-config.yaml')
        assert config_path.exists()

        # Basic validation of content
        content = config_path.read_text()
        assert 'rules-sync' in content
        assert 'rules-validate' in content
        assert 'bazel run' in content


class TestMainScript:
    """Test the main script entry point logic."""

    def test_main_sync_detection(self):
        """Test that main detects sync command."""
        with patch.object(sys, 'argv', ['rules_sync_hook']):
            with patch('company_os.domains.rules_service.adapters.pre_commit.hooks.sync_main') as mock_sync:
                mock_sync.return_value = 0
                with pytest.raises(SystemExit) as exc_info:
                    import company_os.domains.rules_service.adapters.pre_commit.hooks
                    exec(open('company_os/domains/rules_service/adapters/pre_commit/hooks.py').read())

                assert exc_info.value.code == 0

    def test_main_validate_detection(self):
        """Test that main detects validate command."""
        with patch.object(sys, 'argv', ['rules_validate_hook']):
            with patch('company_os.domains.rules_service.adapters.pre_commit.hooks.validate_main') as mock_validate:
                mock_validate.return_value = 0
                with pytest.raises(SystemExit) as exc_info:
                    import company_os.domains.rules_service.adapters.pre_commit.hooks
                    exec(open('company_os/domains/rules_service/adapters/pre_commit/hooks.py').read())

                assert exc_info.value.code == 0
