"""Flowchart command - Creates diagrams with pop-up"""

import os
from pathlib import Path

name = "flowchart"
description = "Create flowchart from steps"

def run(args):
    if not args:
        return "Usage: /flowchart <steps>\nExample: /flowchart Start->Process->End"
    
    try:
        # Try to use graphviz if available
        import graphviz
        
        steps = args.split('->')
        steps = [s.strip() for s in steps]
        
        dot = graphviz.Digraph(comment='Flowchart')
        dot.attr(rankdir='TB')
        
        for i, step in enumerate(steps):
            dot.node(str(i), step, shape='box', style='filled', fillcolor='lightblue')
            if i < len(steps) - 1:
                dot.edge(str(i), str(i+1))
        
        agent_dir = Path(__file__).parent.parent
        exports_dir = agent_dir / "exports"
        exports_dir.mkdir(exist_ok=True)
        
        path = exports_dir / f"flowchart_{hash(args)%10000}"
        dot.render(str(path), format='png', cleanup=True)
        
        png_path = str(path) + '.png'
        os.startfile(png_path)
        
        return f"🔷 Flowchart created!\nSteps: {len(steps)}\n✅ Opening..."
        
    except ImportError:
        # Fallback: Create simple text diagram
        agent_dir = Path(__file__).parent.parent
        exports_dir = agent_dir / "exports"
        exports_dir.mkdir(exist_ok=True)
        
        steps = args.split('->')
        diagram = "Flowchart:\n\n"
        for i, step in enumerate(steps):
            diagram += f"[{step.strip()}]\n"
            if i < len(steps) - 1:
                diagram += "   ↓\n"
        
        path = exports_dir / f"flowchart_{hash(args)%10000}.txt"
        path.write_text(diagram, encoding='utf-8')
        os.startfile(str(path))
        
        return f"🔷 Flowchart created!\n(Install graphviz for images: pip install graphviz)"
