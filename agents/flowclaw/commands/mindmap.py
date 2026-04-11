"""Mindmap command - Creates mind maps"""

import os
from pathlib import Path

name = "mindmap"
description = "Create mind map"

def run(args):
    if not args:
        return "Usage: /mindmap <topic>\nExample: /mindmap Clawpack"
    
    agent_dir = Path(__file__).parent.parent
    exports_dir = agent_dir / "exports"
    exports_dir.mkdir(exist_ok=True)
    
    # Create simple text mindmap
    mindmap = f"🧠 Mind Map: {args}\n\n"
    mindmap += f"    {args}\n"
    mindmap += "    ├── Feature 1\n"
    mindmap += "    ├── Feature 2\n"
    mindmap += "    └── Feature 3\n"
    
    path = exports_dir / f"mindmap_{hash(args)%10000}.txt"
    path.write_text(mindmap, encoding='utf-8')
    os.startfile(str(path))
    
    return f"🧠 Mind map created for: {args}\n✅ Opening..."
