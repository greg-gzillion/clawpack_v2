"""Sketch command - Pencil, charcoal, and ink sketching styles"""
from pathlib import Path
from datetime import datetime
import sys, os, random, math
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

def run(args):
    from PIL import Image, ImageDraw, ImageFilter

    d = args.lower() if args else "pencil"

    # Detect sketch style
    style = 'pencil'
    if any(w in d for w in ['charcoal', 'dark', 'bold']):
        style = 'charcoal'
    elif any(w in d for w in ['ink', 'pen', 'line art', 'lineart']):
        style = 'ink'
    elif any(w in d for w in ['blueprint', 'technical', 'drafting']):
        style = 'blueprint'
    elif any(w in d for w in ['crosshatch', 'hatching', 'shade']):
        style = 'crosshatch'
    elif any(w in d for w in ['contour', 'outline', 'silhouette']):
        style = 'contour'
    elif any(w in d for w in ['scribble', 'loose', 'rough']):
        style = 'scribble'

    # Style-specific settings
    styles = {
        'pencil': {'bg': '#F5F0E0', 'stroke': '#4A4A4A', 'light': '#C8C0B0', 'medium': '#8A8078', 'dark': '#3A3A3A'},
        'charcoal': {'bg': '#E8E0D0', 'stroke': '#1a1a1a', 'light': '#999999', 'medium': '#555555', 'dark': '#1a1a1a'},
        'ink': {'bg': '#FFFFFF', 'stroke': '#000000', 'light': '#E0E0E0', 'medium': '#666666', 'dark': '#000000'},
        'blueprint': {'bg': '#1a3a5c', 'stroke': '#FFFFFF', 'light': '#4A7AB5', 'medium': '#7AAAE0', 'dark': '#FFFFFF'},
        'crosshatch': {'bg': '#F0EDE4', 'stroke': '#2C2C2C', 'light': '#C8C0B8', 'medium': '#6A6258', 'dark': '#2C2C2C'},
        'contour': {'bg': '#FAF8F5', 'stroke': '#333333', 'light': '#DDDDDD', 'medium': '#888888', 'dark': '#333333'},
        'scribble': {'bg': '#F5F0E5', 'stroke': '#3A3A3A', 'light': '#C0B8B0', 'medium': '#706860', 'dark': '#3A3A3A'},
    }
    s = styles.get(style, styles['pencil'])

    img = Image.new('RGB', (800, 600), color=s['bg'])
    draw = ImageDraw.Draw(img)

    # Detect subject
    detect_subject(draw, d, s, style)

    # Style-specific overlay effects
    if style == 'pencil':
        # Pencil grain texture
        for _ in range(random.randint(500, 1500)):
            x, y = random.randint(0, 800), random.randint(0, 600)
            if random.random() > 0.7:
                draw.point((x, y), fill=s['light'])

    elif style == 'charcoal':
        # Smudge effects
        for _ in range(random.randint(5, 15)):
            x, y = random.randint(100, 700), random.randint(80, 500)
            for _ in range(random.randint(20, 50)):
                sx = x + random.randint(-40, 40)
                sy = y + random.randint(-40, 40)
                shade = random.choice([s['light'], s['medium']])
                draw.point((sx, sy), fill=shade)
        # Charcoal dust
        for _ in range(300):
            draw.point((random.randint(0, 800), random.randint(0, 600)), fill=s['light'])

    elif style == 'ink':
        # Ink splatter
        for _ in range(random.randint(3, 8)):
            x, y = random.randint(100, 700), random.randint(80, 400)
            for _ in range(random.randint(8, 20)):
                sx = x + random.randint(-25, 25)
                sy = y + random.randint(-25, 25)
                sr = random.randint(1, 4)
                draw.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=s['dark'])

    elif style == 'blueprint':
        # Grid lines
        for x in range(0, 800, 40):
            draw.line([(x, 0), (x, 600)], fill=s['light'], width=1)
        for y in range(0, 600, 40):
            draw.line([(0, y), (800, y)], fill=s['light'], width=1)
        # Border
        draw.rectangle([15, 55, 785, 585], outline=s['stroke'], width=2)
        draw.rectangle([20, 60, 780, 580], outline=s['medium'], width=1)

    elif style == 'crosshatch':
        # Hatching overlay
        for angle in [30, 150]:
            rad = math.radians(angle)
            for offset in range(-400, 1200, 8):
                x1 = offset
                y1 = int(offset * math.tan(rad))
                x2 = offset + 800
                y2 = int(y1 + 800 * math.tan(rad))
                draw.line([(x1, y1), (x2, y2)], fill=s['light'], width=1)

    # Title bar
    draw.rectangle([0, 0, 800, 45], fill=s['dark'])
    draw.text((15, 12), f'DRAWCLAW SKETCH: {style.upper()} - {args[:50]}', fill=s['bg'])
    draw.rectangle([0, 45, 800, 48], fill=s['medium'])

    # Signature area
    sig_y = 565
    draw.line([(600, sig_y), (750, sig_y)], fill=s['medium'], width=1)
    draw.text((620, sig_y-15), 'DrawClaw Studio', fill=s['medium'])

    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = Path('exports') / f'sketch_{ts}.png'
    img.save(str(path))
    os.startfile(str(path))
    return f'Saved: {path.name} | Style: {style}'


