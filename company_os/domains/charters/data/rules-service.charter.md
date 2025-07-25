---
title: "Charter: Rules Service"
version: 0.2
status: "Draft"
owner: "OS Core Team"
last_updated: "2025-07-15"
parent_charter: "/os/domains/charters/data/service-architecture.charter.md"
tags: ["charter","rules","knowledge","service-domain","validation"]
---

## 1 Purpose
Provide a **single, deterministic source of truth** for all `.rules.md` documents and expose them to humans, coding agents, and workflows through stable read / sync / query interfaces. This includes validating rules documents as a core capability of the service.

## 2 Scope
* Stage 0: file discovery & sync
* Stage 1: local API (Python) + CLI + validation engine
* Stage 2+: indexed store for tag / full-text queries + ML-powered validation

## 3 First Principles (inherits all Service-Architecture principles)
1. **Rule Atomicity** Each rule file is an addressable node with explicit metadata (tags, last_updated).
2. **Agent Neutral** No rule is tailored to one IDE/agent; adapters map to agent-specific folders.
3. **Append-Only History** Rule changes emit events; deletions are tombstones, not hard deletes.
4. **Self-Validation** Service lints its own rule files before exposing them.
5. **Validation as Service** Document validation is a first-class capability, generating signals and maintaining validation rule synchronization with templates.

## 4 Success Indicators
* <60 s new-clone initialisation
* 100 % rule copy accuracy across configured agent folders
* Indexed rule query latency <100 ms (Stage 1+)
* Validation coverage >90% of all markdown documents
* Auto-fix success rate >80% for formatting issues

## 5 Evolution Path
Stage 0 (now) → Stage 1 API when validation runs exceed 100/week → Stage 2 DB when document count exceeds 1000 or query latency becomes friction signal.
