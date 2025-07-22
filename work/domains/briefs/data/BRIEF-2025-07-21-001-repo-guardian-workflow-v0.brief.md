
title: “Repo Guardian Workflow v0”
brief_id: “BRIEF-2025-07-21-001”
version: 1.0
status: “Active”
owner: “@christian”
last_updated: “2025-07-21T16:00:00-07:00”
parent_charter: “../../../../company_os/domains/charters/data/repo-guardian.charter.md”
tags: [“workflow”, “ai-agent”, “temporal”, “guardian”, “llm-integration”]

Vision

Set up a strong foundation for human-ai orchestrated workflows for our platform, that can be used for development of the platform itself, as for external facing features. For our first use-case create an automated Repo Guardian workflow that leverages Temporal and AI agents (LLMs) to proactively maintain, manage complexity, and ensure consistent quality in the Company OS repository. This system identifies structural issues, validates code patterns, generates actionable tasks, and enforces explicit memory and self-evolution.

Goals & Objectives
	•	Automate Complexity Management: Automatically monitor and manage repository complexity and structure.
	•	Proactive Quality Assurance: Verify code and document changes adhere strictly to established patterns and standards.
	•	Continuous Improvement: Capture signals from operations to drive self-evolution and inform backlog prioritization.
	•	Robust Orchestration: Use Temporal to ensure reliability, scalability, statefulness, and atomicity of the workflow.

Scope & Boundaries

In Scope
	•	Workflow orchestration with Temporal (Python SDK)
	•	AI agent integration (OpenAI, Claude)
	•	Structured LLM outputs (JSON enforced)
	•	Diff-based incremental code analysis
	•	Automatic backlog and GitHub issue creation
	•	Metric emissions (Prometheus-compatible)
	•	Idempotent and retry-safe activities
	•	Secret management (AWS/GCP Secret Manager)
	•	Sandboxed repository cloning operations

Out of Scope
	•	Full repository context analysis (RAG)
	•	Human-in-the-loop escalations (future phase)
	•	Full distributed tracing (next phase)

High-Level Requirements

Functional Requirements
	•	Clone and analyze repository diffs incrementally
	•	Validate complexity and structural compliance against OS standards
	•	Generate structured, actionable issues and recommendations
	•	Emit operational metrics (e.g., cycle times, escape defects)

Non-Functional Requirements
	•	LLM cost and latency optimizations (diff-based prompts)
	•	Idempotency and reliability (activity retries and deduplication)
	•	Security standards compliance (sandboxing, secret management)
	•	Explicit structured output format (JSON responses)
	•	Maintainability and extensibility (hexagonal architecture)

Architecture & Technical Approach

Hexagonal Architecture Layers
	•	Domain Logic: Temporal workflows
	•	Ports: Clearly defined workflow functions
	•	Adapters:
	•	LLM interactions (OpenAI, Claude)
	•	GitHub integration
	•	Metrics and tracing adapters

Repo Integration
	•	Bazel-managed Python and TypeScript client stubs
	•	Defined directory and Bazel BUILD structure

Implementation Plan (v0)

Setup & Bootstrap
	•	Establish Bazel directory scaffolding (src/company_os/services/repo_guardian)
	•	Define OpenAPI spec (shared/schemas/repo_guardian/openapi.yaml)
	•	Generate client stubs using provided scripts

Temporal Workflow Development
	•	Implement workflow logic in Python (Temporal SDK)
	•	Set up local Temporal dev environment (temporal server start-dev)

AI Adapter Implementation
	•	Develop structured LLM activity outputs with JSON enforcement
	•	Integrate OpenAI GPT-4o and Claude 3 APIs
	•	Implement diff-based context for prompts

Operational Integration
	•	Set up metrics emission activity
	•	Integrate with Prometheus monitoring
	•	Implement sandboxed repository clone activity
	•	Configure secrets management

