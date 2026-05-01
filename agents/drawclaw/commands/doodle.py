"""Doodle command - Algorithmic art with styles and patterns"""
from pathlib import Path
from datetime import datetime
import random, sys, os, math
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

def run(args):
    from PIL import Image, ImageDraw
    
    d = args.lower() if args else "random"
    
    # Detect style from keywords
    style = 'random'
    if any(w in d for w in ['geometric', 'geo', 'shapes']):
        style = 'geometric'
    elif any(w in d for w in ['spiral', 'swirl', 'vortex']):
        style = 'spiral'
    elif any(w in d for w in ['flower', 'floral', 'petal', 'bloom']):
        style = 'floral'
    elif any(w in d for w in ['wave', 'ocean', 'sine']):
        style = 'wave'
    elif any(w in d for w in ['grid', 'maze', 'labyrinth']):
        style = 'grid'
    elif any(w in d for w in ['star', 'cosmic', 'space', 'galaxy']):
        style = 'cosmic'
    elif any(w in d for w in ['circle', 'bubble', 'orb']):
        style = 'bubbles'
    elif any(w in d for w in ['line', 'stripes', 'parallel']):
        style = 'lines'
    elif any(w in d for w in ['dot', 'point', 'stipple']):
        style = 'stipple'
    elif any(w in d for w in ['chaos', 'messy', 'wild']):
        style = 'chaos'
    
    # Style-specific colors
    palettes = {
        'geometric': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'],
        'spiral': ['#FFD700', '#FF8C00', '#FF6347', '#FF1493', '#9400D3', '#4169E1'],
        'floral': ['#FF69B4', '#FFB6C1', '#FF1493', '#DA70D6', '#BA55D3', '#9370DB'],
        'wave': ['#006994', '#0088CC', '#00BFFF', '#87CEEB', '#4A90D9', '#1E90FF'],
        'grid': ['#2C3E50', '#34495E', '#7F8C8D', '#95A5A6', '#BDC3C7', '#ECF0F1'],
        'cosmic': ['#0a0a2e', '#1a1a4e', '#4a0a6e', '#8B008B', '#FFD700', '#FFFFFF'],
        'bubbles': ['#FF69B4', '#87CEEB', '#DDA0DD', '#98FB98', '#FFB6C1', '#ADD8E6'],
        'lines': ['#FF4500', '#32CD32', '#1E90FF', '#FFD700', '#FF1493', '#00CED1'],
        'stipple': ['#1a1a1a', '#333333', '#666666', '#999999', '#CCCCCC', '#4a4a4a'],
        'chaos': ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF'],
    }
    
    colors = palettes.get(style, palettes['random'] if style == 'random' else ['#FF6B6B', '#4ECDC4', '#45B7D1'])
    
    # Background
    bg_colors = {
        'cosmic': '#0a0a1e',
        'grid': '#1a1a1a',
        'stipple': '#FAFAFA',
        'lines': '#1a1a1a',
        'default': '#FAFAFA'
    }
    bg = bg_colors.get(style, bg_colors['default'])
    img = Image.new('RGB', (800, 600), color=bg)
    draw = ImageDraw.Draw(img)
    
    # Title bar
    bar_color = '#1a1a1a' if bg == '#FAFAFA' else '#333333'
    draw.rectangle([0, 0, 800, 45], fill=bar_color)
    draw.text((20, 12), f'DRAWCLAW DOODLE: {style.upper()} - {args[:40]}', fill='#ffffff')
    
    if style == 'geometric':
        for _ in range(random.randint(30, 60)):
            x, y = random.randint(0, 800), random.randint(50, 600)
            s = random.randint(20, 100)
            sides = random.randint(3, 8)
            c = random.choice(colors)
            angle = random.uniform(0, 2*math.pi)
            pts = []
            for i in range(sides):
                a = angle + (2*math.pi*i/sides)
                px = x + int(s * math.cos(a))
                py = y + int(s * math.sin(a))
                pts.append((px, py))
            draw.polygon(pts, fill=c, outline='#333333')
    
    elif style == 'spiral':
        cx, cy = 400, 320
        for i in range(200):
            angle = i * 0.2
            radius = 5 + i * 1.5
            x = cx + int(radius * math.cos(angle))
            y = cy + int(radius * math.sin(angle))
            c = colors[i % len(colors)]
            draw.ellipse([x-4, y-4, x+4, y+4], fill=c)
    
    elif style == 'floral':
        for _ in range(random.randint(8, 15)):
            cx, cy = random.randint(100, 700), random.randint(100, 500)
            petals = random.randint(5, 12)
            size = random.randint(20, 60)
            c = random.choice(colors)
            for i in range(petals):
                angle = (2*math.pi*i/petals) + random.uniform(-0.1, 0.1)
                px = cx + int(size * 0.6 * math.cos(angle))
                py = cy + int(size * 0.6 * math.sin(angle))
                ps = random.randint(size//2, size)
                draw.ellipse([px-ps//2, py-ps//2, px+ps//2, py+ps//2], fill=c)
            draw.ellipse([cx-size//4, cy-size//4, cx+size//4, cy+size//4], fill='#FFD700')
    
    elif style == 'wave':
        for wave_num in range(random.randint(5, 12)):
            points = []
            amplitude = random.randint(20, 80)
            frequency = random.uniform(0.01, 0.05)
            phase = random.uniform(0, 2*math.pi)
            y_offset = 80 + wave_num * 45
            c = colors[wave_num % len(colors)]
            for x in range(0, 801, 5):
                y = y_offset + int(amplitude * math.sin(frequency*x + phase))
                points.append((x, y))
            for i in range(len(points)-1):
                draw.line([points[i], points[i+1]], fill=c, width=random.randint(1, 3))
    
    elif style == 'grid':
        spacing = random.randint(30, 60)
        for x in range(0, 801, spacing):
            for y in range(50, 601, spacing):
                c = random.choice(colors)
                if random.random() > 0.5:
                    draw.rectangle([x+2, y+2, x+spacing-2, y+spacing-2], fill=c, outline='')
                else:
                    draw.ellipse([x+2, y+2, x+spacing-2, y+spacing-2], fill=c, outline='')
    
    elif style == 'cosmic':
        # Stars
        for _ in range(random.randint(80, 150)):
            x, y = random.randint(0, 800), random.randint(50, 600)
            r = random.randint(1, 3)
            c = random.choice(['#FFFFFF', '#FFD700', '#87CEEB', '#FF69B4'])
            draw.ellipse([x-r, y-r, x+r, y+r], fill=c)
        # Nebula-like circles
        for _ in range(random.randint(5, 10)):
            x, y = random.randint(100, 700), random.randint(100, 500)
            for r in range(40, 0, -10):
                alpha = r / 40
                c = random.choice(colors)
                draw.ellipse([x-r, y-r, x+r, y+r], fill=c, outline='')
    
    elif style == 'bubbles':
        for _ in range(random.randint(40, 80)):
            x, y = random.randint(0, 800), random.randint(50, 600)
            r = random.randint(10, 60)
            c = random.choice(colors)
            draw.ellipse([x-r, y-r, x+r, y+r], fill=c, outline='#FFFFFF')
            # Shine
            draw.ellipse([x-r//3, y-r//3, x+r//4, y+r//4], fill='#FFFFFF')
    
    elif style == 'lines':
        for _ in range(random.randint(20, 50)):
            x1, y1 = random.randint(0, 800), random.randint(50, 600)
            x2, y2 = random.randint(0, 800), random.randint(50, 600)
            c = random.choice(colors)
            w = random.randint(1, 4)
            draw.line([(x1, y1), (x2, y2)], fill=c, width=w)
    
    elif style == 'stipple':
        for _ in range(random.randint(500, 2000)):
            x, y = random.randint(0, 800), random.randint(50, 600)
            c = random.choice(colors)
            draw.point((x, y), fill=c)
    
    elif style == 'chaos':
        for _ in range(random.randint(100, 200)):
            x, y = random.randint(0, 800), random.randint(50, 600)
            c = random.choice(colors)
            t = random.choice(['rect', 'ellipse', 'line', 'point'])
            w, h = random.randint(5, 80), random.randint(5, 80)
            if t == 'rect':
                draw.rectangle([x, y, x+w, y+h], fill=c, outline=random.choice(colors))
            elif t == 'ellipse':
                draw.ellipse([x, y, x+w, y+h], fill=c, outline=random.choice(colors))
            elif t == 'line':
                draw.line([(x, y), (x+w, y+h)], fill=c, width=random.randint(1, 5))
            else:
                draw.point((x, y), fill=c)
    
    else:  # random - mix everything
        for _ in range(random.randint(40, 70)):
            x, y = random.randint(0, 800), random.randint(50, 600)
            s = random.randint(10, 80)
            c = random.choice(colors)
            shape = random.choice(['circle', 'rect', 'line', 'polygon'])
            if shape == 'circle':
                draw.ellipse([x, y, x+s, y+s], fill=c, outline='#333333')
            elif shape == 'rect':
                draw.rectangle([x, y, x+s, y+s], fill=c, outline='#333333')
            elif shape == 'line':
                draw.line([(x, y), (x+s, y+s)], fill=c, width=random.randint(1, 4))
            else:
                pts = [(x, y), (x+s, y), (x+s//2, y-s)]
                draw.polygon(pts, fill=c, outline='#333333')
    
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = Path('exports') / f'doodle_{ts}.png'
    img.save(str(path))
    os.startfile(str(path))
    return f'Saved: {path.name} | Style: {style}'