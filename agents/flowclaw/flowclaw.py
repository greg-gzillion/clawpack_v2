#!/usr/bin/env python3
"""FlowClaw - Reliable Diagram Generator"""

import sys
import webbrowser
import tempfile
import re
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# 100% VALID MERMAID TEMPLATES (All from official docs)
# ============================================================================

TEMPLATES = {
    'login': """flowchart TD
    A[Start] --> B[Enter Email]
    B --> C[Enter Password]
    C --> D{Valid?}
    D -->|Yes| E[Dashboard]
    D -->|No| F[Error]
    F --> B""",

    'decision': """flowchart TD
    A[Start] --> B{Choose Option}
    B -->|Option 1| C[Path A]
    B -->|Option 2| D[Path B]
    C --> E[End]
    D --> E""",

    'gantt': """gantt
    title A Gantt Diagram
    dateFormat YYYY-MM-DD
    section Section
    A task :a1, 2014-01-01, 30d
    Another task :after a1, 20d
    section Another
    Task in sec :2014-01-12, 12d
    another task :24d""",

    'sequence': """sequenceDiagram
    participant Alice
    participant Bob
    Alice->>John: Hello John, how are you?
    loop Healthcheck
        John->>John: Fight against hypochondria
    end
    Note right of John: Rational thoughts!
    John-->>Alice: Great!
    John->>Bob: How about you?
    Bob-->>John: Jolly good!""",

    'simple': """flowchart LR
    A[Start] --> B[Process]
    B --> C[End]""",
    
    'process': """flowchart TD
    A[Start] --> B[Step 1]
    B --> C[Step 2]
    C --> D[End]""",
    
    'workflow': """flowchart LR
    A[Input] --> B[Process]
    B --> C{Decision}
    C -->|Yes| D[Output]
    C -->|No| B""",
}

# ============================================================================
# LLM INTERFACE
# ============================================================================

class LLMInterface:
    def __init__(self):
        self.llm = None
        self.chronicle = None
        self._init_llm()
        self._init_chronicle()
    
    def _init_llm(self):
        try:
            from shared.llm import get_llm_client
            self.llm = get_llm_manager()
            print("✅ LLM Connected", file=sys.stderr)
        except:
            pass
    
    def _init_chronicle(self):
        try:
            from shared.chronicle_helper import search_chronicle
            self.chronicle = search_chronicle
            print("✅ Chronicle Connected", file=sys.stderr)
        except:
            pass
    
    def search_references(self, topic: str, max_results: int = 3) -> list:
        if not self.chronicle:
            return []
        try:
            results = self.chronicle(topic, max_results)
            return [getattr(r, 'url', str(r)) for r in results]
        except:
            return []
    
    def generate_diagram(self, description: str) -> str:
        if self.llm:
            prompt = f"Create a valid Mermaid flowchart for: {description}. Use flowchart TD format. Output ONLY the code."
            try:
                code = self.llm.chat_sync(prompt, task_type="diagram")
                code = code.replace('```mermaid', '').replace('```', '').strip()
                if code.startswith('flowchart') or code.startswith('graph'):
                    return code
            except:
                pass
        return TEMPLATES['process']

# ============================================================================
# RENDERER
# ============================================================================

