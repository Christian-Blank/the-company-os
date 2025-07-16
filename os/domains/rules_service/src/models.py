from pydantic import Field
from typing import Optional, List
from enum import Enum
from pathlib import Path
import sys
from company_os_core.models import BaseDocument

class EnforcementLevel(str, Enum):
    STRICT = "strict"
    ADVISORY = "advisory"
    DEPRECATED = "deprecated"

class RuleDocument(BaseDocument):
    """Model for .rules.md documents"""
    rule_set_version: Optional[str] = None
    enforcement_level: EnforcementLevel = EnforcementLevel.STRICT
    applies_to: List[str] = Field(default_factory=list)
    parent_charter: str  # Required for rules
    file_path: Optional[str] = None  # Path to the source file
    
    @property
    def rule_category(self) -> str:
        """Extract rule category from filename"""
        if self.parent_charter:
            return Path(self.parent_charter).stem.replace('.charter', '')
        return "uncategorized"