"""Agent Collaboration Bridge - Enable agents to call each other"""

import subprocess
import json
import requests
from pathlib import Path
from typing import Dict, Any

class AgentBridge:
    """Bridge for agents to communicate and collaborate"""
    
    def __init__(self, a2a_url="http://127.0.0.1:8766"):
        self.a2a_url = a2a_url
        self.agents = {
            "lawclaw": "Legal research and court data",
            "flowclaw": "Diagram generation",
            "docuclaw": "Document processing",
            "mathematicaclaw": "Math visualization",
            "txclaw": "Blockchain contracts",
            "interpretclaw": "Translation",
            "langclaw": "Language lessons",
            "claw_coder": "Code generation",
            "fileclaw": "File management"
        }
    
    def call_agent(self, agent_name: str, task: str) -> Dict:
        """Call another agent via A2A"""
        try:
            response = requests.post(
                f"{self.a2a_url}/v1/message/{agent_name}",
                json={"task": task},
                timeout=60
            )
            if response.status_code == 200:
                return response.json()
            return {"error": f"Agent {agent_name} not responding"}
        except Exception as e:
            return {"error": str(e)}
    
    def law_to_flow(self, legal_topic: str) -> str:
        """LawClaw asks FlowClaw to diagram a legal process"""
        # First, get legal info
        law_result = self.call_agent("lawclaw", f"summarize {legal_topic}")
        # Then create diagram
        flow_result = self.call_agent("flowclaw", f"create flowchart for {legal_topic}")
        return f"Legal summary: {law_result.get('result', 'N/A')}\n\nDiagram: {flow_result.get('result', 'N/A')}"
    
    def doc_to_tx(self, contract_type: str) -> str:
        """DocClaw asks TXClaw to generate a contract"""
        return self.call_agent("txclaw", f"create {contract_type} contract").get('result', 'Error')
    
    def math_to_flow(self, equation: str) -> str:
        """MathClaw asks FlowClaw to visualize an equation"""
        return self.call_agent("flowclaw", f"create flowchart for solving {equation}").get('result', 'Error')

agent_bridge = AgentBridge()
