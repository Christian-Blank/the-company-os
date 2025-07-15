---
title: "Brief: Rules Service v0 – Discovery & Sync"
type: "brief"
brief_id: "BRIEF-2025-07-15-001"
brief_type: "technical"
priority: "high"
status: "draft"
governing_charter: "/os/domains/charters/data/rules-service.charter.md"
source_signals: ["/work/domains/signals/data/SIG-2025-07-14-001-system-complexity.signal.md"]
strategic_theme: "Developer Experience"
estimated_effort: "5-20"
date_created: "2025-07-15"
date_reviewed: ""
date_approved: ""
related_briefs: []
depends_on: []
implemented_by: ""
superseded_by: ""
tags: ["rules","service","v0","dx"]
---

# **Brief: Rules Service v0 – Discovery & Sync**

**Type**: technical **Priority**: high **Status**: draft  
**Strategic Theme**: Developer Experience **Estimated Effort**: 5‑20 points  
**Date Created**: 2025‑07‑15

---

## Executive Summary
Coding agents (Cline, Cursor, Windsurf) and humans need a consistent set of `.rules.md` files. Manual copying causes drift, breaking agent context and onboarding speed.  
*Rules Service v0* will scan the repo, copy rules into agent‑specific folders during `clone` (`rules init`), and keep them in sync via CLI command + pre‑commit hook. This delivers immediate quality‑of‑life gains and lays the Stage‑0 foundation for later API/DB evolution.

---

## Problem Statement
**Current State** – Rules live only in `/os/domains/rules/data/…`; IDE plug‑ins look for `.clinerules/`, `.cursor/rules/`, etc. Developers copy by hand or forget.  
**Pain Points**

* Repeated copy‑paste on every rule change  
* Agents sometimes read stale rules ➜ inconsistent behaviour  
* New contributors miss critical governance rules

---

## Proposed Solution
*Domain engine* inside `company_os_core.rules_service`  
1. **discover_rules** – glob `*.rules.md`, parse front‑matter  
2. **plan_sync / apply_sync** – produce and execute copy/delete actions  
3. **tag query** – simple filter for `rules query --tag governance`

*Adapters*  
* **CLI** commands `rules init|sync|query` (Typer)  
* **Pre‑commit hook** auto‑runs `rules sync` on changed rule files

**Success Criteria**

| Metric | Target |
|--------|--------|
| `rules init` completes <30 s on repo clone | 100 % |
| Pre‑commit sync latency | <2 s |
| Post‑deployment drift incidents | 0 in first 30 days |

---

## Charter Alignment
*Rules Service Charter* Principle 2 “Agent Neutral” – expose rules equally to any coding agent.  
Supports Service‑Architecture Principle 3 “Start Simple, Evolve on Demand” by shipping Stage 0 functionality now.

---

## Effort & Risks
**Effort** ≈ 10 points (core engine 4, CLI 3, tests 3).  
**Risks**

| Risk | Mitigation |
|------|------------|
| Agent folder paths differ per OS | Configurable mapping in `rules.toml` |
| Hook conflicts with existing hooks | Append, don’t overwrite, during install |

---

## Immediate Next Steps
1. Scaffold `rules_service` engine & unit tests.  
2. Implement `rules init|sync|query` CLI.  
3. Add pre‑commit installer to `rules init`.  
4. Write integration test on fixture repo; wire to CI.