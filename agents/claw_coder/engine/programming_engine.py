"""Programming Engine - Uses webclaw references and chronicle index"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.llm_manager import get_llm_manager

class ProgrammingEngine:
    def __init__(self, language: str = "python"):
        self.language = language.lower()
        self.llm = get_llm_manager()
        self.refs_path = PROJECT_ROOT / "agents/webclaw/references/claw_coder"
        self.chronicle = None
        self._init_chronicle()
    
    def _init_chronicle(self):
        try:
            from shared.chronicle_helper import search_chronicle
            self.chronicle = search_chronicle
            print("✅ Chronicle connected", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ Chronicle error: {e}", file=sys.stderr)
            self.chronicle = None
    
    def get_references(self, task: str) -> list:
        refs = []
        
        # Local references
        lang_dir = self.refs_path / self.language
        if lang_dir.exists():
            for md_file in lang_dir.glob("*.md"):
                content = md_file.read_text(encoding='utf-8', errors='ignore')
                import re
                urls = re.findall(r'https?://[^\s<>"\')\]]+', content)
                for url in urls:
                    refs.append({'url': url, 'source': f'local/{self.language}', 'type': 'doc'})
            print(f"📁 Found {len(refs)} local refs for {self.language}", file=sys.stderr)
        
        # Chronicle references
        if self.chronicle:
            try:
                chronicle_refs = self.chronicle(f"{task} {self.language}", 3)
                for ref in chronicle_refs:
                    refs.append({'url': ref.url, 'source': getattr(ref, 'source', 'chronicle'), 'type': 'chronicle'})
                print(f"📚 Found {len(chronicle_refs)} chronicle refs for '{task}'", file=sys.stderr)
            except Exception as e:
                print(f"⚠️ Chronicle search error: {e}", file=sys.stderr)
        
        return refs
    
    def generate_code(self, task: str) -> dict:
        refs = self.get_references(task)
        
        ref_text = ""
        if refs:
            ref_text = "\n\n## References & Best Practices\n"
            for ref in refs:
                ref_text += f"- {ref['url']} ({ref['source']})\n"
            ref_text += "\nUse these references to inform your solution.\n"
            print(f"📖 Including {len(refs)} references in prompt", file=sys.stderr)
        
        prompt = f"""You are an expert {self.language} programmer. Generate code for: {task}

{ref_text}

Requirements:
- Follow best practices from the references above
- Include error handling
- Add comments explaining key decisions
- Make it production-ready

Output ONLY the {self.language} code:"""
        
        code = self.llm.chat(prompt)
        
        if code.startswith("```"):
            lines = code.split("\n")
            code = "\n".join(lines[1:-1])
            if code.startswith(self.language):
                code = code[len(self.language):].lstrip()
        
        return {
            'language': self.language,
            'task': task,
            'code': code.strip(),
            'references': refs,
            'model': 'Groq' if self.llm.groq_client else 'DeepSeek-Coder'
        }


