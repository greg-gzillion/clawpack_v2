#!/usr/bin/env python3
"""Clawpack A2A Server - Unified with Memory, WebClaw, and 21 Agents"""
import json
import sys
import subprocess
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import memory system
from shared.memory import get_memory

# Import WebClaw handler
from agents.webclaw.agent_handler import process_task as webclaw_process
from agents.llmclaw.agent_handler import process_task as llmclaw_process
from agents.lawclaw.agent_handler import process_task as lawclaw_process
from agents.mediclaw.agent_handler import process_task as mediclaw_process
from agents.claw_coder.agent_handler import process_task as clawcoder_process
from agents.mathematicaclaw.agent_handler import process_task as mathclaw_process
from agents.crustyclaw.agent_handler import process_task as crustyclaw_process
from agents.interpretclaw.agent_handler import process_task as interpretclaw_process
from agents.dataclaw.agent_handler import process_task as dataclaw_process
from agents.langclaw.agent_handler import process_task as langclaw_process
from agents.liberateclaw.agent_handler import process_task as liberateclaw_process

# Initialize memory
a2a_memory = get_memory("a2a_server")

AGENTS = {
    "llmclaw": {"script": "agents/llmclaw/llmclaw.py", "cmd_prefix": ["/llm"], "desc": "Model selection and management"},
    "liberateclaw": {"script": "agents/liberateclaw/liberateclaw.py", "cmd_prefix": ["liberate"], "desc": "LLM Model Liberation"},
    "flowclaw": {"script": "agents/flowclaw/flowclaw.py", "cmd_prefix": ["diagram"], "desc": "AI-powered diagram generator"},
    "designclaw": {"script": "agents/designclaw/designclaw.py", "cmd_prefix": ["design"], "desc": "Graphic design and logos"},
    "draftclaw": {"script": "agents/draftclaw/draftclaw.py", "cmd_prefix": ["draft"], "desc": "Technical drawings and blueprints"},
    "drawclaw": {"script": "agents/drawclaw/drawclaw.py", "cmd_prefix": ["draw"], "desc": "Drawing and sketching"},
    "dreamclaw": {"script": "agents/dreamclaw/dreamclaw.py", "cmd_prefix": ["dream"], "desc": "AI vision and generation"},
    "plotclaw": {"script": "agents/plotclaw/plotclaw.py", "cmd_prefix": ["plot"], "desc": "Charts and graphs"},
    "docuclaw": {"script": "agents/docuclaw/docuclaw.py", "cmd_prefix": ["doc"], "desc": "AI-powered document processor"},
    "dataclaw": {"script": "agents/dataclaw/dataclaw.py", "cmd_prefix": ["search"], "desc": "Data analysis and local references"},
    "webclaw": {"script": "agents/webclaw/webclaw.py", "cmd_prefix": ["search"], "desc": "Web search and indexing"},
    "mathematicaclaw": {"script": "agents/mathematicaclaw/mathematicaclaw.py", "cmd_prefix": ["math"], "desc": "AI-powered mathematics solver"},
    "fileclaw": {"script": "agents/fileclaw/fileclaw.py", "cmd_prefix": ["file"], "desc": "File analysis and organization"},
    "interpretclaw": {"script": "agents/interpretclaw/interpretclaw.py", "cmd_prefix": ["translate"], "desc": "Translation and interpretation"},
    "langclaw": {"script": "agents/langclaw/langclaw.py", "cmd_prefix": ["learn"], "desc": "Language teacher"},
    "lawclaw": {"script": "agents/lawclaw/lawclaw.py", "cmd_prefix": ["search"], "desc": "Legal research assistant"},
    "mediclaw": {"script": "agents/mediclaw/mediclaw.py", "cmd_prefix": ["diagnose"], "desc": "Medical references and diagnosis"},
    "txclaw": {"script": "agents/txclaw/txclaw.py", "cmd_prefix": ["tx"], "desc": "Blockchain and smart contract developer"},
    "claw_coder": {"script": "agents/claw_coder/claw_coder.py", "cmd_prefix": ["code"], "desc": "Code generation (38 languages)"},
    "rustypycraw": {"script": "agents/rustypycraw/rustypycraw.py", "cmd_prefix": ["crawl"], "desc": "Code crawler and analyzer"},
    "crustyclaw": {"script": "agents/crustyclaw/crustyclaw.py", "cmd_prefix": ["rust"], "desc": "Rust AI Assistant"},
}

