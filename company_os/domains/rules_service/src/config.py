"""Configuration models and parser for the Rules Service."""

from typing import List, Dict, Any
from pathlib import Path
from pydantic import BaseModel, Field, field_validator
from enum import Enum
import yaml
from yaml import YAMLError


class ConflictStrategy(str, Enum):
    """Strategies for handling file conflicts during sync."""
    OVERWRITE = "overwrite"
    SKIP = "skip"
    ASK = "ask"


class AgentFolder(BaseModel):
    """Configuration for an agent-specific folder."""
    path: str
    description: str
    enabled: bool = True

    @field_validator('path')
    @classmethod
    def validate_path(cls, v: str) -> str:
        """Ensure path ends with a slash."""
        if not v.endswith('/'):
            v += '/'
        return v


class SyncConfig(BaseModel):
    """Sync operation configuration."""
    conflict_strategy: ConflictStrategy = ConflictStrategy.OVERWRITE
    include_patterns: List[str] = Field(default_factory=lambda: ["*.rules.md"])
    exclude_patterns: List[str] = Field(default_factory=list)
    create_directories: bool = True
    clean_orphaned: bool = True


class PerformanceConfig(BaseModel):
    """Performance-related configuration."""
    max_parallel_operations: int = 10
    use_checksums: bool = True
    checksum_algorithm: str = "sha256"

    @field_validator('checksum_algorithm')
    @classmethod
    def validate_algorithm(cls, v: str) -> str:
        """Validate checksum algorithm."""
        allowed = {"md5", "sha256", "sha512"}
        if v not in allowed:
            raise ValueError(f"Algorithm must be one of {allowed}")
        return v


class RulesServiceConfig(BaseModel):
    """Main configuration for the Rules Service."""
    version: str
    agent_folders: List[AgentFolder]
    sync: SyncConfig = Field(default_factory=SyncConfig)
    performance: PerformanceConfig = Field(default_factory=PerformanceConfig)

    @classmethod
    def from_file(cls, config_path: Path) -> "RulesServiceConfig":
        """Load configuration from a YAML file."""
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        try:
            with open(config_path, 'r') as f:
                data = yaml.safe_load(f)
                return cls(**data)
        except YAMLError as e:
            raise ValueError(f"Invalid YAML in configuration file: {e}")
        except Exception as e:
            raise ValueError(f"Error loading configuration: {e}")

    def get_enabled_folders(self) -> List[AgentFolder]:
        """Get only the enabled agent folders."""
        return [folder for folder in self.agent_folders if folder.enabled]

    def merge_with_overrides(self, overrides: Dict[str, Any]) -> "RulesServiceConfig":
        """Merge configuration with user-specific overrides."""
        # Deep copy current config as dict
        config_dict = self.model_dump()

        # Apply overrides (simple implementation - can be enhanced)
        for key, value in overrides.items():
            if '.' in key:
                # Handle nested keys like "sync.conflict_strategy"
                parts = key.split('.')
                current = config_dict
                for part in parts[:-1]:
                    current = current.setdefault(part, {})
                current[parts[-1]] = value
            else:
                config_dict[key] = value

        return RulesServiceConfig(**config_dict)