def detect_subject(draw, desc, s, style):
    """Detect subject from description and sketch it."""
    d = desc
    cx, cy = 400, 320

    # Portrait / face
    if any(w in d for w in ['portrait', 'face', 'person', 'head', 'man', 'woman', 'boy', 'girl']):
        _sketch_face(draw, 400, 280, 120, s, style)

    # Animal
    elif any(w in d for w in ['cat', 'kitten', 'feline']):
        _sketch_cat(draw, 400, 300, s, style)
    elif any(w in d for w in ['dog', 'puppy', 'canine']):
        _sketch_dog(draw, 400, 300, s, style)
    elif any(w in d for w in ['bird', 'eagle', 'hawk', 'sparrow']):
        _sketch_bird(draw, 400, 280, s, style)
    elif any(w in d for w in ['fish', 'shark', 'whale']):
        _sketch_fish(draw, 400, 320, s, style)

    # Landscape / nature
    elif any(w in d for w in ['mountain', 'peak', 'alpine', 'hill']):
        _sketch_mountains(draw, s, style)
    elif any(w in d for w in ['tree', 'forest', 'woods', 'pine']):
        _sketch_trees(draw, s, style)
    elif any(w in d for w in ['flower', 'rose', 'daisy', 'tulip']):
        _sketch_flower(draw, 400, 350, s, style)
    elif any(w in d for w in ['ocean', 'sea', 'wave', 'water']):
        _sketch_ocean(draw, s, style)
    elif any(w in d for w in ['sun', 'moon', 'star']):
        _sketch_celestial(draw, s, style)

    # Architecture
    elif any(w in d for w in ['house', 'cabin', 'cottage', 'home']):
        _sketch_house(draw, 400, 350, s, style)
    elif any(w in d for w in ['city', 'building', 'skyline', 'tower']):
        _sketch_city(draw, s, style)
    elif any(w in d for w in ['bridge', 'arch']):
        _sketch_bridge(draw, s, style)

    # Objects
    elif any(w in d for w in ['car', 'vehicle', 'truck']):
        _sketch_car(draw, 350, 380, s, style)
    elif any(w in d for w in ['boat', 'ship', 'sail']):
        _sketch_boat(draw, 400, 350, s, style)
    elif any(w in d for w in ['cup', 'mug', 'glass', 'bottle']):
        _sketch_cup(draw, 400, 320, s, style)
    elif any(w in d for w in ['book', 'notebook']):
        _sketch_book(draw, 350, 320, s, style)

    # Abstract / default - geometric study
    else:
        _sketch_geometric(draw, s, style)


