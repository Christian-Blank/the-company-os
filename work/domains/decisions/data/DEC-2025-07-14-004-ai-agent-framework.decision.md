---
title: "Decision: Adopt Temporal for Deterministic Workflow Orchestration"
type: "decision"
decision_id: "DEC-2025-07-14-004"
status: "accepted"
date_proposed: "2025-07-14"
date_decided:  "2025-07-15"
deciders: ["Christian Blank", "OS Core Team"]
parent_charter: "/os/domains/charters/data/service-architecture.charter.md"
related_signals:
  - "/work/domains/signals/data/SIG-2025-07-14-001-system-complexity.signal.md"
related_brief:  ""
related_project: "/work/domains/projects/data/automation-infrastructure.vision.md"
supersedes: ""
superseded_by: ""
tags: ["adr", "orchestration", "temporal", "deterministic", "evolution"]
---

# Context

## Problem Statement  
Manual upkeep of an ever‑growing markdown knowledge graph is already exceeding human capacity (Signal SIG‑2025‑07‑14‑001). We need automated agents that (1) run multi‑step workflows, (2) survive process restarts, (3) emit a complete, replayable event history, and (4) integrate seamlessly with the hexagonal architecture.

## Triggering Signals  
* **SIG‑2025‑07‑14‑001 – “System complexity exceeding manual maintenance capacity.”**  
  *Highlights repeated friction in validating links, enforcing schemas, and surfacing inconsistencies.*

## Constraints  
| Category | Details |
|----------|---------|
| **Technical** | Agents must run locally first; determinism & replayability are non‑negotiable; must remain adapter‑bound to preserve hexagonal purity. |
| **Resource** | ≤ 1 week to first production agent; single‑developer bandwidth. |
| **Business** | OSS‑friendly license; no hard vendor lock‑in for core architecture. |
| **Philosophical** | Must align with “Shared Explicit Memory” & “Process‑First, Tools‑Second” principles. |

## Assumptions  
* Markdown‑file representation will remain Stage 0 for at least three months.  
* Future UI & multi‑agent orchestration will reuse the same event spine.  
* Network access to external LLMs will remain intermittent; workflows must pause/resume safely.

## Environment State (2025‑07‑15)  
* **Repo commit**: `d08f23f` on `main`.  
* **Stack**: Python 3.13, Pydantic v2, Node 22 / Next 15.4.1, Bazel.  
* **Team**: Solo developer (Christian) + AI Coding assistants.  
* **External factors**: Consider impact on service architecture for document generators, linters, and similar tooling that needs to also be available to humans, automated workfloes, and ai agents.

# Options Considered

| Option | Description | Pros | Cons | Effort | Key Risks |
|--------|-------------|------|------|--------|-----------|
| **A. Temporal** (selected) | Durable workflow engine; replay from event history; OSS & SaaS. | *Deterministic*, first‑class Signals/Queries, strong Python SDK, self‑host or cloud. | Adds infrastructure (worker, cluster); learning curve. | 1 day to first dev‑server PoC; 3 days to CI integration. | Infra complexity; mis‑config could stall workflows. |
| **B. LangGraph + custom event log** | In‑process graph orchestration with manual persistence. | Very lightweight; code‑only; no extra infra. | No built‑in durability; replay fidelity manual; concurrency limits. | 6 h PoC | Hidden state bugs; divergent behaviour over time. |
| **C. Vertex AI Agent Builder** | Managed Google cloud agent framework. | Autoscale, integrated Gemini models, GUI tooling. | Cloud lock‑in; no deterministic replay; IAM overhead; costs. | 2–3 days setup | Model upgrades break determinism; limited offline dev. |

# Decision

*Selected Option A – Adopt Temporal.*

## Rationale  
Temporal is the only option providing **byte‑for‑byte deterministic replay**, aligning directly with Rule 0.1 “Every Decision is Traceable” and the need for audit‑grade event history. Its OSS licence satisfies resource constraints, and isolating it in an **adapter layer** honours the hexagonal architecture. The extra infrastructure cost is acceptable given the criticality of replayability.

