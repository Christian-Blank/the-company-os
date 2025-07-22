---
title: "Decision: Repo Guardian Architecture and Technology Stack"
decision_id: "DEC-2025-07-22-001"
decision_type: "architecture"
status: "approved"
owner: "@christian"
decision_date: "2025-07-22"
review_date: "2025-10-22"
parent_charter: "company_os/domains/charters/data/repo-guardian.charter.md"
tags: ["architecture", "temporal", "ai", "workflow", "repo-guardian"]
---

# Decision: Repo Guardian Architecture and Technology Stack

## Context

We need to implement a human-AI workflow system for automated repository quality management. This system must:
- Orchestrate complex, long-running workflows
- Integrate multiple AI providers (OpenAI, Anthropic)
- Handle repository operations safely
- Scale from local development to cloud deployment
- Maintain deterministic execution and replay capability

## Decision

We will implement Repo Guardian using:
1. **Temporal** for workflow orchestration
2. **Hexagonal Architecture** for clean separation of concerns
3. **Python** as the primary language
4. **Docker Compose** for local development
5. **Stage 0 (file-based)** initial implementation

## Alternatives Considered

### 1. Celery + Redis
- **Pros**: Simple, widely used, good Python support
- **Cons**: No built-in workflow semantics, complex retry handling, no replay capability
- **Rejected because**: Lacks workflow-specific features we need

### 2. Apache Airflow
- **Pros**: Mature, good for data pipelines, strong community
- **Cons**: Designed for batch jobs not event-driven workflows, heavy infrastructure
- **Rejected because**: Overkill for our use case, not ideal for long-running workflows

### 3. AWS Step Functions
- **Pros**: Serverless, AWS integration, visual workflow editor
- **Cons**: Vendor lock-in, limited local development, cost at scale
- **Rejected because**: Need local development capability and vendor independence

## Rationale

### Why Temporal?
1. **Deterministic Execution**: Workflows are replayable and debuggable
2. **Fault Tolerance**: Automatic retries and failure handling
3. **Long-Running Workflows**: Can run for days/weeks without issues
4. **Strong Typing**: Good Python SDK with type hints
5. **Local Development**: Same stack locally and in production

### Why Hexagonal Architecture?
1. **Clean Boundaries**: Clear separation between domain logic and infrastructure
2. **Testability**: Easy to test without external dependencies
3. **Evolution-Ready**: Can swap implementations without changing core logic
4. **AI Integration**: Clean ports for different AI providers

### Why Stage 0?
1. **Simplicity First**: Start with file-based implementation
2. **Measured Evolution**: Only add complexity when friction demands it
3. **Company OS Principle**: "Evolution on demand, not by roadmap"

## Implementation Details

### Architecture Layers
```
┌─────────────────────────────────────┐
│         Domain (Workflows)          │
├─────────────────────────────────────┤
│     Ports (Activity Interfaces)     │
├─────────────────────────────────────┤
│        Adapters (External)          │
│  GitHub │ OpenAI │ Claude │ Metrics │
└─────────────────────────────────────┘
```

### Technology Stack
- **Temporal Server**: 1.24.2
- **Python**: 3.12+
- **temporalio**: 1.9.0
- **OpenAI SDK**: 1.61.0
- **Anthropic SDK**: 0.42.0
- **PyGithub**: 2.5.0

## Success Metrics

1. **Development Velocity**: Setup time < 30 minutes
2. **Reliability**: Workflow failure rate < 1%
3. **Performance**: Workflow latency < 5 seconds
4. **Cost Efficiency**: AI token usage tracked and optimized
5. **Maintainability**: Code coverage > 80%

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Temporal complexity | High learning curve | Comprehensive docs, examples |
| AI API costs | Budget overrun | Token limits, caching, monitoring |
| Repository operations | Data loss | Sandboxing, read-only by default |
| Vendor lock-in (Temporal) | Medium | Standard workflow patterns, abstraction layer |

## Review Triggers

Review this decision if:
- Workflow volume exceeds 1000/day
- AI costs exceed $1000/month
- Team size grows beyond 5 developers
- Alternative orchestrators mature significantly

## References

- [Temporal Documentation](https://docs.temporal.io)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [Company OS Service Architecture](company_os/domains/charters/data/service-architecture.charter.md)
- [Repo Guardian Charter](company_os/domains/charters/data/repo-guardian.charter.md)

---

*Decision follows Company OS principle: "Effectiveness is the measure of truth" - we'll measure and adapt based on real usage.*
