"""A2A Protocol Server - Agent-to-Agent communication"""

import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="Clawpack A2A Server")

AGENT_CARD = {
    "name": "Clawpack",
    "version": "2.0.0",
    "description": "Unified AI Agent Ecosystem",
    "capabilities": [
        "diagram_generation",
        "document_processing",
        "mathematics",
        "blockchain_smart_contracts",
        "translation",
        "data_analysis"
    ],
    "endpoints": {
        "message": "/v1/message",
        "stream": "/v1/stream"
    }
}

@app.get("/.well-known/agent.json")
async def agent_discovery():
    """A2A agent discovery endpoint"""
    return AGENT_CARD

@app.post("/v1/message")
async def handle_message(request: Request):
    """Handle A2A messages from other agents"""
    body = await request.json()
    
    # Route to appropriate agent based on message type
    message_type = body.get('type', 'unknown')
    
    return JSONResponse({
        "status": "processing",
        "agent": "clawpack",
        "response": f"Processing {message_type} request"
    })