## Charter Alignment  
* **Service Architecture Charter** mandates loose coupling of core logic from technology choices. By confining Temporal to `/adapters/temporal`, we preserve domain purity.  
* **Evolution Architecture Charter** values measurable improvement—Temporal’s built‑in metrics feed the Signal Intelligence system.

# Consequences

### Immediate Impact  
* Adds `docker‑compose.temporal.yaml`, Temporal worker process, and first Workflow (`GraphCheckerWorkflow`).  
* CI pipeline updated to spin up Temporal Dev Server & run integration tests.

### Long‑Term Effects  
* **Enables**: Durable human‑in‑loop workflows, event‑sourced analytics, easier rollback.  
* **Prevents**: Non‑deterministic agent executions creeping into production.  
* **Creates**: Dependency on Temporal server; requires infra maintenance.

### Success Metrics  
* 100 % Workflow history replay passes on CI.  
* Mean setup‑to‑run time for new agent ≤ 15 min.  
* > 90 % reduction in “broken link” incidents within 30 days.

### Risk Mitigation  
| Risk | Mitigation |
|------|------------|
| Worker crashes stall agents | Temporal guarantees re‑execution; monitor via Temporal UI & alerts. |
| SDK breaking change | Pin `temporalio` version; integration tests catch regressions. |
| Infra sprawl | Use single docker‑compose file; document teardown. |

# Implementation

## Action Items  
1. **Add Temporal infrastructure**  
   *Owner*: Christian · *Timeline*: 2025‑07‑16 · *Deps*: repo clone, Docker.  
2. **Implement Temporal adapter & GraphCheckerWorkflow**  
   *Owner*: Christian · *Timeline*: 2025‑07‑17.  
3. **Write unit + integration tests**  
   *Owner*: Christian · *Timeline*: 2025‑07‑18.  
4. **Update CI pipeline**  
   *Owner*: Christian · *Timeline*: 2025‑07‑18.  
5. **Document local dev guide**  
   *Owner*: Christian · *Timeline*: 2025‑07‑19.

## Implementation Path  
1. `poetry add temporalio` (SDK ≥ 1.4).  
2. Commit `infra/docker-compose.temporal.yaml`; verify `docker compose up`.  
3. Scaffold `adapters/temporal/worker.py` + `graph_workflow.py`.  
4. Port existing `check_graph` use‑case into Temporal Activity.  
5. Add `WorkflowEnvironment` tests; ensure replay passes.  
6. Merge; monitor first CI run in GitHub Actions.

## Rollback Plan  
*Trigger*: Workflow failure rate > 20 % or setup time > 4 h after two days.  
*Steps*:  
1. Revert adapter commits.  
2. Remove Temporal from `poetry.lock` and CI.  
3. Activate LangGraph adapter with identical interface (hot‑swap).  
*Data*: Preserve event logs; no user data in Temporal state for v0.

# Review

| Trigger | Condition |
|---------|-----------|
| **Time‑based** | Review after 90 days (2025‑10‑13). |
| **Event‑based** | Any Workflow replay failure in production. |
| **Metric‑based** | If “mean agent start latency” > 500 ms for three consecutive days. |

**Review Process**  
1. Gather Temporal metrics + CI logs.  
2. Analyse replay fidelity & performance.  
3. Decide maintain / modify / supersede adapter.

# Learning Capture

*Expected Outcomes*  
* Deterministic, inspectable history for every agent run.  
* Faster debugging via Temporal UI stack traces.  

*Monitoring Plan*  
* Collect `WorkflowTaskFailed` and `ActivityFailed` counts daily.  
* Track time‑to‑detect broken links pre‑ vs post‑deployment.  

*Signal Generation*  
* Positive: <5 min mean time‑to‑repair → generate **Opportunity** signal.  
* Negative: Repeated worker crashes → generate **Friction** signal.  
* Unexpected: Exponential Workflow queue growth → **Exploration** signal.

# Notes

*Temporal Dev Server* supersedes Temporalite as of v1.27; same Docker image used in local and CI.  
This decision will guide all subsequent agent orchestration; future supersession requires an equally deterministic alternative.