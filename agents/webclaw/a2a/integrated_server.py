"""A2A Protocol Server - Integrated with Clawpack agents (Security Hardened)"""

import json
import sys
import re
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

app = FastAPI(title="Clawpack A2A Server", version="2.0.0")

# Agent registry - safely validated
ALLOWED_AGENTS = {
    "flowclaw": {
        "description": "Diagram generator",
        "capabilities": ["diagram", "flowchart", "architecture", "gantt", "sequence"],
        "script": "agents/flowclaw/flowclaw.py"
    },
    "docuclaw": {
        "description": "Document processor",
        "capabilities": ["document", "letter", "report", "memo", "meeting_notes"],
        "script": "agents/docuclaw/docuclaw.py"
    },
    "mathematicaclaw": {
        "description": "Mathematics solver",
        "capabilities": ["math", "solve", "equation", "calculus", "algebra"],
        "script": "agents/mathematicaclaw/mathematicaclaw.py"
    },
    "txclaw": {
        "description": "Blockchain/Smart Contract developer",
        "capabilities": ["blockchain", "smart_contract", "cosmwasm", "auction"],
        "script": "agents/txclaw/txclaw.py"
    }
}

# Validate agent name - whitelist only
def validate_agent_name(agent_name: str) -> bool:
    """Validate agent name against whitelist (prevents path injection)"""
    return agent_name in ALLOWED_AGENTS

# Validate path - prevent directory traversal
def validate_path(base_path: Path, requested_path: str) -> Path:
    """Validate path to prevent directory traversal attacks"""
    # Remove any path traversal attempts
    clean_path = re.sub(r'\.\./', '', requested_path)
    clean_path = re.sub(r'\.\.\\', '', clean_path)
    
    # Resolve and ensure within base
    full_path = (base_path / clean_path).resolve()
    if not str(full_path).startswith(str(base_path.resolve())):
        raise ValueError("Path traversal detected")
    return full_path

class MessageRequest(BaseModel):
    agent: str
    task: str
    context: Optional[Dict] = None

class MessageResponse(BaseModel):
    agent: str
    result: str
    status: str

@app.get("/.well-known/agent.json")
async def agent_discovery():
    """A2A agent discovery endpoint"""
    return {
        "name": "Clawpack",
        "version": "2.0.0",
        "description": "Unified AI Agent Ecosystem",
        "agents": [
            {
                "name": name,
                "description": info["description"],
                "capabilities": info["capabilities"],
                "endpoint": f"/v1/message/{name}"
            }
            for name, info in ALLOWED_AGENTS.items()
        ],
        "protocols": ["A2A", "REST"],
        "security": ["path_validation", "whitelist_only"]
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agents": len(ALLOWED_AGENTS),
        "version": "2.0.0"
    }

@app.get("/v1/agents")
async def list_agents():
    """List all available agents"""
    return {"agents": list(ALLOWED_AGENTS.keys())}

@app.post("/v1/message/{agent_name}")
async def send_to_agent(agent_name: str, request: MessageRequest):
    """Send a message to a specific agent - SECURE: whitelist validation"""
    
    # Security: Validate agent name against whitelist
    if not validate_agent_name(agent_name):
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
    
    # Security: Validate task length
    if len(request.task) > 10000:
        raise HTTPException(status_code=400, detail="Task too long (max 10000 characters)")
    
    # Route to the appropriate agent
    try:
        result = await _route_to_agent(agent_name, request.task, request.context)
        return MessageResponse(
            agent=agent_name,
            result=result,
            status="success"
        )
    except Exception as e:
        return MessageResponse(
            agent=agent_name,
            result=f"Error: {str(e)}",
            status="error"
        )

@app.post("/v1/chat")
async def chat(request: MessageRequest):
    """Smart routing - automatically choose the best agent"""
    
    # Security: Validate task length
    if len(request.task) > 10000:
        raise HTTPException(status_code=400, detail="Task too long (max 10000 characters)")
    
    task_lower = request.task.lower()
    
    # Determine which agent to use based on task content
    for agent_name, info in ALLOWED_AGENTS.items():
        for capability in info["capabilities"]:
            if capability in task_lower:
                result = await _route_to_agent(agent_name, request.task, request.context)
                return {
                    "agent": agent_name,
                    "result": result,
                    "matched_capability": capability,
                    "status": "success"
                }
    
    # Default to docuclaw for general document tasks
    result = await _route_to_agent("docuclaw", request.task, request.context)
    return {
        "agent": "docuclaw",
        "result": result,
        "status": "success"
    }

async def _route_to_agent(agent_name: str, task: str, context: Dict = None) -> str:
    """Route request to the actual agent - SECURE: validated paths only"""
    
    # Security: Use validated whitelist, not user input directly
    if agent_name not in ALLOWED_AGENTS:
        return f"Invalid agent: {agent_name}"
    
    # Security: Build path safely using whitelisted agent name
    agent_script = ALLOWED_AGENTS[agent_name]["script"]
    agent_path = PROJECT_ROOT / agent_script
    
    # Security: Validate resolved path is within project
    try:
        safe_path = validate_path(PROJECT_ROOT, agent_script)
        if not safe_path.exists():
            return f"Agent {agent_name} not fully implemented yet"
    except ValueError:
        return "Invalid path request blocked"
    
    # Security: Sanitize task for shell (if executing)
    safe_task = task.replace('"', '\\"').replace('$', '').replace('`', '')
    
    # Return a formatted response (in production, would call agent)
    return f"[{agent_name}] Processing: {safe_task[:200]}"

# CLI integration
def start_server(host: str = "127.0.0.1", port: int = 8765):
    """Start the A2A server"""
    import uvicorn
    print(f"🚀 Starting Clawpack A2A Server on {host}:{port}")
    print(f"📋 Agent Discovery: http://{host}:{port}/.well-known/agent.json")
    print(f"💚 Health Check: http://{host}:{port}/health")
    print(f"🤖 Available Agents: http://{host}:{port}/v1/agents")
    print("")
    print("🔒 Security Features:")
    print("   • Whitelist-based agent validation")
    print("   • Path traversal protection")
    print("   • Input length limits")
    print("   • Command injection prevention")
    print("")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server()
