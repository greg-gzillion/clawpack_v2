"""Enhanced BaseAgent with A2A collaboration - All agents should inherit this"""
import json
import requests
from pathlib import Path
from typing import Optional, Dict, Any

A2A_URL = "http://127.0.0.1:8766"

class BaseAgent:
    """Base class for all Clawpack agents with A2A collaboration"""
    
    def __init__(self, name: str):
        self.name = name
        self.a2a_url = A2A_URL
    
    def collaborate(self, target_agent: str, task: str, timeout: int = 60) -> Optional[str]:
        """Call another agent via A2A"""
        try:
            response = requests.post(
                f"{self.a2a_url}/v1/message/{target_agent}",
                json={"task": task, "agent": self.name},
                timeout=timeout
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    return data.get("result", "")
            return None
        except Exception as e:
            print(f"[{self.name}] A2A error calling {target_agent}: {e}")
            return None
    
    def ask_llm(self, prompt: str) -> Optional[str]:
        """Get LLM response via llmclaw"""
        return self.collaborate("llmclaw", f"/llm {prompt}")
    
    def search_knowledge(self, query: str) -> Optional[str]:
        """Search WebClaw for knowledge"""
        return self.collaborate("webclaw", f"search {query}")
    
    def process(self, task: str) -> str:
        """Override this in subclasses"""
        raise NotImplementedError("Subclasses must implement process()")
