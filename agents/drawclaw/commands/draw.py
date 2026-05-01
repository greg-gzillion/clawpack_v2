"""Draw command - AI-assisted scene rendering with keyword fallback"""
import sys, os, json, random
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

# Scene composition functions
def _sky_gradient(draw, desc):
    d = desc.lower()
    if any(w in d for w in ['sunset', 'golden hour', 'dusk']):
        draw.rectangle([0, 0, 800, 600], fill='#FF7B42')
        for i in range(20):
            y = i * 30
            r = 255 - i*8
            g = 123 - i*6
            b = 66 - i*3
            color = f'#{max(0,r):02x}{max(0,g):02x}{max(0,b):02x}'
            draw.rectangle([0, y, 800, y+30], fill=color)
    elif any(w in d for w in ['night', 'dark', 'moon']):
        for i in range(20):
            y = i * 30
            v = 20 + i*2
            color = f'#{v:02x}{v:02x}{v+10:02x}'
            draw.rectangle([0, y, 800, y+30], fill=color)
    else:
        for i in range(14):
            y = i * 30
            r = 135 + i*8
            g = 206 - i*5
            b = 235 - i*8
            color = f'#{min(255,r):02x}{max(50,g):02x}{max(50,b):02x}'
            draw.rectangle([0, y, 800, y+30], fill=color)
        draw.rectangle([0, 420, 800, 600], fill='#4A7C3F')

