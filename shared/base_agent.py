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
        self._unified_memory = None  # Lazy-init unified shared memory
        self._llmclaw_available = True

    @property
    def webclaw(self):
        if self._webclaw is None:
            from agents.webclaw.providers.webclaw_provider import WebclawProvider
            self._webclaw = WebclawProvider()
        return self._webclaw


    @property
    def memory(self):
        """Unified shared memory for all agents — lazy-init singleton."""
        if self._unified_memory is None:
            from shared.memory.unified_memory import get_memory
            self._unified_memory = get_memory()
        return self._unified_memory

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
    def search_web(self, query: str, max_results: int = 10) -> str:
        """Search WebClaw's SQLite index (1.5M terms)"""
        return self.webclaw.search_with_context(query, max_results)

    def search_web_raw(self, query: str, max_results: int = 20) -> str:
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
                            return "[Shared Knowledge]\n" + result
        except:
            pass
        return ""

    def call_agent(self, agent_name: str, task: str, timeout: int = 120) -> str:
        """Call another agent through A2A. Returns full response with no truncation."""
        try:
            r = requests.post(
                f'{self.A2A}/v1/message/{agent_name}',
                json={'task': task},
                timeout=timeout
            )
            if r.status_code == 200:
                return r.json().get('result', '')
        except:
            pass
        return ''

    def _gather_all_context(self, query=""):
        """Gather context from all specialists. No truncation."""
        parts = []
        agents = [
            ("webclaw", f"search {query}"),
            ("dataclaw", f"search {query}"),
            ("fileclaw", f"context {query}"),
            ("lawclaw", f"/ask {query}"),
            ("mediclaw", f"/med {query}"),
            ("txclaw", f"/search {query}"),
            ("claw_coder", f"/explain {query}"),
            ("crustyclaw", f"/explain {query}"),
            ("interpretclaw", f"/detect {query}"),
            ("flowclaw", f"/flowchart {query}"),
            ("plotclaw", f"/plot {query}"),
            ("mathematicaclaw", f"/solve {query}"),
        ]
        for name, task in agents:
            try:
                result = self.call_agent(name, task, timeout=10)
                if result and len(result) > 20:
                    parts.append(f"[{name}]: {result}")
            except:
                pass
        
        # Search chronicle index - no truncation
        try:
            chronicle_results = self.search_chronicle(query, limit=10)
            if chronicle_results:
                ctx_parts = []
                for c in chronicle_results:
                    if isinstance(c, dict):
                        ctx = c.get('context', '') or c.get('url', '')
                    elif hasattr(c, 'context'):
                        ctx = getattr(c, 'context', '')
                    else:
                        ctx = str(c)
                    if ctx:
                        ctx_parts.append(ctx)
                if ctx_parts:
                    parts.append("[chronicle]: " + " | ".join(ctx_parts))
        except:
            pass
        
        return "\n\n".join(parts) if parts else ""

    def ask_llm(self, prompt: str) -> str:
        """Call LLMClaw with full chronicle context. No truncation, no limits."""
        try:
            # Search chronicle for ALL relevant context - no limit on results or content
            context = ""
            chronicle_results = self.search_chronicle(prompt, limit=10)
            if chronicle_results:
                lines = []
                for c in chronicle_results:
                    if isinstance(c, dict):
                        ctx = c.get('context', '') or c.get('url', '')
                    elif hasattr(c, 'context'):
                        ctx = getattr(c, 'context', '')
                    else:
                        ctx = str(c)
                    if ctx:
                        lines.append(ctx)
                if lines:
                    context = "\n---\n".join(lines)
            
            full_prompt = prompt
            if context:
                full_prompt = f"CONTEXT (use this data to answer):\n{context}\n\nQUERY: {prompt}\n\nAnswer the query directly using all relevant data from the context above. Include names, addresses, phone numbers, descriptions, and any other details found in the context."
            
            r = requests.post(
                f"{self.A2A}/v1/message/llmclaw",
                json={"task": f"/llm {full_prompt}"},
                timeout=600
            )
            if r.status_code == 200:
                return r.json().get("result", "")
        except:
            pass
        return "LLMClaw unavailable"

    # ---- Chronicle ----
    def search_chronicle(self, query: str, limit: int = 10) -> list:
        """Search the chronicle ledger. Filters by agent's domain."""
        try:
            from agents.webclaw.core.chronicle_ledger import get_chronicle
            chronicle = get_chronicle()
            return chronicle.recover_by_context(query, limit, source_filter=self.name)
        except:
            # Fallback if source_filter not supported yet
            try:
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
        """Learn a fact into UNIFIED shared memory — all agents benefit."""
        self.memory.learn(self.name, fact[:80], fact, source='agent_learned')

    def get_facts(self):
        """Get facts from unified memory — cross-agent knowledge."""
        results = self.memory.recall('', limit=50)
        return {r['key']: r['value'] for r in results if r.get('agent') == self.name}

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
        """Constitutional ask: Retrieval -> Truth -> Policy -> LLM.
        
        Every agent query passes through:
        1. WebClaw Retriever (BM25 + source confidence)
        2. Truth Resolver (web_verified > chronicle > memory > inference)
        3. Execution Policy (permission check)
        4. LLM inference (lowest trust tier, grounded by verified sources)
        """
        retriever_results = []
        try:
            from agents.webclaw.core.retriever import search as retriever_search
            retrieved = retriever_search(query, top_k=5)
            retriever_results = retrieved.get("results", [])
        except Exception:
            pass
        
        memory_results = self.memory.recall(query, limit=3) if hasattr(self, "memory") else []
        llm_response = self.ask_llm(query)
        
        from shared.truth_resolver import merge_with_retriever
        resolved = merge_with_retriever(
            retriever_results=retriever_results,
            memory_results=memory_results,
            llm_inference=llm_response,
            llm_confidence=0.5,
        )
        
        from shared.execution_policy import ExecutionPolicy
        from shared.decision_ledger import get_ledger
        policy_check = ExecutionPolicy.check("ALLOW_HTTP_REQUEST")
        if not policy_check["allowed"]:
            return f"Execution blocked: {policy_check["reason"]}"
        
        if resolved["status"] == "conflict_detected":
            response = llm_response + "\n\n[TRUTH CONFLICT DETECTED] Resolved to: " + str(resolved.get("source_type","")) + " (" + str(resolved.get("source","")) + ")"
        elif resolved["source_type"] == "web_verified" and resolved.get("confidence", 0) > 0.5:
            grounding = "\n\n[GROUND TRUTH - " + str(resolved.get("source","")) + "]\n" + str(resolved.get("resolved",""))
            prompt = "Using the verified information below, answer: " + query + grounding
            response = self.ask_llm(prompt)
        elif resolved["source_type"] == "inference":
            response = llm_response + "\n\n[CONFIDENCE: UNCERTAIN - No authoritative source verified]"
        else:
            response = llm_response
        
        try:
            if hasattr(self, "memory"):
                from shared.memory_guard import should_persist
                if should_persist(resolved.get("source_type", "inference"), resolved.get("confidence", 0)):
                    self.memory.learn_from_interaction(self.name, query, response)
        except Exception:
            pass
        
        return response