# Subject sketching functions
def _sketch_face(draw, cx, cy, size, s, style):
    """Sketch a face/portrait."""
    # Head oval
    draw.ellipse([cx-size, cy-size, cx+size, cy+size+20], outline=s['stroke'], width=2)
    # Center line
    draw.line([(cx, cy-size), (cx, cy+size+20)], fill=s['medium'], width=1)
    # Eye line
    draw.line([(cx-size+20, cy-20), (cx+size-20, cy-20)], fill=s['medium'], width=1)
    # Eyes
    for ex in [cx-35, cx+35]:
        draw.ellipse([ex-15, cy-35, ex+15, cy-10], outline=s['stroke'], width=2)
        draw.ellipse([ex-5, cy-28, ex+5, cy-18], fill=s['dark'])
    # Nose
    draw.line([(cx, cy-10), (cx-15, cy+20)], fill=s['medium'], width=1)
    draw.line([(cx-15, cy+20), (cx, cy+25)], fill=s['medium'], width=1)
    # Mouth
    draw.arc([cx-30, cy+30, cx+30, cy+60], start=0, end=180, fill=s['stroke'], width=2)
    # Hair suggestion
    for i in range(-30, 31, 8):
        draw.arc([cx+size-10, cy-size-20+i, cx+size+40, cy-size+40+i], 
                 start=200, end=340, fill=s['medium'], width=2)

def _sketch_cat(draw, cx, cy, s, style):
    draw.ellipse([cx-70, cy-60, cx+70, cy+50], outline=s['stroke'], width=2)
    draw.polygon([(cx-50, cy-30), (cx-80, cy-90), (cx-20, cy-40)], outline=s['stroke'], width=2)
    draw.polygon([(cx+50, cy-30), (cx+80, cy-90), (cx+20, cy-40)], outline=s['stroke'], width=2)
    for ex in [cx-20, cx+20]:
        draw.ellipse([ex-12, cy-15, ex+12, cy+5], outline=s['stroke'], width=2)
        draw.line([(ex-8, cy-5), (ex, cy-10)], fill=s['dark'], width=2)
        draw.line([(ex, cy-10), (ex+8, cy-5)], fill=s['dark'], width=2)
    draw.polygon([(cx-8, cy+15), (cx+8, cy+15), (cx, cy+25)], fill=s['dark'])
    draw.line([(cx, cy+25), (cx, cy+50)], fill=s['stroke'], width=1)
    for side in [-1, 1]:
        for wy in range(-5, 15, 8):
            draw.line([(cx+side*60, cy+wy), (cx+side*100, cy+wy-10)], fill=s['medium'], width=1)

def _sketch_dog(draw, cx, cy, s, style):
    draw.ellipse([cx-60, cy-50, cx+60, cy+40], outline=s['stroke'], width=2)
    draw.ellipse([cx+30, cy+10, cx+90, cy+50], fill=s['bg'], outline=s['stroke'], width=2)
    for ex in [cx-20, cx+15]:
        draw.ellipse([ex-8, cy-10, ex+8, cy+5], fill=s['dark'])
    draw.ellipse([cx-5, cy+10, cx+5, cy+20], fill=s['dark'])
    draw.arc([cx-20, cy+20, cx+20, cy+45], start=0, end=180, fill=s['stroke'], width=2)
    # Floppy ears
    draw.ellipse([cx-70, cy-30, cx-35, cy+15], fill=s['bg'], outline=s['stroke'], width=2)
    draw.ellipse([cx+45, cy-20, cx+75, cy+20], fill=s['bg'], outline=s['stroke'], width=2)

def _sketch_bird(draw, cx, cy, s, style):
    draw.ellipse([cx-20, cy-15, cx+30, cy+20], outline=s['stroke'], width=2)
    draw.ellipse([cx-30, cy-5, cx-10, cy+15], outline=s['stroke'], width=2)
    draw.polygon([(cx+25, cy), (cx+50, cy-5), (cx+25, cy+8)], fill=s['stroke'])
    draw.ellipse([cx-25, cy-2, cx-18, cy+5], fill=s['dark'])
    # Wings
    for wy in range(-15, 20, 5):
        draw.arc([cx-25, cy-40, cx+15, cy-10], start=300, end=60, fill=s['medium'], width=1)
        draw.arc([cx-25, cy-40+wy, cx+15, cy-10+wy], start=300, end=60, fill=s['medium'], width=1)