CI/CD & Cloud Deployment
	•	Create GitHub Actions CI pipeline with Bazel tests
	•	Prepare Terraform and Helm charts for cloud deployment (AWS EKS / GCP GKE)
	•	Define container images using Bazel rules_docker

Testing & Validation
	•	Unit tests for all activities (py_test with Bazel)
	•	Workflow replay and integration tests

Success Metrics
	•	Reduction in cycle time for code validation (<50%)
	•	Reduction in escape defects (target <5% per sprint)
	•	AI cost efficiency (tracked monthly, target stable costs)
	•	Reliability metrics (workflow failures <1%)

Risks & Mitigations
	•	Cost escalation with LLMs: Mitigated by diff-based prompts and token budgets
	•	Security concerns: Addressed by sandboxing and robust secret management
	•	Complexity in orchestration: Controlled by explicit architecture boundaries and continuous monitoring

Below is a repo‑aware revision of the v0 implementation guide.
All paths, BUILD targets, and naming now align with your current Bazel + Company OS layout. Nothing is sacred—treat every choice as a measured experiment.

File name & location
Save as docs/developers/IMPLEMENT_V0_GUIDE.md (the existing developer docs area).

# IMPLEMENT‑V0 GUIDE  
*Repo‑Guardian Workflow for **the‑company‑os***  
(Temporal + AI, Bazel‑friendly)

---

## 0 Why this guide exists

* Provide a **single, ready‑to‑run recipe** to spin up the v0 Repo Guardian on your existing Bazel monorepo.  
* Let **O3/Opus** (planning in Cline) design & refactor, while **GPT‑4o 4.1/Sonnet** (execution) writes code and tests.  
* Respect the Company OS philosophy: explicit memory, evolution on measured friction, hexagonal boundaries.

---

## 1 Where things live in this repo

| Purpose | Path in repo |
|---------|--------------|
| **Charters** | `company_os/domains/charters/data/` |
| **Rules** | `company_os/domains/rules/data/` |
| **Processes / Methodologies** | `company_os/domains/processes/data/` |
| **Work products** (signals, briefs, decisions, projects) | `work/domains/**/data/` |
| **Python service code** | `src/company_os/services/` (new guardian code goes here) |
| **Shared libs** | `shared/libraries/company_os_core/` |
| **Bazel BUILDs** | already present alongside src & data |
| **Developer docs** | `docs/developers/` |

---

## 2 Prerequisites

* VS Code + Cline (O3/Opus + GPT‑4o 4.1/Sonnet)
* **Bazel** ≥ 8.3.1  
* **Python** 3.13.5 (toolchain already declared in `MODULE.bazel`)  
* **Docker** ≥ 24  
* **Temporal CLI** 1.4.1+  
* **Node 22.15.0+** (for TypeScript(≥5.8.3) client gen)  

> *Tip*: Add `temporal` and `docker` to `.bazelrc` `build --action_env=` so Bazel rules can shell‑out when needed.

---

## 3 Directory & BUILD scaffolding (10 min)

### 3.1 Create new service directories

