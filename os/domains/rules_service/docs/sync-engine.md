# Rules Service Sync Engine Documentation

## Overview

The Sync Engine is responsible for distributing rules from the canonical source (`.rules.md` files in the repository) to agent-specific folders where development tools can access them. This ensures all AI agents and IDE extensions work with the same set of rules.

## Architecture

### Components

1. **SyncService**: Core synchronization logic
2. **FileHashCache**: Efficient change detection using checksums
3. **Configuration**: YAML-based configuration for agent folders and sync behavior
4. **SyncResult**: Detailed reporting of sync operations

### Key Features

- **Multi-folder Support**: Sync to multiple agent folders simultaneously
- **Change Detection**: Only sync files that have changed (using SHA256 by default)
- **Conflict Resolution**: Configurable strategies (overwrite, skip, ask)
- **Orphan Cleanup**: Remove outdated rules from agent folders
- **Parallel Processing**: Concurrent file operations for performance
- **Dry Run Mode**: Preview changes without modifying files

## Configuration

The sync engine is configured via `rules-service.config.yaml`:

```yaml
version: 1.0

agent_folders:
  - path: ".clinerules/"
    description: "Rules for the Gemini CLI agent"
    enabled: true
    
  - path: ".cursor/rules/"
    description: "Rules for the Cursor IDE"
    enabled: true

sync:
  conflict_strategy: "overwrite"  # overwrite, skip, or ask
  include_patterns: ["*.rules.md"]
  exclude_patterns: ["*draft*.rules.md"]
  create_directories: true
  clean_orphaned: true

performance:
  max_parallel_operations: 10
  use_checksums: true
  checksum_algorithm: "sha256"  # md5, sha256, or sha512
```

## Usage

### Basic Sync Operation

```python
from pathlib import Path
from src.config import RulesServiceConfig
from src.sync import SyncService
from src.discovery import RuleDiscoveryService

# Load configuration
config = RulesServiceConfig.from_file(Path("rules-service.config.yaml"))

# Discover rules
discovery = RuleDiscoveryService(Path("."))
rules, errors = discovery.discover_rules()

# Perform sync
sync_service = SyncService(config, Path("."))
result = sync_service.sync_rules(rules)

print(f"Added: {result.added}")
print(f"Updated: {result.updated}")
print(f"Deleted: {result.deleted}")
print(f"Skipped: {result.skipped}")
```

### Dry Run

```python
# Preview what would be synced without making changes
result = sync_service.sync_rules(rules, dry_run=True)
```

### Check Sync Status

```python
# Get current sync status for all folders
status = sync_service.get_sync_status(rules)
for folder, info in status.items():
    print(f"{folder}: {info['sync_state']} ({info['rule_count']} rules)")
```

## Sync Strategies

### Conflict Resolution

When a file exists in both source and target with different content:

1. **overwrite**: Replace target with source (default)
2. **skip**: Keep existing target file
3. **ask**: Prompt user (falls back to skip in automated mode)

### File Filtering

- **Include Patterns**: Glob patterns for files to sync (default: `*.rules.md`)
- **Exclude Patterns**: Glob patterns for files to skip (e.g., `*draft*.rules.md`)

### Orphan Cleanup

When `clean_orphaned` is enabled, files in target folders that don't exist in the source are deleted. This prevents accumulation of outdated rules.

## Performance Considerations

### Change Detection

The sync engine uses file checksums (SHA256 by default) to detect changes:
- Fast for unchanged files (cached)
- Accurate change detection
- Configurable algorithm for different security/speed tradeoffs

### Parallel Operations

File operations are performed in parallel (default: 10 concurrent operations) for faster syncing of large rule sets.

### Caching

File hashes are cached based on modification time to avoid recalculating for unchanged files.

## Error Handling

The sync engine handles errors gracefully:
- Permission errors are logged but don't stop the sync
- Individual file errors don't affect other files
- All errors are collected in `SyncResult.errors`

## Integration Points

### With Discovery Service

```python
# Sync only rules with specific tags
validation_rules = discovery.query_by_tags(["validation"])
result = sync_service.sync_rules(validation_rules)
```

### With CLI

The sync engine will be integrated with CLI commands:
- `rules sync`: Manual sync operation
- `rules init`: Initial setup and sync
- Pre-commit hooks for automatic sync

## Best Practices

1. **Regular Syncing**: Run sync after rule updates or as part of CI/CD
2. **Exclude Drafts**: Use exclude patterns for work-in-progress rules
3. **Monitor Status**: Check sync status to ensure agents have latest rules
4. **Handle Errors**: Review sync errors and address permission issues
5. **Test Changes**: Use dry run mode to preview sync operations

## Troubleshooting

### Common Issues

1. **Permission Denied**
   - Ensure write permissions for agent folders
   - Check if folders are not locked by other processes

2. **Out of Sync**
   - Run sync manually with `refresh_cache=True`
   - Check exclude patterns aren't filtering needed rules

3. **Performance Issues**
   - Reduce `max_parallel_operations` for systems with limited resources
   - Consider using MD5 for faster (but less secure) checksums

### Debug Mode

Enable logging for detailed sync information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

1. **Watch Mode**: Real-time sync on file changes
2. **Selective Sync**: Sync only specific rule categories
3. **Backup**: Create backups before overwriting
4. **Metrics**: Detailed performance metrics and monitoring