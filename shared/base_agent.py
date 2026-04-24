"""BaseAgent - All agents inherit from this"""
import sys
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Any, Optional, Dict

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class BaseAgent:
    """Base class for all agents with shared capabilities"""

    def __init__(self, name: str):
        self.name = name
        self.memory_file = Path("data/shared_memory.json")
        self.state = self._load_state()
        self.A2A = "http://127.0.0.1:8766"
        
        # Lazy-loaded providers
        self._webclaw = None
        self._llmclaw_available = True

    @property
    def webclaw(self):
        if self._webclaw is None:
            from agents.webclaw.providers.webclaw_provider import WebclawProvider
            self._webclaw = WebclawProvider()
        return self._webclaw

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

    # ---- WebClaw - SQLite index search ----
    def search_web(self, query: str, max_results: int = 5) -> str:
        """Search WebClaw's SQLite index (1.5M terms)"""
        return self.webclaw.search_with_context(query, max_results)

    def search_web_raw(self, query: str, max_results: int = 10) -> str:
        """Search WebClaw without context snippets"""
        return self.webclaw.search(query, max_results)

    # ---- DataClaw - local references ----
    def search_local(self, query: str) -> str:
        """Search DataClaw local index"""
        try:
            from agents.dataclaw.modules.search.local_search import search_local
            return search_local(query)
        except:
            return ""

    # ---- LLMClaw via A2A ----
    def ask_memory(self, query: str) -> str:
        """Check if any agent already answered this"""
        try:
            r = requests.get(f"{self.A2A}/memory/stats", timeout=5)
            if r.status_code == 200:
                stats = r.json()
                if stats.get("semantic_facts", 0) > 0:
                    r2 = requests.post(f"{self.A2A}/v1/message/webclaw",
                        json={"task": f"search {query}"}, timeout=10)
                    if r2.status_code == 200:
                        result = r2.json().get("result", "")
                        if result and len(result) > 20:
                            return "[Shared Knowledge]\n" + result[:1000]
        except:
            pass
        return ""

    def ask_llm(self, prompt: str) -> str:
        """Call LLMClaw through A2A"""
        try:
            r = requests.post(
                f"{self.A2A}/v1/message/llmclaw",
                json={"task": f"/llm {prompt}"},
                timeout=60
            )
            if r.status_code == 200:
                return r.json().get("result", "")
        except:
            pass
        return "LLMClaw unavailable"

    # ---- Chronicle ----
    def search_chronicle(self, query: str, limit: int = 5) -> list:
        """Search the chronicle ledger"""
        try:
            from agents.webclaw.core.chronicle_ledger import get_chronicle
            chronicle = get_chronicle()
            return chronicle.recover_by_context(query, limit)
        except:
            return []

    def record_in_chronicle(self, url: str, context: str, source: str = None) -> None:
        """Record a URL in the chronicle ledger"""
        try:
            from agents.webclaw.core.chronicle_ledger import get_chronicle
            chronicle = get_chronicle()
            chronicle.record_fetch(url=url, context=context, source=source or self.name)
        except:
            pass

    # ---- Memory ----
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

    def track_interaction(self):
        self.state["interactions"] = self.state.get("interactions", 0) + 1
        self._save_state()

    def get_stats(self):
        return {"name": self.name, "interactions": self.state.get("interactions", 0)}

    # ---- Agent handler interface ----
    def handle(self, task: str) -> dict:
        """Override in subclass"""
        self.track_interaction()
        return {"status": "error", "result": f"{self.name}: handle() not implemented"}

    def smart_ask(self, query: str, domain: str = "") -> str:
        """Ask with shared memory first, then LLM"""
        memory = self.ask_memory(query)
        if memory:
            prompt = "Context from shared knowledge: " + memory + "\n\nQuestion: " + query
        else:
            prompt = query
        return self.ask_llm(prompt)
