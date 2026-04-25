"""Core Medical Engine - uses LLMClaw + WebClaw"""
import sys
from pathlib import Path

MEDICLAW_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = MEDICLAW_DIR.parent.parent

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "agents" / "llmclaw"))

from commands.llm_enhanced import run as llm_run

class MedicalEngine:
    def __init__(self):
        self._init_webclaw()

    def _init_webclaw(self):
        try:
            from agents.webclaw.providers.webclaw_provider import WebclawProvider
            self.webclaw = WebclawProvider()
        except:
            self.webclaw = None

    def _search_context(self, query: str) -> str:
        if self.webclaw:
            try:
                results = self.webclaw.search_with_context(f"medical {query}", max_results=5)
                return str(results) if results else ""
            except:
                pass
        return ""

    def _call_llm(self, prompt: str, context: str = "") -> str:
        if context:
            prompt = f"Medical reference context:\n{context[:2000]}\n\n{prompt}"
        return llm_run(prompt)

    def diagnose(self, symptoms: str) -> str:
        context = self._search_context(symptoms)
        return self._call_llm(
            f"Differential diagnosis for {symptoms}. Include primary, secondary, red flags, tests, urgency.",
            context
        )

    def treatment(self, condition: str) -> str:
        context = self._search_context(condition)
        return self._call_llm(
            f"Treatment guidelines for {condition}. Include first-line, medications, monitoring, follow-up.",
            context
        )

    def research(self, query: str) -> str:
        context = self._search_context(query)
        return self._call_llm(
            f"Medical research on {query}. Provide current treatments and guidelines.",
            context
        )

    def list_sources(self) -> list:
        path = Path("C:/Users/greg/dev/clawpack_v2/agents/webclaw/references/mediclaw")
        if path.exists():
            return sorted([d.name for d in path.iterdir() if d.is_dir()])
        return []
