"""Paint command - Color block paintings"""
from pathlib import Path
from datetime import datetime
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

def run(args):
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (800, 600), color='#e8f4f8')
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 800, 50], fill='#2d2d2d')
    draw.text((20, 12), 'DRAWCLAW PAINT: ' + args[:60], fill='#ffffff')
    for i in range(5):
        y = 70 + i * 100
        color = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7'][i]
        draw.rectangle([30, y, 770, y+80], fill=color)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = Path('exports') / f'paint_{ts}.png'
    img.save(str(path))
    return f'Saved: {path.name}'
