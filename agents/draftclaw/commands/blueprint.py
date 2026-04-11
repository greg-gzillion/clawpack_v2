"""Blueprint command - Create technical blueprints"""

import os
from pathlib import Path

name = "blueprint"
description = "Create technical blueprint"

def run(args):
    if not args:
        return "Usage: /blueprint <specs>\nExample: /blueprint 800x600 living room"
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Parse dimensions
        parts = args.split()
        if 'x' in parts[0]:
            width, height = map(int, parts[0].split('x'))
            label = ' '.join(parts[1:]) if len(parts) > 1 else "Blueprint"
        else:
            width, height = 800, 600
            label = args
        
        # Create blueprint-style image
        img = Image.new('RGB', (width, height), color='#0a1628')
        draw = ImageDraw.Draw(img)
        
        # Grid lines
        for x in range(0, width, 50):
            draw.line([(x, 0), (x, height)], fill='#1a3a5c', width=1)
        for y in range(0, height, 50):
            draw.line([(0, y), (width, y)], fill='#1a3a5c', width=1)
        
        # Border
        draw.rectangle([10, 10, width-10, height-10], outline='#4a9eff', width=3)
        
        # Title block
        draw.rectangle([width-200, height-60, width-20, height-20], outline='#4a9eff', width=2)
        draw.text((width-190, height-50), f"DRAFTCLAW", fill='#4a9eff')
        draw.text((width-190, height-35), label, fill='#7ab8ff')
        
        # Save
        agent_dir = Path(__file__).parent.parent
        exports_dir = agent_dir / "exports"
        exports_dir.mkdir(exist_ok=True)
        
        path = exports_dir / f"blueprint_{hash(args)%10000}.png"
        img.save(str(path))
        os.startfile(str(path))
        
        return f"📐 Blueprint created: {label}\n✅ Opening..."
        
    except ImportError:
        return "❌ PIL not installed. Run: pip install pillow"
    except Exception as e:
        return f"❌ Error: {e}"
