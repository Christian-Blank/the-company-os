---
title: "Milestone 5: CLI Interface"
milestone_id: "M5"
project_id: "rules-service-v0"
status: "not_started"
complexity: 6
estimated_duration: "2 days"
dependencies: ["M3", "M4"]
owner: "Christian Blank"
created_date: "2025-07-16T10:00:00-07:00"
last_updated: "2025-07-16T10:00:00-07:00"
tags: ["cli", "typer", "ux", "interface", "automation"]
---

# **Milestone 5: CLI Interface (6 points)**

## **Objective**
Implement a user-friendly, robust command-line interface (CLI) for interacting with all features of the Rules Service.

## **Strategic Context**
The CLI is the primary human-computer interface for the Rules Service. A well-designed CLI makes the service accessible, discoverable, and easy to use for developers, driving adoption and ensuring the service's benefits are realized.

## **Deliverables**
- [ ] `rules init` command for initial setup.
- [ ] `rules sync` command for manual synchronization.
- [ ] `rules query` command for rule discovery.
- [ ] `validate` command for document validation.
- [ ] Rich output formatting and progress indicators.

## **Acceptance Criteria**
- [ ] All commands complete successfully with expected outcomes.
- [ ] CLI provides clear, helpful text and error messages (`--help`).
- [ ] Progress indicators (e.g., spinners, progress bars) are used for long-running operations.
- [ ] Commands return proper exit codes (0 for success, non-zero for failures).

## **Implementation Tasks**

### **Task 5.1: Implement `rules` command group**
- [ ] Set up a `Typer` application for the `rules` command.
- [ ] Create the `init` command to create a default configuration file.
- [ ] Create the `sync` command, which calls the `SyncService` from M3.
- [ ] Create the `query` command, which calls the `RuleDiscoveryService` from M2 and displays results in a formatted table.

### **Task 5.2: Implement `validate` command**
- [ ] Set up a `Typer` application for the `validate` command.
- [ ] The command should accept one or more file paths or glob patterns.
- [ ] It should call the `ValidationService` from M4 for each file.
- [ ] Add an `--auto-fix` flag to apply safe fixes.
- [ ] Display results in a clear, readable format, grouped by file.

### **Task 5.3: Build rich output and progress indicators**
- [ ] Integrate a library like `rich` for formatted tables, colors, and spinners.
- [ ] Implement progress bars for validation of multiple files.
- [ ] Ensure output is clean and easy to parse for both humans and scripts.

### **Task 5.4: Add robust error handling and exit codes**
- [ ] Implement global error handling to catch exceptions and display user-friendly messages.
- [ ] Ensure different failure modes return distinct exit codes.

## **Architecture Decisions**

### **CLI Structure (Typer)**
```python
# /os/domains/rules_service/adapters/cli/commands/rules.py
import typer
from typing import List
from pathlib import Path
import sys
sys.path.append('/os/domains/rules_service')
from src.discovery import RuleDiscoveryService
from src.sync import SyncService

app = typer.Typer()

@app.command()
def sync():
    """Synchronize rules to agent folders."""
    # ... implementation ...

@app.command()
def query(tag: str = typer.Option(None, "--tag")):
    """Query for rules in the repository."""
    # ... implementation ...

# /os/domains/rules_service/adapters/cli/commands/validate.py
import typer
from typing import List
from pathlib import Path
import sys
sys.path.append('/os/domains/rules_service')
from src.validation import ValidationService

app = typer.Typer()

@app.command()
def validate(files: List[Path], auto_fix: bool = False):
    """Validate markdown files against rules."""
    # ... implementation ...
```

## **Dependencies**
- **Milestone 3**: Sync Engine (for `rules sync`).
- **Milestone 4**: Validation Core (for `validate`).
- **External**: `Typer`, `rich`.

## **Testing Strategy**
- **Integration Tests**: Use `Typer`'s test runner to invoke commands and assert on output and exit codes.
- **End-to-End Tests**: Run the CLI on a sample repository structure and verify the results on the file system.

## **Success Metrics**
- All CLI commands behave as documented.
- Help text is comprehensive and useful.
- Output formatting is clear and enhances usability.
- Error reporting is robust and helps users self-diagnose issues.

## **Potential Blockers**
- **Dependency Conflicts**: Issues with `Typer`, `rich`, and other dependencies.
- **UI/UX Design**: Making the output clear and intuitive can be challenging.

## **Completion Checklist**
- [ ] All implementation tasks completed.
- [ ] All acceptance criteria met.
- [ ] Integration tests cover all commands and major options.
- [ ] CLI documentation (in-code and `README.md`) is complete.
- [ ] Code committed.

## **Next Steps**
- **Milestone 6**: Pre-commit Integration (the CLI will be called by the git hooks).
- **User Adoption**: The service is now ready for developers to start using manually.
