"""Draw command - AI-assisted drawings with detailed fallback scenes"""
import sys, os, json, random
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / 'agents' / 'llmclaw'))

def _draw_computer(draw):
    # 1970s mainframe/terminal
    draw.rectangle([150, 200, 650, 480], fill='#D2B48C', outline='#8B7355', width=3)  # Desk
    draw.rectangle([200, 100, 500, 200], fill='#2F4F4F', outline='#1a3030', width=3)  # Monitor
    draw.rectangle([220, 120, 480, 180], fill='#1a1a2e', outline='#333333', width=2)  # Screen
    draw.text((300, 145), '> READY.', fill='#00FF00')  # Green text
    draw.rectangle([250, 200, 450, 220], fill='#2F4F4F', outline='#1a3030', width=2)  # Stand
    draw.rectangle([280, 220, 420, 380], fill='#696969', outline='#4a4a4a', width=2)  # Tower
    draw.ellipse([300, 240, 320, 260], fill='#cc0000')  # Power light
    draw.rectangle([300, 300, 400, 320], fill='#333333', outline='#555555', width=1)  # Floppy drive
    draw.rectangle([200, 400, 380, 440], fill='#DDDDDD', outline='#999999', width=2)  # Keyboard
    for i in range(10):
        x = 210 + i * 17
        draw.rectangle([x, 405, x+12, 420], fill='#EEEEEE', outline='#cccccc', width=1)
    return 12

def _draw_house(draw, x=250, y=280):
    draw.rectangle([x, y, x+200, y+150], fill='#D2691E', outline='#8B4513', width=3)
    draw.polygon([(x-30, y), (x+100, y-100), (x+230, y)], fill='#8B0000', outline='#5a0000', width=3)
    draw.rectangle([x+80, y+60, x+130, y+150], fill='#4a3520', outline='#333333', width=2)
    draw.rectangle([x+20, y+30, x+60, y+70], fill='#87CEEB', outline='#5a8aab', width=2)
    draw.rectangle([x+180, y+30, x+220, y+70], fill='#87CEEB', outline='#5a8aab', width=2)
    draw.rectangle([x-20, y+120, x+20, y+150], fill='#FFD700', outline='#FFA500', width=1)
    return 7

def _draw_tree(draw, x=600):
    draw.rectangle([x, 350, x+30, 480], fill='#8B6914', outline='#5a4410', width=2)
    draw.ellipse([x-60, 220, x+90, 380], fill='#228B22', outline='#1a6b1a', width=2)
    draw.ellipse([x-40, 250, x+70, 340], fill='#2E8B2E', outline='#1a6b1a', width=1)
    return 3

def _draw_sun(draw, x=80, y=80):
    draw.ellipse([x, y, x+100, y+100], fill='#FFD700', outline='#FFA500', width=3)
    for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
        import math
        rad = math.radians(angle)
        ex = x+50 + int(55*math.cos(rad))
        ey = y+50 + int(55*math.sin(rad))
        draw.line([(ex-15, ey-15), (ex+15, ey+15)], fill='#FFD700', width=2)
    return 9

def _draw_car(draw, x=200, y=420):
    draw.rectangle([x, y, x+250, y+60], fill='#FF4444', outline='#cc0000', width=3)
    draw.rectangle([x+60, y-30, x+180, y], fill='#FF6666', outline='#cc0000', width=3)
    draw.rectangle([x+70, y-25, x+100, y-5], fill='#87CEEB', outline='#5a8aab', width=2)
    draw.rectangle([x+140, y-25, x+170, y-5], fill='#87CEEB', outline='#5a8aab', width=2)
    draw.ellipse([x+30, y+50, x+80, y+90], fill='#333333')
    draw.ellipse([x+180, y+50, x+230, y+90], fill='#333333')
    draw.ellipse([x+35, y+55, x+75, y+85], fill='#666666')
    draw.ellipse([x+185, y+55, x+225, y+85], fill='#666666')
    return 8

def _draw_robot(draw, x=350, y=200):
    draw.rectangle([x, y, x+100, y+150], fill='#C0C0C0', outline='#808080', width=3)
    draw.rectangle([x-20, y-60, x+120, y+10], fill='#C0C0C0', outline='#808080', width=3)
    draw.ellipse([x+15, y-45, x+45, y-15], fill='#00BFFF', outline='#006699', width=2)
    draw.ellipse([x+55, y-45, x+85, y-15], fill='#00BFFF', outline='#006699', width=2)
    draw.rectangle([x+30, y-5, x+70, y+20], fill='#333333', outline='#555555', width=1)
    for i in range(3):
        draw.ellipse([x+35+i*12, y+5, x+45+i*12, y+15], fill='#ff0000')
    draw.ellipse([x-15, y+100, x+25, y+140], fill='#999999', outline='#666666', width=1)
    draw.ellipse([x+75, y+100, x+115, y+140], fill='#999999', outline='#666666', width=1)
    return 10

SCENES = {
    'house': _draw_house,
    'tree': _draw_tree,
    'sun': _draw_sun,
    'car': _draw_car,
    'robot': _draw_robot,
    'computer': _draw_computer,
}

def run(args):
    from commands.llm_enhanced import run as llm_run
    from PIL import Image, ImageDraw
    
    if not args:
        return 'Usage: /draw <description>\nTry: house, tree, car, robot, sun, computer\nCombine: a house with a tree and sun'
    
    img = Image.new('RGB', (800, 600), color='#E8F0F8')
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 800, 450], fill='#87CEEB')  # Sky
    draw.rectangle([0, 450, 800, 600], fill='#90EE90')  # Ground
    
    count = 0
    args_lower = args.lower()
    
    # Try AI first, fall back to scene detection
    try:
        response = llm_run(f'Output ONLY valid JSON. Draw: {args}. Format: {{"objects":[{{"type":"circle|rectangle|line|triangle","x":0,"y":0,"w":50,"h":50,"color":"#hex"}}]}}. Canvas 800x600. Sky blue bg, green ground. 5-15 objects.')
        if '`' in response:
            response = response.split('`')[1]
            if 'json' in response[:10]:
                response = response[4:]
        data = json.loads(response)
        objects = data.get('objects', [])
        for obj in objects[:20]:
            t = obj.get('type', 'rectangle')
            x = obj.get('x', 50)
            y = max(50, obj.get('y', 50))
            w = obj.get('w', 50)
            h = obj.get('h', 50)
            c = obj.get('color', '#666666')
            if t == 'circle':
                draw.ellipse([x, y, x+w, y+h], fill=c, outline='#333333', width=2)
            elif t == 'line':
                draw.line([(x, y), (x+w, y+h)], fill=c, width=3)
            elif t == 'triangle':
                draw.polygon([(x, y+h), (x+w//2, y), (x+w, y+h)], fill=c, outline='#333333', width=2)
            else:
                draw.rectangle([x, y, x+w, y+h], fill=c, outline='#333333', width=2)
            count += 1
    except:
        # Fallback: detect keywords and draw scenes
        for keyword, draw_func in SCENES.items():
            if keyword in args_lower:
                count += draw_func(draw)
    
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = Path('exports') / f'draw_{ts}.png'
    img.save(str(path))
    os.startfile(str(path))
    
    return f'Saved: {path.name} | {count} objects drawn'
