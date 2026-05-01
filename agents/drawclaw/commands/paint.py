"""Paint command - Artistic painting styles with brush effects"""
from pathlib import Path
from datetime import datetime
import sys, os, random, math
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

def run(args):
    from PIL import Image, ImageDraw, ImageFilter
    
    d = args.lower() if args else "abstract"
    
    # Detect painting style
    style = 'abstract'
    if any(w in d for w in ['watercolor', 'water', 'wash']):
        style = 'watercolor'
    elif any(w in d for w in ['oil', 'impasto', 'thick']):
        style = 'oil'
    elif any(w in d for w in ['pixel', '8bit', 'retro']):
        style = 'pixel'
    elif any(w in d for w in ['stripe', 'stripes', 'bands']):
        style = 'stripes'
    elif any(w in d for w in ['drip', 'splatter', 'pollock']):
        style = 'drip'
    elif any(w in d for w in ['gradient', 'blend', 'fade']):
        style = 'gradient'
    elif any(w in d for w in ['pointillism', 'dots', 'point']):
        style = 'pointillism'
    elif any(w in d for w in ['stained', 'glass', 'mosaic']):
        style = 'stained_glass'
    elif any(w in d for w in ['sunset', 'sky', 'horizon']):
        style = 'sunset'
    elif any(w in d for w in ['ocean', 'sea', 'marine']):
        style = 'ocean'
    elif any(w in d for w in ['forest', 'woods', 'trees']):
        style = 'forest'
    elif any(w in d for w in ['city', 'urban', 'skyline']):
        style = 'city'
    
    img = Image.new('RGB', (800, 600), color='#FAFAFA')
    draw = ImageDraw.Draw(img)
    
    if style == 'watercolor':
        # Soft, blended color washes
        colors = ['#FFB6C1', '#87CEEB', '#DDA0DD', '#98FB98', '#FFD700', '#FFA07A']
        for _ in range(random.randint(20, 40)):
            x, y = random.randint(0, 800), random.randint(0, 600)
            rx, ry = random.randint(60, 200), random.randint(40, 120)
            c = random.choice(colors)
            for offset in range(5):
                ox = random.randint(-10, 10)
                oy = random.randint(-10, 10)
                draw.ellipse([x+ox, y+oy, x+rx+ox, y+ry+oy], fill=c, outline='')
    
    elif style == 'oil':
        # Thick, textured strokes
        base_colors = ['#8B0000', '#006400', '#00008B', '#8B8B00', '#8B008B', '#008B8B']
        for _ in range(random.randint(30, 60)):
            x1, y1 = random.randint(0, 800), random.randint(0, 600)
            angle = random.uniform(0, 2*math.pi)
            length = random.randint(30, 120)
            x2 = x1 + int(length * math.cos(angle))
            y2 = y1 + int(length * math.sin(angle))
            c = random.choice(base_colors)
            width = random.randint(3, 12)
            draw.line([(x1, y1), (x2, y2)], fill=c, width=width)
            # Texture dots along stroke
            for _ in range(3):
                tx = random.randint(min(x1,x2), max(x1,x2))
                ty = random.randint(min(y1,y2), max(y1,y2))
                draw.ellipse([tx-2, ty-2, tx+2, ty+2], fill=c)
    
    elif style == 'pixel':
        # Retro pixel art blocks
        pixel_size = random.randint(8, 20)
        colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF',
                  '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
        for y in range(0, 600, pixel_size):
            for x in range(0, 800, pixel_size):
                if random.random() > 0.3:
                    c = random.choice(colors)
                    draw.rectangle([x, y, x+pixel_size, y+pixel_size], fill=c)
    
    elif style == 'stripes':
        # Vertical or horizontal bands
        colors = _generate_palette(args)
        direction = 'vertical' if random.random() > 0.5 else 'horizontal'
        if direction == 'vertical':
            stripe_w = random.randint(15, 60)
            for x in range(0, 800, stripe_w):
                c = random.choice(colors)
                draw.rectangle([x, 0, x+stripe_w, 600], fill=c)
        else:
            stripe_h = random.randint(15, 40)
            for y in range(0, 600, stripe_h):
                c = random.choice(colors)
                draw.rectangle([0, y, 800, y+stripe_h], fill=c)
    
    elif style == 'drip':
        # Paint drips and splatters
        bg_color = random.choice(['#1a1a1a', '#2C2C2C', '#F5F0E8', '#FFFFFF'])
        img = Image.new('RGB', (800, 600), color=bg_color)
        draw = ImageDraw.Draw(img)
        paint_colors = ['#FF0000', '#FFD700', '#FF1493', '#00FF00', '#4169E1', '#FF8C00', '#FFFFFF']
        # Splatters
        for _ in range(random.randint(20, 50)):
            x, y = random.randint(0, 800), random.randint(0, 600)
            c = random.choice(paint_colors)
            for _ in range(random.randint(5, 20)):
                sx = x + random.randint(-30, 30)
                sy = y + random.randint(-30, 30)
                sr = random.randint(1, 8)
                draw.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=c)
        # Drips from top
        for _ in range(random.randint(10, 25)):
            x = random.randint(0, 800)
            length = random.randint(50, 400)
            c = random.choice(paint_colors)
            draw.line([(x, 0), (x, length)], fill=c, width=random.randint(2, 6))
            draw.ellipse([x-4, length-4, x+4, length+4], fill=c)
    
    elif style == 'gradient':
        # Smooth color gradient
        colors = _generate_palette(args)
        for i in range(800):
            t = i / 800
            idx = int(t * (len(colors)-1))
            next_idx = min(idx+1, len(colors)-1)
            frac = (t * (len(colors)-1)) - idx
            c = _blend_colors(colors[idx], colors[next_idx], frac) if idx < len(colors)-1 else colors[-1]
            draw.line([(i, 0), (i, 600)], fill=c)
    
    elif style == 'pointillism':
        # Dot-based painting
        colors = _generate_palette(args)
        for _ in range(random.randint(2000, 5000)):
            x, y = random.randint(0, 800), random.randint(0, 600)
            r = random.randint(2, 6)
            c = random.choice(colors)
            draw.ellipse([x-r, y-r, x+r, y+r], fill=c)
    
    elif style == 'stained_glass':
        # Geometric mosaic
        colors = ['#FF0000', '#0000FF', '#FFD700', '#00FF00', '#FF1493', '#00CED1',
                  '#FF8C00', '#9370DB', '#228B22', '#FF69B4']
        cells = random.randint(30, 80)
        points = [(random.randint(0, 800), random.randint(0, 600)) for _ in range(cells)]
        for i, (px, py) in enumerate(points):
            for j in range(i+1, len(points)):
                if random.random() < 0.15:
                    draw.line([(px, py), points[j]], fill='#1a1a1a', width=2)
            c = random.choice(colors)
            size = random.randint(20, 80)
            draw.rectangle([px, py, px+size, py+size], fill=c, outline='#1a1a1a')
    
    elif style == 'sunset':
        # Sunset gradient with sun
        sunset_colors = ['#FF7B42', '#FF6347', '#FF4500', '#FFD700', '#FF1493', '#9400D3']
        for i in range(600):
            t = i / 600
            idx = int(t * (len(sunset_colors)-1))
            next_idx = min(idx+1, len(sunset_colors)-1)
            frac = (t * (len(sunset_colors)-1)) - idx
            c = _blend_colors(sunset_colors[idx], sunset_colors[next_idx], frac) if idx < len(sunset_colors)-1 else sunset_colors[-1]
            draw.rectangle([0, i, 800, i+1], fill=c)
        # Sun
        draw.ellipse([500, 250, 700, 450], fill='#FFD700', outline='#FFA500')
        # Reflection on water
        for i in range(450, 600, 15):
            alpha = (i-450)/150
            draw.rectangle([300+i%50, i, 500-i%50, i+3], fill='#FFD700')
        # Ground
        draw.rectangle([0, 450, 800, 600], fill='#2C1810')
    
    elif style == 'ocean':
        # Ocean scene
        ocean_colors = ['#006994', '#0088CC', '#00A8E8', '#4A90D9', '#1E90FF', '#87CEEB']
        for i in range(600):
            t = i / 600
            idx = int(t * (len(ocean_colors)-1))
            next_idx = min(idx+1, len(ocean_colors)-1)
            frac = (t * (len(ocean_colors)-1)) - idx
            c = _blend_colors(ocean_colors[idx], ocean_colors[next_idx], frac) if idx < len(ocean_colors)-1 else ocean_colors[-1]
            draw.rectangle([0, i, 800, i+1], fill=c)
        # Waves
        for _ in range(8):
            y = random.randint(100, 500)
            for x in range(0, 800, 3):
                wy = y + int(15 * math.sin(x*0.05 + random.random()))
                draw.point((x, wy), fill='#FFFFFF')
        # Horizon line
        draw.line([(0, 350), (800, 350)], fill='#87CEEB', width=2)
    
    elif style == 'forest':
        # Forest scene
        sky_colors = ['#87CEEB', '#4A90D9']
        for i in range(500):
            t = i / 500
            c = _blend_colors(sky_colors[0], sky_colors[1], t)
            draw.rectangle([0, i, 800, i+1], fill=c)
        # Ground
        draw.rectangle([0, 400, 800, 600], fill='#2D5A27')
        # Trees
        for _ in range(random.randint(15, 30)):
            tx = random.randint(0, 800)
            th = random.randint(80, 250)
            draw.rectangle([tx+3, 400-th, tx+9, 400], fill='#5C3A1E')
            for level in range(3):
                ty = 400 - th + level*60
                tw = random.randint(40, 80)
                draw.polygon([(tx-tw//2+6, ty), (tx+6, ty-50), (tx+tw//2+6, ty)], fill='#228B22')
        # Fog/mist
        for _ in range(10):
            fx = random.randint(0, 700)
            fy = random.randint(250, 450)
            draw.ellipse([fx, fy, fx+100, fy+20], fill='#FFFFFF')
    
    elif style == 'city':
        # City skyline
        sky = ['#0a0a2e', '#1a1a4e', '#2a2a6e']
        for i in range(450):
            t = i / 450
            idx = min(int(t * 2), 1)
            c = _blend_colors(sky[idx], sky[idx+1], t*2-idx) if idx < 2 else sky[-1]
            draw.rectangle([0, i, 800, i+1], fill=c)
        # Buildings
        building_colors = ['#1a1a1a', '#2C2C2C', '#333333', '#1a1a2e', '#0a0a0a']
        for _ in range(random.randint(15, 25)):
            bx = random.randint(-20, 780)
            bw = random.randint(30, 90)
            bh = random.randint(100, 350)
            c = random.choice(building_colors)
            draw.rectangle([bx, 450-bh, bx+bw, 450], fill=c)
            # Windows
            for wy in range(450-bh+20, 440, 25):
                for wx in range(bx+8, bx+bw-8, 15):
                    if random.random() > 0.3:
                        win_color = '#FFD700' if random.random() > 0.5 else '#87CEEB'
                        draw.rectangle([wx, wy, wx+8, wy+10], fill=win_color)
        # Stars
        for _ in range(random.randint(30, 80)):
            sx, sy = random.randint(0, 800), random.randint(0, 300)
            draw.point((sx, sy), fill='#FFFFFF')
    
    else:  # abstract - original style enhanced
        colors = _generate_palette(args)
        for _ in range(random.randint(8, 15)):
            y = random.randint(0, 500)
            h = random.randint(40, 120)
            c = random.choice(colors)
            draw.rectangle([0, y, 800, y+h], fill=c)
            for _ in range(3):
                cx = random.randint(0, 700)
                cy = y + random.randint(0, h)
                r = random.randint(20, 60)
                draw.ellipse([cx, cy, cx+r, cy+r], fill=random.choice(colors))
    
    # Title bar
    draw.rectangle([0, 0, 800, 40], fill='#1a1a1a')
    draw.text((15, 10), f'DRAWCLAW PAINT: {style.upper()} - {args[:50]}', fill='#FFFFFF')
    
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = Path('exports') / f'paint_{ts}.png'
    img.save(str(path))
    os.startfile(str(path))
    return f'Saved: {path.name} | Style: {style}'


def _generate_palette(desc):
    """Generate a color palette from description keywords."""
    palettes = {
        'warm': ['#FF6B6B', '#FF8E53', '#FFA07A', '#FFD700', '#FF6347', '#FF7F50'],
        'cool': ['#4A90D9', '#87CEEB', '#00CED1', '#4169E1', '#1E90FF', '#00BFFF'],
        'nature': ['#228B22', '#2D5A27', '#4A7C3F', '#8FBC8F', '#D2691E', '#87CEEB'],
        'pastel': ['#FFB6C1', '#DDA0DD', '#B0E0E6', '#98FB98', '#FFFACD', '#E6E6FA'],
        'bold': ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF'],
        'dark': ['#1a1a1a', '#2C2C2C', '#4a4a4a', '#8B0000', '#00008B', '#006400'],
        'vintage': ['#C0A080', '#8B7355', '#B8860B', '#800020', '#2F4F4F', '#D2B48C'],
    }
    
    for key, palette in palettes.items():
        if key in desc.lower():
            return palette
    
    return ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']


def _blend_colors(c1, c2, t):
    """Blend two hex colors."""
    r1, g1, b1 = int(c1[1:3],16), int(c1[3:5],16), int(c1[5:7],16)
    r2, g2, b2 = int(c2[1:3],16), int(c2[3:5],16), int(c2[5:7],16)
    r = int(r1 + (r2-r1)*t)
    g = int(g1 + (g2-g1)*t)
    b = int(b1 + (b2-b1)*t)
    return f'#{r:02x}{g:02x}{b:02x}'