"""Illustrate command - Story panels, comic strips, and sequential art"""
from pathlib import Path
from datetime import datetime
import sys, os, random, math
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

def run(args):
    from PIL import Image, ImageDraw

    d = args.lower() if args else "story"

    # Detect format
    if any(w in d for w in ['comic', 'strip', 'cartoon']):
        format_type = 'comic'
        panels = random.randint(3, 6)
        panel_w, panel_h = 230, 250
        cols = 3
    elif any(w in d for w in ['storyboard', 'film', 'movie']):
        format_type = 'storyboard'
        panels = random.randint(4, 8)
        panel_w, panel_h = 180, 140
        cols = 4
    elif any(w in d for w in ['tutorial', 'steps', 'how to']):
        format_type = 'tutorial'
        panels = random.randint(3, 5)
        panel_w, panel_h = 350, 160
        cols = 2
    elif any(w in d for w in ['manga', 'anime', 'japanese']):
        format_type = 'manga'
        panels = random.randint(4, 7)
        panel_w, panel_h = 200, 280
        cols = 3
    else:
        format_type = 'classic'
        panels = random.randint(3, 6)
        panel_w, panel_h = 220, 250
        cols = 3

    # Calculate canvas
    rows = (panels + cols - 1) // cols
    margin = 20
    width = margin*2 + cols*panel_w + (cols-1)*10
    height = margin*2 + 55 + rows*panel_h + (rows-1)*10
    width = max(width, 800)
    height = max(height, 600)

    # Style themes
    themes = {
        'comic': {'bg': '#FFFFFF', 'border': '#1a1a1a', 'text': '#1a1a1a', 'accent': '#FF0000'},
        'storyboard': {'bg': '#F5F0E8', 'border': '#666666', 'text': '#333333', 'accent': '#4169E1'},
        'tutorial': {'bg': '#FAFAFA', 'border': '#4A90D9', 'text': '#2C3E50', 'accent': '#27AE60'},
        'manga': {'bg': '#F8F8F8', 'border': '#1a1a1a', 'text': '#1a1a1a', 'accent': '#FF69B4'},
        'classic': {'bg': '#FFFAF0', 'border': '#8B4513', 'text': '#2C1810', 'accent': '#D2691E'}
    }
    theme = themes.get(format_type, themes['classic'])

    img = Image.new('RGB', (width, height), color=theme['bg'])
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, width, 45], fill=theme['border'])
    title_text = f'ILLUSTRATION: {format_type.upper()} - {args[:50]}'
    draw.text((15, 12), title_text, fill='#FFFFFF')

    # Draw panels
    for p in range(panels):
        row = p // cols
        col = p % cols
        px = margin + col*(panel_w+10)
        py = margin + 50 + row*(panel_h+10)
        
        # Panel border
        draw.rectangle([px, py, px+panel_w, py+panel_h], 
                       outline=theme['border'], width=3)
        
        # Panel number
        draw.text((px+5, py+5), str(p+1), fill=theme['border'])
        
        # Panel content - different for each format
        if format_type == 'comic':
            _draw_comic_panel(draw, px, py, panel_w, panel_h, p, theme)
        elif format_type == 'storyboard':
            _draw_storyboard_panel(draw, px, py, panel_w, panel_h, p, theme)
        elif format_type == 'tutorial':
            _draw_tutorial_panel(draw, px, py, panel_w, panel_h, p, theme)
        elif format_type == 'manga':
            _draw_manga_panel(draw, px, py, panel_w, panel_h, p, theme)
        else:
            _draw_classic_panel(draw, px, py, panel_w, panel_h, p, theme)
    
    # Description area at bottom
    desc_y = margin + 55 + rows*(panel_h+10) + 10
    draw.text((margin, desc_y), f'Sequence: {args[:100]}', fill=theme['text'])

    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = Path('exports') / f'illustrate_{ts}.png'
    img.save(str(path))
    os.startfile(str(path))
    return f'Saved: {path.name} | Format: {format_type} | {panels} panels'


