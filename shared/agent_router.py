"""Agent Router - Routes to existing agents"""
import subprocess
import sys
from pathlib import Path

class AgentRouter:
    def __init__(self):
        self.agents_path = Path("agents")
        self.agent_map = {
            "math": ["mathematicaclaw", "mathclaw"],
            "translate": ["interpretclaw", "langclaw"],
            "document": ["docuclaw"],
            "data": ["dataclaw"],
            "web": ["webclaw"],
            "blockchain": ["txclaw"],
            "medical": ["mediclaw"],
            "legal": ["lawclaw"],
            "plot": ["plotclaw"],
            "dream": ["dreamclaw"],
            "flow": ["flowclaw"],
            "draft": ["draftclaw"],
            "design": ["designclaw"]
        }
    
    def detect_task(self, query: str) -> str:
        query_lower = query.lower()
        
        if any(kw in query_lower for kw in ["solve", "derivative", "integral", "equation", "calculate"]):
            return "math"
        if any(kw in query_lower for kw in ["translate", " to spanish", " to french", " to german"]):
            return "translate"
        if any(kw in query_lower for kw in ["document", "pdf", "docx", "convert"]):
            return "document"
        if any(kw in query_lower for kw in ["data", "analyze", "statistics", "csv"]):
            return "data"
        if any(kw in query_lower for kw in ["chart", "plot", "graph", "visualize"]):
            return "plot"
        if any(kw in query_lower for kw in ["image", "picture", "generate", "dream"]):
            return "dream"
        if any(kw in query_lower for kw in ["diagram", "flowchart", "mindmap"]):
            return "flow"
        
        return None
    
    def route(self, query: str, task: str = None) -> str:
        if not task:
            task = self.detect_task(query)
        
        if not task or task not in self.agent_map:
            return None
        
        for agent_name in self.agent_map[task]:
            agent_path = self.agents_path / agent_name / f"{agent_name}.py"
            if agent_path.exists():
                return str(agent_path)
        
        return None
    
    def execute(self, agent_path: str, query: str) -> str:
        try:
            result = subprocess.run(
                [sys.executable, agent_path, query],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.agents_path.parent)
            )
            return result.stdout.strip() or result.stderr.strip()
        except subprocess.TimeoutExpired:
            return "Request timed out"
        except Exception as e:
            return f"Error: {e}"
