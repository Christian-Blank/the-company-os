---
title: "Charter: The Repository Architecture"
version: 1.0
status: "Draft"
owner: "OS Core Team"
last_updated: "2025-07-14T16:22:00-07:00"
parent_charter: "knowledge-architecture.charter.md"
tags: ["charter", "architecture", "repository", "monorepo", "governance", "source-control"]
---

# **Charter: The Repository Architecture**

This Charter is the North Star for the structure of our unified repository. It defines the vision, rationale, and first principles for organizing all files, ensuring that our digital workspace provides cognitive clarity and scales gracefully.

---

## **1. Vision: The Organized Workshop**

To create a self-organizing repository architecture that acts as a well-organized workshop. It provides cognitive clarity by creating distinct, high-level "benches" for different kinds of work: defining the system's **laws** (`/os`), logging its **work** (`/work`), building its **tools** (`/src`), and storing its **blueprints** (`/schemas`).

This separation allows collaborators—human or AI—to focus on the task at hand without being distracted by unrelated files, enabling parallel workstreams and independent evolution of concerns.

---

## **2. The "Why" (Core Rationale)**

A single, undifferentiated folder structure creates cognitive drag and scales poorly. This architecture is designed to solve for:

1.  **Clarity**: A developer fixing a bug in `/src` should not have to navigate through thousands of unrelated project records in `/work`.
2.  **Scalability**: Prevents the repository root from becoming an unmanageable junk drawer, ensuring that finding and storing information remains efficient as the system grows.
3.  **Independent Cadence**: The system's "constitution" in `/os` evolves slowly and deliberately, while the code in `/src` can iterate rapidly and projects in `/work` can be created and archived daily.

---

## **3. First Principles (The Mental Model)**

*All organization within this repository MUST adhere to these principles.*

1.  **Separation of Concerns is Paramount**: We physically separate files based on their fundamental purpose. The repository is divided into four primary, mutually exclusive workspaces: `os`, `work`, `src`, and `schemas`.
2.  **Shallow by Default, Nested by Exception**: Top-level folders are treated as namespaces, not the start of a deep hierarchy. Nesting is only permitted within a well-defined context (e.g., inside a specific project folder at `/work/20_projects/my-project/`).
3.  **Organize by Type, Not by Topic**: We group files by their universal `type` (e.g., all `.spec.md` files together), not by a temporary or subjective `topic` (e.g., "Project Phoenix Docs").
4.  **Location is a Hint, Not the Truth**: The folder a file lives in (e.g., `/work/13_specs/`) is a hint to its *type*. The file's *true relationships* to other entities in the graph are defined exclusively by the metadata links within its frontmatter.

---

## **4. The Canonical Structure (v1.0)**

The repository is organized into the following top-level directories:

* **`/os/`**: The immutable definition of the Company OS itself. Contains all Charters, Methodologies, and Rules.
* **`/work/`**: The execution log of the OS. Contains all Signals, Decisions, Briefs, Specs, and active Project folders.
* **`/src/`**: The implementation. Contains all source code for services, packages, and tools.
* **`/schemas/`**: The data contracts. Contains all shared JSON Schema definitions used by `/os`, `/work`, and `/src`.

---

## **5. Process for Evolution**

This architecture is a living system. Any proposal to add, remove, or significantly change a top-level directory must follow the Synapse Methodology: it must be captured as a `Signal Record`, synthesized into an `Opportunity Brief` explaining the rationale and impact, and approved via the pull request process defined in `company-os.charter.md`.