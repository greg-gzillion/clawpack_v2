"""BaseAgent - All agents inherit from this"""
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Any, Optional, Dict

sys.path.insert(0, str(Path(__file__).parent.parent))

class BaseAgent:
    """Base class for all agents with shared capabilities"""
    
    def __init__(self, name: str):
        self.name = name
        self.memory_file = Path("data/shared_memory.json")
        self.webclaw_path = Path(__file__).parent.parent / "agents" / "webclaw" / "webclaw.py"
        self.dataclaw_path = Path("agents/dataclaw/dataclaw.py")
        self.state = self._load_state()
    
    def _load_state(self):
        if self.memory_file.exists():
            try:
                data = json.loads(self.memory_file.read_text())
                return data.get("agent_states", {}).get(self.name, {})
            except:
                pass
        return {"interactions": 0, "successful": 0}
    
    def _save_state(self):
        data = {}
        if self.memory_file.exists():
            try:
                data = json.loads(self.memory_file.read_text())
            except:
                pass
        if "agent_states" not in data:
            data["agent_states"] = {}
        data["agent_states"][self.name] = self.state
        self.memory_file.parent.mkdir(exist_ok=True)
        self.memory_file.write_text(json.dumps(data, indent=2))
    
    def learn(self, key: str, value: Any):
        self.state[key] = value
        self._save_state()
    
    def recall(self, key: str):
        return self.state.get(key)
    
    def learn_fact(self, fact: str):
        data = {}
        if self.memory_file.exists():
            try:
                data = json.loads(self.memory_file.read_text())
            except:
                pass
        if "learned_facts" not in data:
            data["learned_facts"] = {}
        data["learned_facts"][fact] = {"source": self.name, "learned_at": str(datetime.now())}
        self.memory_file.write_text(json.dumps(data, indent=2))
    
    def get_facts(self):
        if self.memory_file.exists():
            try:
                return json.loads(self.memory_file.read_text()).get("learned_facts", {})
            except:
                pass
        return {}
    
    def ask_webclaw(self, query: str) -> str:
        if not self.webclaw_path.exists():
            return f"[{self.name}] WebClaw not found"
        try:
            result = subprocess.run(
                [sys.executable, str(self.webclaw_path), "search", query],
                capture_output=True, text=True, timeout=10
            )
            return result.stdout.strip() or "No results"
        except Exception as e:
            return f"[{self.name}] WebClaw error: {e}"
    
    def ask_dataclaw(self, query: str) -> str:
        if not self.dataclaw_path.exists():
            return f"[{self.name}] Dataclaw not found"
        try:
            result = subprocess.run(
                [sys.executable, str(self.dataclaw_path), query],
                capture_output=True, text=True, timeout=10
            )
            return result.stdout.strip() or "No results"
        except Exception as e:
            return f"[{self.name}] Dataclaw error: {e}"
    
    def track_interaction(self):
        self.state["interactions"] = self.state.get("interactions", 0) + 1
        self._save_state()
    
    def get_stats(self):
        return {"name": self.name, "interactions": self.state.get("interactions", 0)}
    
    def handle(self, query: str) -> str:
        self.track_interaction()
        return f"[{self.name}] Processing: {query}"
    
    def run_cli(self):
        if len(sys.argv) > 1:
            cmd = ' '.join(sys.argv[1:])
            print(self.handle(cmd))
        else:
            print(f"{self.name} ready")



    def search_chronicle(self, query: str, limit: int = 5) -> list:
        """Search the chronicle ledger for relevant URLs"""
        try:
            import sys
            from pathlib import Path
            sys.path.insert(0, str(Path(__file__).parent.parent / "agents/webclaw"))
            from core.chronicle_ledger import get_chronicle
            chronicle = get_chronicle()
            return chronicle.recover_by_context(query, limit)
        except:
            return []
    
    def record_in_chronicle(self, url: str, context: str, source: str = None) -> None:
        """Record a URL in the chronicle ledger"""
        try:
            import sys
            from pathlib import Path
            sys.path.insert(0, str(Path(__file__).parent.parent / "agents/webclaw"))
            from core.chronicle_ledger import get_chronicle
            chronicle = get_chronicle()
            chronicle.record_fetch(
                url=url,
                context=context,
                source=source or self.name
            )
        except:
            pass
