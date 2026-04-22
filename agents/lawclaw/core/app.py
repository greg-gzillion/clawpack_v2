"""LawClaw Core - A2A ONLY"""
import requests

A2A = "http://127.0.0.1:8766"

class LawClaw:
    def __init__(self):
        self.commands = self._load_commands()
    
    def _load_commands(self):
        """Load commands from commands/ directory"""
        from commands import COMMAND_REGISTRY, load_all_commands
        load_all_commands()
        return COMMAND_REGISTRY
    
    def run(self, user_input):
        """Route command through A2A"""
        parts = user_input.strip().split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd in self.commands:
            return self.commands[cmd](args)
        else:
            return f"Unknown command: {cmd}. Type /help"
    
    def call_webclaw(self, query):
        """Call WebClaw via A2A"""
        response = requests.post(
            f"{A2A}/v1/message/webclaw",
            json={"task": f"/search {query}", "agent": "lawclaw"},
            timeout=10
        )
        return response.json().get("result", "") if response.status_code == 200 else ""
    
    def call_llm(self, prompt):
        """Call LLM via A2A"""
        response = requests.post(
            f"{A2A}/v1/message/llmclaw",
            json={"task": f"/ask {prompt}", "agent": "lawclaw"},
            timeout=60
        )
        return response.json().get("result", "") if response.status_code == 200 else ""
