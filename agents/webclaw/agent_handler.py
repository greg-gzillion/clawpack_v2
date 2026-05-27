"""A2A Handler for WebClaw - AI-Powered Search & Fetch"""
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from webclaw import Webclaw
from agents.webclaw.providers.webclaw_provider import WebclawProvider
from shared.base_agent import BaseAgent

webclaw = Webclaw()
provider = WebclawProvider()


class WebClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("webclaw")

    def handle(self, task):
        self.track_interaction()
        task = task.strip()

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
                return {"status": "error", "result": str(e)}

        if task.startswith("search "):
            query = task[7:].strip()
        else:
            query = task

        try:
            result = provider.search_with_context(query)

            try:
                from agents.webclaw.core.chronicle_ledger import get_chronicle
                chronicle = get_chronicle()
                chronicle_results = chronicle.recover_by_context(query, limit=2000000)
                if chronicle_results:
                    result += "\n\n=== Web Results ==="
                    for c in chronicle_results[:3]:
                        url = c.url if hasattr(c, "url") else str(c)
                        try:
                            cited = webclaw.fetch_with_citation(url)
                            if cited.get("success"):
                                result += "\n\n" + cited["citation"] + "\n"
                                result += cited["content"][:1000]
                        except Exception:
                            pass
            except Exception as e:
                result += "\n\n(chronicle: " + str(e) + ")"

            try:
                prompt = (
                    "Analyze these search results and provide the most "
                    "relevant information for: " + query + "\n\nResults:\n" +
                    result[:3000]
                )
                analysis = self.ask_llm(prompt)
                if analysis:
                    result = "## AI Analysis\n" + analysis + "\n\n## Raw Results\n" + result
                    self.learn("search:" + query, result[:1000])
            except Exception as e:
                result += "\n\n(AI analysis: " + str(e) + ")"

            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "result": str(e)}


_agent = WebClawAgent()


def process_task(task: str, agent: Optional[str] = None):
    return _agent.handle(task)