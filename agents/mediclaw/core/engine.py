"""Core Medical Engine - uses chronicle index + LLMClaw with citations"""
import sys
from pathlib import Path

MEDICLAW_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = MEDICLAW_DIR.parent.parent

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "agents" / "llmclaw"))

from commands.llm_enhanced import run as llm_run

class MedicalEngine:
    def __init__(self):
        pass

    def _search_context(self, query: str) -> str:
        """Search chronicle index for relevant medical context"""
        try:
            from agents.webclaw.core.chronicle_ledger import get_chronicle
            chronicle = get_chronicle()
            results = chronicle.recover_by_context(query, limit=100)
            if results:
                lines = []
                for r in results:
                    lines.append(f"Source: {r['url']}\nContext: {r['context'][:50000]}")
                return "\n\n".join(lines)
        except:
            pass
        return ""

    def _call_llm(self, prompt: str, context: str = "") -> str:
        if context:
            prompt = f"Reference context from chronicle medical sources:\n{context[:2000]}\n\n{prompt}"
        prompt += "\n\nIMPORTANT: Cite specific sources from the reference context above. Include URLs inline as [Source: url]. If using general medical knowledge, cite established guidelines (AHA/ACC, NIH, CDC, WHO)."
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