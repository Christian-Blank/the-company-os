---
title: "Charter: Agentic Process Notation (APN)"
version: 1.0
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-17T12:51:27-07:00"
parent_charter: "synapse.methodology.md"
tags: ["charter", "apn", "workflow", "process", "dsl"]
---

# **Charter: Agentic Process Notation (APN)**

This document defines the vision, principles, and scope for APN, the human-readable language we use to codify all workflows within the Company OS.

---

## **1. Vision**

To provide a simple, powerful, and evolvable "lingua franca" for human-AI process collaboration. APN will serve as the explicit, version-controlled blueprint for any repeatable task, ensuring clarity, determinism, and seamless execution by any qualified agent.

---

## **2. Core Principles**

1.  **Human & AI Parity**: APN's syntax must be as easy for a human to write in a text editor as it is for an LLM to generate, parse, and modify. Simplicity and clarity are paramount.
2.  **Explicit Over Implicit**: The workflow must contain all necessary information to be executed. It should not rely on hidden context.
3.  **Structure for Clarity, Not Constraint**: APN provides a clear structure (Workflow -> Process -> Task -> Action) to manage complexity, but it must not be so rigid that it stifles expert intuition.
4.  **Support for the Dual Path**: The notation must inherently support both a detailed, step-by-step "Guided Path" and allow for an "Expert Path" where outcomes are the measure of success, not mere step completion.
5.  **Deterministic & Replayable**: Given the same inputs and context, an APN workflow should produce a predictable and repeatable outcome, enabling reliable automation and auditing.

---

## **3. Scope & Boundaries**

* **In Scope**:
    * Defining sequential and conditional workflows.
    * Structuring work into Processes, Tasks, and Actions.
    * Serving as checklists and execution guides for humans and agents.
    * Providing context and instructions for tool execution.

* **Out of Scope**:
    * Performing complex computations (APN instructs *tools* to do this).
    * Storing large datasets (APN references data, it doesn't contain it).
    * Defining user interfaces.

---

## **4. Process for Evolution**

APN is a living language. Changes to its syntax, primitives, or core features must be proposed via an **Opportunity Brief**. If approved, changes must be reflected first in an update to this charter, followed by implementation in any parsing or execution tools.
