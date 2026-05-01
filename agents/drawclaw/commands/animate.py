"""Animate command - Generate animated GIFs from drawing sequences"""
import sys, os
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

def run(args):
    if not args:
        return "Usage: /animate <style> <frames>\nExample: /animate spiral 30\n         /animate waves 20\n         /animate geometric 25"
    
    import imageio
    import numpy as np
    from PIL import Image, ImageDraw
    import random, math
    
    d = args.lower()
    
    # Detect style and frame count
    parts = d.split()
    frame_count = 30
    for p in parts:
        if p.isdigit():
            frame_count = min(int(p), 60)
            break
    
    mode = 'spiral'
    if any(w in d for w in ['wave', 'ocean', 'sine']): mode = 'wave'
    elif any(w in d for w in ['geometric', 'geo', 'shapes']): mode = 'geometric'
    elif any(w in d for w in ['flower', 'bloom', 'open']): mode = 'bloom'
    elif any(w in d for w in ['bubble', 'pop', 'float']): mode = 'bubble'
    elif any(w in d for w in ['kaleidoscope', 'kaleido', 'mirror']): mode = 'kaleidoscope'
    
    frames = []
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFD700', '#DDA0DD', '#FF69B4', '#87CEEB']
    
    for frame in range(frame_count):
        img = Image.new('RGB', (400, 400), color='#1a1a2e')
        draw = ImageDraw.Draw(img)
        t = frame / frame_count
        
        if mode == 'spiral':
            for i in range(100):
                angle = i * 0.15 + t * 2*math.pi
                radius = 3 + i * 2
                x = 200 + int(radius * math.cos(angle))
                y = 200 + int(radius * math.sin(angle))
                c = colors[i % len(colors)]
                draw.ellipse([x-2, y-2, x+2, y+2], fill=c)
        
        elif mode == 'wave':
            for y in range(0, 400, 3):
                offset = int(30 * math.sin(y*0.05 + t*2*math.pi))
                c = colors[(y//3) % len(colors)]
                draw.line([(0, y), (400, y+offset)], fill=c, width=2)
        
        elif mode == 'geometric':
            for i in range(3, 8):
                pts = []
                for j in range(i):
                    angle = 2*math.pi*j/i + t*math.pi
                    r = 100 + 30*math.sin(t*2*math.pi + i)
                    x = 200 + int(r * math.cos(angle))
                    y = 200 + int(r * math.sin(angle))
                    pts.append((x, y))
                draw.polygon(pts, fill=colors[i%len(colors)], outline='#FFFFFF')
        
        elif mode == 'bloom':
            petals = 8
            for i in range(petals):
                angle = 2*math.pi*i/petals + t*0.5
                size = 30 + t * 80
                px = 200 + int(size*0.5 * math.cos(angle))
                py = 200 + int(size*0.5 * math.sin(angle))
                draw.ellipse([px-size//4, py-size//4, px+size//4, py+size//4], 
                            fill=colors[i%len(colors)])
            draw.ellipse([190, 190, 210, 210], fill='#FFD700')
        
        elif mode == 'bubble':
            for i in range(20):
                bx = 200 + int(100*math.cos(i*0.5 + t))
                by = 200 + int(80*math.sin(i*0.7 + t*1.3))
                r = int(5 + 15*math.sin(i + t))
                draw.ellipse([bx-r, by-r, bx+r, by+r], fill=colors[i%len(colors)], outline='#FFFFFF')
                draw.ellipse([bx-r//3, by-r//3, bx+r//4, by+r//4], fill='#FFFFFF')
        
        elif mode == 'kaleidoscope':
            for quadrant in range(4):
                qx = 200 if quadrant % 2 == 0 else 0
                qy = 200 if quadrant < 2 else 0
                for i in range(10):
                    angle = i * 0.5 + t
                    r = 20 + i * 8
                    x = qx + int(r*math.cos(angle))
                    y = qy + int(r*math.sin(angle))
                    draw.ellipse([x-4, y-4, x+4, y+4], fill=colors[(i+quadrant)%len(colors)])
        
        frames.append(np.array(img))
    
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = Path('exports') / f'animate_{ts}.gif'
    imageio.mimsave(str(path), frames, duration=0.1, loop=0)
    os.startfile(str(path))
    return f'Saved: {path.name} | {mode} style | {frame_count} frames'