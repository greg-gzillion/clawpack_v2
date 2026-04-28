"""A2A Handler for LLMClaw - Model Management + Multi-Agent Orchestration"""
import sys, os, json
from pathlib import Path

LLMCLAW_DIR = Path(__file__).parent
PROJECT_ROOT = LLMCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(LLMCLAW_DIR))

from shared.base_agent import BaseAgent

def _get_working_llms():
    f = PROJECT_ROOT / "models" / "working_llms.json"
    if f.exists():
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except:
            pass
    return []

def _get_active():
    f = PROJECT_ROOT / "models" / "active_model.json"
    if f.exists():
        try:
            return json.loads(f.read_text())
        except:
            pass
    return {"model": "llama-3.1-8b-instant", "source": "groq"}

def _set_active(model_name, source):
    config = _get_active()
    config["model"] = model_name
    config["source"] = source
    f = PROJECT_ROOT / "models" / "active_model.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(config, indent=2))

class LLMClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("llmclaw")

    def _run_llm(self, prompt):
        os.chdir(str(LLMCLAW_DIR))
        from commands.llm import run
        return run(prompt)

    def orchestrate(self, query: str, domain: str = "") -> str:
        """Intelligent multi-agent orchestration. Claude decides which agents to call."""
        
        # Available agents and their capabilities
        agent_catalog = """Available agents and what they do:
- mediclaw: medical research, diagnoses, treatments, medications, lab tests
- lawclaw: legal research, case law, statutes, court information, contracts
- webclaw: online web search, URL fetching, web content retrieval
- dataclaw: local file and document search
- fileclaw: file management, format conversion, import/export
- draftclaw: document drafting, templates, blueprints
- interpretclaw: language translation, interpretation
- mathematicaclaw: math, calculations, equations, graphing
- txclaw: blockchain, cryptocurrency, smart contracts
- crustyclaw: Rust/Cargo operations
- rustypycraw: code scanning and analysis
- plotclaw: data visualization and charts"""
        
        # Ask Claude to decide what to do
        plan_prompt = f"""You are an AI orchestrator. Decide which agents to query and what to ask them.

USER QUERY: {query}
DOMAIN (if specified): {domain}

{agent_catalog}

Return a JSON plan with agent calls. Format:
{{"agents": [{{"agent": "agentname", "task": "command or query to send"}}]}}

Choose the most relevant agents. Use specific commands where possible. Only include agents that would provide useful information.
Keep it to 3 agents maximum for speed.

Return ONLY valid JSON, no other text:"""
        
        plan_json = self._run_llm(plan_prompt)
        
        # Parse the plan
        try:
            # Extract JSON from response (Claude might wrap it)
            import re
            json_match = re.search(r'\{.*\}', plan_json, re.DOTALL)
            if json_match:
                plan = json.loads(json_match.group())
            else:
                plan = json.loads(plan_json)
        except:
            # Fallback: basic chronicle + web search
            plan = {"agents": [
                {"agent": "webclaw", "task": f"search {query}"}
            ]}
        
        # Execute the plan
        context_parts = []
        for step in plan.get("agents", []):
            agent = step["agent"]
            task = step["task"]
            try:
                result = self.call_agent(agent, task, timeout=20)
                if result and "Error" not in str(result) and "error" not in str(result).lower():
                    context_parts.append(f"[{agent}]: {result[:1000]}")
            except:
                pass
        
        # Also search chronicle directly
        chronicle_results = self.search_chronicle(query, limit=5)
        if chronicle_results:
            chronicle_lines = []
            for c in chronicle_results:
                ctx = c.get('context', '') if isinstance(c, dict) else str(c)
                chronicle_lines.append(ctx[:300])
            if chronicle_lines:
                context_parts.insert(0, "[chronicle]: " + "\n".join(chronicle_lines))
        
        context = "\n\n".join(context_parts)
        
        # Final synthesis
        final_prompt = f"""User query: {query}

Research context from specialists:
{context[:4000]}

Provide a comprehensive answer with citations from the context above. Include specific sources, URLs, and file references. If the context is insufficient, note what's missing."""
        
        return self._run_llm(final_prompt)

    def handle(self, task: str) -> dict:
        self.track_interaction()
        os.chdir(str(LLMCLAW_DIR))
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""

        try:
            if cmd == "/llm" and args:
                result = self._run_llm(args)
            
            elif cmd == "/orchestrate" and args:
                result = self.orchestrate(args)
            
            elif cmd in ("/models", "/list", "models", "list"):
                models = _get_working_llms()
                obliterated = [m for m in models if m.get("obliterated")]
                standard = [m for m in models if not m.get("obliterated")]
                active = _get_active()
                result = f"Active: {active.get('model')} ({active.get('source')})\n\n"
                result += f"OBLITERATED ({len(obliterated)}):\n"
                result += "\n".join(f"  - {m['model']} ({m.get('size','?')})" for m in obliterated)
                result += f"\n\nSTANDARD ({len(standard)}):\n"
                result += "\n".join(f"  - {m['model']} ({m.get('size','?')})" for m in standard)
                result += "\n\nUse /use <model_name> to switch"
            elif cmd in ("/use", "use") and args:
                _set_active(args, "ollama" if ":" in args else "groq")
                result = f"Switched to: {args}"
            elif cmd in ("/obliterated", "obliterated"):
                models = _get_working_llms()
                lib = [m for m in models if m.get("obliterated")]
                result = f"Obliterated models available: {len(lib)}\n" + "\n".join(m["model"] for m in lib)
            elif cmd in ("/normal", "normal"):
                models = _get_working_llms()
                std = [m for m in models if not m.get("obliterated")]
                result = f"Standard models available: {len(std)}\n" + "\n".join(m["model"] for m in std)
            elif cmd in ("/help", "help"):
                result = "LLMClaw - Model Manager + Orchestrator\n  /llm <prompt> - Direct inference\n  /orchestrate <query> - Multi-agent orchestration\n  /models /use /obliterated /normal /help /stats"
            elif cmd in ("/stats", "stats"):
                active = _get_active()
                result = f"LLMClaw | Active: {active.get('model')} ({active.get('source')}) | Interactions: {self.state.get('interactions', 0)}"
            else:
                # Default: orchestrate unknown commands
                result = self.orchestrate(task)

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = LLMClawAgent()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)