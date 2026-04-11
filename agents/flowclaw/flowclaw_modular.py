#!/usr/bin/env python3
"""FlowClaw - Modular Diagram Generator"""

import sys
from modules.generators import FlowchartGenerator, SequenceGenerator, ArchitectureGenerator
from modules.renderers.html_renderer import HTMLRenderer
from modules.exporters.file_exporter import FileExporter
from modules.templates.library import TemplateLibrary

class FlowClawModular:
    def __init__(self):
        self.generators = {
            'flowchart': FlowchartGenerator(),
            'sequence': SequenceGenerator(),
            'architecture': ArchitectureGenerator()
        }
        self.exporter = FileExporter('output')
        self.renderer = HTMLRenderer()
    
    def view(self, diagram_type, description):
        # Get generator
        generator = self.generators.get(diagram_type)
        if not generator:
            return f"Unknown type: {diagram_type}"
        
        # Generate code
        code = generator.generate(description)
        
        # Save to file
        filepath = self.exporter.save(code, diagram_type)
        
        # Render in browser
        self.renderer.render(code, f"{diagram_type}: {description}")
        
        return f"✅ Saved: {filepath}\n🌐 Browser opened"
    
    def template(self, name=None):
        if not name:
            return f"Templates: {', '.join(TemplateLibrary.list_all())}"
        code = TemplateLibrary.get(name)
        filepath = self.exporter.save(code, f"template_{name}")
        return f"✅ Template '{name}' saved to: {filepath}"
    
    def process(self, cmd, *args):
        if cmd == "view" and len(args) >= 2:
            return self.view(args[0], ' '.join(args[1:]))
        elif cmd == "template":
            return self.template(args[0] if args else None)
        else:
            return self.help()
    
    def help(self):
        return """
🎨 FlowClaw - MODULAR Diagram Generator

ARCHITECTURE:
  modules/generators/  - Diagram type generators
  modules/renderers/   - HTML/browser renderers
  modules/exporters/   - File save/export
  modules/templates/   - Template library

COMMANDS:
  view <type> <desc>   - Generate and view diagram
  template [name]      - Use or list templates

TYPES: flowchart, sequence, architecture
TEMPLATES: login, api, deploy

EXAMPLE:
  view flowchart "user login"
  template login
"""

def main():
    agent = FlowClawModular()
    if len(sys.argv) < 2:
        print(agent.help())
        return
    result = agent.process(sys.argv[1], *sys.argv[2:])
    print(result)

if __name__ == "__main__":
    main()
