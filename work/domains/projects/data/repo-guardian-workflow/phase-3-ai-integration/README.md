---
title: "Phase 3: AI Integration"
phase_number: 3
status: "Not Started"
duration: "1 week"
parent_project: "../../repo-guardian-workflow.vision.md"
last_updated: "2025-07-22T13:48:00-07:00"
tags: ["phase", "ai", "llm", "openai", "anthropic"]
---

# Phase 3: AI Integration

Implement LLM adapters with structured outputs and cost optimization for intelligent repository analysis.

## Phase Overview

**Duration:** 1 week
**Start Date:** TBD
**End Date:** TBD
**Status:** Not Started
**Owner:** @christian
**Prerequisites:** Phase 2 completed

## Objectives

1. Build adapters for OpenAI and Claude APIs
2. Implement structured JSON output enforcement
3. Optimize token usage with diff-based prompts
4. Create intelligent analysis capabilities

## Task Checklist

### LLM Adapters
- [ ] **OpenAI Adapter (`adapters/openai.py`)**
  - [ ] Implement client initialization with retry logic
  - [ ] Create structured output wrapper using JSON mode
  - [ ] Add token counting and cost tracking
  - [ ] Implement rate limiting
  - [ ] Add fallback for API errors
  - [ ] Support GPT-4.1 model

- [ ] **Claude Adapter (`adapters/claude.py`)**
  - [ ] Implement Anthropic client setup
  - [ ] Create structured output using XML/JSON
  - [ ] Add token management
  - [ ] Implement rate limiting
  - [ ] Add error handling
  - [ ] Support Claude 4 Opus/Sonnet

- [ ] **Claude Adapter (`adapters/gemini.py`)**
  - [ ] Implement Google GenAI client setup
  - [ ] Create structured output using XML/JSON
  - [ ] Add token management
  - [ ] Implement rate limiting
  - [ ] Add error handling
  - [ ] Support Gemini 2.5Pro and 2.5 Flash

- [ ] **Adapter Interface**
  - [ ] Define common LLM interface
  - [ ] Standardize request/response models
  - [ ] Create adapter factory pattern
  - [ ] Enable easy provider switching

### Prompt Engineering
- [ ] **Analysis Prompts**
  - [ ] Code complexity analysis prompt
  - [ ] Pattern compliance verification prompt
  - [ ] Documentation quality assessment prompt
  - [ ] Issue generation prompt
  - [ ] Summary generation prompt

- [ ] **Prompt Optimization**
  - [ ] Use diff-based context to minimize tokens
  - [ ] Implement prompt templates with variables
  - [ ] Create few-shot examples for consistency
  - [ ] Add system prompts for role definition

### Structured Output
- [ ] **JSON Schema Definition**
  - [ ] Define schemas for each analysis type:
    ```python
    class ComplexityAnalysis(BaseModel):
        files: List[FileComplexity]
        overall_score: float
        recommendations: List[str]
        critical_issues: List[Issue]
    ```
  - [ ] Validate outputs against schemas
  - [ ] Handle malformed responses gracefully

- [ ] **Output Parsing**
  - [ ] Implement JSON extraction from responses
  - [ ] Add validation and error correction
  - [ ] Create fallback parsing strategies
  - [ ] Log parsing failures for debugging

### Cost Optimization
- [ ] **Token Management**
  - [ ] Implement token counting before requests
  - [ ] Set token budgets per analysis type
  - [ ] Track cumulative usage
  - [ ] Alert on budget overruns

- [ ] **Context Optimization**
  - [ ] Use git diffs instead of full files
  - [ ] Implement sliding window for large diffs
  - [ ] Cache repeated analysis patterns
  - [ ] Batch similar requests when possible

### Integration with Activities
- [ ] **Update LLM Activities**
  - [ ] Integrate adapters into `activities/llm.py`
  - [ ] Add provider selection logic
  - [ ] Implement fallback between providers
  - [ ] Add comprehensive logging

- [ ] **Error Handling**
  - [ ] Handle rate limits with backoff
  - [ ] Retry transient errors
  - [ ] Fail gracefully on persistent errors
  - [ ] Log all LLM interactions for debugging

### Testing
- [ ] **Unit Tests**
  - [ ] Test adapter initialization
  - [ ] Test structured output parsing
  - [ ] Test error handling scenarios
  - [ ] Mock API responses

- [ ] **Integration Tests**
  - [ ] Test with real API calls (limited)
  - [ ] Verify output schema compliance
  - [ ] Test provider switching
  - [ ] Measure token usage accuracy

## Deliverables

1. **Working LLM Adapters** - Both OpenAI and Claude functional
2. **Structured Output System** - Reliable JSON responses
3. **Optimized Prompts** - Token-efficient analysis
4. **Cost Tracking** - Usage metrics and budgets
5. **Test Coverage** - Comprehensive adapter tests

## Success Criteria

- [ ] Both LLM providers successfully analyze code
- [ ] 95%+ structured output parsing success rate
- [ ] Token usage 50% lower than naive approach
- [ ] Cost tracking accurate within 5%
- [ ] Graceful handling of API failures

## Technical Decisions

### Provider Selection
- Default to GPT-4.1 for code analysis
- Default to GPT o3 for pattern analysis
- Default to Gemini 2.5Pro for documentation analysis
- Default to Claude Opus generating final analysis reports
- Allow configuration override

### Output Format
- Always request JSON output
- Use Pydantic for validation
- Fail fast on schema violations

### Cost Controls
- Hard limit: 10k tokens per file
- Soft warning: 5k tokens per file
- Monthly budget tracking

## Next Phase

Upon completion, proceed to [Phase 4: GitHub Integration](../phase-4-github-integration/README.md)

---

*AI integration implements "Cost-Conscious AI" principle: smart context management for sustainable operations.*
