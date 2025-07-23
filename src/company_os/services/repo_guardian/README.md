# Repo Guardian Service

An AI-powered Temporal workflow service that proactively maintains repository quality and manages complexity for the Company OS.

## Overview

Repo Guardian is a self-evolving workflow system that combines Temporal orchestration with AI analysis (OpenAI GPT-4 and Claude) to:

- Monitor repository changes and complexity
- Verify adherence to architectural patterns
- Generate actionable GitHub issues for improvements
- Emit operational metrics for continuous improvement
- Capture signals for system evolution

## Architecture

The service follows a hexagonal architecture pattern:

```
┌─────────────────────────────────────────────────────────────┐
│                        Temporal Worker                        │
├─────────────────────────────────────────────────────────────┤
│  Workflows                │  Activities                      │
│  - RepoGuardianWorkflow   │  - Repository operations        │
│                           │  - Code analysis                 │
│                           │  - LLM integration               │
│                           │  - GitHub integration            │
├─────────────────────────────────────────────────────────────┤
│  Adapters                                                    │
│  - OpenAI Client          │  - Anthropic Client              │
│  - GitHub Client          │  - Metrics Emitter               │
└─────────────────────────────────────────────────────────────┘
```

## Setup

### Prerequisites

- Python 3.12+
- Bazel 8.x
- Docker & Docker Compose
- Temporal CLI (optional)

### Environment Configuration

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Fill in your API credentials:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `ANTHROPIC_API_KEY`: Your Anthropic API key
   - `GITHUB_TOKEN`: GitHub personal access token with repo scope

### Running Locally

#### Option 1: Using Docker Compose (Recommended)

```bash
# Start Temporal and dependencies in detached mode
docker-compose up --detach

# Verify services are running
docker-compose ps

# Access Temporal UI
open http://localhost:8080

# View logs if needed
docker-compose logs -f temporal

# Stop services when done
docker-compose down
```

#### Option 2: Using Temporal CLI

```bash
# Install Temporal CLI
brew install temporal

# Start development server
temporal server start-dev

# UI available at http://localhost:8233
```

### Building with Bazel

```bash
# Build the service
bazel build //src/company_os/services/repo_guardian:repo_guardian

# Run the worker
bazel run //src/company_os/services/repo_guardian:worker
```

### Running with Python directly

```bash
# From repository root
python -m src.company_os.services.repo_guardian.worker_main
```

## Usage

### Starting a Workflow

```python
from temporalio.client import Client
from src.company_os.services.repo_guardian.models.domain import WorkflowInput

async def start_analysis():
    # Connect to Temporal
    client = await Client.connect("localhost:7233")

    # Define workflow input
    workflow_input = WorkflowInput(
        repository_url="https://github.com/org/repo",
        branch="main",
        analysis_depth="standard",
        create_issues=True
    )

    # Start workflow
    handle = await client.start_workflow(
        "RepoGuardianWorkflow",
        workflow_input,
        id=f"repo-guardian-{repo_name}-{timestamp}",
        task_queue="repo-guardian-task-queue"
    )

    # Get result
    result = await handle.result()
    print(f"Analysis complete: {result}")
```

### Workflow Parameters

- `repository_url`: GitHub repository URL to analyze
- `branch`: Branch to analyze (default: "main")
- `since_commit`: Starting commit SHA for incremental analysis (optional)
- `analysis_depth`: Analysis thoroughness - "light", "standard", or "deep"
- `create_issues`: Whether to create GitHub issues (default: true)
- `issue_labels`: Labels to apply to created issues

## Development

### Project Structure

```
repo_guardian/
├── workflows/          # Temporal workflow definitions
├── activities/         # Temporal activity implementations
├── adapters/          # External service integrations
├── models/            # Domain models and types
├── tests/             # Unit and integration tests
├── BUILD.bazel        # Bazel build configuration
└── worker_main.py     # Worker entry point
```

### Adding New Activities

1. Create activity function in appropriate module
2. Decorate with `@activity.defn(name="activity_name")`
3. Register in worker_main.py
4. Add to workflow orchestration

### Testing

```bash
# Run unit tests
bazel test //src/company_os/services/repo_guardian/tests:all

# Run integration tests
bazel test //src/company_os/services/repo_guardian/tests:integration_test
```

## Configuration

### Analysis Rules

The service uses configurable rules for analysis, stored in:
- `company_os/domains/rules/data/`

### Metrics

Prometheus metrics are exposed on port 9090 by default:
- `repo_guardian_workflow_duration_seconds`
- `repo_guardian_issues_created_total`
- `repo_guardian_llm_tokens_used_total`
- `repo_guardian_llm_cost_dollars_total`

## Troubleshooting

### Common Issues

1. **Temporal connection refused**
   - Ensure Temporal is running: `docker-compose ps`
   - Check logs: `docker-compose logs temporal`

2. **LLM API errors**
   - Verify API keys in `.env`
   - Check rate limits and quotas

3. **GitHub API errors**
   - Ensure token has required permissions
   - Check GitHub API rate limits

### Debug Mode

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
bazel run //src/company_os/services/repo_guardian:worker
```

## Contributing

Follow the Company OS development workflow:
1. Create feature branch from `main`
2. Make changes following existing patterns
3. Ensure tests pass
4. Submit PR with clear description

## License

Part of the Company OS - see root LICENSE file.

---

*Built with ❤️ following Company OS principles: explicit memory, continuous evolution, and human-AI partnership.*
