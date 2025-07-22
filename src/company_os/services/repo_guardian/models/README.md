---
title: "Repo Guardian Domain Models"
parent: "../README.md"
tags: ["models", "domain", "repo-guardian"]
---

# Repo Guardian Domain Models

This directory contains the domain models and data structures used throughout the Repo Guardian service.

## Overview

Domain models represent the core business concepts and data structures, independent of any specific technology or framework.

## Model Structure

### domain.py
Core domain models:
- `RepositoryConfig`: Repository analysis configuration
- `AnalysisResult`: Results from code analysis
- `Issue`: Structured issue representation
- `Metric`: Performance and quality metrics
- `WorkflowInput`/`WorkflowOutput`: Workflow data contracts

## Design Principles

### 1. **Immutability**
Models use Pydantic's frozen classes:
```python
class Issue(BaseModel):
    class Config:
        frozen = True
```

### 2. **Validation**
Built-in validation for all fields:
```python
class RepositoryConfig(BaseModel):
    url: HttpUrl
    branch: str = "main"
    depth: PositiveInt = Field(default=1, le=100)
```

### 3. **Serialization**
All models are JSON-serializable for Temporal:
- Use standard Python types
- Custom types with serializers
- Avoid complex nested structures

### 4. **Evolution**
Models support backward compatibility:
- Optional fields for new features
- Deprecation notices for removals
- Version fields when needed

## Usage Examples

```python
# Creating a workflow input
input_data = WorkflowInput(
    repository_url="https://github.com/owner/repo",
    branch="main",
    analysis_depth=10,
    create_issues=False
)

# Parsing analysis results
result = AnalysisResult.model_validate(analysis_data)
for issue in result.issues:
    print(f"{issue.severity}: {issue.title}")
```

## Testing

Models are tested for:
- Validation rules
- Serialization/deserialization
- Edge cases and invalid data
- Performance with large datasets

See `/tests/models/` for examples.

---

*Part of the Repo Guardian service following domain-driven design principles.*