class Renderer:
    @staticmethod
    def show(code: str, title: str, silent: bool = False) -> str:
        if silent:
            return ""
        
        safe_code = code.replace('</', '<\\/')
        
        html = f'''<!DOCTYPE html>
<html>
<head><title>{title}</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
body{{font-family:Arial;margin:20px;background:#f0f2f5}}
.container{{max-width:1000px;margin:0 auto;background:white;border-radius:12px;padding:20px}}
h1{{color:#667eea}}
.mermaid{{text-align:center;background:white;padding:20px}}
</style>
</head>
<body>
<div class="container">
<h1>🎨 {title}</h1>
<div class="mermaid">
{safe_code}
</div>
</div>
<script>mermaid.initialize({{startOnLoad:true,securityLevel:'loose'}});</script>
</body>
</html>'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html)
            temp_path = f.name
        webbrowser.open(f'file://{temp_path}')
        return temp_path

# ============================================================================
# MAIN AGENT
# ============================================================================

class FlowClaw:
    def __init__(self):
        self.llm = LLMInterface()
        self.renderer = Renderer()
    
    def view(self, template: str, description: str = "") -> str:
        if template in TEMPLATES:
            code = TEMPLATES[template]
        elif description:
            code = self.llm.generate_diagram(description)
        else:
            code = TEMPLATES['simple']
        
        self.renderer.show(code, f"FlowClaw: {template}")
        filename = OUTPUT_DIR / f"{template}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mmd"
        filename.write_text(code)
        return f"✅ Diagram opened\n📁 Saved: {filename}"
    
    def ai(self, description: str) -> str:
        code = self.llm.generate_diagram(description)
        self.renderer.show(code, f"AI: {description}")
        filename = OUTPUT_DIR / f"ai_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mmd"
        filename.write_text(code)
        return f"✅ AI diagram generated\n📁 Saved: {filename}"
    
    def search(self, topic: str) -> str:
        refs = self.llm.search_references(topic, 5)
        if not refs:
            return f"No references found for '{topic}'"
        result = f"📚 Found {len(refs)} references:\n"
        for i, ref in enumerate(refs, 1):
            result += f"{i}. {ref}\n"
        return result
    
    def status(self) -> str:
        llm_status = "✅" if self.llm.llm else "❌"
        chronicle_status = "✅" if self.llm.chronicle else "❌"
        return f"""
┌────────────────────────────────┐
│       FLOWCLAW STATUS          │
├────────────────────────────────┤
│ 🤖 LLM: {llm_status} Connected                 │
│ 📚 Chronicle: {chronicle_status} Connected             │
│ 📁 Output: {OUTPUT_DIR.name}/                    │
│ 📊 Templates: {len(TEMPLATES)}                    │
└────────────────────────────────┘"""
    
    def templates(self) -> str:
        return "Available templates:\n" + "\n".join(f"  • {t}" for t in TEMPLATES.keys())
    
    def test_all(self) -> str:
        """Test all templates WITHOUT opening browser windows"""
        results = []
        valid_count = 0
        
        for name, code in TEMPLATES.items():
            # Basic syntax validation
            has_content = len(code.strip()) > 20
            valid_starts = ['flowchart', 'graph', 'sequenceDiagram', 'gantt']
            has_valid_start = any(code.strip().startswith(v) for v in valid_starts)
            
            # Special check for gantt (different syntax)
            if name == 'gantt':
                has_title = 'title' in code
                has_dateFormat = 'dateFormat' in code
                has_section = 'section' in code
                is_valid = has_title and has_dateFormat and has_section
            else:
                is_valid = has_content and has_valid_start and '-->' in code
            
            if is_valid:
                valid_count += 1
                results.append(f"  ✅ {name}")
            else:
                results.append(f"  ❌ {name}")
        
        summary = f"""
{'='*40}
TEMPLATE VALIDATION: {valid_count}/{len(TEMPLATES)} valid
{'='*40}"""
        
        return summary + "\n" + "\n".join(results)
    
    def process(self, cmd: str, *args):
        if cmd == "status":
            return self.status()
        elif cmd == "search" and args:
            return self.search(' '.join(args))
        elif cmd == "ai" and args:
            return self.ai(' '.join(args))
        elif cmd == "view" and args:
            return self.view(args[0], ' '.join(args[1:]) if len(args) > 1 else "")
        elif cmd == "templates":
            return self.templates()
        elif cmd == "test":
            return self.test_all()
        else:
            return self.help()
    
    def help(self):
        return """
╔══════════════════════════════════════════════════════════════╗
║                    FLOWCLAW - Diagram Generator              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  COMMANDS:                                                   ║
║    test                      - Validate all templates       ║
║    status                    - Show connections              ║
║    templates                 - List all templates            ║
║    view <template>           - View a template               ║
║    ai <description>          - Generate with AI              ║
║    search <topic>            - Search chronicle              ║
║                                                              ║
║  TEMPLATES: login, decision, gantt, sequence, simple, process, workflow ║
║                                                              ║
║  EXAMPLES:                                                   ║
║    python flowclaw.py test                                   ║
║    python flowclaw.py view login                             ║
║    python flowclaw.py view gantt                             ║
║    python flowclaw.py ai "user registration"                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝"""

def main():
    agent = FlowClaw()
    if len(sys.argv) < 2:
        print(agent.help())
        return
    result = agent.process(sys.argv[1], *sys.argv[2:])
    print(result)

if __name__ == "__main__":
    main()

    def smart_view(self, description):
        """Use smart routing for diagram generation"""
        from shared.smart_router import smart_router
        result = smart_router.route(description)
        if result.tier.value < 3:
            print(f"🎯 Fast path: {result.handler}")
        return self.view("flowchart", description)
