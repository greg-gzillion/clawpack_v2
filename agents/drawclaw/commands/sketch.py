"""Sketch command - Quick pencil-style sketches"""
from pathlib import Path
from datetime import datetime
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

def run(args):
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (800, 600), color='#f5f0e0')
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 800, 50], fill='#2d2d2d')
    draw.text((20, 12), 'DRAWCLAW SKETCH: ' + args[:60], fill='#ffffff')
    for x in range(0, 800, 30):
        draw.line([(x, 50), (x + 150, 600)], fill='#d0c8b8', width=1)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = Path('exports') / f'sketch_{ts}.png'
    img.save(str(path))
    return f'Saved: {path.name}'
