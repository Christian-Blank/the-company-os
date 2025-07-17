---
title: "Milestone 6: Pre-commit Integration"
milestone_id: "M6"
project_id: "rules-service-v0"
status: "not_started"
complexity: 3
estimated_duration: "1 day"
dependencies: ["M5"]
owner: "Christian Blank"
created_date: "2025-07-16T10:00:00-07:00"
last_updated: "2025-07-16T10:00:00-07:00"
tags: ["pre-commit", "git", "hooks", "automation", "ci"]
---

# **Milestone 6: Pre-commit Integration (3 points)**

## **Objective**
Integrate the Rules Service with the `pre-commit` framework to automate validation and synchronization on every `git commit`.

## **Strategic Context**
This milestone moves the Rules Service from a manually-invoked tool to a fully automated, "always-on" guardrail. It ensures that no non-compliant code or out-of-sync rule set can be committed to the repository, maximizing the impact of the service.

## **Deliverables**
- [ ] Pre-commit hook scripts for validation and sync.
- [ ] Hook installation/removal commands.
- [ ] Configuration for selective validation (e.g., only on changed files).
- [ ] Performance optimization for fast execution within the git hook context.

## **Acceptance Criteria**
- [ ] The pre-commit hook installs correctly via `pre-commit install`.
- [ ] The hook validates only the markdown files staged for commit.
- [ ] The hook completes in <2s for typical changes to prevent developer friction.
- [ ] The hook provides clear, actionable feedback on validation failures and blocks the commit.
- [ ] The hook automatically runs `rules sync`.

## **Implementation Tasks**

### **Task 6.1: Create pre-commit hook configuration**
- [ ] Create a `.pre-commit-hooks.yaml` file to define the hooks.
- [ ] Define a `rules-validate` hook that calls the `validate` command from M5.
- [ ] Define a `rules-sync` hook that calls the `rules sync` command from M5.

### **Task 6.2: Implement hook logic**
- [ ] The hook script should intelligently receive the list of staged files from `pre-commit`.
- [ ] Pass the file list to the `validate` command.
- [ ] Ensure the `rules sync` command runs efficiently.

### **Task 6.3: Add hook to project configuration**
- [ ] Add the new hooks to the main `.pre-commit-config.yaml` for the repository.
- [ ] Configure file patterns (`files: \.md$`) and exclusions.

### **Task 6.4: Optimize for performance**
- [ ] Ensure the CLI commands start up quickly.
- [ ] Confirm that validation is only run on the necessary subset of files.

## **Architecture Decisions**

### **`.pre-commit-config.yaml` Entry**
```yaml
-   repo: local
    hooks:
    -   id: rules-sync
        name: Rules Service - Sync
        entry: rules sync
        language: python
        stages: [commit]
        always_run: true
    -   id: rules-validate
        name: Rules Service - Validate
        entry: validate
        language: python
        types: [markdown]
        stages: [commit]
```

## **Dependencies**
- **Milestone 5**: CLI Interface (the hooks directly call the CLI commands).
- **External**: `pre-commit` framework.

## **Testing Strategy**
- **Manual Testing**: Run `pre-commit run --all-files` and test commits with both valid and invalid files.
- **Automated Testing**: It's difficult to automate tests for pre-commit hooks directly, but the underlying CLI commands should have full coverage.

## **Success Metrics**
- Pre-commit hook successfully blocks commits with validation errors.
- Pre-commit hook successfully passes commits with valid files.
- The sync and validation process adds negligible time to the commit workflow.

## **Potential Blockers**
- **`pre-commit` environment**: Ensuring the hook runs in the correct Python environment with all dependencies.
- **Performance**: Slow startup time of the CLI could impact developer experience.

## **Completion Checklist**
- [ ] All implementation tasks completed.
- [ ] All acceptance criteria met.
- [ ] Pre-commit hooks are configured and tested.
- [ ] Documentation on how to set up and use the hooks is written.
- [ ] Code committed.

## **Next Steps**
- **Milestone 7**: Testing & Documentation (Finalize all testing and docs).
- **Project Completion**: The core functionality of the Rules Service is now complete and automated.
