"""Dream command - Generate AI images with pop-up"""

import os
from pathlib import Path

name = "dream"
description = "Generate AI image from prompt"

def run(args):
    if not args:
        return "Usage: /dream <prompt>\nExample: /dream a lobster teaching Spanish"
    
    # For now, create a placeholder image with text
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create image
        img = Image.new('RGB', (800, 600), color='#1a1a2e')
        draw = ImageDraw.Draw(img)
        
        # Add text
        text = f"🎨 Dreamclaw\n\n{args}"
        draw.text((400, 300), text, fill='white', anchor='mm')
        
        # Save
        agent_dir = Path(__file__).parent.parent
        exports_dir = agent_dir / "exports"
        exports_dir.mkdir(exist_ok=True)
        
        path = exports_dir / f"dream_{hash(args)%10000}.png"
        img.save(str(path))
        
        # Open pop-up
        os.startfile(str(path))
        
        return f"🎨 AI Image generated!\nPrompt: {args}\n✅ Opening..."
        
    except ImportError:
        # Fallback: create text file
        agent_dir = Path(__file__).parent.parent
        exports_dir = agent_dir / "exports"
        exports_dir.mkdir(exist_ok=True)
        
        path = exports_dir / f"dream_{hash(args)%10000}.txt"
        path.write_text(f"🎨 Dreamclaw Prompt:\n\n{args}", encoding='utf-8')
        os.startfile(str(path))
        
        return f"🎨 Prompt saved!\n{args}\n(Install PIL for images: pip install pillow)"
