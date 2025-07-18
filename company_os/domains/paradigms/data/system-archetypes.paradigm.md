---
title: "Paradigm: The System Archetypes"
version: 1.1
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-17T13:00:32-07:00"
parent_charter: "company-os.charter.md"
tags: ["paradigm", "mental-model", "archetype", "first-principles", "system-design"]
---

# **Paradigm: The System Archetypes**

This document explains the foundational paradigm of our Company OS: that it is a **system composed of distinct conceptual archetypes**, each with a clear purpose and relationship to the others.

---

## **1. The Core Idea**

Instead of viewing the OS as a monolithic entity, we see it as a constellation of interconnected, purpose-driven concepts. By understanding the role of each "archetype"—like a Charter, a Principle, or a Process—we create a shared language that allows us to reason about, navigate, and evolve the system with precision and clarity.

## **2. The Problem it Solves**

This paradigm prevents conceptual chaos and architectural decay. Without it, the lines blur between a long-term vision (a Charter), a strategic approach (a Methodology), and a tactical plan (a Process). This confusion leads to building the wrong things, applying rules inconsistently, and an inability to scale gracefully.

## **3. The Mental Model Explained**

The OS is a living system where different types of ideas have different jobs. We can visualize their relationship as a map of intent:

```mermaid
graph TD
    subgraph "Foundational Layer (Timeless Truths)"
        P(Principle)
    end

    subgraph "Governance Layer (Long-Term Mission)"
        C(Charter)
    end

    subgraph "Execution Layer (Strategic & Tactical)"
        M(Methodology) --> Proc(Process / APN)
    end

    subgraph "Learning Layer (Real-Time Feedback)"
        S(Signal)
    end

    subgraph "Context Layer (Shared Brain)"
        K(Knowledge)
    end

    P --"Informs"--> C;
    C --"Governs"--> M;
    M --"Guides the creation of"--> Proc;
    Proc --"Generates"--> S;
    S --"Triggers evolution in"--> P;
    S --"Triggers evolution in"--> C;
    S --"Triggers evolution in"--> M;

    K <--> P;
    K <--> C;
    K <--> M;
    K <--> Proc;
    K <--> S;
