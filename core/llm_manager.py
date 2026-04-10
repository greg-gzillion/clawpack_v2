"""LLM Manager - Handles model selection and API calls"""
import json
from pathlib import Path
from typing import Optional, List, Dict

class LLMManager:
    def __init__(self):
        self.llms = []
        self.selected_model: Optional[Dict] = None
        self.load_config()
    
    def load_config(self):
        config_path = Path("working_llms.json")
        if config_path.exists():
            data = json.loads(config_path.read_text())
            self.llms = data
    
    def list_models(self) -> str:
        if not self.llms:
            return "No LLMs configured"
        output = [f"\n📦 Working LLMs ({len(self.llms)} total):\n"]
        sources = {}
        for llm in self.llms:
            src = llm["source"]
            if src not in sources:
                sources[src] = []
            sources[src].append(llm["model"])
        for src, models in sources.items():
            output.append(f"\n{src.upper()} ({len(models)}):")
            for m in models:
                marker = " ✅" if self.selected_model and self.selected_model["model"] == m else ""
                output.append(f"  • {m}{marker}")
        return '\n'.join(output)
    
    def find_model(self, query: str) -> Optional[Dict]:
        query_lower = query.lower()
        for llm in self.llms:
            if query_lower in llm["model"].lower():
                return llm
        return None
    
    def select_model(self, query: str) -> str:
        if query == "liberated":
            liberated = [l for l in self.llms if "liberated" in l["model"]]
            if liberated:
                self.selected_model = liberated[0]
                return f"✅ Using liberated models (e.g., {self.selected_model['model']})"
            return "❌ No liberated models available"
        if query in ["reset", "auto"]:
            self.selected_model = None
            return "✅ Reset to auto-select mode"
        found = self.find_model(query)
        if found:
            self.selected_model = found
            return f"✅ Selected: {found['model']} ({found['source']})"
        return f"❌ Model not found: {query}"
    
    def get_current_model(self) -> str:
        if self.selected_model:
            return f"📌 {self.selected_model['model']} ({self.selected_model['source']})"
        return "📌 Auto-select (prefers liberated for creative tasks)"
    
    async def chat(self, prompt: str, model: str = None) -> str:
        return f"[LLM] Response to: {prompt[:50]}..."
