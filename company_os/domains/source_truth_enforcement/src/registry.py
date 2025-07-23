"""
Source Truth Enforcement Service - Registry Loader

This module handles loading and parsing the source truth registry file.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from .models import RegistryDefinition, RegistryConfig, Severity


class SourceTruthRegistry:
    """Loads and manages the source truth registry configuration."""

    def __init__(self, registry_path: Optional[Path] = None):
        """Initialize the registry loader.

        Args:
            registry_path: Path to the registry file. If None, uses default location.
        """
        if registry_path is None:
            registry_path = self._find_default_registry_path()

        self.registry_path = Path(registry_path)
        self.raw_data = self._load_registry()
        self.definitions = self._parse_definitions()
        self.global_config = self._parse_global_config()

    def _find_default_registry_path(self) -> Path:
        """Find the default registry path, handling both Bazel runfiles and normal execution."""
        # Try Bazel runfiles first
        import os
        runfiles_dir = os.environ.get('RUNFILES_DIR')
        if runfiles_dir:
            bazel_path = Path(runfiles_dir) / "_main" / "company_os" / "domains" / "source_truth_enforcement" / "data" / "source_truth_registry.yaml"
            if bazel_path.exists():
                return bazel_path

        # Try relative to current working directory (normal execution)
        cwd_path = Path.cwd() / "company_os" / "domains" / "source_truth_enforcement" / "data" / "source_truth_registry.yaml"
        if cwd_path.exists():
            return cwd_path

        # Try relative to this file (development)
        service_dir = Path(__file__).parent.parent
        file_relative_path = service_dir / "data" / "source_truth_registry.yaml"
        if file_relative_path.exists():
            return file_relative_path

        # Fallback - return the expected path even if it doesn't exist (will error in _load_registry)
        return service_dir / "data" / "source_truth_registry.yaml"

    def _load_registry(self) -> Dict[str, Any]:
        """Load the raw registry data from YAML file."""
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry file not found: {self.registry_path}")

        with open(self.registry_path, 'r') as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict):
            raise ValueError("Registry file must contain a YAML dictionary")

        return data

    def _parse_definitions(self) -> Dict[str, RegistryDefinition]:
        """Parse registry definitions into structured objects."""
        registry_section = self.raw_data.get("registry", {})
        definitions = {}

        for name, config in registry_section.items():
            try:
                # Ensure severity is valid
                if "severity" in config:
                    config["severity"] = Severity(config["severity"])

                definitions[name] = RegistryDefinition(**config)
            except Exception as e:
                raise ValueError(f"Invalid definition '{name}': {e}")

        return definitions

    def _parse_global_config(self) -> RegistryConfig:
        """Parse global configuration settings."""
        global_section = self.raw_data.get("global_config", {})
        return RegistryConfig(**global_section)

    def get_definition(self, name: str) -> Optional[RegistryDefinition]:
        """Get a specific definition by name."""
        return self.definitions.get(name)

    def list_definitions(self) -> Dict[str, RegistryDefinition]:
        """Get all registry definitions."""
        return self.definitions.copy()

    def get_definitions_by_type(self, definition_type: str) -> Dict[str, RegistryDefinition]:
        """Get definitions filtered by type."""
        return {
            name: defn for name, defn in self.definitions.items()
            if defn.type == definition_type
        }

    def get_definitions_by_severity(self, severity: Severity) -> Dict[str, RegistryDefinition]:
        """Get definitions filtered by severity."""
        return {
            name: defn for name, defn in self.definitions.items()
            if defn.severity == severity
        }

    def validate_registry(self) -> bool:
        """Validate the registry configuration."""
        try:
            # Check required top-level sections
            required_sections = ["version", "registry"]
            for section in required_sections:
                if section not in self.raw_data:
                    raise ValueError(f"Missing required section: {section}")

            # Validate version
            version = self.raw_data.get("version")
            if not isinstance(version, str):
                raise ValueError("Version must be a string")

            # Validate all definitions parsed successfully
            if not self.definitions:
                raise ValueError("No valid definitions found in registry")

            return True

        except Exception as e:
            raise ValueError(f"Registry validation failed: {e}")

    def get_source_value(self, definition_name: str) -> Optional[str]:
        """Get the source of truth value for a definition."""
        definition = self.get_definition(definition_name)
        if not definition or not definition.source:
            return None

        source_path = Path(definition.source)
        if not source_path.is_absolute():
            # Make relative to repository root
            repo_root = self.registry_path.parent.parent.parent.parent
            source_path = repo_root / source_path

        if not source_path.exists():
            return None

        try:
            with open(source_path, 'r') as f:
                return f.read().strip()
        except Exception:
            return None

    def reload(self) -> None:
        """Reload the registry from disk."""
        self.raw_data = self._load_registry()
        self.definitions = self._parse_definitions()
        self.global_config = self._parse_global_config()
