"""A2A Protocol Server - Integrated with Clawpack agents"""

import json
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

app = FastAPI(title="Clawpack A2A Server", version="2.0.0")

# Agent registry - maps agent names to their capabilities
AGENT_REGISTRY = {
    "flowclaw": {
        "description": "Diagram generator (flowcharts, architecture, gantt)",
        "capabilities": ["diagram", "flowchart", "architecture", "gantt", "sequence"]
    },
    "docuclaw": {
        "description": "Document processor (letters, reports, memos)",
        "capabilities": ["document", "letter", "report", "memo", "meeting_notes"]
    },
    "mathematicaclaw": {
        "description": "Mathematics solver",
        "capabilities": ["math", "solve", "equation", "calculus", "algebra"]
    },
    "txclaw": {
        "description": "Blockchain/Smart Contract developer",
        "capabilities": ["blockchain", "smart_contract", "cosmwasm", "auction"]
    },
    "interpretclaw": {
        "description": "Translation and interpretation",
        "capabilities": ["translate", "language", "interpret", "speak"]
    },
    "langclaw": {
        "description": "Language teacher",
        "capabilities": ["language", "teach", "lesson", "vocabulary"]
    }
}

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
        "description": "Unified AI Agent Ecosystem - 15+ specialized agents",
        "agents": [
            {
                "name": name,
                "description": info["description"],
                "capabilities": info["capabilities"],
                "endpoint": f"/v1/message/{name}"
            }
            for name, info in AGENT_REGISTRY.items()
        ],
        "protocols": ["A2A", "REST", "JSON-RPC"],
        "documentation": "https://github.com/greg-gzillion/clawpack_v2"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agents": len(AGENT_REGISTRY),
        "version": "2.0.0"
    }

@app.get("/v1/agents")
async def list_agents():
    """List all available agents"""
    return {"agents": list(AGENT_REGISTRY.keys())}

@app.post("/v1/message/{agent_name}")
async def send_to_agent(agent_name: str, request: MessageRequest):
    """Send a message to a specific agent"""
    
    if agent_name not in AGENT_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
    
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
    
    task_lower = request.task.lower()
    
    # Determine which agent to use based on task content
    for agent_name, info in AGENT_REGISTRY.items():
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
    """Route request to the actual agent"""
    
    agent_path = Path(PROJECT_ROOT) / "agents" / agent_name / f"{agent_name}.py"
    
    if not agent_path.exists():
        return f"Agent {agent_name} not fully implemented yet"
    
    # For now, return a formatted response
    # In production, this would call the agent's process method
    return f"[{agent_name}] Processing: {task[:200]}"

# CLI integration
def start_server(host: str = "127.0.0.1", port: int = 8765):
    """Start the A2A server"""
    import uvicorn
    print(f"🚀 Starting Clawpack A2A Server on {host}:{port}")
    print(f"📋 Agent Discovery: http://{host}:{port}/.well-known/agent.json")
    print(f"💚 Health Check: http://{host}:{port}/health")
    print(f"🤖 Available Agents: http://{host}:{port}/v1/agents")
    print("")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server()
