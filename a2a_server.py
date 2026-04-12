#!/usr/bin/env python3
"""A2A Protocol Server - All Agents Including LawClaw"""

import json
import subprocess
import sys
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).resolve().parent

AGENTS = {
    "flowclaw": {
        "description": "AI-powered diagram generator",
        "script": "agents/flowclaw/flowclaw.py",
        "cmd_prefix": ["view", "flowchart"]
    },
    "docuclaw": {
        "description": "AI-powered document processor", 
        "script": "agents/docuclaw/docuclaw.py",
        "cmd_prefix": ["create", "letter"]
    },
    "lawclaw": {
        "description": "Legal research assistant",
        "script": "agents/lawclaw/lawclaw.py",
        "cmd_prefix": []
    },
    "mathematicaclaw": {
        "description": "AI-powered mathematics solver",
        "script": "agents/mathematicaclaw/mathematicaclaw.py",
        "cmd_prefix": ["solve"]
    },
    "txclaw": {
        "description": "Blockchain and smart contract developer",
        "script": "agents/txclaw/txclaw.py",
        "cmd_prefix": ["deploy"]
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
    "webclaw": {
        "description": "Web search and indexing",
        "script": "agents/webclaw/webclaw.py",
        "cmd_prefix": ["search"]
    },
    "dataclaw": {
        "description": "Data analysis and local references",
        "script": "agents/dataclaw/dataclaw.py",
        "cmd_prefix": ["search"]
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
            
            # Route based on task
            task_lower = task.lower()
            if any(w in task_lower for w in ['flowchart', 'diagram']):
                agent_name = "flowclaw"
                cmd_args = ["view", "flowchart", task]
            elif any(w in task_lower for w in ['searchindex', 'court']):
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
    
    ddef _execute_agent(self, agent_name, cmd_args):
        """Safely execute agent command with validated arguments"""
        agent_script = PROJECT_ROOT / AGENTS[agent_name]["script"]
        if not agent_script.exists():
            return f"Agent script not found: {agent_script}"
        
        # SECURITY: Validate all command arguments
        safe_args = []
        for arg in cmd_args:
            arg = str(arg)
            # Block dangerous shell characters
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
    print(f"\n🦞 Clawpack A2A Server v2.0 - {len(AGENTS)} agents")
    print(f"📍 http://127.0.0.1:{port}")
    print("Press Ctrl+C to stop\n")
    server.serve_forever()

if __name__ == "__main__":
    main()
