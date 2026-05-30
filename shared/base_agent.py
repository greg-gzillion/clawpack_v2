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
        self._webclaw = None
        self._unified_memory = None
        self._llmclaw_available = True

    @property
    def webclaw(self):
        if self._webclaw is None:
            from agents.webclaw.providers.webclaw_provider import WebclawProvider
            self._webclaw = WebclawProvider()
        return self._webclaw

    @property
    def memory(self):
        if self._unified_memory is None:
            from shared.memory.unified_memory import get_memory
            self._unified_memory = get_memory()
        return self._unified_memory

    def _load_state(self):
        if self.memory_file.exists():
            try:
                data = json.loads(self.memory_file.read_text())
                return data.get("agent_states", {}).get(self.name, {})
            except Exception as e:
                self._log_error("memory_load", str(e))
        return {"interactions": 0, "successful": 0}

    def _save_state(self):
        data = {}
        if self.memory_file.exists():
            try:
                data = json.loads(self.memory_file.read_text())
            except Exception as e:
                self._log_error("memory_init", str(e))
        if "agent_states" not in data:
            data["agent_states"] = {}
        data["agent_states"][self.name] = self.state
        self.memory_file.parent.mkdir(exist_ok=True)
        self.memory_file.write_text(json.dumps(data, indent=2))

    def _log_error(self, context, error):
        try:
            print(f"[{self.name}] {context}: {error}", flush=True)
        except:
            pass

    def learn(self, key: str, value: Any):
        self.state[key] = value
        self._save_state()

    def recall(self, key: str):
        return self.state.get(key)

    def search_web(self, query: str, max_results: int = 10) -> str:
        return self.webclaw.search_with_context(query, max_results)

    def search_web_raw(self, query: str, max_results: int = 20) -> str:
        return self.webclaw.search(query, max_results)

    def search_local(self, query: str) -> str:
        try:
            from agents.dataclaw.modules.search.local_search import search_local
            return search_local(query)
        except Exception as e:
            self._log_error("local_search", str(e))
            return ""

    def ask_memory(self, query: str) -> str:
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
        except Exception as e:
            self._log_error("shared_knowledge", str(e))
        return ""

    def call_agent(self, agent_name: str, task: str, timeout: int = 120) -> str:
        """Call another agent with circuit breaker protection.
        After 5 consecutive failures, the circuit opens and calls fail fast
        for 60 seconds before attempting recovery.
        """
        from shared.error_handler import get_circuit_breaker
        breaker = get_circuit_breaker(agent_name)
        
        def _do_call():
            r = requests.post(
                f'{self.A2A}/v1/message/{agent_name}',
                json={'task': task},
                timeout=timeout
            )
            if r.status_code == 200:
                return r.json().get('result', '')
                raise Exception(f'HTTP {r.status_code}')
        
        try:
            return breaker.call(_do_call)
        except Exception as e:
            self._log_error(f'call_agent:{agent_name}', str(e)[:200])
            return f'[{agent_name}] unavailable: {str(e)[:100]}'

    def _gather_all_context(self, query=""):
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
        """Call Sovereign Gateway directly. Constitutional path per Article I."""
        try:
            context = ""
            chronicle_results = self.search_chronicle(prompt, limit=10)
            if chronicle_results:
                lines_ctx = []
                for c in chronicle_results:
                    if isinstance(c, dict):
                        ctx = c.get("context", "") or c.get("url", "")
                    elif hasattr(c, "context"):
                        ctx = getattr(c, "context", "")
                    else:
                        ctx = str(c)
                    if ctx:
                        lines_ctx.append(ctx)
                if lines_ctx:
                    context = "\n---\n".join(lines_ctx)
            full_prompt = prompt
            if context:
                full_prompt = (
                    "CONTEXT (use this data to answer):\n" + context +
                    "\n\nQUERY: " + prompt +
                    "\n\nAnswer the query directly using all relevant data from the context above."
                )
            from shared.llm.client import get_llm_client
            client = get_llm_client()
            response = client.call_sync(full_prompt, agent=self.name, provider='anthropic')
            return response.content
        except Exception as e:
            self._log_error("sovereign_gateway", str(e))
        return "Sovereign Gateway unavailable"

    def ask_llm_smart(self, prompt: str, task_type: str = None, agent_name: str = None) -> str:
        """Constitutional routing through Sovereign Gateway with task detection."""
        from shared.llm.router import route as router_route

        name = agent_name or self.name
        detected_type = task_type

        if not detected_type:
            prompt_lower = prompt.lower()
            if any(kw in prompt_lower for kw in ["code", "function", "class", "def ", "write a", "generate", "implement"]):
                detected_type = "code_generation"
            elif any(kw in prompt_lower for kw in ["plan", "orchestrate", "design", "architect", "strategy", "analyze"]):
                detected_type = "orchestration"
            elif any(kw in prompt_lower for kw in ["summarize", "summary", "explain", "translate"]):
                detected_type = "summarization"
            elif any(kw in prompt_lower for kw in ["private", "sensitive", "confidential", "secret"]):
                detected_type = "private_reasoning"

        provider = router_route(task_type=detected_type)
        route_hint = ""
        if provider == "direct_model":
            route_hint = " [ROUTE: obliterated local model]"
        elif provider == "anthropic":
            route_hint = " [ROUTE: cloud model]"

        context = ""
        try:
            chronicle_results = self.search_chronicle(prompt, limit=5)
            if chronicle_results:
                lines = []
                for c in chronicle_results:
                    if isinstance(c, dict):
                        ctx = c.get("context", "") or c.get("url", "")
                    elif hasattr(c, "context"):
                        ctx = getattr(c, "context", "")
                    else:
                        ctx = str(c)
                    if ctx:
                        lines.append(ctx)
                if lines:
                    context = "\n---\n".join(lines)
        except Exception as e:
            self._log_error("context_extract", str(e))

        full_prompt = prompt
        if context:
            full_prompt = "CONTEXT:\n" + context + "\n\nQUERY: " + prompt

        task_prefix = f"[TASK:{detected_type}] " if detected_type else ""
        full_prompt = task_prefix + full_prompt

        try:
            from shared.llm.client import get_llm_client
            client = get_llm_client()
            response = client.call_sync(full_prompt, agent=name)
            result = response.content
            if route_hint:
                result = result + "\n\n" + route_hint
            return result
        except Exception as e:
            self._log_error("sovereign_gateway", str(e))
        return "Sovereign Gateway unavailable"

    def search_chronicle(self, query: str, limit: int = 10) -> list:
        try:
            from agents.webclaw.core.chronicle_ledger import get_chronicle
            chronicle = get_chronicle()
            return chronicle.recover_by_context(query, limit)
        except Exception as e:
            self._log_error("chronicle_recover", str(e))
            try:
                return chronicle.recover_by_context(query, limit)
            except Exception as e2:
                self._log_error("chronicle_recover_fallback", str(e2))
                return []

    def record_in_chronicle(self, url: str, context: str, source: str = None) -> None:
        try:
            from agents.webclaw.core.chronicle_ledger import get_chronicle
            chronicle = get_chronicle()
            chronicle.record_fetch(url=url, context=context, source=source or self.name)
        except Exception as e:
            self._log_error("chronicle_record", str(e))

    def learn_fact(self, fact: str):
        self.memory.learn(self.name, fact[:80], fact, source='agent_learned')

    def get_facts(self):
        results = self.memory.recall('', limit=50)
        return {r['key']: r['value'] for r in results if r.get('agent') == self.name}

    def lookup_jurisdiction(self, city_state: str, resource_type: str = "all") -> dict:
        """Search 3,800+ city jurisdiction files using Chronicle FTS5 index.
        Args: city_state e.g. 'Denver CO', resource_type: 'library','hospital','police','building_codes','all'
        Returns: dict with libraries, hospitals, police, building_codes, urls, municipal_info
        """
        import re
        
        parts = city_state.strip().split()
        if len(parts) < 2:
            return {"error": "Provide city and state, e.g. 'Denver CO'"}
        
        state = parts[-1].upper()
        city = " ".join(parts[:-1])
        
        result = {"city": city, "state": state, "libraries": [], "hospitals": [], "police": [], "building_codes": [], "urls": [], "municipal_info": []}
        
        # Use Chronicle FTS5 index ? searches across county boundaries automatically
        try:
            from agents.webclaw.core.chronicle_ledger import get_chronicle
            chronicle = get_chronicle()
            
            # Search for city+state in the jurisdiction reference files
            query = f"{city} {state}"
            chronicle_results = chronicle.recover_by_context(query, limit=50)
            
            for entry in chronicle_results:
                ctx = entry.get("context", "") if isinstance(entry, dict) else str(entry)
                url = entry.get("url", "") if isinstance(entry, dict) else ""
                
                if not ctx:
                    continue
                
                # Only process jurisdiction reference files
                if "jurisdictions/us" not in str(url) and "jurisdictions/us" not in str(ctx):
                    continue
                
                # Extract by resource type
                for line in ctx.split("\n"):
                    line_stripped = line.strip()
                    if not line_stripped or len(line_stripped) < 10:
                        continue
                    
                    if resource_type in ("all", "library"):
                        if "library" in line_stripped.lower() and ("http" in line_stripped or chr(8212) in line_stripped or "" in line_stripped):
                            if line_stripped not in result["libraries"]:
                                result["libraries"].append(line_stripped[:200])
                    
                    if resource_type in ("all", "hospital"):
                        if ("hospital" in line_stripped.lower() or "medical center" in line_stripped.lower()) and len(line_stripped) > 20:
                            if line_stripped not in result["hospitals"]:
                                result["hospitals"].append(line_stripped[:200])
                    
                    if resource_type in ("all", "police"):
                        if "police" in line_stripped.lower() and len(line_stripped) > 20:
                            if line_stripped not in result["police"]:
                                result["police"].append(line_stripped[:200])
                    
                    if resource_type in ("all", "building_codes"):
                        if any(kw in line_stripped.lower() for kw in ["ibc ", "irc ", "building code", "frost depth", "snow load", "wind speed", "seismic", "permit"]):
                            if line_stripped not in result["building_codes"]:
                                result["building_codes"].append(line_stripped[:200])
                    
                    if "https://" in line_stripped:
                        extracted_url = line_stripped[line_stripped.index("https://"):].split()[0].rstrip(")")
                        if extracted_url not in result["urls"]:
                            result["urls"].append(extracted_url)
        
        except Exception:
            pass
        
        return result
    
    def track_interaction(self):
        self.state["interactions"] = self.state.get("interactions", 0) + 1
        self._save_state()

    def get_stats(self):
        return {"name": self.name, "interactions": self.state.get("interactions", 0)}

    def handle(self, task: str) -> dict:
        self.track_interaction()
        return {"status": "error", "result": f"{self.name}: handle() not implemented"}

    def smart_ask(self, query: str, domain: str = "") -> str:
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
        policy_check = ExecutionPolicy.check("ALLOW_HTTP_REQUEST")
        if not policy_check["allowed"]:
            reason = policy_check['reason']
            return "Execution blocked: " + reason

        if resolved["status"] == "conflict_detected":
            response = (
                llm_response +
                "\n\n[TRUTH CONFLICT DETECTED] Resolved to: " +
                str(resolved.get("source_type", "")) +
                " (" + str(resolved.get("source", "")) + ")"
            )
        elif resolved["source_type"] == "web_verified" and resolved.get("confidence", 0) > 0.5:
            grounding = (
                "\n\n[GROUND TRUTH - " +
                str(resolved.get("source", "")) + "]\n" +
                str(resolved.get("resolved", ""))
            )
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

    # ── Shared Learning (all 21 agents inherit these) ─────────────────────────

    def learn_from_task(self, query: str, result: str, source_type: str = "web_verified",
                        confidence: float = 0.85, urls: list = None) -> bool:
        """Write task result to unified cross-agent memory. All agents share this.
        MemoryGuard enforces: source must be web_verified or chronicle, confidence >= 0.75.
        Call this at the end of handle() after a successful task.
        Returns True if persisted, False if blocked by guard."""
        try:
            from shared.memory_guard import sanitize_memory_write
            check = sanitize_memory_write(self.name, result[:100], source_type, confidence)
            if not check.get("allowed"):
                return False

            fact = f"{query} -> {result[:200]}"
            self.memory.learn(self.name, fact[:80], fact, source='agent_learned')
            self.state["successful"] = self.state.get("successful", 0) + 1
            self._save_state()
            return True
        except Exception as e:
            self._log_error("learn_from_task", str(e))
        return False

    def recall_prior(self, query: str, limit: int = 5) -> list:
        """Search unified memory for prior results related to this query.
        Returns list of fact dicts sorted by relevance."""
        try:
            return self.memory.recall(query, limit)
        except Exception as e:
            self._log_error("recall_prior", str(e))
        return []