def _draw_comic_panel(draw, x, y, w, h, panel_num, theme):
    """Draw a comic-style panel with speech bubbles and action"""
    c = x + w//2
    cy = y + h//2
    
    # Simple character
    head_size = min(w, h) // 6
    draw.ellipse([c-head_size, cy-head_size-15, c+head_size, cy+head_size-15], 
                 fill='#FFE4C4', outline=theme['border'], width=2)
    # Body
    draw.rectangle([c-head_size//2, cy+head_size-10, c+head_size//2, cy+head_size*2], 
                   fill=theme['accent'])
    
    # Speech bubble (alternating sides)
    bubble_x = x + 10 if panel_num % 2 == 0 else x + w - 70
    bubble_y = y + 10
    draw.ellipse([bubble_x, bubble_y, bubble_x+60, bubble_y+35], 
                 fill='#FFFFFF', outline=theme['border'], width=1)
    # Tail
    tail_x = c - 10 if panel_num % 2 == 0 else c + 10
    draw.polygon([(bubble_x+20, bubble_y+35), (tail_x, cy-30), (bubble_x+40, bubble_y+35)], 
                 fill='#FFFFFF', outline=theme['border'], width=1)


def _draw_storyboard_panel(draw, x, y, w, h, panel_num, theme):
    """Draw a storyboard-style panel with camera notes"""
    # Scene framing
    draw.rectangle([x+10, y+10, x+w-10, y+h-10], outline=theme['border'], width=1)
    
    # Action lines
    for i in range(3):
        ly = y + 30 + i*30
        draw.line([(x+20, ly), (x+w-20, ly)], fill=theme['border'], width=1)
    
    # Camera notes
    notes = ['WIDE', 'MED', 'CLOSE', 'POV', 'OTS', 'LOW', 'HIGH', 'DOLLY']
    note = notes[panel_num % len(notes)]
    draw.text((x+5, y+h-20), note, fill=theme['accent'])


def _draw_tutorial_panel(draw, x, y, w, h, panel_num, theme):
    """Draw a tutorial panel with step indicators"""
    # Step circle
    r = 20
    cx, cy = x + 30, y + 30
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=theme['accent'], outline=theme['border'], width=2)
    draw.text((cx-5, cy-8), str(panel_num+1), fill='#FFFFFF')
    
    # Arrow to next if not last
    draw.rectangle([x+50, cy-2, x+w-30, cy+2], fill=theme['border'])
    # Arrowhead
    draw.polygon([(x+w-30, cy-6), (x+w-20, cy), (x+w-30, cy+6)], fill=theme['border'])
    
    # Instruction lines
    for i in range(3):
        ly = y + 60 + i*25
        draw.rectangle([x+20, ly, x+80, ly+15], fill=theme['border'])
    
    # Checkmark on last panel
    if panel_num >= 2:
        cx2 = x + w - 35
        draw.line([(cx2-20, cy+20), (cx2-8, cy+35)], fill=theme['accent'], width=3)
        draw.line([(cx2-8, cy+35), (cx2+15, cy+10)], fill=theme['accent'], width=3)


def _draw_manga_panel(draw, x, y, w, h, panel_num, theme):
    """Draw a manga-style panel with speed lines"""
    # Speed/action lines
    for i in range(8):
        lx = x + random.randint(5, w-5)
        ly = y + random.randint(5, h-5)
        draw.line([(lx, ly), (lx+random.randint(-30, 30), ly+random.randint(-30, 30))], 
                  fill=theme['border'], width=1)
    
    # Character silhouette
    head_y = y + h//5
    head_r = min(w, h)//8
    draw.ellipse([x+w//2-head_r, head_y, x+w//2+head_r, head_y+head_r*2], 
                 fill=theme['border'])
    draw.rectangle([x+w//2-head_r//2, head_y+head_r*2, x+w//2+head_r//2, head_y+head_r*5], 
                   fill=theme['border'])
    
    # Screen tone pattern (hatching)
    for i in range(0, w, 6):
        for j in range(0, h, 8):
            if (i+j) % 4 == 0:
                draw.point((x+i, y+j), fill=theme['border'])


def _draw_classic_panel(draw, x, y, w, h, panel_num, theme):
    """Draw a classic illustration panel"""
    # Decorative border
    draw.rectangle([x+5, y+5, x+w-5, y+h-5], outline=theme['border'], width=1)
    
    # Vignette corners
    corner_size = 15
    for cx, cy in [(x+10, y+10), (x+w-10, y+10), (x+10, y+h-10), (x+w-10, y+h-10)]:
        draw.arc([cx-corner_size, cy-corner_size, cx+corner_size, cy+corner_size], 
                 0, 90, fill=theme['accent'], width=2)
    
    # Central illustration element
    center_x, center_y = x + w//2, y + h//2
    size = min(w, h)//4
    draw.ellipse([center_x-size, center_y-size, center_x+size, center_y+size], 
                 fill=theme['accent'], outline=theme['border'], width=2)
    
    # Decorative elements
    for i in range(4):
        angle = (math.pi/2) * i + math.pi/4
        px = center_x + int(size*1.3 * math.cos(angle))
        py = center_y + int(size*1.3 * math.sin(angle))
        draw.ellipse([px-8, py-8, px+8, py+8], fill=theme['border'])