"""Bar command - Creates real bar charts"""

import os
from pathlib import Path

name = "bar"
description = "Create bar chart"

def run(args):
    if not args:
        return "Usage: /bar <values>\nExample: /bar 10,20,15,30,25"
    
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        values = [float(x.strip()) for x in args.split(',')]
        labels = [f"Item {i+1}" for i in range(len(values))]
        
        plt.figure(figsize=(10, 6))
        colors = plt.cm.viridis([i/len(values) for i in range(len(values))])
        plt.bar(labels, values, color=colors, edgecolor='black')
        plt.title(f"Bar Chart")
        plt.ylabel("Value")
        plt.grid(axis='y', alpha=0.3)
        
        for i, v in enumerate(values):
            plt.text(i, v + max(values)*0.01, str(v), ha='center')
        
        # FIXED: Use absolute path
        agent_dir = Path(__file__).parent.parent
        exports_dir = agent_dir / "exports"
        exports_dir.mkdir(exist_ok=True)
        
        path = exports_dir / f"bar_{hash(args)%10000}.png"
        plt.savefig(str(path), dpi=150, bbox_inches='tight')
        plt.close()
        
        # Open the file
        if os.path.exists(str(path)):
            os.startfile(str(path))
            return f"📊 Bar chart created! Opening..."
        else:
            return f"❌ Failed to save chart"
        
    except ImportError:
        return "❌ matplotlib not installed. Run: pip install matplotlib numpy"
    except Exception as e:
        return f"❌ Error: {e}"
