"""Unit tests for configuration handling."""

import tempfile
from pathlib import Path
import pytest
import yaml

from company_os.domains.rules_service.src.config import (
    RulesServiceConfig, AgentFolder, PerformanceConfig, ConflictStrategy
)


class TestAgentFolder:
    """Test AgentFolder model."""
    
    def test_path_normalization(self):
        """Test that paths are normalized to end with slash."""
        folder1 = AgentFolder(path=".clinerules", description="Test", enabled=True)
        assert folder1.path == ".clinerules/"
        
        folder2 = AgentFolder(path=".clinerules/", description="Test", enabled=True)
        assert folder2.path == ".clinerules/"


class TestPerformanceConfig:
    """Test PerformanceConfig model."""
    
    def test_valid_checksum_algorithms(self):
        """Test valid checksum algorithms."""
        for algo in ["md5", "sha256", "sha512"]:
            config = PerformanceConfig(checksum_algorithm=algo)
            assert config.checksum_algorithm == algo
    
    def test_invalid_checksum_algorithm(self):
        """Test invalid checksum algorithm raises error."""
        with pytest.raises(ValueError, match="Algorithm must be one of"):
            PerformanceConfig(checksum_algorithm="invalid")


class TestRulesServiceConfig:
    """Test main configuration model."""
    
    @pytest.fixture
    def sample_config_dict(self):
        """Sample configuration dictionary."""
        return {
            "version": "1.0",
            "agent_folders": [
                {
                    "path": ".clinerules/",
                    "description": "CLI rules",
                    "enabled": True
                },
                {
                    "path": ".cursor/rules/",
                    "description": "Cursor rules",
                    "enabled": False
                }
            ],
            "sync": {
                "conflict_strategy": "skip",
                "include_patterns": ["*.rules.md", "*.rule.md"],
                "create_directories": False
            },
            "performance": {
                "max_parallel_operations": 20,
                "checksum_algorithm": "md5"
            }
        }
    
    def test_from_dict(self, sample_config_dict):
        """Test creating config from dictionary."""
        config = RulesServiceConfig(**sample_config_dict)
        
        assert config.version == "1.0"
        assert len(config.agent_folders) == 2
        assert config.agent_folders[0].path == ".clinerules/"
        assert config.sync.conflict_strategy == ConflictStrategy.SKIP
        assert config.performance.max_parallel_operations == 20
    
    def test_from_file(self, sample_config_dict):
        """Test loading config from YAML file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(sample_config_dict, f)
            temp_path = Path(f.name)
        
        try:
            config = RulesServiceConfig.from_file(temp_path)
            assert config.version == "1.0"
            assert len(config.agent_folders) == 2
        finally:
            temp_path.unlink()
    
    def test_from_file_not_found(self):
        """Test error when config file not found."""
        with pytest.raises(FileNotFoundError):
            RulesServiceConfig.from_file(Path("/nonexistent/config.yaml"))
    
    def test_from_file_invalid_yaml(self):
        """Test error with invalid YAML."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("invalid: yaml: content: [[[")
            temp_path = Path(f.name)
        
        try:
            with pytest.raises(ValueError, match="Invalid YAML"):
                RulesServiceConfig.from_file(temp_path)
        finally:
            temp_path.unlink()
    
    def test_get_enabled_folders(self, sample_config_dict):
        """Test getting only enabled folders."""
        config = RulesServiceConfig(**sample_config_dict)
        enabled = config.get_enabled_folders()
        
        assert len(enabled) == 1
        assert enabled[0].path == ".clinerules/"
    
    def test_merge_with_overrides(self, sample_config_dict):
        """Test merging with overrides."""
        config = RulesServiceConfig(**sample_config_dict)
        
        overrides = {
            "sync.conflict_strategy": "overwrite",
            "performance.max_parallel_operations": 50,
            "version": "2.0"
        }
        
        merged = config.merge_with_overrides(overrides)
        
        assert merged.version == "2.0"
        assert merged.sync.conflict_strategy == ConflictStrategy.OVERWRITE
        assert merged.performance.max_parallel_operations == 50
        # Original should be unchanged
        assert config.sync.conflict_strategy == ConflictStrategy.SKIP
    
    def test_default_values(self):
        """Test configuration with minimal required fields."""
        minimal_config = {
            "version": "1.0",
            "agent_folders": [
                {"path": ".test/", "description": "Test"}
            ]
        }
        
        config = RulesServiceConfig(**minimal_config)
        
        # Check defaults
        assert config.sync.conflict_strategy == ConflictStrategy.OVERWRITE
        assert config.sync.create_directories is True
        assert config.sync.clean_orphaned is True
        assert config.performance.use_checksums is True
        assert config.performance.checksum_algorithm == "sha256"