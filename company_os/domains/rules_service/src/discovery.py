import os
from typing import List, Optional, Dict, Tuple
from pathlib import Path
from .models import RuleDocument
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError
from pydantic import ValidationError

class FrontmatterParser:
    """Parses the YAML frontmatter from a markdown file."""

    def parse(self, file_path: Path) -> Tuple[Optional[Dict], Optional[str]]:
        """Extracts and parses the YAML frontmatter from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Simple check for frontmatter fences
                if not content.startswith(('---', '+++')):
                    return None, None

                delimiter = '---' if content.startswith('---') else '+++'
                parts = content.split(delimiter)
                if len(parts) < 3:
                    return None, f"Invalid frontmatter structure in {file_path}"

                frontmatter_str = parts[1]
                yaml = YAML(typ='safe', pure=True)
                return yaml.load(frontmatter_str), None
        except (IOError, YAMLError) as e:
            return None, f"Error parsing frontmatter for {file_path}: {e}"


class RuleDiscoveryService:
    """Service for discovering and parsing rule files"""

    def __init__(self, root_path: Path):
        self.root_path = root_path
        self._cache: Dict[Path, RuleDocument] = {}
        self.parser = FrontmatterParser()

    def discover_rules(self, refresh_cache: bool = False) -> Tuple[List[RuleDocument], List[str]]:
        """
        Discovers all rule files (`.rules.md`) in the repository, parses their
        frontmatter, and returns a list of RuleDocument objects and a list of
        any errors encountered.

        Args:
            refresh_cache: If True, forces a re-scan of the repository and
                           updates the cache.

        Returns:
            A tuple containing a list of RuleDocument objects and a list of
            error messages.
        """
        if not refresh_cache and self._cache:
            return list(self._cache.values()), []

        self._cache.clear()
        errors = []

        for root, dirs, files in os.walk(self.root_path, topdown=True, followlinks=False):
            # Exclude hidden directories (like .git, .venv, etc.)
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for file in files:
                if file.endswith('.rules.md'):
                    file_path = Path(root) / file
                    if file_path in self._cache and not refresh_cache:
                        continue

                    frontmatter, error = self.parser.parse(file_path)

                    if error:
                        errors.append(error)
                        continue

                    if not frontmatter:
                        # This is not an error, just a file without frontmatter to parse.
                        continue

                    try:
                        if not isinstance(frontmatter, dict) or not all(isinstance(k, str) for k in frontmatter):
                            raise ValueError("Front-matter must be a mapping with string keys")
                        if 'version' in frontmatter:
                            frontmatter['version'] = str(frontmatter['version'])
                        # Add file_path to the frontmatter data
                        frontmatter['file_path'] = str(file_path)
                        rule_doc = RuleDocument(**frontmatter)
                        self._cache[file_path] = rule_doc
                    except (ValidationError, TypeError, ValueError) as e:
                        errors.append(f"Validation error for {file_path.name}: {e}")

        return list(self._cache.values()), errors

    def query_by_tags(self, tags: List[str], match_all: bool = True, sort_by: str = 'title', limit: Optional[int] = None, offset: int = 0) -> List[RuleDocument]:
        """
        Queries the cached rules by a list of tags.

        Args:
            tags: A list of tags to query for.
            match_all: If True, only returns documents that have all of the
                       specified tags. If False, returns documents that have
                       any of the specified tags.
            sort_by: The field to sort the results by.
            limit: The maximum number of results to return.
            offset: The number of results to skip.

        Returns:
            A list of RuleDocument objects that match the query.
        """
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
        """
        Retrieves a single rule document by its file path.

        Args:
            path: The path to the rule file.

        Returns:
            A RuleDocument object if the file is found and valid, otherwise None.
        """
        if path in self._cache:
            return self._cache[path]

        frontmatter, error = self.parser.parse(path)
        if frontmatter:
            try:
                # Add file_path to the frontmatter data
                frontmatter['file_path'] = str(path)
                rule_doc = RuleDocument(**frontmatter)
                self._cache[path] = rule_doc
                return rule_doc
            except ValidationError as e:
                print(f"Validation error for {path}: {e}")
        return None
