#!/usr/bin/env python3
"""
BlackRoad Workflow Runner
Executes multi-step agent workflows by chaining Ollama calls.
"""

import json
import sys
import subprocess
import argparse
import time
from datetime import datetime


DEFAULT_MODEL = "llama3.2"
OLLAMA_HOST = "http://localhost:11434"

PERSONAS = {
    "road": "You are Road, the fleet commander of BlackRoad OS. Coordinate and delegate.",
    "coder": "You are Coder, a software engineer. Write clean, production-ready code with error handling.",
    "scholar": "You are Scholar, a researcher. Provide thorough, evidence-based analysis.",
    "pascal": "You are Pascal, a mathematician. Be rigorous and precise in proofs and calculations.",
    "writer": "You are Writer, a content creator. Write concisely with clear structure.",
    "cipher": "You are Cipher, a security specialist. Think about threats, vulnerabilities, and defenses.",
    "tutor": "You are Tutor, an educator. Explain clearly for beginners, use analogies.",
    "alice": "You are Alice, a network specialist. Think in packets, routes, and uptime.",
    "cecilia": "You are Cecilia, an AI inference specialist. Think about models and compute.",
    "octavia": "You are Octavia, a DevOps engineer. Think about pipelines and reliability.",
    "lucidia": "You are Lucidia, a web hosting specialist. Serve content reliably.",
    "aria": "You are Aria, a monitoring specialist. Watch systems and detect anomalies.",
}


def query_ollama(model, system_prompt, user_prompt, host=OLLAMA_HOST):
    """Query Ollama and return response text."""
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False
    })

    try:
        result = subprocess.run(
            ["curl", "-s", "-X", "POST", f"{host}/api/chat",
             "-H", "Content-Type: application/json",
             "-d", payload],
            capture_output=True, text=True, timeout=180
        )
        if result.returncode != 0:
            return None, f"curl failed: {result.stderr.strip()}"

        data = json.loads(result.stdout)
        content = data.get("message", {}).get("content", "")
        return content, None
    except subprocess.TimeoutExpired:
        return None, "Timeout after 180s"
    except json.JSONDecodeError:
        return None, "Invalid JSON from Ollama"
    except Exception as e:
        return None, str(e)


def load_workflows(filepath="workflows.json"):
    """Load workflow definitions from JSON file."""
    with open(filepath) as f:
        data = json.load(f)
    return {w["id"]: w for w in data.get("workflows", [])}


def resolve_template(template, context):
    """Replace {key} placeholders in template with context values."""
    result = template
    for key, value in context.items():
        result = result.replace("{" + key + "}", str(value))
    return result


def run_workflow(workflow, user_input, model=DEFAULT_MODEL, host=OLLAMA_HOST, verbose=False):
    """
    Execute a workflow by running each step sequentially.

    Args:
        workflow: Workflow definition dict
        user_input: The initial user input/request
        model: Ollama model to use
        host: Ollama API host
        verbose: Print full responses

    Returns:
        Execution result dict with all step outputs
    """
    print(f"\n=== Workflow: {workflow['name']} ===")
    print(f"    {workflow['description']}")
    print(f"    Steps: {len(workflow['steps'])}")
    print(f"    Model: {model}\n")

    context = {"input": user_input}
    step_results = []
    start_time = time.time()

    for step_def in workflow["steps"]:
        step_num = step_def["step"]
        agent_id = step_def["agent"]
        action = step_def["action"]
        template = step_def["prompt_template"]
        output_key = step_def["output_key"]

        print(f"  Step {step_num}: [{agent_id}] {action}...")

        # Resolve the prompt template with current context
        prompt = resolve_template(template, context)
        persona = PERSONAS.get(agent_id, "You are a helpful assistant.")

        step_start = time.time()
        response, error = query_ollama(model, persona, prompt, host)
        step_latency = round(time.time() - step_start, 2)

        if error:
            print(f"    ERROR: {error}")
            step_results.append({
                "step": step_num,
                "agent": agent_id,
                "action": action,
                "status": "error",
                "error": error,
                "latency_seconds": step_latency
            })
            # Stop workflow on error
            break

        # Store output in context for next steps
        context[output_key] = response

        word_count = len(response.split()) if response else 0
        print(f"    Done ({word_count} words, {step_latency}s)")

        if verbose and response:
            preview = response[:500]
            if len(response) > 500:
                preview += "..."
            print(f"    ---\n    {preview}\n    ---")

        step_results.append({
            "step": step_num,
            "agent": agent_id,
            "action": action,
            "output_key": output_key,
            "status": "success",
            "word_count": word_count,
            "latency_seconds": step_latency
        })

    total_time = round(time.time() - start_time, 2)
    success = all(s["status"] == "success" for s in step_results)

    print(f"\n  {'COMPLETED' if success else 'FAILED'} in {total_time}s")

    execution = {
        "workflow_id": workflow["id"],
        "workflow_name": workflow["name"],
        "input": user_input,
        "model": model,
        "started_at": datetime.utcnow().isoformat() + "Z",
        "total_seconds": total_time,
        "status": "success" if success else "error",
        "steps": step_results,
        "outputs": {k: v for k, v in context.items() if k != "input"}
    }

    return execution


def list_workflows(workflows):
    """Print available workflows."""
    print("\nAvailable workflows:\n")
    print(f"  {'ID':<20} {'Name':<25} {'Steps':>5}  Description")
    print("  " + "-" * 80)
    for wf in workflows.values():
        step_agents = " -> ".join(s["agent"] for s in wf["steps"])
        print(f"  {wf['id']:<20} {wf['name']:<25} {len(wf['steps']):>5}  {wf['description']}")
        print(f"  {'':20} Chain: {step_agents}")
    print()


def main():
    parser = argparse.ArgumentParser(description="BlackRoad Workflow Runner")
    parser.add_argument("workflow", nargs="?", help="Workflow ID to run")
    parser.add_argument("input", nargs="?", help="User input for the workflow")
    parser.add_argument("--list", action="store_true", help="List available workflows")
    parser.add_argument("--workflows-file", default="workflows.json",
                        help="Path to workflows.json")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help="Ollama model to use")
    parser.add_argument("--host", default=OLLAMA_HOST,
                        help="Ollama API host")
    parser.add_argument("--output", default=None,
                        help="Output file for JSON execution log")
    parser.add_argument("--verbose", action="store_true",
                        help="Print full step outputs")

    args = parser.parse_args()

    try:
        workflows = load_workflows(args.workflows_file)
    except FileNotFoundError:
        print(f"Error: '{args.workflows_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{args.workflows_file}'.", file=sys.stderr)
        sys.exit(1)

    if args.list or not args.workflow:
        list_workflows(workflows)
        if not args.workflow:
            print("Usage: python3 runner.py <workflow-id> \"<your input>\"")
        sys.exit(0)

    if args.workflow not in workflows:
        print(f"Error: Unknown workflow '{args.workflow}'.", file=sys.stderr)
        print(f"Available: {', '.join(workflows.keys())}", file=sys.stderr)
        sys.exit(1)

    if not args.input:
        print("Error: Input required. Provide the task description.", file=sys.stderr)
        sys.exit(1)

    workflow = workflows[args.workflow]
    result = run_workflow(
        workflow,
        args.input,
        model=args.model,
        host=args.host,
        verbose=args.verbose
    )

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\nExecution log saved to {args.output}")


if __name__ == "__main__":
    main()
