---
title: "Repo Guardian Adapters"
parent: "../README.md"
tags: ["adapters", "integration", "repo-guardian"]
---

# Repo Guardian Adapters

This directory contains adapter implementations for external service integrations.

## Overview

Adapters implement the ports defined by the domain layer, providing concrete implementations for external services. This follows the hexagonal architecture pattern.

## Planned Adapters (Phase 3)

### github.py
GitHub API integration:
- Repository operations
- Issue creation and management
- Pull request interactions
- Webhook handling

### openai.py
OpenAI GPT integration:
- Code analysis prompts
- Issue generation
- Structured output parsing
- Token management

### claude.py
Anthropic Claude integration:
- Alternative AI provider
- Specialized analysis tasks
- Cross-validation with GPT
- Cost optimization

### metrics.py
Metrics and monitoring:
- Prometheus metrics export
- Custom metric definitions
- Performance tracking
- Cost tracking

## Adapter Pattern

```python
# Port (defined in domain)
class LLMPort(Protocol):
    async def analyze_code(self, code: str, context: Context) -> Analysis:
        ...

# Adapter (implements port)
class OpenAIAdapter:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    async def analyze_code(self, code: str, context: Context) -> Analysis:
        # OpenAI-specific implementation
        response = await self.client.chat.completions.create(...)
        return self._parse_response(response)
```

## Configuration

Adapters are configured via environment variables:
- `GITHUB_TOKEN`: GitHub API authentication
- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Claude API key
- `PROMETHEUS_PORT`: Metrics endpoint port

## Testing

Adapters should be tested with:
- Unit tests with mocked external services
- Integration tests (using test accounts)
- Contract tests for port compliance
- Performance tests for rate limits

## Development Status

**Current**: Placeholder directory (Phase 1)
**Next**: Implementation in Phase 3 after core workflow is complete

---

*Part of the Repo Guardian service following hexagonal architecture principles.*