def _sketch_fish(draw, cx, cy, s, style):
    draw.ellipse([cx-60, cy-20, cx+40, cy+25], outline=s['stroke'], width=2)
    draw.polygon([(cx+35, cy+2), (cx+70, cy-15), (cx+70, cy+20), (cx+35, cy+2)], outline=s['stroke'], width=2)
    draw.ellipse([cx-40, cy-5, cx-25, cy+8], fill=s['dark'])
    for i in range(5):
        y = cy - 35 + i*15
        draw.arc([cx-20, y, cx+10, y+15], start=300, end=60, fill=s['light'], width=1)

def _sketch_mountains(draw, s, style):
    for i in range(3):
        h = random.randint(150, 300)
        x = i*250 + random.randint(-30, 30)
        draw.polygon([(x, 400), (x+150, 400-h), (x+300, 400)], outline=s['stroke'], width=2)
        # Snow caps
        if h > 220:
            draw.polygon([(x+130, 400-h+40), (x+150, 400-h), (x+170, 400-h+40)], 
                        fill=s['bg'], outline=s['stroke'], width=1)
    # Ground line
    draw.line([(0, 400), (800, 400)], fill=s['medium'], width=2)

def _sketch_trees(draw, s, style):
    for _ in range(random.randint(4, 8)):
        tx = random.randint(50, 750)
        th = random.randint(80, 200)
        draw.rectangle([tx+3, 400-th, tx+7, 400], fill=s['dark'])
        for level in range(3):
            ty = 400 - th + level*55
            tw = random.randint(40, 70)
            draw.polygon([(tx-tw//2+5, ty), (tx+5, ty-45), (tx+tw//2+5, ty)], 
                        outline=s['stroke'], width=2)
    draw.line([(0, 400), (800, 400)], fill=s['medium'], width=2)

def _sketch_flower(draw, cx, cy, s, style):
    draw.line([(cx, cy+60), (cx, cy-20)], fill=s['dark'], width=2)
    for i in range(8):
        angle = (2*math.pi/8) * i
        px = cx + int(30 * math.cos(angle))
        py = cy - 10 + int(30 * math.sin(angle))
        draw.ellipse([px-12, py-12, px+12, py+12], outline=s['stroke'], width=2)
    draw.ellipse([cx-8, cy-18, cx+8, cy-2], fill=s['dark'])
    # Leaves
    for side in [-1, 1]:
        draw.ellipse([cx+side*5, cy+15, cx+side*40, cy+40], outline=s['stroke'], width=1)

def _sketch_ocean(draw, s, style):
    draw.line([(0, 350), (800, 350)], fill=s['medium'], width=2)
    for i in range(100):
        y = 350 + i*2.5
        for x in range(0, 800, 5):
            wy = y + int(8 * math.sin(x*0.03 + i*0.5))
            if random.random() > 0.7:
                draw.point((x, wy), fill=s['medium'])

def _sketch_celestial(draw, s, style):
    draw.ellipse([500, 80, 650, 230], outline=s['stroke'], width=2)
    for i in range(8):
        angle = (2*math.pi/8) * i
        px = 575 + int(90 * math.cos(angle))
        py = 155 + int(90 * math.sin(angle))
        draw.line([(575, 155), (px, py)], fill=s['medium'], width=1)
    for _ in range(30):
        sx, sy = random.randint(0, 800), random.randint(0, 350)
        draw.point((sx, sy), fill=s['medium'])

def _sketch_house(draw, cx, cy, s, style):
    draw.rectangle([cx-60, cy-40, cx+60, cy+50], outline=s['stroke'], width=2)
    draw.polygon([(cx-80, cy-40), (cx, cy-100), (cx+80, cy-40)], outline=s['stroke'], width=2)
    draw.rectangle([cx-15, cy, cx+15, cy+50], outline=s['stroke'], width=2)
    draw.ellipse([cx+5, cy+20, cx+12, cy+28], fill=s['dark'])
    for wx in [cx-40, cx+25]:
        draw.rectangle([wx-15, cy-25, wx+15, cy-5], outline=s['stroke'], width=1)

def _sketch_city(draw, s, style):
    for _ in range(random.randint(8, 15)):
        bx = random.randint(0, 780)
        bw = random.randint(30, 80)
        bh = random.randint(100, 300)
        draw.rectangle([bx, 400-bh, bx+bw, 400], outline=s['stroke'], width=2)
        for wy in range(400-bh+20, 390, 20):
            for wx in range(bx+10, bx+bw-10, 15):
                if random.random() > 0.4:
                    draw.rectangle([wx, wy, wx+8, wy+10], outline=s['medium'], width=1)

def _sketch_bridge(draw, s, style):
    for x in range(100, 701, 100):
        draw.rectangle([x-5, 200, x+5, 380], outline=s['stroke'], width=2)
    draw.arc([100, 160, 700, 260], start=0, end=180, fill=s['stroke'], width=3)
    for y in range(210, 380, 20):
        draw.line([(120, y), (680, y)], fill=s['medium'], width=1)

def _sketch_car(draw, cx, cy, s, style):
    draw.rectangle([cx-100, cy-20, cx+100, cy+15], outline=s['stroke'], width=2)
    draw.arc([cx-60, cy-50, cx+60, cy-15], start=0, end=180, fill=s['stroke'], width=2)
    for wx in [cx-50, cx+50]:
        draw.ellipse([wx-20, cy+5, wx+20, cy+35], outline=s['stroke'], width=2)
    draw.rectangle([cx-60, cy-40, cx-20, cy-20], outline=s['medium'], width=1)
    draw.rectangle([cx+20, cy-40, cx+60, cy-20], outline=s['medium'], width=1)

def _sketch_boat(draw, cx, cy, s, style):
    draw.polygon([(cx-80, cy+30), (cx-30, cy-30), (cx+30, cy-30), (cx+80, cy+30)], 
                 outline=s['stroke'], width=2)
    draw.line([(cx, cy-30), (cx, cy-100)], fill=s['dark'], width=2)
    draw.polygon([(cx, cy-95), (cx+50, cy-40), (cx, cy-30)], outline=s['stroke'], width=1)

def _sketch_cup(draw, cx, cy, s, style):
    draw.rectangle([cx-30, cy-20, cx+30, cy+40], outline=s['stroke'], width=2)
    draw.ellipse([cx-30, cy-20, cx+30, cy-5], outline=s['stroke'], width=2)
    draw.arc([cx+20, cy-5, cx+50, cy+20], start=250, end=350, fill=s['stroke'], width=2)
    draw.ellipse([cx-20, cy+3, cx+20, cy+15], outline=s['medium'], width=1)

def _sketch_book(draw, cx, cy, s, style):
    draw.polygon([(cx-60, cy+30), (cx-70, cy), (cx-50, cy-40), (cx+10, cy-30),
                  (cx+20, cy), (cx+60, cy), (cx+70, cy+30), (cx+10, cy)],
                 outline=s['stroke'], width=2)
    draw.line([(cx-50, cy-40), (cx+10, cy-30)], fill=s['stroke'], width=2)
    for line_y in range(-20, 30, 10):
        draw.line([(cx-55, cy+line_y), (cx+55, cy+line_y)], fill=s['medium'], width=1)

def _sketch_geometric(draw, s, style):
    for _ in range(random.randint(5, 10)):
        cx, cy = random.randint(100, 700), random.randint(100, 500)
        size = random.randint(30, 100)
        shape = random.choice(['circle', 'square', 'triangle', 'hexagon'])
        if shape == 'circle':
            draw.ellipse([cx-size, cy-size, cx+size, cy+size], outline=s['stroke'], width=2)
            draw.ellipse([cx-size//2, cy-size//2, cx+size//2, cy+size//2], outline=s['medium'], width=1)
        elif shape == 'square':
            draw.rectangle([cx-size, cy-size, cx+size, cy+size], outline=s['stroke'], width=2)
            draw.rectangle([cx-size//2, cy-size//2, cx+size//2, cy+size//2], outline=s['medium'], width=1)
        elif shape == 'triangle':
            draw.polygon([(cx, cy-size), (cx-size, cy+size), (cx+size, cy+size)], 
                        outline=s['stroke'], width=2)
        elif shape == 'hexagon':
            pts = []
            for i in range(6):
                angle = math.pi/3 * i
                pts.append((cx + int(size*math.cos(angle)), cy + int(size*math.sin(angle))))
            draw.polygon(pts, outline=s['stroke'], width=2)