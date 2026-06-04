"""A2A Handler for LLMClaw - Model Management + Multi-Agent Orchestration"""
import sys, os, json, time
from pathlib import Path

LLMCLAW_DIR = Path(__file__).parent
PROJECT_ROOT = LLMCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(LLMCLAW_DIR))

from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err

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

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search AI model {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + str(web)[:2000])
        chronicle_results = self.search_chronicle(query, limit=5)
        if chronicle_results:
            lines = []
            for c in chronicle_results:
                ctx = c.get("context", "") if isinstance(c, dict) else str(c)
                if ctx: lines.append(ctx[:1000])
            if lines: parts.append("[Chronicle]: " + "\n".join(lines))
        return "\n".join(parts) if parts else ""

    def _run_llm(self, prompt):
        os.chdir(str(LLMCLAW_DIR))
        from commands.llm import run
        return run(prompt)

    def orchestrate(self, query: str, domain: str = "") -> str:
        """Intelligent multi-agent orchestration."""
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
        
        try:
            import re
            json_match = re.search(r'\{.*\}', plan_json, re.DOTALL)
            if json_match:
                plan = json.loads(json_match.group())
            else:
                plan = json.loads(plan_json)
        except:
            plan = {"agents": [
                {"agent": "webclaw", "task": f"search {query}"}
            ]}
        
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
        
        chronicle_results = self.search_chronicle(query, limit=5)
        if chronicle_results:
            chronicle_lines = []
            for c in chronicle_results:
                ctx = c.get('context', '') if isinstance(c, dict) else str(c)
                chronicle_lines.append(ctx[:300])
            if chronicle_lines:
                context_parts.insert(0, "[chronicle]: " + "\n".join(chronicle_lines))
        
        context = "\n\n".join(context_parts)
        
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
                active = _get_active()
                result = f"Active: {active.get('model')} ({active.get('source')})\n\n"
                oblit_dir = Path(__file__).parent.parent.parent / "models" / "obliterated"
                obliterated = []
                if oblit_dir.exists():
                    for model_dir in sorted(oblit_dir.iterdir()):
                        if model_dir.is_dir():
                            meta = model_dir / "abliteration_metadata.json"
                            if meta.exists():
                                d = json.loads(meta.read_text())
                                obliterated.append({
                                    "name": model_dir.name,
                                    "source": d.get("source_model", "unknown"),
                                    "technique": d.get("technique", "unknown"),
                                })
                            else:
                                obliterated.append({"name": model_dir.name, "source": "unknown", "technique": "unknown"})
                result += f"OBLITERATED ({len(obliterated)}):\n"
                for m in obliterated:
                    result += f"  - {m['name']}\n"
                    result += f"    Source: {m['source']}\n"
                    result += f"    Method: {m['technique']}\n"
                models = _get_working_llms()
                standard = [m for m in models if not m.get("obliterated")]
                result += f"\nSTANDARD ({len(standard)}):\n"
                result += "\n".join(f"  - {m['model']} ({m.get('size','?')})" for m in standard)
                result += "\n\nUse /use <model_name> to switch"

            elif cmd in ("/use", "use"):
                from commands.use import run
                result = run(args)

            elif cmd in ("/obliterated", "obliterated"):
                import json as _json
                oblit_dir = Path(__file__).parent.parent.parent / "models" / "obliterated"
                lines = ["OBLITERATED MODELS (safety guardrails surgically removed):", ""]
                if oblit_dir.exists():
                    for model_dir in sorted(oblit_dir.iterdir()):
                        if model_dir.is_dir():
                            meta = model_dir / "abliteration_metadata.json"
                            if meta.exists():
                                d = _json.loads(meta.read_text())
                                source = d.get("source_model", model_dir.name)
                                technique = d.get("technique", "unknown")
                                lines.append("  " + model_dir.name)
                                lines.append("    Source: " + source)
                                lines.append("    Method: " + technique)
                                lines.append("")
                            else:
                                lines.append("  " + model_dir.name + " (no metadata)")
                                lines.append("")
                else:
                    lines.append("  No obliterated models found.")
                lines.append("Use /use <model_name> to activate.")
                result = "\n".join(lines)

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
                result = self.orchestrate(task)

            final_result = str(result)
            if final_result and len(final_result) > 20:
                try:
                    from shared.log_manager import get_logger
                    get_logger().info(f"llmclaw.{cmd}", extra={"args": (args or "")[:100]})
                except Exception:
                    pass
                try:
                    from shared.metrics import get_metrics
                    get_metrics().counter("llmclaw_commands_total", "Total commands").inc()
                except Exception:
                    pass
                try:
                    from agents.llmclaw.commands._memory import remember
                    remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception:
                    pass

            return {"status": "success", "result": str(final_result)}
        except Exception as e:
            log_err("llmclaw", cmd or "unknown", str(e)[:200])
            return {"status": "error", "result": str(e)}


_agent = LLMClawAgent()


def process_task(task: str, agent: str = None):
    return _agent.handle(task)