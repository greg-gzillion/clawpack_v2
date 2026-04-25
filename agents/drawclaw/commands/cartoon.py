"""Cartoon command - Simple cartoon faces"""
from pathlib import Path
from datetime import datetime
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

def run(args):
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (800, 600), color='#fff0f5')
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 800, 50], fill='#2d2d2d')
    draw.text((20, 12), 'DRAWCLAW CARTOON: ' + args[:60], fill='#ffffff')
    draw.ellipse([200, 100, 600, 500], outline='#333333', width=4)
    draw.ellipse([300, 230, 350, 280], fill='#333333')
    draw.ellipse([450, 230, 500, 280], fill='#333333')
    draw.arc([300, 320, 500, 420], start=0, end=180, fill='#333333', width=3)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = Path('exports') / f'cartoon_{ts}.png'
    img.save(str(path))
    return f'Saved: {path.name}'
