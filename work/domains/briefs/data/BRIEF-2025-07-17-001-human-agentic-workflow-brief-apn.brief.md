---
title: "Brief: Human-Agentic Workflows v0"
version: 1.0
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-17T12:44:08-07:00"
parent_charter: "synapse.methodology.md"
tags: ["brief", "workflow", "process", "apn", "agentic"]
---

# **Brief: Human-Agentic Workflows v0**

## **1. Vision**

To bring structure and clarity to repetitive work by codifying it into **Workflows**. These workflows will serve as a deterministic, replayable, and evolvable "lingua franca" for both human and AI agent collaboration, turning chaotic processes into a managed, intelligent system.

## **2. Core Principles**

This system operationalizes our core methodologies with the following principles:

1.  **Codification of Work**: All repeatable, multi-step procedures should be codified into a version-controlled Workflow file.
2.  **Human & AI Parity**: The workflow format must be equally readable and executable by both human and AI collaborators. We will start with a simple markdown format.
3.  **Dual-Path Execution**: In line with our methodology, every workflow implicitly supports two paths:
    * **Guided Path (Default)**: Following the steps precisely, ideal for new tasks or collaborators.
    * **Expert Path (Opt-Out)**: An expert human or agent may bypass or combine steps, but remains accountable for achieving the same explicit outcomes and quality standards.
4.  **Progressive Automation**: A workflow that becomes highly rigid, with zero deviation over many runs, is a prime candidate to be fully automated into a single script or tool call. The workflow's purpose is to manage complexity, not to be a machine.

## **3. The v0 Primitives & Data Model**

We will adopt a clear hierarchy to structure work:

* **Workflow**: The highest-level container, representing a complete, end-to-end job to be done (e.g., "Onboard a New Project"). A workflow consists of one or more Processes.
* **Process**: A distinct phase of a workflow (e.g., "Planning Phase," "Implementation Phase"). A process consists of one or more Tasks.
* **Task**: A logical unit of work with a clear goal and acceptance criteria (e.g., "Create Project Context Files"). A task consists of one or more Actions.
* **Action**: The most atomic, unambiguous instruction (e.g., "Create file `README.md`," "Write the project goal to the README").

### **v0 Markdown Format**

Workflows will be markdown files using headings and checklists:

```markdown
# Workflow: [Workflow Name]
## Process: [Process Name]
### Task: [Task Name]
- [ ] Action 1
- [ ] Action 2
