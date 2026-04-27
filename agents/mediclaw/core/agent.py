"""Mediclaw Agent - Stateful session agent wrapping MedicalEngine + LLMClaw"""
import sys
from pathlib import Path
import time

MEDICLAW_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = MEDICLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "agents" / "llmclaw"))

from core.engine import MedicalEngine
from commands.llm_enhanced import run as llm_run


class MediclawAgent:
    def __init__(self):
        self.engine = MedicalEngine()
        self.session = {
            "started": time.strftime("%Y-%m-%d %H:%M"),
            "queries": [],
        }

    # ---- Engine delegates (these use engine._call_llm which includes citations) ----
    def diagnose(self, symptoms: str) -> str:
        self.session["queries"].append(f"diagnose:{symptoms}")
        return self.engine.diagnose(symptoms)

    def treatment(self, condition: str) -> str:
        self.session["queries"].append(f"treatment:{condition}")
        return self.engine.treatment(condition)

    def research(self, query: str) -> str:
        self.session["queries"].append(f"research:{query}")
        return self.engine.research(query)

    def list_sources(self) -> list:
        return self.engine.list_sources()

    def webclaw_sources(self) -> list:
        return self.engine.list_sources()

    def get_stats(self) -> dict:
        return {
            "started": self.session["started"],
            "queries": len(self.session["queries"]),
            "sources": len(self.list_sources()),
        }

    # ---- LLM-backed commands with citations ----
    def _ask_medical(self, specialty: str, query: str) -> str:
        prompt = f"You are a medical AI assistant specializing in {specialty}. Provide accurate, helpful information about: {query}. Include relevant medical context, standard practices, and any warnings or precautions.\n\nIMPORTANT: Cite authoritative medical sources (e.g., NIH, CDC, WHO, AHA/ACC, specialty college guidelines, UpToDate, peer-reviewed journals). Include specific guideline names and years where applicable. Note: this is informational, not medical advice."
        return llm_run(prompt)

    def medications(self, drug: str) -> str:
        self.session["queries"].append(f"medications:{drug}")
        return self._ask_medical("pharmacology", f"drug information for {drug}. Include uses, dosing, side effects, contraindications, and interactions.")

    def interactions(self, drugs: str) -> str:
        self.session["queries"].append(f"interactions:{drugs}")
        return self._ask_medical("pharmacology", f"drug interactions between: {drugs}. Include severity, mechanism, and management recommendations.")

    def warnings(self, drug: str) -> str:
        self.session["queries"].append(f"warnings:{drug}")
        return self._ask_medical("pharmacology", f"FDA warnings, black box warnings, and safety concerns for: {drug}.")

    def pediatrics(self, issue: str) -> str:
        self.session["queries"].append(f"pediatrics:{issue}")
        return self._ask_medical("pediatrics", f"pediatric care for: {issue}. Include age-specific considerations, dosing if applicable, and warning signs.")

    def geriatrics(self, issue: str) -> str:
        self.session["queries"].append(f"geriatrics:{issue}")
        return self._ask_medical("geriatrics", f"geriatric care for: {issue}. Include age-related considerations, polypharmacy risks, and fall/prevention guidance.")

    def lab_tests(self, test: str) -> str:
        self.session["queries"].append(f"lab:{test}")
        return self._ask_medical("laboratory medicine", f"lab test: {test}. Include normal ranges, interpretation of abnormal results, and clinical significance.")

    def coding(self, diagnosis: str) -> str:
        self.session["queries"].append(f"icd:{diagnosis}")
        return self._ask_medical("medical coding", f"ICD-10 codes for: {diagnosis}. Include primary code, alternatives, and coding guidelines.")

    def prevention(self, condition: str) -> str:
        self.session["queries"].append(f"prevention:{condition}")
        return self._ask_medical("preventive medicine", f"prevention guidelines for: {condition}. Include screening recommendations, lifestyle modifications, and risk reduction strategies.")

    def diet(self, condition: str) -> str:
        self.session["queries"].append(f"diet:{condition}")
        return self._ask_medical("clinical nutrition", f"dietary recommendations for: {condition}. Include foods to eat, foods to avoid, and meal planning guidance.")

    def exercise(self, condition: str) -> str:
        self.session["queries"].append(f"exercise:{condition}")
        return self._ask_medical("physical medicine and rehabilitation", f"exercise guidance for: {condition}. Include recommended activities, intensity levels, precautions, and contraindications.")

    def natural(self, condition: str) -> str:
        self.session["queries"].append(f"natural:{condition}")
        return self._ask_medical("integrative medicine", f"natural and complementary remedies for: {condition}. Include evidence-based options, efficacy data, and safety considerations.")

    def natural_remedies(self, condition: str) -> str:
        return self.natural(condition)

    def procedure(self, name: str) -> str:
        self.session["queries"].append(f"procedure:{name}")
        return self._ask_medical("surgery and procedures", f"medical procedure: {name}. Include indications, technique overview, risks, recovery, and alternatives.")

    def procedures(self, name: str) -> str:
        return self.procedure(name)

    def prognosis(self, condition: str) -> str:
        self.session["queries"].append(f"prognosis:{condition}")
        return self._ask_medical("internal medicine", f"disease prognosis for: {condition}. Include survival rates, progression patterns, prognostic factors, and quality of life considerations.")

    def referral(self, condition: str) -> str:
        self.session["queries"].append(f"referral:{condition}")
        return self._ask_medical("primary care", f"specialist referral guidance for: {condition}. Include which specialty to refer to, urgency, and what workup to complete before referral.")

    def emergency(self, symptom: str) -> str:
        self.session["queries"].append(f"emergency:{symptom}")
        return self._ask_medical("emergency medicine", f"emergency triage for: {symptom}. Include red flags, immediate actions, when to call 911, and differential for life-threatening causes.")
