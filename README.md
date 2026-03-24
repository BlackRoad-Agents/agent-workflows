# agent-workflows

Multi-step agent pipelines for BlackRoad OS. Chain agents together to complete complex tasks.

## What This Is

A workflow engine that defines and executes multi-step agent pipelines. Each workflow chains 2-3 agents together, passing the output of one step as input to the next. Workflows are defined in JSON and executed via the Python runner, which calls agents through Ollama.

## Requirements

- Python 3.6+
- Ollama running locally (or specify --host)
- curl

## Workflows

| ID | Name | Chain | Description |
|----|------|-------|-------------|
| plan-and-code | Plan and Code | scholar -> coder -> coder | Design, implement, review |
| research | Research and Write | scholar -> writer | Research then write article |
| debug | Debug Pipeline | coder -> coder -> coder | Diagnose, fix, test |
| content | Content Pipeline | writer -> writer | Draft then edit |
| security-audit | Security Audit | cipher -> cipher -> coder | Scan, prioritize, fix |
| onboard | Onboarding Guide | tutor -> tutor | Explain then FAQ |

## Usage

```bash
# List available workflows
python3 runner.py --list

# Run a workflow
python3 runner.py plan-and-code "Build a REST API for agent message routing"

# Verbose output (show full responses)
python3 runner.py research "The history of self-hosted infrastructure" --verbose

# Save execution log
python3 runner.py debug "Users report 502 errors on /api/chat after deploying v2.1" \
  --output debug-log.json

# Use different model
python3 runner.py security-audit "$(cat nginx.conf)" --model codellama
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `workflow` | (required) | Workflow ID to run |
| `input` | (required) | User input / task description |
| `--list` | false | List available workflows |
| `--workflows-file` | workflows.json | Path to workflow definitions |
| `--model` | llama3.2 | Ollama model for all steps |
| `--host` | http://localhost:11434 | Ollama API endpoint |
| `--output` | stdout | Output file for execution log |
| `--verbose` | false | Print full step outputs |

## Workflow Definition Format

```json
{
  "id": "my-workflow",
  "name": "My Workflow",
  "description": "What this workflow does",
  "steps": [
    {
      "step": 1,
      "agent": "scholar",
      "action": "research",
      "prompt_template": "Research this: {input}",
      "output_key": "research_notes"
    },
    {
      "step": 2,
      "agent": "writer",
      "action": "write",
      "prompt_template": "Write based on: {research_notes}",
      "output_key": "article"
    }
  ]
}
```

Templates use `{key}` placeholders. `{input}` is the user's original input. Each step's `output_key` becomes available to subsequent steps.

Part of BlackRoad-Agents. Remember the Road. Pave Tomorrow. Incorporated 2025.
