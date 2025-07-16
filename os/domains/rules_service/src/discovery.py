from typing import List, Optional, Dict
from pathlib import Path
from models import RuleDocument
import glob
from ruamel.yaml import YAML
from pydantic import ValidationError

class FrontmatterParser:
    """Parses the YAML frontmatter from a markdown file."""

    def parse(self, file_path: Path) -> Optional[Dict]:
        """Extracts and parses the YAML frontmatter from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Simple check for frontmatter fences
                if not content.startswith(('---', '+++')):
                    return None

                parts = content.split('---' if content.startswith('---') else '+++')
                if len(parts) < 3:
                    return None

                frontmatter_str = parts[1]
                yaml = YAML(typ='safe', pure=True)
                return yaml.load(frontmatter_str)
        except (IOError, yaml.YAMLError) as e:
            print(f"Error parsing frontmatter for {file_path}: {e}")
            return None

import os

class RuleDiscoveryService:
    """Service for discovering and parsing rule files"""
    
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self._cache: Dict[Path, RuleDocument] = {}
        self.parser = FrontmatterParser()
    
    def discover_rules(self, refresh_cache: bool = False) -> List[RuleDocument]:
        """Discover all rule files in the repository"""
        if not refresh_cache and self._cache:
            return list(self._cache.values())

        self._cache.clear()
        
        for root, dirs, files in os.walk(self.root_path, topdown=True, followlinks=False):
            # Exclude hidden directories (like .git, .venv, etc.)
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.endswith('.rules.md'):
                    file_path = Path(root) / file
                    if file_path in self._cache and not refresh_cache:
                        continue

                    frontmatter = self.parser.parse(file_path)
                    if frontmatter:
                        if 'version' in frontmatter:
                            frontmatter['version'] = str(frontmatter['version'])
                        try:
                            rule_doc = RuleDocument(**frontmatter)
                            self._cache[file_path] = rule_doc
                        except ValidationError as e:
                            print(f"Validation error for {file_path}: {e}")
        
        return list(self._cache.values())
    
    def query_by_tags(self, tags: List[str], match_all: bool = True, sort_by: str = 'title', limit: Optional[int] = None, offset: int = 0) -> List[RuleDocument]:
        """Query rules by tags"""
        if not self._cache:
            self.discover_rules()

        results = []
        for doc in self._cache.values():
            doc_tags = set(doc.tags)
            query_tags = set(tags)
            if match_all and query_tags.issubset(doc_tags):
                results.append(doc)
            elif not match_all and not query_tags.isdisjoint(doc_tags):
                results.append(doc)
        
        # Sort results
        results.sort(key=lambda x: getattr(x, sort_by, ''))

        # Paginate results
        if limit is not None:
            return results[offset:offset + limit]
        return results
    
    def get_rule_by_path(self, path: Path) -> Optional[RuleDocument]:
        """Get a specific rule by file path"""
        if path in self._cache:
            return self._cache[path]
        
        frontmatter = self.parser.parse(path)
        if frontmatter:
            try:
                rule_doc = RuleDocument(**frontmatter)
                self._cache[path] = rule_doc
                return rule_doc
            except ValidationError as e:
                print(f"Validation error for {path}: {e}")
        return None
