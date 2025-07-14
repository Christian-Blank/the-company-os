---
title: "Rule Set: The Knowledge System"
version: 1.0
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-14T14:32:54-07:00"
parent_charter: "knowledge-architecture.charter.md"
tags: ["rules", "knowledge", "metadata", "governance", "best-practices"]
---

# **Rule Set: The Knowledge System**

This document provides the v0 rule set for all collaborators (human and AI) to create, maintain, and navigate the Company OS knowledge base. These rules operationalize the principles in the `knowledge-architecture.charter.md`.

---

## **0. Core Principles (The Mental Model)**

These are the foundational mental models to hold when interacting with the knowledge system.

* **Rule 0.1: Think Graph, Not Folders.** Every document is a node in a web of knowledge. Its location in a directory is secondary to its explicit links and metadata.
* **Rule 0.2: Git is the Single Source of Truth.** The version-controlled markdown file is the canonical record. All other databases or views are derivative.
* **Rule 0.3: Every Document is an Atomic Node.** A document should represent one primary concept and be explicitly connected to the graph.

---

## **1. Rules for Creating Documents**

Follow these rules when adding a new node to the knowledge graph.

* **Rule 1.1: One Document, One Concept.** A new document should focus on a single, atomic purpose (e.g., one charter, one methodology, one spec). If a document grows too complex, it must be broken into smaller, linked documents.
* **Rule 1.2: Follow the Naming Convention.** All files must be named using the `name.type.md` format.
    * **Known Types (v1.0):** `charter`, `methodology`, `rules`, `principle`, `vision`, `spec`, `brief`.
    * *Example:* `synapse.methodology.md`
* **Rule 1.3: All Documents MUST Have Standard Frontmatter.** This metadata is how we build the graph. Every document must begin with a YAML frontmatter block containing at least these keys:
    * `title`: (string) The human-readable title.
    * `version`: (string) e.g., "1.0".
    * `status`: (string) e.g., "Draft", "Active", "Deprecated", "Archived".
    * `owner`: (string) The team or individual responsible.
    * `last_updated`: (string) ISO 8601 timestamp.
    * `parent_charter`: (string) The filename of the direct parent Charter governing this document. `null` only for the root charter.
    * `tags`: (array of strings) Lowercase keywords for discovery.
* **Rule 1.4: Link Explicitly.** Every new document must link to its `parent_charter`. Where relevant, it should also include hyperlinks to other related documents within its body or frontmatter to strengthen the graph.

---

## **2. Rules for Maintaining Documents**

Follow these rules for the lifecycle management of existing nodes.

* **Rule 2.1: Updates Require Versioning.** When a document's content is changed, its `version` and `last_updated` fields in the frontmatter MUST be updated. Use semantic versioning (e.g., `1.1` for minor additions, `2.0` for breaking changes).
* **Rule 2.2: Revise & Delete, Don't Deprecate or Archive.** History is preserved in git. Outdated versions can lead to large contexts and overwhelment. If something is not needed, radically delete, if something is outdated, revise immediatelly. Every rule has an exception. Only deprecate or archive when there is a really good reason - for example project tickets or any other history that should be visibly preserved compared to stored behind a git layer.
* **Rule 2.3: Maintain Link Integrity.** When editing a document, you are responsible for verifying that the links within it still point to relevant and active documents.

---

## **3. Rules for Navigating & Finding Documents**

Follow these rules to discover knowledge within the graph.

* **Rule 3.1: Start from the Root.** The primary entry point for navigation is always the `company-os.charter.md`.
* **Rule 3.2: Navigate via Parent Charters.** The `parent_charter` links form the primary hierarchy of the system. Follow them "up" to understand context and "down" to find specifics.
* **Rule 3.3: Discover via Tags.** To find related concepts across different branches of the hierarchy, use text search on the `tags` in the frontmatter (e.g., search for files with the "governance" tag).

---

## **4. Rules for System Evolution**

Follow these rules to ensure the knowledge system itself evolves gracefully and avoids entropy.

* **Rule 4.1: Proposing a New Document Type.** If a new, recurring type of document is needed, you must propose an update to this rule set. The process is:
    1.  Create a `Signal Record` identifying the need.
    2.  Synthesize the need into an `Opportunity Brief`.
    3.  If approved, create a pull request to amend **Rule 1.2** in *this document* (`knowledge-system.rules.md`) to include the new type.
* **Rule 4.2: Updating These Rules.** This rule set is a living document. Any proposed changes must follow the standard Charter evolution process (pull request, approvals) as defined in its parent, the `knowledge-architecture.charter.md`.