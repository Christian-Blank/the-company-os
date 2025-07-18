---
title: "Principle: The Dual-Path Process"
version: 1.0
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-17T12:54:11-07:00"
parent_charter: "company-os.charter.md"
tags: ["principle", "dual-path", "methodology", "autonomy", "governance"]
---

# **Principle: The Dual-Path Process**

This document provides a detailed explanation of the **Dual-Path Process**, a First Principle of the Company OS.

---

## **1. The Principle Defined**

The Dual-Path Principle states that any process within the OS must support two modes of execution: a **Guided Path** and an **Expert Path**. This is the operationalization of our core value, "Context Over Compliance."

## **2. The Core Problem It Solves**

This principle directly solves the "Rigidity vs. Chaos" trap inherent in traditional process design.

* **Rigidity Trap**: A single, comprehensive process creates unnecessary bureaucracy and slows down experienced collaborators.
* **Chaos Trap**: A lack of process creates inconsistency, knowledge silos, and zero support for those new to a task.

The Dual-Path model provides a solution that is simultaneously structured and flexible.

## **3. The Two Paths Explained**

### **The Guided Path (Opt-In Structure)**

This is the default path for executing any process.

* **Purpose**: To provide maximum clarity, ensure safety and compliance, facilitate onboarding, and transfer knowledge.
* **Characteristics**: It is a step-by-step, explicit workflow (as defined in an APN file) with embedded context and clear acceptance criteria for each task. It is designed to be followed precisely.

### **The Expert Path (Opt-Out Accountability)**

This path is available to collaborators (human or AI) with demonstrated capability in a specific context.

* **Purpose**: To maximize velocity and empower autonomy by leveraging existing expertise.
* **Characteristics**: It is outcome-focused. An expert may skip, combine, or re-order steps from the Guided Path, so long as they verifiably meet the exact same final acceptance criteria and adhere to all governing principles. The accountability for the outcome is higher, as the safety rails of the guided process have been removed.

## **4. The Enabler: Dynamic Capability Recognition**

The right to use the Expert Path is not based on title or tenure, but on **demonstrated, context-specific capability**. The OS, over time, will learn to recognize agents (human or AI) who consistently produce high-quality outcomes on a specific type of task. This data-driven recognition is what makes a collaborator eligible for the Expert Path, ensuring the system is both meritocratic and safe.

## **5. Implementation in APN**

An `APN` workflow file, by default, defines the **Guided Path**. It can optionally contain an `expert_criteria` block that specifies the conditions under which an agent is permitted to switch to the **Expert Path**.
