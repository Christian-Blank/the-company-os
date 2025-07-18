---
title: "Rule Set: The Knowledge System"
version: 2.1
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-17T15:59:58-07:00"
parent_charter: "os/domains/charters/data/knowledge-architecture.charter.md"
tags: ["rules", "knowledge", "documentation", "services", "maintenance"]
---

# **Rule Set: The Knowledge System**

This document provides the operational rules for all collaborators (human and AI) to create, maintain, and navigate the Company OS knowledge base. These rules operationalize the principles in the `knowledge-architecture.charter.md` within the context of the service-oriented architecture.

---

## **0. Core Principles (The Mental Model)**

These are the foundational mental models to hold when interacting with the knowledge system.

* **Rule 0.1: Documentation as Code.** All knowledge is version-controlled markdown that evolves with the system it documents. Documentation lives alongside code, not in separate systems.
* **Rule 0.2: Service Ownership.** Each service domain owns its documentation. Global documentation provides navigation and patterns, not duplication.
* **Rule 0.3: Audience-Specific Entry Points.** Create clear paths for users, developers, and LLM consumption. Same source, different presentations.
* **Rule 0.4: Practical Over Perfect.** Document what exists and works. Remove what doesn't. Evolution beats perfection.

---

## **1. Rules for Creating Documentation**

Follow these rules when adding documentation to the knowledge system.

* **Rule 1.1: Choose the Right Location.**
    * **Service-specific documentation**: Create in `/service_domain/docs/`
    * **Global documentation**: Create in `/docs/`
    * **Formal documents**: Use established patterns (`name.type.md`)
    * **Working documentation**: Use descriptive names (`getting-started.md`)

* **Rule 1.2: Follow Audience-Appropriate Patterns.**
    * **User documentation**: Focus on tasks and workflows
    * **Developer documentation**: Include examples and implementation details
    * **LLM documentation**: Optimize for context and patterns
    * **API documentation**: Use consistent structure and examples

* **Rule 1.3: Use Appropriate Frontmatter.** Include essential metadata:
    ```yaml
    ---
    title: "Clear, descriptive title"
    type: "guide|reference|api|overview"
    service: "service_name"  # if service-specific
    audience: ["users", "developers", "llm"]
    last_updated: "2025-07-16T15:35:00-07:00"
    tags: ["relevant", "searchable", "tags"]
    ---
    ```

* **Rule 1.4: Structure for Usability.**
    1. **Purpose**: What this document covers
    2. **Quick Start**: Immediate actionable information
    3. **Details**: Comprehensive information
    4. **Examples**: Working examples where applicable
    5. **References**: Links to related documentation

* **Rule 1.5: Verify Timestamps.** Always verify the current date and time before creating or updating documentation. Use ISO 8601 format with timezone information.

---

## **2. Rules for Maintaining Documentation**

Follow these rules for the lifecycle management of documentation.

* **Rule 2.1: Update with Changes.** Documentation updates are part of feature development. Code changes must include corresponding documentation updates.

* **Rule 2.2: Remove Obsolete Content.** Delete outdated documentation immediately. Git preserves history. Stale documentation is worse than no documentation.

* **Rule 2.3: Maintain Working Examples.** All examples must be tested and working. Broken examples destroy trust in documentation.

* **Rule 2.4: Review Documentation in Code Reviews.** Documentation changes are reviewed alongside code changes. Documentation quality is part of code quality.

* **Rule 2.5: Update Cross-References.** When changing document structure or location, update all references to maintain navigation integrity.

---

## **3. Rules for Service Documentation**

Follow these rules for service-specific documentation.

* **Rule 3.1: Create Service Documentation Structure.**
    ```
    /service_domain/docs/
    ├── README.md              # Service overview and quick start
    ├── api.md                 # API documentation
    ├── implementation.md      # Implementation details
    ├── patterns.md            # Service-specific patterns
    └── examples/              # Working examples
    ```

* **Rule 3.2: Maintain Service README.** Every service must have a clear README that covers:
    * Purpose and scope
    * Quick start instructions
    * Key concepts and terminology
    * Links to detailed documentation

* **Rule 3.3: Document Public APIs.** All public APIs must have documentation including:
    * Clear parameter descriptions
    * Return value specifications
    * Working examples
    * Error handling guidance

* **Rule 3.4: Include Implementation Guidance.** Document key implementation patterns, architectural decisions, and extension points for future developers.

---

## **4. Rules for Global Documentation**

Follow these rules for global documentation maintenance.

* **Rule 4.1: Maintain Navigation Hub.** The global `/docs/README.md` serves as the master navigation hub. Keep it current and organized.

* **Rule 4.2: Document Cross-Service Patterns.** Global documentation covers:
    * System architecture and service boundaries
    * Cross-service integration patterns
    * Development workflow and tooling
    * Testing and deployment patterns

* **Rule 4.3: Avoid Duplication.** Global documentation links to service documentation rather than duplicating it. Maintain single sources of truth.

* **Rule 4.4: Maintain LLM Context.** LLM-specific documentation must be kept current with system changes. Generate automatically where possible.

---

## **5. Rules for Extended Document Types**

Follow these rules for specialized document types beyond standard documentation.

