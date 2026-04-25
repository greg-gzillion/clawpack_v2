"""Doodle command - Random playful doodles"""
from pathlib import Path
from datetime import datetime
import random
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

def run(args):
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (800, 600), color='#fff8e7')
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 800, 50], fill='#2d2d2d')
    draw.text((20, 12), 'DRAWCLAW DOODLE: ' + args[:60], fill='#ffffff')
    for _ in range(50):
        x, y = random.randint(0, 800), random.randint(50, 600)
        r = random.randint(5, 30)
        draw.ellipse([x-r, y-r, x+r, y+r], outline='#999999', width=2)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = Path('exports') / f'doodle_{ts}.png'
    img.save(str(path))
    return f'Saved: {path.name}'
