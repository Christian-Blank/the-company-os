---
title: "Brief: Developer CLI v0 – Unified Local Tooling"
type: "brief"
brief_id: "BRIEF-2025-07-15-002"
brief_type: "technical"
priority: "high"
status: "draft"
governing_charter: "/os/domains/charters/data/service-architecture.charter.md"
source_signals: ["/work/domains/signals/data/SIG-2025-07-14-001-system-complexity.signal.md"]
strategic_theme: "Developer Experience"
estimated_effort: "5-20"
date_created: "2025-07-15"
date_reviewed: ""
date_approved: ""
related_briefs: ["BRIEF-2025-07-15-001"]
depends_on: []
implemented_by: ""
superseded_by: ""
tags: ["cli","tooling","v0","dx"]
---

# **Brief: Developer CLI v0 – Unified Local Tooling**

**Type**: technical **Priority**: high **Status**: draft
**Strategic Theme**: Developer Experience **Estimated Effort**: 5‑20 points
**Date Created**: 2025‑07‑15

---

## Executive Summary
Multiple ad‑hoc scripts exist for graph checks, rule sync, etc., confusing newcomers and fragmenting UX.
The new **`company-os`** CLI will provide a single command entry point that exposes Rules Service commands now and future service adapters later, dramatically simplifying local and CI workflows.

---

## Problem Statement
* Scripts live in different folders with inconsistent flags.
* Onboarding instructions are lengthy (“run script X, then Y”).
* CI must call scripts with hard‑coded paths.

---

## Proposed Solution
*Typer‑based multi‑command CLI* published as `company-os`.
**Initial command groups**

| Group | Commands |
|-------|----------|
| `rules` | `init • sync • query` (from Brief‑001) |
| `graph` | placeholder – delegates to Graph Checker when available |

CLI conforms to optional‑dependencies model (`pip install company-os[watch]`).

**Success Criteria**

* CLI install via `pipx` <1 min.
* `company-os --help` lists rules commands.
* >80 % of documented local workflows executed via CLI within first month.

---

## Charter Alignment
Fulfils Service‑Architecture Principle 4 “Stable APIs, Evolving Implementations” by giving humans a stable interface while underlying adapters change.

---

## Effort & Risks
**Effort** ≈ 8 points (skeleton 3, integrate rules 3, docs/tests 2).
**Risks**

| Risk | Mitigation |
|------|------------|
| Dependency bloat | Keep adapters optional via extras |
| Command clashes later | Namespace commands by service (`company-os rules …`) |

---

## Immediate Next Steps
1. Generate Typer skeleton with plugin discovery (`company_os_services.` namespace).
2. Hook in Rules Service commands.
3. Create CI smoke tests (`company-os --help`).
4. Draft README install section and update onboarding docs.
