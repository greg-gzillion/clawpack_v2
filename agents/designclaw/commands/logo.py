"""Logo command - Generate logos"""

import os
from pathlib import Path

name = "logo"
description = "Generate logo design"

def run(args):
    if not args:
        return "Usage: /logo <name> <style>\nExample: /logo Clawpack modern"
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        parts = args.split()
        name = parts[0]
        style = parts[1] if len(parts) > 1 else "modern"
        
        # Create logo canvas
        img = Image.new('RGB', (600, 400), color='#1a1a2e')
        draw = ImageDraw.Draw(img)
        
        # Style-based design
        if style == "modern":
            # Geometric shapes
            draw.ellipse([100, 100, 300, 300], outline='#e94560', width=5)
            draw.rectangle([250, 150, 450, 250], outline='#0f3460', width=3)
            draw.text((150, 320), name.upper(), fill='white')
        elif style == "minimal":
            draw.line([100, 200, 500, 200], fill='#533483', width=4)
            draw.text((200, 150), name, fill='white')
        else:
            draw.text((150, 180), name.upper(), fill='#e94560')
            draw.text((180, 220), style.title(), fill='#533483')
        
        # Save
        agent_dir = Path(__file__).parent.parent
        exports_dir = agent_dir / "exports"
        exports_dir.mkdir(exist_ok=True)
        
        path = exports_dir / f"logo_{name}_{hash(args)%1000}.png"
        img.save(str(path))
        os.startfile(str(path))
        
        return f"🎨 Logo created: {name} ({style})\n✅ Opening..."
        
    except ImportError:
        return "❌ PIL not installed. Run: pip install pillow"
    except Exception as e:
        return f"❌ Error: {e}"
