---
title: "Charter: The Knowledge Architecture"
version: 1.1
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-14T17:51:24-07:00"
parent_charter: "os/domains/charters/data/service-architecture.charter.md"
tags: ["charter", "knowledge", "architecture", "metadata", "graph", "decisions"]
---

# **Charter: The Knowledge Architecture**

This document defines the vision and principles for organizing all records, documents, and knowledge within the Company OS. It serves as the blueprint for our "Shared, Explicit Memory."

---

## **1. Vision (The North Star ⭐)**

To create a self-organizing, living knowledge graph that serves as the canonical memory for the entire Company OS. This graph will make all context discoverable, traceable, and intelligent for both human and AI collaborators, evolving from a simple file-based system into a rich, queryable network as the need emerges.

---

## **2. First Principles**

*This architecture is governed by the principles of its parent, `company-os.charter.md`, and is further guided by the following:*

1.  **Git as the Source of Truth**: The canonical state of all knowledge is its version-controlled representation in our Git repository. All dedicated services (databases, vector stores, etc.) are considered derivative, queryable caches of this truth, not the source itself.
2.  **Semantic, Not Hierarchical, Organization**: We organize knowledge by its meaning and relationships, not by its location in a folder. The system is a graph of interconnected concepts, not a tree of directories.
3.  **Atomicity & Addressability**: Each document should represent a single, atomic unit of knowledge (a process, a charter, a decision record). Every document must have a unique, stable address (`name.type.md`) that allows for persistent linking.
4.  **Structure Through Metadata**: Relationships, status, ownership, and other critical context are defined explicitly within a document's frontmatter. This metadata is the primary mechanism for building our knowledge graph.
5.  **Evolve on Demand**: We will start with the simplest possible implementation (markdown files in Git) and only introduce more complex systems (e.g., a graph database, a dedicated search service) when a measured pain point demonstrates a clear need that justifies the added complexity.

---

## **3. The Mental Model: The Knowledge Graph**

We think of our entire knowledge base as a graph, even in its initial file-based implementation.

* **Nodes**: Every `.md` file is a **node** in the graph, representing a single entity or concept.
* **Edges**: Hyperlinks between files (`[link](./other-file.md)`) and relational links in the frontmatter (`parent_charter: ...`) are the **edges** that connect the nodes.
* **Properties**: The YAML frontmatter of each file contains the **properties** of that node (its version, status, tags, etc.).

### **Special Node Types**

While all knowledge nodes are equal in the graph structure, certain types serve critical functions for system evolution:

* **Decision Records**: Capture the rationale, context, and consequences of system decisions. These nodes are essential for deterministic system understanding and self-evolution, as they preserve the "why" behind every choice and enable future reconstruction of decision paths.

This model allows us to reason about our knowledge systemically, paving the way for future automated discovery and analysis.

---

## **4. The Initial Implementation (Phase 0)**

The entire knowledge base will begin as a collection of markdown files within a single Git repository.

* **File Naming**: We will adhere to the `name.type.md` convention to make the purpose of any file immediately clear (e.g., `synapse.methodology.md`, `api-keys.spec.md`).
* **Frontmatter**: All documents MUST include a standardized frontmatter block to ensure they are discoverable and have essential properties.
* **Discovery**: Initial discovery will be handled by text search (e.g., `grep`, IDE search) and by following explicit links between documents.

---

## **5. The Evolution Path**

The system will evolve based on identified needs. Examples of evolutionary triggers include:

* If "finding all active specs owned by a specific team" becomes a common, slow task, we will create a project to ingest the frontmatter into a queryable database.
* If "finding conceptually similar documents" becomes a need, we will create a project to implement semantic search using vector embeddings of the markdown content.

In all cases, the Git repository remains the canonical source, and new services are built to ingest and index that data.

---

## **6. Process for Evolution**

This Charter is a living document. Changes must be proposed via pull request and adhere to the evolution process defined in the parent `company-os.charter.md`.
