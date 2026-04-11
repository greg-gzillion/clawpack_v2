#!/usr/bin/env python3
"""FlowClaw Enhanced - Main Agent with LLM Integration"""

import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from engine.diagram_types import DiagramGenerator
from viewer.advanced_viewer import AdvancedViewer
from templates.library import TemplateLibrary

class LLMIntegrator:
    def __init__(self):
        self.llm = None
        try:
            from core.llm_manager import get_llm_manager
            self.llm = get_llm_manager()
        except:
            pass
    
    def smart_generate(self, diagram_type: str, description: str) -> str:
        if self.llm:
            prompt = f"Create a Mermaid {diagram_type} diagram for: {description}. Output ONLY the Mermaid code."
            try:
                code = self.llm.chat_sync(prompt, task_type="diagram")
                if code and len(code) > 10:
                    return code
            except:
                pass
        return DiagramGenerator.get_template(diagram_type, description)

class FlowClawEnhanced:
    def __init__(self):
        self.output_path = Path(__file__).parent / "output"
        self.output_path.mkdir(exist_ok=True)
        self.llm = LLMIntegrator()
    
    def generate(self, diagram_type: str, description: str) -> dict:
        code = self.llm.smart_generate(diagram_type, description)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_path / f"{diagram_type}_{ts}.mmd"
        output_file.write_text(code)
        return {'code': code, 'path': str(output_file)}
    
    def view(self, diagram_type: str, description: str):
        result = self.generate(diagram_type, description)
        AdvancedViewer.show(result['code'], f"{diagram_type}: {description[:40]}")
        return result
    
    def template(self, name: str = None):
        if not name:
            return f"Templates: {', '.join(TemplateLibrary.list_all())}"
        code = TemplateLibrary.get(name)
        out = self.output_path / f"template_{name}.mmd"
        out.write_text(code)
        return f"Saved: {out}"
    
    def process(self, cmd: str, *args):
        if cmd == "view" and len(args) >= 2:
            return self.view(args[0], ' '.join(args[1:]))
        elif cmd == "template":
            return self.template(args[0] if args else None)
        else:
            return self.help()
    
    def help(self):
        return """
FlowClaw Enhanced - Commands:
  view <type> <desc>  - Generate and show diagram
  template [name]     - Use or list templates
  
Types: flowchart, sequence, architecture, gantt, state, class, er, timeline, pie, mindmap, user_journey, gitgraph, c4
Examples:
  view flowchart "user login process"
  view timeline "project roadmap"
  template business_process
"""

def main():
    agent = FlowClawEnhanced()
    if len(sys.argv) < 2:
        print(agent.help())
        return
    result = agent.process(sys.argv[1], *sys.argv[2:])
    print(result)

if __name__ == "__main__":
    main()
