---
title: "Rules Service Boundaries"
version: 1.0
status: "Active"
owner: "Christian Blank"
last_updated: "2025-07-16T12:00:00-07:00"
parent_charter: "../../charters/data/rules-service.charter.md"
tags: ["rules-service", "boundaries", "architecture"]
---

# Rules Service Boundaries

This document defines the boundaries and responsibilities of the Rules Service.

## The Rules Service Owns:

- **Rule Discovery**: Finding and parsing all `.rules.md` files across the repository.
- **Rule Distribution**: Synchronizing canonical rules to agent-specific folders (e.g., for IDEs, CLIs).
- **Document Validation**: Validating markdown documents against the logic defined in the discovered rules.
- **Validation Rule Extraction**: Deriving validation logic from the templates and patterns within rule files.

## The Rules Service Does NOT Own:

- **Rule Creation**: The content and business logic of rules are authored manually by domain experts.
- **Rule Content**: The semantic meaning of the rules themselves.
- **Document Storage**: Documents remain in their respective service domains; the Rules Service reads them but does not own their storage.
- **Fix Application**: The service can suggest fixes (e.g., via auto-fix or human-in-the-loop comments), but the user or another automated process is responsible for applying them.
