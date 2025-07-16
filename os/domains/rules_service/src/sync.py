"""Synchronization service for distributing rules to agent folders."""

import hashlib
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import fnmatch

from .models import RuleDocument
from .config import RulesServiceConfig, ConflictStrategy, AgentFolder


logger = logging.getLogger(__name__)


@dataclass
class SyncResult:
    """Result of a synchronization operation."""
    added: int = 0
    updated: int = 0
    deleted: int = 0
    skipped: int = 0
    errors: List[str] = field(default_factory=list)
    
    @property
    def total_changes(self) -> int:
        """Total number of changes made."""
        return self.added + self.updated + self.deleted
    
    def merge(self, other: "SyncResult") -> None:
        """Merge another result into this one."""
        self.added += other.added
        self.updated += other.updated
        self.deleted += other.deleted
        self.skipped += other.skipped
        self.errors.extend(other.errors)


class FileHashCache:
    """Cache for file hashes to speed up change detection."""
    
    def __init__(self, algorithm: str = "sha256"):
        self.algorithm = algorithm
        self._cache: Dict[Path, Tuple[float, str]] = {}
    
    def get_hash(self, file_path: Path) -> str:
        """Get hash of a file, using cache if available."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        stat = file_path.stat()
        mtime = stat.st_mtime
        
        # Check cache
        if file_path in self._cache:
            cached_mtime, cached_hash = self._cache[file_path]
            if cached_mtime == mtime:
                return cached_hash
        
        # Calculate hash
        hash_obj = hashlib.new(self.algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hash_obj.update(chunk)
        
        file_hash = hash_obj.hexdigest()
        self._cache[file_path] = (mtime, file_hash)
        return file_hash
    
    def clear(self) -> None:
        """Clear the cache."""
        self._cache.clear()


class SyncService:
    """Service for synchronizing rule files to agent folders."""
    
    def __init__(self, config: RulesServiceConfig, root_path: Path):
        self.config = config
        self.root_path = root_path
        self.hash_cache = FileHashCache(config.performance.checksum_algorithm)
    
    def sync_rules(self, rules: List[RuleDocument], dry_run: bool = False) -> SyncResult:
        """
        Synchronize rules to all configured agent directories.
        
        Args:
            rules: List of rule documents to sync
            dry_run: If True, only report what would be done without making changes
            
        Returns:
            SyncResult with details of the operation
        """
        total_result = SyncResult()
        
        # Get enabled folders
        enabled_folders = self.config.get_enabled_folders()
        if not enabled_folders:
            total_result.errors.append("No agent folders enabled in configuration")
            return total_result
        
        # Filter rules based on patterns
        filtered_rules = self._filter_rules(rules)
        
        # Sync to each folder
        for folder in enabled_folders:
            try:
                folder_result = self._sync_to_folder(filtered_rules, folder, dry_run)
                total_result.merge(folder_result)
            except Exception as e:
                error_msg = f"Error syncing to {folder.path}: {str(e)}"
                logger.error(error_msg)
                total_result.errors.append(error_msg)
        
        return total_result
    
    def _filter_rules(self, rules: List[RuleDocument]) -> List[RuleDocument]:
        """Filter rules based on include/exclude patterns."""
        filtered = []
        
        for rule in rules:
            # Assume rule has a file_path attribute (from discovery)
            if not hasattr(rule, 'file_path'):
                continue
                
            file_name = Path(rule.file_path).name
            
            # Check include patterns
            included = any(
                fnmatch.fnmatch(file_name, pattern) 
                for pattern in self.config.sync.include_patterns
            )
            
            # Check exclude patterns
            excluded = any(
                fnmatch.fnmatch(file_name, pattern)
                for pattern in self.config.sync.exclude_patterns
            )
            
            if included and not excluded:
                filtered.append(rule)
        
        return filtered
    
    def _sync_to_folder(self, rules: List[RuleDocument], folder: AgentFolder, 
                       dry_run: bool) -> SyncResult:
        """Sync rules to a specific agent folder."""
        result = SyncResult()
        target_dir = self.root_path / folder.path
        
        # Create directory if needed
        if not dry_run and self.config.sync.create_directories:
            target_dir.mkdir(parents=True, exist_ok=True)
        elif not target_dir.exists():
            result.errors.append(f"Target directory does not exist: {target_dir}")
            return result
        
        # Build source to target mapping
        source_files: Set[Path] = set()
        target_to_source: Dict[Path, Path] = {}
        
        for rule in rules:
            if not hasattr(rule, 'file_path'):
                continue
            
            source_path = Path(rule.file_path)
            target_path = target_dir / source_path.name
            source_files.add(source_path)
            target_to_source[target_path] = source_path
        
        # Sync files
        with ThreadPoolExecutor(max_workers=self.config.performance.max_parallel_operations) as executor:
            futures = []
            
            for target_path, source_path in target_to_source.items():
                future = executor.submit(
                    self._sync_file, source_path, target_path, dry_run
                )
                futures.append((future, source_path, target_path))
            
            for future, source_path, target_path in futures:
                try:
                    action = future.result()
                    if action == "added":
                        result.added += 1
                    elif action == "updated":
                        result.updated += 1
                    elif action == "skipped":
                        result.skipped += 1
                except Exception as e:
                    result.errors.append(f"Error syncing {source_path}: {str(e)}")
        
        # Clean orphaned files
        if self.config.sync.clean_orphaned:
            orphan_result = self._clean_orphaned_files(
                target_dir, set(target_to_source.keys()), dry_run
            )
            result.deleted += orphan_result
        
        return result
    
    def _sync_file(self, source: Path, target: Path, dry_run: bool) -> str:
        """
        Sync a single file, handling conflicts according to strategy.
        
        Returns:
            Action taken: "added", "updated", "skipped"
        """
        # Check if target exists
        if not target.exists():
            if not dry_run:
                self._copy_file_atomic(source, target)
            return "added"
        
        # Check if files are different
        if self.config.performance.use_checksums:
            try:
                source_hash = self.hash_cache.get_hash(source)
                target_hash = self.hash_cache.get_hash(target)
                files_identical = source_hash == target_hash
            except Exception as e:
                logger.warning(f"Error comparing files, falling back to size comparison: {e}")
                files_identical = source.stat().st_size == target.stat().st_size
        else:
            files_identical = source.stat().st_size == target.stat().st_size
        
        if files_identical:
            return "skipped"
        
        # Handle conflict
        if self.config.sync.conflict_strategy == ConflictStrategy.SKIP:
            return "skipped"
        elif self.config.sync.conflict_strategy == ConflictStrategy.OVERWRITE:
            if not dry_run:
                self._copy_file_atomic(source, target)
            return "updated"
        else:  # ASK strategy
            # In automated context, default to skip
            logger.info(f"Conflict for {target}, skipping (ASK strategy in automated mode)")
            return "skipped"
    
    def _copy_file_atomic(self, source: Path, target: Path) -> None:
        """Copy file atomically to prevent partial writes."""
        temp_target = target.with_suffix(target.suffix + '.tmp')
        try:
            shutil.copy2(source, temp_target)
            temp_target.replace(target)
        except Exception:
            if temp_target.exists():
                temp_target.unlink()
            raise
    
    def _clean_orphaned_files(self, target_dir: Path, expected_files: Set[Path], 
                             dry_run: bool) -> int:
        """Remove files in target directory that are not in expected set."""
        deleted_count = 0
        
        # Find all .rules.md files in target
        existing_files = set(target_dir.glob("*.rules.md"))
        
        # Find orphans
        orphans = existing_files - expected_files
        
        for orphan in orphans:
            if not dry_run:
                try:
                    orphan.unlink()
                    deleted_count += 1
                except Exception as e:
                    logger.error(f"Error deleting orphaned file {orphan}: {e}")
            else:
                deleted_count += 1
        
        return deleted_count
    
    def get_sync_status(self, rules: List[RuleDocument]) -> Dict[str, Dict[str, str]]:
        """
        Get current sync status for all agent folders.
        
        Returns:
            Dict mapping folder paths to their sync status
        """
        status = {}
        filtered_rules = self._filter_rules(rules)
        
        for folder in self.config.get_enabled_folders():
            folder_status = {
                "enabled": str(folder.enabled),
                "exists": str((self.root_path / folder.path).exists()),
                "rule_count": "0",
                "last_sync": "never"
            }
            
            target_dir = self.root_path / folder.path
            if target_dir.exists():
                rule_files = list(target_dir.glob("*.rules.md"))
                folder_status["rule_count"] = str(len(rule_files))
                
                # Check if files match source
                matches = 0
                for rule in filtered_rules:
                    if hasattr(rule, 'file_path'):
                        target_path = target_dir / Path(rule.file_path).name
                        if target_path.exists():
                            matches += 1
                
                if matches == len(filtered_rules) and matches == len(rule_files):
                    folder_status["sync_state"] = "in_sync"
                else:
                    folder_status["sync_state"] = "out_of_sync"
            else:
                folder_status["sync_state"] = "not_initialized"
            
            status[folder.path] = folder_status
        
        return status