
---
title: "Brief: Maintenance Foundations v0 – Continuous Conformance Bootstrap"
type: "brief"
brief_id: "BRIEF-2025-07-16-001"
brief_type: "technical"
priority: "critical"
status: "draft"
governing_charter: "/os/domains/charters/data/maintenance-service.charter.md"
source_signals: ["/work/domains/signals/data/SIG-2025-07-14-001-system-complexity.signal.md"]
strategic_theme: "System‑Health"
estimated_effort: "5-20"
date_created: "2025-07-16"
tags: ["maintenance","v0","conformance","system-health"]
---

## Executive Summary
System complexity now outstrips manual upkeep.  
Maintenance v0 will introduce three automated checks—schema‑linter, graph‑integrity, rule‑sync—wired into pre‑commit and CI via Temporal. It delivers the first Continuous Conformance loop and clears "critical" Signal SIG‑2025‑07‑14‑001.

## Problem Statement
Manual validation of front‑matter, cross‑links, and rule copies takes ~45 min per change; drift already occurring.

## Proposed Solution
* **Check 1 – Schema Linter**: validate front‑matter against Pydantic models.  
* **Check 2 – Graph Integrity**: no orphans, no cycles where forbidden.  
* **Check 3 – Rule Sync**: ensure `.clinerules/`, `.cursor/rules/` folders reflect source.  
All three run via:  
* `pre‑commit` (local)  
* Temporal **GraphCheckerWorkflow** (CI)

**Success Criteria**
| Metric | Target |
|--------|--------|
| Failed pre‑commit hooks fixable <2 min | 95 % |
| CI conformance pass rate | 100 % on `main` |
| New drift incidents after 30 days | 0 |

## Charter Alignment
Supports Maintenance‑Service Principles 1 & 2 and Service‑Architecture Stage transition (0 → 1).

## Effort & Risks
~15 points total. Main risk: false‑positives blocking commits ➜ start with warn‑only mode for one week.

## Immediate Next Steps
1. Approve Maintenance‑Service Charter draft.  
2. Generate schemata in `company_os_core.models`.  
3. Implement linters & Temporal wiring.  
4. Roll out warn‑only; move to block after one week of clean passes.