```bash
# Within repo root
mkdir -p src/company_os/services/repo_guardian/{workflows,activities,adapters,llm,tracing}
touch src/company_os/services/repo_guardian/__init__.py

3.2 Bazel BUILD

src/company_os/services/repo_guardian/BUILD.bazel

py_library(
    name = "repo_guardian_lib",
    srcs = glob(["**/*.py"]),
    deps = [
        "//shared/libraries/company_os_core:core_lib",
        "@pypi__temporalio//:pkg",
        "@pypi__pydantic//:pkg",
        "@pypi__openai//:pkg",
        "@pypi__anthropic//:pkg",
        "@pypi__opentelemetry_sdk//:pkg",
    ],
)

py_binary(
    name = "worker",
    srcs = ["worker_main.py"],
    deps = [":repo_guardian_lib"],
)

Add a MODULE.bazel pip block for any new PyPI deps.

⸻

4 Charter location & naming

Save the Adaptive Planning & Execution Workflow Charter here:

company_os/domains/charters/data/repo-guardian.charter.md

Update its parent_charter front‑matter to:

parent_charter: "../../company-os.charter.md"

The relative path keeps the existing charter hierarchy intact.

⸻

5 Canonical spec & stub generation

5.1 Spec path

shared/schemas/repo_guardian/openapi.yaml

5.2 regen.sh adapts to Bazel

#!/usr/bin/env bash
set -euo pipefail
SPEC=shared/schemas/repo_guardian/openapi.yaml

# Python client under shared libs (so Bazel picks it up)
datamodel-code-generator \
  --input $SPEC --input-file-type openapi \
  --output shared/libraries/company_os_core/repo_guardian_client

# TypeScript stubs into bazel-bin ignored dir
openapi-typescript-codegen \
  --input $SPEC \
  --output bazel-bin/repo_guardian_ts \
  --client fetch --name GuardianClient

Add an external workspace binding for the TS client if you want Bazel build steps later; for v 0 we only need the Python stubs.

⸻

6 Local Temporal dev loop

temporal server start-dev           # port 7233
bazel run //src/company_os/services/repo_guardian:worker

Worker entrypoint sample (worker_main.py) lives with py_binary.

⸻

7 CI with Bazel

.github/workflows/ci.yml (excerpt)

    - uses: actions/setup-python@v5
      with: { python-version: '3.12' }
    - uses: bazelbuild/setup-bazelisk@v3
    - run: |
        ./scripts/regen.sh
        git diff --exit-code   # drift check
        bazel test //...       # runs pytests under Bazel


⸻

8 Cloud deployment sketch
	•	Container image: bazel build //src/company_os/services/repo_guardian:worker_image using rules_docker.
	•	Helm values under infrastructure/environments/staging/guardian-values.yaml.
	•	Terraform module in infrastructure/environments/staging/main.tf with EKS + RDS.

Workers are stateless; scale via Deployment.replicas.

⸻

9 Hexagonal mapping in this repo

Layer	Directory / Bazel target
Domain (Temporal workflows)	src/company_os/services/repo_guardian/workflows/
Ports	Function signatures in workflows/guardian.py
Adapters – LLM	src/company_os/services/repo_guardian/llm/ each provider
Adapters – GitHub	src/company_os/services/repo_guardian/adapters/github.py
Adapters – Metrics / Tracing	src/.../tracing/
External	OpenAI, Claude, GitHub REST, Prometheus, etc.

Bazel BUILD keeps each adapter’s external deps isolated via deps.

⸻

10 Backlog slice (Bazel labels)

Task	Bazel label	Owner
Structured JSON output	//src/.../activities:generate_structured_issues.py	@agent-cortex
Diff builder	//src/.../activities:verify_code.py	@agent-cortex
Secrets DataConverter	//src/.../tracing:data_converter.py	@christian
Docker sandbox rule	//infrastructure/scripts:sandbox_clone.sh	@agent-loop
Metrics emitter	//src/.../activities:emit_metrics.py	@agent-loop


⸻

11 Testing conventions
	•	Unit tests live in the same package tree, *_test.py, referenced in BUILD via py_test.
	•	Workflow replay tests under src/.../workflows/tests/.
	•	Integration (Temporal + Docker sandbox) under tests/ root.

⸻

12 Iterate without sacred cows

Every BUILD, spec path, or directory name is fair game—log rationale in:

work/domains/decisions/data/DEC-YYYY-MM-DD-NNN-topology-adjustment.decision.md

Use signals if friction emerges (e.g., Bazel build times) and let the system evolve.

⸻

Ship this guide, run temporal server start-dev, and trigger the first workflow via Bazel run.
Effectiveness will be obvious in metrics.  Continuous improvement is the default.
No sacred cows—measure and refactor relentlessly.