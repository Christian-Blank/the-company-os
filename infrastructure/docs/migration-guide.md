---
title: "Migration Guide: Service-Oriented Architecture"
version: 1.0
status: "Draft"
owner: "OS Core Team"
last_updated: "2025-07-14T16:53:00-07:00"
parent_charter: "os/domains/charters/data/repository-architecture.charter.md"
tags: ["migration", "guide", "services", "refactoring", "transition"]
---

# **Migration Guide: Service-Oriented Architecture**

This guide provides step-by-step instructions for migrating the current repository to the new service-oriented architecture defined in the updated charters.

---

## **1. Overview of Changes**

### New Charter Hierarchy
- Added `service-architecture.charter.md` as a child of `company-os.charter.md`
- Updated `repository-architecture.charter.md` (v2.0) as a child of service architecture
- Updated `knowledge-architecture.charter.md` to have service architecture as parent

### New Rules Documents
- `service-system.rules.md` - Rules for service domains
- `repository-system.rules.md` - Rules for file organization
- Updated `knowledge-system.rules.md` (v1.1) - Added service context

### Repository Structure Change
From flat files to service domains:
```
# Current Structure
/
├── *.charter.md
├── *.methodology.md
├── *.rules.md
└── /projects/

# New Structure
/os/domains/{service}/data/
/work/domains/{service}/data/
/products/{product}/domains/{service}/data/
/shared/
/infrastructure/
```

---

## **2. Migration Steps**

### Phase 1: Create Directory Structure

```bash
# Create OS service domains
mkdir -p os/domains/charters/data
mkdir -p os/domains/processes/data
mkdir -p os/domains/knowledge/data
mkdir -p os/domains/evolution/data
mkdir -p os/domains/configuration/data
mkdir -p os/domains/registry/data

# Create Work service domains
mkdir -p work/domains/projects/data
mkdir -p work/domains/signals/data
mkdir -p work/domains/briefs/data
mkdir -p work/domains/decisions/data

# Create shared directories
mkdir -p shared/schemas
mkdir -p shared/libraries
mkdir -p shared/mcp-servers

# Create infrastructure
mkdir -p infrastructure/environments
mkdir -p infrastructure/scripts
```

### Phase 2: File Migration Map

| Current Location | New Location |
|-----------------|--------------|
| `company-os.charter.md` | `/os/domains/charters/data/company-os.charter.md` |
| `service-architecture.charter.md` | `/os/domains/charters/data/service-architecture.charter.md` |
| `repository-architecture.charter.md` | `/os/domains/charters/data/repository-architecture.charter.md` |
| `knowledge-architecture.charter.md` | `/os/domains/charters/data/knowledge-architecture.charter.md` |
| `brand.charter.md` | `/os/domains/charters/data/brand.charter.md` |
| `synapse.methodology.md` | `/os/domains/processes/data/synapse.methodology.md` |
| `*.rules.md` | Domain-specific `/docs/` directories |
| `/projects/*.vision.md` | `/work/domains/projects/data/` |

### Phase 3: Update References

After moving files, update all internal references:
1. Update relative paths to absolute paths from repository root
2. Update parent_charter references if paths changed
3. Update any documentation that references old paths

### Phase 4: Create Service Registry

Create `/os/domains/registry/data/services.registry.md`:
```markdown
---
title: "Service Registry"
version: 1.0
status: "Active"
owner: "OS Core Team"
last_updated: "2025-07-14"
parent_charter: "service-architecture.charter.md"
tags: ["registry", "services", "directory"]
---

# Service Registry

## OS Services
- **charters**: Charter management (Stage 0)
- **processes**: Process/workflow management (Stage 0)
- **knowledge**: Knowledge graph (Stage 0)
- **evolution**: System improvement (Stage 0)
- **configuration**: Configuration management (Stage 0)
- **registry**: This service registry (Stage 0)

## Work Services
- **projects**: Project management (Stage 0)
- **signals**: Signal capture (Stage 0)
- **briefs**: Opportunity briefs (Stage 0)
- **decisions**: Decision records (Stage 0)
```

---

## **3. Migration Commands**

```bash
# Example migration commands (adjust paths as needed)
git mv company-os.charter.md os/domains/charters/data/
git mv service-architecture.charter.md os/domains/charters/data/
git mv repository-architecture.charter.md os/domains/charters/data/
git mv knowledge-architecture.charter.md os/domains/charters/data/
git mv brand.charter.md os/domains/charters/data/
git mv synapse.methodology.md os/domains/processes/data/
git mv projects/*.vision.md work/domains/projects/data/

# Move rules to appropriate docs directories
git mv knowledge-system.rules.md os/domains/knowledge/docs/
git mv service-system.rules.md os/domains/charters/docs/
git mv repository-system.rules.md os/domains/charters/docs/
```

---

## **4. Post-Migration Checklist**

- [x] All files moved to correct service domains
- [x] Git history preserved using `git mv`
- [x] All internal links updated
- [x] Service registry created
- [x] README.md updated with new structure
- [x] Migration guide moved to `/infrastructure/docs/`
- [x] Commit with clear migration message

---

## **5. Future Evolution Path**

Once files are migrated, services can evolve independently:
1. **Stage 0** (Current): Direct file manipulation
2. **Stage 1**: Add API definitions and MCP servers
3. **Stage 2**: Add local database caching
4. **Stage 3**: Add external adapters (GitHub, etc.)
5. **Stage 4**: Full platform migration

Each service evolves based on actual friction and need, not predetermined timeline.