* **Rule 5.1: Analysis Documents (`.analysis.md`)**
    * **Purpose**: System analysis, evaluations, and critical assessments
    * **Required Fields**: `title`, `version`, `status`, `owner`, `last_updated`, `parent_charter`, `tags`
    * **Structure**: Executive Summary, Context, Analysis sections, Conclusions/Recommendations
    * **Location**: Appropriate service domain `/data/` directory
    * **Naming**: `topic-name.analysis.md` (descriptive, hyphenated)

* **Rule 5.2: Paradigm Documents (`.paradigm.md`)**
    * **Purpose**: Foundational mental models and ways of thinking that underpin the system
    * **Required Fields**: `title`, `version`, `status`, `owner`, `last_updated`, `parent_charter`, `tags`
    * **Structure**: Core Concept, Mental Model, Applications, Examples, Boundaries
    * **Location**: `/company_os/domains/paradigms/data/`
    * **Naming**: `paradigm-name.paradigm.md` (descriptive, hyphenated)

* **Rule 5.3: Principle Documents (`.principle.md`)**
    * **Purpose**: Deep-dive explanations of First Principles stated in charters
    * **Required Fields**: `title`, `version`, `status`, `owner`, `last_updated`, `parent_charter`, `tags`
    * **Structure**: Principle Statement, Rationale, Applications, Examples, Boundaries
    * **Location**: `/company_os/domains/principles/data/`
    * **Naming**: `principle-name.principle.md` (descriptive, hyphenated)

* **Rule 5.4: Workflow Documents (`.workflow.md`)**
    * **Purpose**: Step-by-step, executable procedures for specific tasks
    * **Required Fields**: `title`, `version`, `status`, `owner`, `last_updated`, `parent_charter`, `tags`
    * **Structure**: Overview, Phases with sequential steps, Examples, Success Metrics
    * **Location**: `/company_os/domains/workflows/data/`
    * **Naming**: `workflow-name.workflow.md` (descriptive, hyphenated)

* **Rule 5.5: Validation Requirements**
    * All extended document types must include complete frontmatter
    * All must link to their governing charter via `parent_charter` field
    * All must use proper timestamp format: ISO 8601 with timezone
    * All must include appropriate tags for discoverability

---

## **6. Rules for LLM Context Management**

Follow these rules for LLM-optimized documentation.

* **Rule 6.1: Generate from Canonical Sources.** LLM context documents are generated from the same sources as human documentation. Maintain consistency.

* **Rule 6.2: Include Essential Context.** LLM context must include:
    * System architecture and service boundaries
    * Key patterns and principles
    * Development workflow and tooling
    * Current project status and priorities

* **Rule 6.3: Optimize for Development Workflow.** LLM context should enable efficient development collaboration. Include practical examples and patterns.

* **Rule 6.4: Maintain Context Consistency.** Ensure LLM context remains consistent across development sessions. Update incrementally rather than recreating.

---

## **7. Rules for Documentation Quality**

Follow these rules to maintain high documentation quality.

* **Rule 7.1: Test Documentation.** All procedural documentation must be tested by following the documented steps. Verify examples work.

* **Rule 7.2: Write for Your Audience.** Match language, detail level, and examples to the target audience. User docs differ from developer docs.

* **Rule 7.3: Measure Documentation Success.** Track metrics:
    * Time to find information
    * Task completion success rate
    * Documentation accuracy and completeness
    * User satisfaction with documentation

* **Rule 7.4: Iterate Based on Usage.** Improve documentation based on actual usage patterns and feedback. Document what people actually need.

---

## **8. Rules for System Evolution**

Follow these rules to ensure the knowledge system evolves effectively.

* **Rule 8.1: Evolve Documentation Patterns.** When establishing new documentation patterns:
    1. Test with real usage
    2. Document the pattern
    3. Update these rules if needed
    4. Migrate existing documentation gradually

* **Rule 8.2: Maintain Backward Compatibility.** Changes to documentation structure must maintain navigation and reference integrity.

* **Rule 8.3: Automate Where Possible.** Automate documentation generation, validation, and maintenance where it improves consistency without sacrificing quality.

* **Rule 8.4: Update These Rules.** This rule set is a living document. Changes must follow the standard Charter evolution process defined in the parent `knowledge-architecture.charter.md`.

---

## **9. Implementation Guidelines**

### **For Service Teams**
1. Create and maintain service documentation following Rule 3 patterns
2. Update documentation as part of development workflow
3. Include working examples and clear API documentation
4. Review documentation changes in code reviews

### **For Global Documentation Maintainers**
1. Focus on navigation and cross-service patterns
2. Maintain clear entry points for different audiences
3. Avoid duplicating service-specific information
4. Regularly review and update global documentation

### **For LLM Context Management**
1. Generate context from canonical documentation sources
2. Include essential system context and development patterns
3. Maintain consistency across development sessions
4. Optimize for development workflow efficiency

---

## **10. Success Metrics**

* **Discoverability**: Time to find relevant information
* **Accuracy**: Documentation matches current implementation
* **Completeness**: Coverage of user and developer needs
* **Maintainability**: Effort required to keep documentation current
* **Usability**: User success rate in accomplishing documented tasks
