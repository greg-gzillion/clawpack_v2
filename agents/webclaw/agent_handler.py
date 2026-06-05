"""A2A Handler for WebClaw - AI-Powered Search & Fetch"""
import sys, time
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from webclaw import Webclaw
from agents.webclaw.providers.webclaw_provider import WebclawProvider
from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err

webclaw = Webclaw()
provider = WebclawProvider()


class WebClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("webclaw")

    def _gather_context(self, query=""):
        parts = []
        chronicle_results = self.search_chronicle(query, limit=5)
        if chronicle_results:
            lines = []
            for c in chronicle_results:
                ctx = c.get("context", "") if isinstance(c, dict) else str(c)
                if ctx: lines.append(ctx[:1000])
            if lines: parts.append("[Chronicle]: " + "\n".join(lines))
        return "\n".join(parts) if parts else ""

    def handle(self, task):
        self.track_interaction()
        track_start = time.time()
        task = task.strip()

        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""

        if cmd in ("/delegate",) and args:
                parts2 = args.split(maxsplit=1); target = parts2[0]
                task_text = parts2[1] if len(parts2) > 1 else ""
                known = ["plotclaw","flowclaw","claw_coder","crustyclaw","dataclaw","designclaw","draftclaw","drawclaw","dreamclaw","docuclaw","lawclaw","mathematicaclaw","interpretclaw","langclaw","fileclaw","txclaw","mediclaw","liberateclaw","llmclaw","rustypycraw"]
                if target in known: result = str(self.call_agent(target, task_text) or "")
                else: result = f"Unknown: {target}"
                return {"status": "success", "result": result}
        if cmd in ("/stats",):
            return {"status": "success", "result": f"WebClaw | Chronicle: 35K+ entries | Interactions: {self.state.get('interactions', 0)}"}
        if cmd in ("/help",):
            return {"status": "success", "result": "WebClaw - Web Search & Chronicle\n  search <query>  fetch <url>  /stats  /delegate <agent> <task>"}
        if task.startswith("fetch ") or task.startswith("http"):
            url = task.replace("fetch ", "", 1).strip() if task.startswith("fetch ") else task
            try:
                result = webclaw.fetch_with_citation(url)
                if result.get("success"):
                    return {
                        "status": "success",
                        "result": result["citation"] + "\n\n" + result["content"]
                    }
                return {
                    "status": "error",
                    "result": result.get("error", "fetch failed")
                }
            except Exception as e:
                log_err("webclaw", "fetch_error", str(e)[:200])
                return {"status": "error", "result": str(e)}

        if task.startswith("search "):
            query = task[7:].strip()
        else:
            query = task

        try:
            # Extract namespace from calling agent
            namespace = None
            if query.startswith("ns:"):
                parts = query.split(" ", 1)
                namespace = parts[0][3:]
                query = parts[1] if len(parts) > 1 else query
            # 1. Structured candidates from provider
            provider_docs = provider.search_structured(query, max_results=20, namespace=namespace)

            # 2. Chronicle candidates
            chronicle_docs = []
            try:
                from agents.webclaw.core.chronicle_ledger import get_chronicle
                chronicle = get_chronicle()
                chronicle_results = chronicle.recover_by_context(
                    f"ns:{namespace} {query}" if namespace else query, limit=10
                )
                for c in chronicle_results:
                    chronicle_docs.append({
                        "url": c.get("url", ""),
                        "context": c.get("context", ""),
                        "source": c.get("source", "chronicle"),
                    })
            except Exception as e:
                log_err("webclaw", "chronicle_error", str(e)[:200])

            # 3. Merge and BM25 re-rank with source confidence
            all_docs = provider_docs + chronicle_docs
            if all_docs:
                from agents.webclaw.core.retriever import get_retriever
                retriever = get_retriever()
                retriever.bm25.index(all_docs)
                ranked = retriever.bm25.search(query, top_k=10)

                lines = [f"Found {len(ranked)} results for '{query}':\n"]
                for i, doc in enumerate(ranked, 1):
                    lines.append(
                        f"{i}. {doc.get('url', '')} "
                        f"[score: {doc.get('final_score', 0):.3f}, "
                        f"source: {doc.get('source_weight', 0):.2f}]"
                    )
                    ctx = doc.get('context', '')
                    if ctx:
                        lines.append(f"   {ctx[:300]}...")
                    lines.append("")
                result = "\n".join(lines)
            else:
                result = f"No results found for '{query}'"

            return {"status": "success", "result": str(result)}
        except Exception as e:
            log_err("webclaw", "search_error", str(e)[:200])
            return {"status": "error", "result": str(e)}


_agent = WebClawAgent()


def process_task(task: str, agent: Optional[str] = None):
    return _agent.handle(task)
