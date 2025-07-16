# Rules Service

This service is responsible for managing and validating the rules of the Company OS.

## Overview

The Rules Service provides the following capabilities:

- **Rule Discovery**: Scans the repository for `.rules.md` files.
- **Synchronization**: Keeps agent-specific rule folders in sync with the canonical rules.
- **Validation**: Validates markdown documents against the discovered rules.

## Setup

To use the Rules Service, you need to have Python 3.13+ and Bazel installed.

## Architecture

The Rules Service follows the Hexagonal Architecture pattern, with a core domain, ports, and adapters. This allows for a clean separation of concerns and makes the service easily testable and extensible.

## Development

To run the tests for the Rules Service, use the following command:

```bash
bazel test //os/domains/rules_service/...
```
