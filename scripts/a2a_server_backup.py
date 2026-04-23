#!/usr/bin/env python3
"""A2A Protocol Server - All 21 Agents"""

import json
import subprocess
import sys
from agents.webclaw.agent_handler import process_task
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).resolve().parent

AGENTS = {
    "llmclaw": {
        "description": "Model selection and management",
        "script": "agents/llmclaw/llmclaw.py",
        "cmd_prefix": []
    },
    "liberateclaw": {
        "description": "LLM Model Liberation",
        "script": "agents/liberateclaw/liberateclaw.py",
        "cmd_prefix": ["obliterate"]
    },
    "flowclaw": {
        "description": "AI-powered diagram generator",
        "script": "agents/flowclaw/flowclaw.py",
        "cmd_prefix": ["view", "flowchart"]
    },
    "designclaw": {
        "description": "Graphic design and logos",
        "script": "agents/designclaw/designclaw.py",
        "cmd_prefix": ["logo"]
    },
    "draftclaw": {
        "description": "Technical drawings and blueprints",
        "script": "agents/draftclaw/draftclaw.py",
        "cmd_prefix": ["blueprint"]
    },
    "drawclaw": {
        "description": "Drawing and sketching",
        "script": "agents/drawclaw/drawclaw.py",
        "cmd_prefix": ["draw"]
    },
    "dreamclaw": {
        "description": "AI vision and generation",
        "script": "agents/dreamclaw/dreamclaw.py",
        "cmd_prefix": ["dream"]
    },
    "plotclaw": {
        "description": "Charts and graphs",
        "script": "agents/plotclaw/plotclaw.py",
        "cmd_prefix": ["plot"]
    },
    "docuclaw": {
        "description": "AI-powered document processor",
        "script": "agents/docuclaw/docuclaw.py",
        "cmd_prefix": ["create", "letter"]
    },
    "dataclaw": {
        "description": "Data analysis and local references",
        "script": "agents/dataclaw/dataclaw.py",
        "cmd_prefix": ["search"]
    },
    "webclaw": {
        "description": "Web search and indexing",
        "script": "agents/webclaw/webclaw.py",
        "cmd_prefix": ["search"]
    },
    "mathematicaclaw": {
        "description": "AI-powered mathematics solver",
        "script": "agents/mathematicaclaw/mathematicaclaw.py",
        "cmd_prefix": ["solve"]
    },
    "fileclaw": {
        "description": "File analysis and organization",
        "script": "agents/fileclaw/fileclaw.py",
        "cmd_prefix": ["analyze"]
    },
    "interpretclaw": {
        "description": "Translation and interpretation",
        "script": "agents/interpretclaw/interpretclaw.py",
        "cmd_prefix": ["translate"]
    },
    "langclaw": {
        "description": "Language teacher",
        "script": "agents/langclaw/langclaw.py",
        "cmd_prefix": ["lesson"]
    },
    "lawclaw": {
        "description": "Legal research assistant",
        "script": "agents/lawclaw/lawclaw.py",
        "cmd_prefix": []
    },
    "mediclaw": {
        "description": "Medical references and diagnosis",
        "script": "agents/mediclaw/mediclaw.py",
        "cmd_prefix": ["diagnose"]
    },
    "txclaw": {
        "description": "Blockchain and smart contract developer",
        "script": "agents/TXclaw/txclaw.py",
        "cmd_prefix": ["deploy"]
    },
    "claw_coder": {
        "description": "Code generation (38 languages)",
        "script": "agents/claw_coder/claw_coder.py",
        "cmd_prefix": ["code"]
    },
    "rustypycraw": {
        "description": "Code crawler and analyzer",
        "script": "agents/rustypycraw/rustypycraw.py",
        "cmd_prefix": ["crawl"]
    },
    "crustyclaw": {
        "description": "Rust AI Assistant",
        "script": "agents/crustyclaw/chronicle_bridge.py",
        "cmd_prefix": []
    }
}

class A2AHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._send_json({"status": "healthy", "agents": len(AGENTS)})
        elif parsed.path == "/.well-known/agent.json":
            self._send_json({
                "name": "Clawpack",
                "version": "2.0.0",
                "description": "Unified AI Agent Ecosystem",
                "agents": list(AGENTS.keys()),
                "protocols": ["A2A", "REST"]
            })
        elif parsed.path == "/v1/agents":
            self._send_json({"agents": list(AGENTS.keys())})
        else:
            self._send_error(404, "Not found")

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/v1/chat":
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            data = json.loads(body)
            task = data.get('task', '')
            task_lower = task.lower()
            if any(w in task_lower for w in ['flowchart', 'diagram']):
                agent_name = "flowclaw"
                cmd_args = ["view", "flowchart", task]
            elif any(w in task_lower for w in ['searchindex', 'court', 'legal']):
                agent_name = "lawclaw"
                cmd_args = [task]
            elif any(w in task_lower for w in ['letter', 'document']):
                agent_name = "docuclaw"
                cmd_args = ["create", "letter"]
            else:
                agent_name = "docuclaw"
                cmd_args = ["ai", task, "report"]
            result = self._execute_agent(agent_name, cmd_args)
            self._send_json({"status": "success", "agent": agent_name, "task": task, "result": result[:500]})
        elif parsed.path.startswith("/v1/message/"):
            agent_name = parsed.path.split("/")[-1]
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            data = json.loads(body)
            task = data.get('task', '')
            if agent_name in AGENTS:
                cmd_args = [task] if agent_name == "lawclaw" else AGENTS[agent_name]["cmd_prefix"] + [task]
                result = self._execute_agent(agent_name, cmd_args)
                self._send_json({"status": "accepted", "agent": agent_name, "task": task, "result": result[:500]})
            else:
                self._send_error(404, f"Agent '{agent_name}' not found")
        else:
            self._send_error(404, "Not found")

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _send_error(self, code, message):
        self._send_json({"error": message}, code)

    def _execute_agent(self, agent_name, cmd_args):
        agent_script = PROJECT_ROOT / AGENTS[agent_name]["script"]
        # Special case: webclaw uses direct import
        if agent_name == "webclaw":
            task = " ".join(cmd_args) if cmd_args else ""
            return process_task(task)

        if not agent_script.exists():
            return f"Agent script not found: {agent_script}"
        safe_args = []
        for arg in cmd_args:
            arg = str(arg)
            dangerous = [';', '|', '&', '$', '`', '>', '<', '\n', '\r']
            if any(c in arg for c in dangerous):
                return f"Error: Invalid characters in argument"
            if len(arg) > 500:
                return f"Error: Argument too long"
            safe_args.append(arg)
        try:
            cmd = [sys.executable, str(agent_script)] + safe_args
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, shell=False)
            return result.stdout[:1000] if result.stdout else "Agent executed"
        except Exception as e:
            return f"Error: {e}"

def main():
    port = 8766
    server = HTTPServer(('127.0.0.1', port), A2AHandler)
    print(f"\nðŸ¦ž Clawpack A2A Server v2.0 - {len(AGENTS)} agents registered")
    print(f"ðŸ“ http://127.0.0.1:{port}")
    print("\nðŸ“‹ Registered Agents:")
    for name, info in AGENTS.items():
        print(f"   âœ… {name:16} - {info['description']}")
    print("\nPress Ctrl+C to stop\n")
    server.serve_forever()

if __name__ == "__main__":
    main()

