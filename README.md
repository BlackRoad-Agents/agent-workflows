<!-- BlackRoad SEO Enhanced -->

# agent workflows

> Part of **[BlackRoad OS](https://blackroad.io)** — Sovereign Computing for Everyone

[![BlackRoad OS](https://img.shields.io/badge/BlackRoad-OS-ff1d6c?style=for-the-badge)](https://blackroad.io)
[![BlackRoad Agents](https://img.shields.io/badge/Org-BlackRoad-Agents-2979ff?style=for-the-badge)](https://github.com/BlackRoad-Agents)
[![License](https://img.shields.io/badge/License-Proprietary-f5a623?style=for-the-badge)](LICENSE)

**agent workflows** is part of the **BlackRoad OS** ecosystem — a sovereign, distributed operating system built on edge computing, local AI, and mesh networking by **BlackRoad OS, Inc.**

## About BlackRoad OS

BlackRoad OS is a sovereign computing platform that runs AI locally on your own hardware. No cloud dependencies. No API keys. No surveillance. Built by [BlackRoad OS, Inc.](https://github.com/BlackRoad-OS-Inc), a Delaware C-Corp founded in 2025.

### Key Features
- **Local AI** — Run LLMs on Raspberry Pi, Hailo-8, and commodity hardware
- **Mesh Networking** — WireGuard VPN, NATS pub/sub, peer-to-peer communication
- **Edge Computing** — 52 TOPS of AI acceleration across a Pi fleet
- **Self-Hosted Everything** — Git, DNS, storage, CI/CD, chat — all sovereign
- **Zero Cloud Dependencies** — Your data stays on your hardware

### The BlackRoad Ecosystem
| Organization | Focus |
|---|---|
| [BlackRoad OS](https://github.com/BlackRoad-OS) | Core platform and applications |
| [BlackRoad OS, Inc.](https://github.com/BlackRoad-OS-Inc) | Corporate and enterprise |
| [BlackRoad AI](https://github.com/BlackRoad-AI) | Artificial intelligence and ML |
| [BlackRoad Hardware](https://github.com/BlackRoad-Hardware) | Edge hardware and IoT |
| [BlackRoad Security](https://github.com/BlackRoad-Security) | Cybersecurity and auditing |
| [BlackRoad Quantum](https://github.com/BlackRoad-Quantum) | Quantum computing research |
| [BlackRoad Agents](https://github.com/BlackRoad-Agents) | Autonomous AI agents |
| [BlackRoad Network](https://github.com/BlackRoad-Network) | Mesh and distributed networking |
| [BlackRoad Education](https://github.com/BlackRoad-Education) | Learning and tutoring platforms |
| [BlackRoad Labs](https://github.com/BlackRoad-Labs) | Research and experiments |
| [BlackRoad Cloud](https://github.com/BlackRoad-Cloud) | Self-hosted cloud infrastructure |
| [BlackRoad Forge](https://github.com/BlackRoad-Forge) | Developer tools and utilities |

### Links
- **Website**: [blackroad.io](https://blackroad.io)
- **Documentation**: [docs.blackroad.io](https://docs.blackroad.io)
- **Chat**: [chat.blackroad.io](https://chat.blackroad.io)
- **Search**: [search.blackroad.io](https://search.blackroad.io)

---


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