def _mountains(draw, desc, start_y=420):
    d = desc.lower()
    colors = ['#6B8E6B', '#5A7D5A', '#4A6B4A']
    if 'snow' in d:
        colors = ['#8B9DAF', '#7A8B9E', '#6A7B8E']
    heights = [random.randint(200, 350), random.randint(180, 320), random.randint(220, 380)]
    for i, h in enumerate(heights):
        x1 = i * 250
        x2 = x1 + 350
        draw.polygon([(x1, start_y), ((x1+x2)//2, start_y-h), (x2, start_y)], fill=colors[i % len(colors)])
        if 'snow' in d and h > 250:
            draw.polygon([((x1+x2)//2-30, start_y-h+50), ((x1+x2)//2, start_y-h), ((x1+x2)//2+30, start_y-h+50)], fill='#FFFFFF')

def _trees(draw, count=5):
    for i in range(count):
        x = random.randint(30, 750)
        y = random.randint(350, 420)
        h = random.randint(40, 80)
        draw.rectangle([x+3, y, x+9, y+h], fill='#5C3A1E')
        draw.polygon([(x-15, y), (x+6, y-h), (x+27, y)], fill='#2D5A27')

def _lake(draw, x=150, y=400, w=500, h=100):
    draw.ellipse([x, y, x+w, y+h], fill='#4A90D9')
    for i in range(5):
        lx = x + random.randint(20, w-40)
        ly = y + random.randint(10, h-20)
        draw.ellipse([lx, ly, lx+30, ly+3], fill='#7AB8E8')

def _sun(draw, x=600, y=60, size=70):
    draw.ellipse([x, y, x+size, y+size], fill='#FFD700')
    for i in range(8):
        angle = i * 45
        import math
        rad = math.radians(angle)
        ex = x+size//2 + int(size*math.cos(rad))
        ey = y+size//2 + int(size*math.sin(rad))
        draw.line([(ex-10, ey-10), (ex+10, ey+10)], fill='#FFD700', width=2)

def _clouds(draw, count=4):
    for i in range(count):
        x = random.randint(0, 700)
        y = random.randint(20, 150)
        for j in range(3):
            cx = x + j*30
            cy = y + random.randint(-10, 10)
            draw.ellipse([cx, cy, cx+40, cy+25], fill='#FFFFFF')

def _cabin(draw, x=350, y=340, w=80, h=60):
    draw.rectangle([x, y, x+w, y+h], fill='#8B4513', outline='#5C2D0E')
    draw.polygon([(x-10, y), (x+w//2, y-40), (x+w+10, y)], fill='#A52A2A', outline='#6B1A1A')
    draw.rectangle([x+25, y+20, x+45, y+45], fill='#4A3520')
    draw.rectangle([x+55, y+15, x+70, y+35], fill='#87CEEB', outline='#5A8AAB')

SCENE_ELEMENTS = {
    'mountain': _mountains,
    'mountains': _mountains,
    'peak': _mountains,
    'alpine': _mountains,
    'tree': lambda d, x: _trees(d, random.randint(3,8)),
    'trees': lambda d, x: _trees(d, random.randint(5,12)),
    'pine': lambda d, x: _trees(d, random.randint(4,10)),
    'forest': lambda d, x: _trees(d, random.randint(8,15)),
    'lake': lambda d, x: _lake(d),
    'water': lambda d, x: _lake(d),
    'pond': lambda d, x: _lake(d, 250, 430, 300, 60),
    'sun': lambda d, x: _sun(d),
    'sunset': lambda d, x: _sun(d, 500, 120, 90),
    'cloud': lambda d, x: _clouds(d, random.randint(3,6)),
    'clouds': lambda d, x: _clouds(d, random.randint(4,8)),
    'cabin': lambda d, x: _cabin(d),
    'house': lambda d, x: _cabin(d),
    'building': lambda d, x: _cabin(d),
    'night': lambda d, x: _sun(d, 500, 40, 50),
    'moon': lambda d, x: draw_moon(d),
}

def draw_moon(draw, x=550, y=40, size=50):
    draw.ellipse([x, y, x+size, y+size], fill='#F5F5DC')

def run(args):
    from PIL import Image, ImageDraw
    
    if not args:
        return 'Usage: /draw <description>\nExamples: /draw a cabin by a mountain lake at sunset\n          /draw forest with trees and clouds'

    img = Image.new('RGB', (800, 600), color='#87CEEB')
    draw = ImageDraw.Draw(img)
    
    # Always try AI first for complex scenes
    from agents.drawclaw.agent_handler import _agent
    try:
        prompt = f"""You are a scene composer. Convert this into PIL drawing commands. Return ONLY valid JSON:
{{"background": "#hex", "elements": [{{"type": "rectangle|ellipse|polygon|line", "x": 0, "y": 0, "w": 100, "h": 100, "color": "#hex", "outline": "#hex"}}]}}
Canvas 800x600. Make it beautiful. Description: {args}"""
        response = _agent.ask_llm(prompt)
        start = response.find("{")
        end = response.rfind("}") + 1
        if start >= 0 and end > start:
            data = json.loads(response[start:end])
            for elem in data.get('elements', []):
                t = elem.get('type', 'rectangle')
                x, y = int(elem.get('x', 0)), int(elem.get('y', 0))
                w, h = int(elem.get('w', 50)), int(elem.get('h', 50))
                c = elem.get('color', '#666')
                o = elem.get('outline', None)
                if t == 'ellipse': draw.ellipse([x, y, x+w, y+h], fill=c, outline=o)
                elif t == 'polygon': draw.polygon(elem.get('points', [(x,y+h),(x+w//2,y),(x+w,y+h)]), fill=c, outline=o)
                elif t == 'line': draw.line([(x,y),(elem.get('x2',x+w),elem.get('y2',y+h))], fill=c, width=elem.get('width',2))
                else: draw.rectangle([x, y, x+w, y+h], fill=c, outline=o)
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            path = Path('exports') / f'draw_{ts}.png'
            img.save(str(path))
            os.startfile(str(path))
            return f"Saved: {path.name} | AI-composed scene"
    except:
        pass
    
    # Fallback: keyword-based scene composition
    d = args.lower()
    _sky_gradient(draw, d)
    
    # Build scene from keywords
    found = []
    for keyword, func in SCENE_ELEMENTS.items():
        if keyword in d:
            try:
                func(draw, d)
                found.append(keyword)
            except:
                pass
    
    if not found:
        # Ultimate fallback: just draw the old hardcoded objects
        for keyword, func in {
            'house': lambda: None, 'tree': lambda: None, 'sun': lambda: None,
            'car': lambda: None, 'robot': lambda: None, 'computer': lambda: None
        }.items():
            if keyword in d:
                break
    
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = Path('exports') / f'draw_{ts}.png'
    img.save(str(path))
    os.startfile(str(path))
    
    return f"Saved: {path.name} | Keywords found: {', '.join(found) if found else 'none'}"