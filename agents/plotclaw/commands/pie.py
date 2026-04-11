"""Pie command - Creates pie charts"""

import os
from pathlib import Path

name = "pie"
description = "Create pie chart"

def run(args):
    if not args:
        return "Usage: /pie <values>\nExample: /pie 30,20,50"
    
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        values = [float(x.strip()) for x in args.split(',')]
        labels = [f"Item {i+1}" for i in range(len(values))]
        
        plt.figure(figsize=(8, 8))
        colors = plt.cm.Set3(range(len(values)))
        plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.title("Pie Chart")
        
        # FIXED: Use absolute path
        agent_dir = Path(__file__).parent.parent
        exports_dir = agent_dir / "exports"
        exports_dir.mkdir(exist_ok=True)
        
        path = exports_dir / f"pie_{hash(args)%10000}.png"
        plt.savefig(str(path), dpi=150, bbox_inches='tight')
        plt.close()
        
        if os.path.exists(str(path)):
            os.startfile(str(path))
            return f"🥧 Pie chart created! Opening..."
        else:
            return f"❌ Failed to save chart"
        
    except ImportError:
        return "❌ matplotlib not installed. Run: pip install matplotlib numpy"
    except Exception as e:
        return f"❌ Error: {e}"
