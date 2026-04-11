#!/usr/bin/env python3
"""A2A Protocol Server - Working Version"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from datetime import datetime

AGENTS = {
    "flowclaw": "AI-powered diagram generator",
    "docuclaw": "AI-powered document processor", 
    "mathematicaclaw": "AI-powered mathematics solver",
    "txclaw": "Blockchain and smart contract developer",
    "interpretclaw": "Translation and interpretation",
    "langclaw": "Language teacher",
    "webclaw": "Web search and indexing",
    "dataclaw": "Data analysis and local references"
}

class A2AHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/health":
            self._send_json({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "agents": len(AGENTS)
            })
        
        elif parsed.path == "/.well-known/agent.json":
            self._send_json({
                "name": "Clawpack",
                "version": "2.0.0",
                "description": "Unified AI Agent Ecosystem",
                "agents": list(AGENTS.keys()),
                "protocols": ["A2A", "REST"]
            })
        
        elif parsed.path == "/v1/agents":
            self._send_json({
                "agents": [{"name": n, "description": d} for n, d in AGENTS.items()]
            })
        
        elif parsed.path == "/":
            self._send_json({
                "service": "Clawpack A2A Server",
                "version": "2.0.0",
                "endpoints": ["/health", "/.well-known/agent.json", "/v1/agents", "/v1/chat"]
            })
        
        else:
            self._send_error(404, f"Unknown endpoint")
    
    def do_POST(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/v1/chat":
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            
            try:
                data = json.loads(body)
                task = data.get('task', '')
                
                # Simple routing
                task_lower = task.lower()
                if any(w in task_lower for w in ['diagram', 'flowchart', 'chart']):
                    agent = 'flowclaw'
                elif any(w in task_lower for w in ['document', 'letter', 'report']):
                    agent = 'docuclaw'
                elif any(w in task_lower for w in ['solve', 'math', 'equation']):
                    agent = 'mathematicaclaw'
                else:
                    agent = 'docuclaw'
                
                self._send_json({
                    "status": "success",
                    "agent": agent,
                    "task": task,
                    "message": f"Task routed to {agent}"
                })
            except:
                self._send_error(400, "Invalid JSON")
        
        elif parsed.path.startswith("/v1/message/"):
            agent_name = parsed.path.split("/")[-1]
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            
            try:
                data = json.loads(body)
                task = data.get('task', '')
                
                if agent_name in AGENTS:
                    self._send_json({
                        "status": "accepted",
                        "agent": agent_name,
                        "task": task
                    })
                else:
                    self._send_error(404, f"Agent '{agent_name}' not found")
            except:
                self._send_error(400, "Invalid JSON")
        
        else:
            self._send_error(404, "Unknown endpoint")
    
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def _send_error(self, code, message):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": message, "code": code}).encode())
    
    def log_message(self, format, *args):
        pass

def main():
    port = 8765
    server = HTTPServer(('127.0.0.1', port), A2AHandler)
    print(f"\n{'='*50}")
    print(f"🦞 Clawpack A2A Server v2.0")
    print(f"{'='*50}")
    print(f"📍 http://127.0.0.1:{port}")
    print(f"{'='*50}")
    print(f"\n📚 Endpoints:")
    print(f"   GET  /health")
    print(f"   GET  /.well-known/agent.json")
    print(f"   GET  /v1/agents")
    print(f"   POST /v1/chat")
    print(f"   POST /v1/message/{list(AGENTS.keys())[0]}")
    print(f"\n🤖 Agents: {', '.join(AGENTS.keys())}")
    print(f"\n{'='*50}")
    print("Press Ctrl+C to stop\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        server.shutdown()

if __name__ == "__main__":
    main()

# Add liberateclaw to A2A agent registry
AGENTS["liberateclaw"] = {
    "description": "Model Liberation Agent - Download and manage local LLM models",
    "capabilities": ["liberate_models", "local_inference", "model_management"],
    "script": "agents/liberateclaw/liberateclaw.py"
}