class UnifiedA2AHandler(BaseHTTPRequestHandler):
    """Unified A2A Handler - Memory + WebClaw + All Agents"""
    
    def log_message(self, format, *args):
        print(f"  {self.address_string()} - {format % args}")
    
    def do_GET(self):
        path = urlparse(self.path).path
        
        if path == "/health":
            self._send_json({
                "status": "healthy",
                "agents": len(AGENTS),
                "memory": {
                    "working_tokens": a2a_memory.working.token_count,
                    "semantic_facts": len(a2a_memory.semantic.facts),
                    "semantic_entities": len(a2a_memory.semantic.entities)
                }
            })
        elif path == "/v1/agents":
            agents_list = [{"name": k, "description": v["desc"]} for k, v in AGENTS.items()]
            self._send_json({"agents": agents_list})
        elif path == "/memory/stats":
            self._send_json({
                "working_tokens": a2a_memory.working.token_count,
                "semantic_facts": len(a2a_memory.semantic.facts),
                "semantic_entities": len(a2a_memory.semantic.entities),
                "working_messages": len(a2a_memory.working.messages),
                "max_tokens": a2a_memory.working.max_tokens
            })
        else:
            self._send_error(404, "Not found")
    
    def do_POST(self):
        path = urlparse(self.path).path

        if path.startswith("/v1/message/"):
            agent_name = path.split("/")[-1]
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)
            task = data.get('task', '')

            a2a_memory.working.add("user", f"[{agent_name}] {task}")

            if agent_name in AGENTS:
                result = self._execute_agent(agent_name, task)
                
                # Handle both dict and string responses
                if isinstance(result, dict):
                    result_text = result.get("result", str(result))
                else:
                    result_text = str(result)
                
                a2a_memory.working.add("assistant", result_text)
                a2a_memory.semantic.add_fact(agent_name, task, result_text[:200])
                compressed = a2a_memory.working.compress()
                
                self._send_json({
                    "status": "success",
                    "agent": agent_name,
                    "task": task,
                    "result": result_text,
                    "memory_tokens": a2a_memory.working.token_count
                })
            else:
                self._send_error(404, f"Agent '{agent_name}' not found")
        else:
            self._send_error(404, "Not found")
    def _send_json(self, data, status=200):
        try:
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
            # Client disconnected - that's fine
            pass

    def _send_error(self, code, message):
        self._send_json({"error": message}, code)
    
    def _execute_agent(self, agent_name: str, task: str) -> str:
        """Execute agent with proper routing"""
        
        # WebClaw uses direct import for performance
        if agent_name == "lawclaw":
            return lawclaw_process(task)
        elif agent_name == "webclaw":
            return webclaw_process(task)
        elif agent_name == "llmclaw":
            return llmclaw_process(task)
        elif agent_name == "mediclaw":
            return mediclaw_process(task)
        elif agent_name == "claw_coder":
            return clawcoder_process(task)
        elif agent_name == "mathematicaclaw":
            return mathclaw_process(task)
        elif agent_name == "crustyclaw":
            return crustyclaw_process(task)
        elif agent_name == "interpretclaw":
            return interpretclaw_process(task)
        elif agent_name == "dataclaw":
            return dataclaw_process(task)
        elif agent_name == "langclaw":
            return langclaw_process(task)
        elif agent_name == "liberateclaw":
            return liberateclaw_process(task)
        
        agent_script = PROJECT_ROOT / AGENTS[agent_name]["script"]
        if not agent_script.exists():
            return f"Agent script not found: {agent_script}"
        
        # Build command args
        cmd_args = [task] if agent_name == "lawclaw" else AGENTS[agent_name]["cmd_prefix"] + [task]
        
        # Security validation
        safe_args = []
        for arg in cmd_args:
            arg = str(arg)
            dangerous = [';', '|', '&', '$', '`', '>', '<', '\n', '\r']
            if any(c in arg for c in dangerous):
                return "Error: Invalid characters in argument"
            if len(arg) > 5000:
                return "Error: Argument too long (max 50000 chars) (max 5000 chars) (max 50000 chars) (max 5000 chars)"
            safe_args.append(arg)
        
        try:
            cmd = [sys.executable, str(agent_script)] + safe_args
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, shell=False, encoding="utf-8", errors="replace", cwd=str(PROJECT_ROOT))
            return result.stdout if result.stdout else "Agent executed"
        except subprocess.TimeoutExpired:
            return "Error: Agent timeout"
        except Exception as e:
            return f"Error: {e}"

def main():
    port = 8766
    server = ThreadingHTTPServer(('127.0.0.1', port), UnifiedA2AHandler)
    
    print("\n" + "="*70)
    print("?? CLAWPACK A2A SERVER - UNIFIED")
    print("="*70)
    print(f"?? http://127.0.0.1:{port}")
    print(f"\n? {len(AGENTS)} Agents Registered")
    print("? Three-Tier Memory: ACTIVE")
    print("? WebClaw Direct Integration: ACTIVE")
    print("\nEndpoints:")
    print("  GET  /health        - Server health + memory stats")
    print("  GET  /v1/agents     - List all agents")
    print("  GET  /memory/stats  - Detailed memory statistics")
    print("  POST /v1/message/{agent} - Send task to agent")
    print("\nPress Ctrl+C to stop\n")
    print("="*70 + "\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n?? Final Memory Stats:")
        print(f"   Working tokens: {a2a_memory.working.token_count}")
        print(f"   Semantic facts: {len(a2a_memory.semantic.facts)}")
        print(f"   Messages processed: {len(a2a_memory.working.messages)}")
        print("\n?? Server stopped")

if __name__ == "__main__":
    main()














