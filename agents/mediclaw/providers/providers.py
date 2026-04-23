"""Providers - API and Webclaw"""

import requests
from config.settings import Config

class APIProvider:
    def __init__(self):
        self.api_key = Config.get_api_key()
    
    def call(self, prompt: str) -> str:
        if not self.api_key:
            return None
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}], "max_tokens": 1500},
                timeout=60
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
        except:
            pass
        return None

class WebclawProvider:
    def __init__(self):
        self.data_path = Config.WEBCLAW_PATH
    
    def search(self, term: str) -> list:
        results = []
        if not self.data_path.exists():
            return results
        
        term_lower = term.lower()
        for specialty_dir in self.data_path.iterdir():
            if not specialty_dir.is_dir():
                continue
            for md_file in specialty_dir.glob("*.md"):
                try:
                    content = md_file.read_text(encoding='utf-8')
                    if term_lower in content.lower() or term_lower in specialty_dir.name.lower():
                        lines = content.split('\n')
                        results.append({
                            "specialty": specialty_dir.name,
                            "file": md_file.name,
                            "content": content,
                            "preview": '\n'.join(lines) + "\n..."
                        })
                except:
                    continue
        return results
    
    def get_specialty(self, name: str) -> str:
        specialty_path = self.data_path / name
        if not specialty_path.exists():
            return None
        md_files = list(specialty_path.glob("*.md"))
        if not md_files:
            return None
        output = f"📚 WEBCLAW: {name.upper()}\n\n"
        for md in md_files:
            output += md.read_text(encoding='utf-8') + "\n\n"
        return output
    
    def list_specialties(self) -> list:
        if self.data_path.exists():
            return sorted([d.name for d in self.data_path.iterdir() if d.is_dir()])
        return []
