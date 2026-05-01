def run(args):
    if not args:
        return "Usage: /style <concept>\nExample: /style vintage travel poster"
    
    from agents.drawclaw.agent_handler import _agent
    from PIL import Image, ImageDraw, ImageFont
    from pathlib import Path
    from datetime import datetime
    import os, textwrap, random, math

    # Get AI style recommendations
    guidance = _agent.ask_llm(
        f"Recommend art styles, techniques, and reference artists. Include specific style names and why they fit.\n\nConcept: {args}"
    )
    
    # Create style reference card
    img = Image.new('RGB', (950, 850), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("arial.ttf", 30)
        heading_font = ImageFont.truetype("arial.ttf", 18)
        body_font = ImageFont.truetype("arial.ttf", 13)
        small_font = ImageFont.truetype("arial.ttf", 11)
    except:
        title_font = ImageFont.load_default()
        heading_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Header
    draw.rectangle([0, 0, 950, 75], fill='#16213e')
    draw.text((25, 12), f'ART STYLE GUIDE', fill='#e94560', font=title_font)
    draw.text((25, 48), f'Concept: {args[:70]}', fill='#8888aa', font=small_font)
    
    # Color palette section
    draw.text((25, 90), 'RECOMMENDED PALETTE', fill='#e94560', font=heading_font)
    
    palettes = _detect_palette(args)
    for i, (palette_name, colors) in enumerate(palettes.items()):
        y = 115 + i*55
        draw.text((35, y-2), palette_name, fill='#CCCCCC', font=body_font)
        for j, color in enumerate(colors):
            x = 200 + j*65
            draw.rectangle([x, y+5, x+55, y+35], fill=color, outline='#333333')
            draw.text((x+3, y+38), color, fill='#888888', font=small_font)
    
    palette_end_y = 115 + len(palettes)*55 + 10
    draw.line([(25, palette_end_y), (925, palette_end_y)], fill='#333355', width=1)
    
    # Style cards
    draw.text((25, palette_end_y+15), 'ART STYLE MATCHES', fill='#e94560', font=heading_font)
    
    y = palette_end_y + 45
    
    # Parse guidance for style names
    import re
    styles_found = []
    for line in guidance.split('\n'):
        line = line.strip()
        # Look for style references
        style_match = re.findall(r'(\*\*[^*]+\*\*|[A-Z][a-z]+ (?:style|School|movement|ism|art|Renaissance|Baroque|Gothic))', line)
        for s in style_match:
            s = s.replace('**', '').strip()
            if len(s) > 3 and s not in styles_found:
                styles_found.append(s)
    
    if not styles_found:
        styles_found = ['Contemporary', 'Digital Art', 'Realism', 'Abstract', 'Minimalist']
    
    # Draw style cards with visual examples
    card_colors = ['#e94560', '#0f3460', '#16213e', '#533483', '#1a1a2e', '#2d6a4f']
    
    for i, style_name in enumerate(styles_found[:6]):
        card_x = 25 + (i % 3) * 310
        card_y = y + (i // 3) * 140
        
        # Card background
        bg = card_colors[i % len(card_colors)]
        draw.rectangle([card_x, card_y, card_x+290, card_y+120], fill=bg, outline='#444466', width=1)
        
        # Style name
        draw.text((card_x+10, card_y+8), style_name[:30], fill='#FFFFFF', font=heading_font)
        
        # Visual pattern representing the style
        _draw_style_pattern(draw, card_x+10, card_y+35, 270, 75, style_name.lower(), i)
    
    y = y + ((len(styles_found[:6])+2)//3) * 140 + 10
    draw.line([(25, y), (925, y)], fill='#333355', width=1)
    
    # Technique recommendations
    y += 15
    draw.text((25, y), 'TECHNIQUE NOTES', fill='#e94560', font=heading_font)
    y += 25
    
    # Extract technique keywords
    techniques = {
        'composition': ['Rule of Thirds', 'Golden Ratio', 'Leading Lines', 'Symmetry', 'Asymmetry', 'Framing'],
        'lighting': ['Golden Hour', 'Rembrandt', 'Rim Light', 'Chiaroscuro', 'Ambient', 'Studio'],
        'color': ['Complementary', 'Analogous', 'Monochromatic', 'Triadic', 'Warm/Cool', 'Split-Complementary'],
        'texture': ['Impasto', 'Glazing', 'Dry Brush', 'Stippling', 'Hatching', 'Wash'],
    }
    
    for tech_cat, items in techniques.items():
        draw.text((35, y), f'{tech_cat.title()}:', fill='#87CEEB', font=body_font)
        draw.text((160, y), ', '.join(random.sample(items, min(4, len(items)))), fill='#CCCCCC', font=small_font)
        y += 22
    
    y += 10
    
    # Full guidance text
    draw.text((25, y), 'FULL RECOMMENDATIONS', fill='#e94560', font=heading_font)
    y += 25
    
    wrapper = textwrap.TextWrapper(width=100)
    for line in wrapper.wrap(guidance):
        if y < 810:
            draw.text((35, y), line, fill='#E0E0E0', font=body_font)
            y += 18
    
    # Footer
    draw.rectangle([0, 825, 950, 850], fill='#16213e')
    draw.text((25, 830), f'DrawClaw Style Guide | {args[:50]}', fill='#666666', font=small_font)
    
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = Path('exports') / f'style_{ts}.png'
    img.save(str(path))
    os.startfile(str(path))
    
    return f"Saved: {path.name} | {len(styles_found)} styles identified\n\n{guidance[:500]}..."


def _detect_palette(desc):
    """Detect color palettes from description."""
    d = desc.lower()
    palettes = {}
    
    if any(w in d for w in ['sunset', 'warm', 'golden', 'autumn', 'fall']):
        palettes['Sunset Warm'] = ['#FF7B42', '#FF6347', '#FFD700', '#FF1493', '#9400D3', '#2C1810']
    if any(w in d for w in ['ocean', 'cool', 'water', 'blue', 'marine', 'winter']):
        palettes['Ocean Cool'] = ['#006994', '#4A90D9', '#87CEEB', '#1E90FF', '#00CED1', '#001F3F']
    if any(w in d for w in ['forest', 'nature', 'green', 'woods', 'earth']):
        palettes['Forest Earth'] = ['#228B22', '#2D5A27', '#4A7C3F', '#8B4513', '#D2691E', '#87CEEB']
    if any(w in d for w in ['vintage', 'retro', 'old', 'classic', 'antique']):
        palettes['Vintage Classic'] = ['#C0A080', '#8B7355', '#B8860B', '#800020', '#2F4F4F', '#D2B48C']
    if any(w in d for w in ['modern', 'minimal', 'clean', 'sleek']):
        palettes['Modern Minimal'] = ['#FFFFFF', '#2C3E50', '#3498DB', '#95A5A6', '#ECF0F1', '#E74C3C']
    if any(w in d for w in ['cyberpunk', 'neon', 'futuristic', 'synth']):
        palettes['Cyberpunk Neon'] = ['#0a0a2e', '#FF00FF', '#00FFFF', '#FFD700', '#FF1493', '#1a1a4e']
    if any(w in d for w in ['pastel', 'soft', 'gentle', 'light']):
        palettes['Pastel Soft'] = ['#FFB6C1', '#DDA0DD', '#B0E0E6', '#98FB98', '#FFFACD', '#E6E6FA']
    if any(w in d for w in ['dark', 'gothic', 'noir', 'night']):
        palettes['Dark Noir'] = ['#1a1a1a', '#2C2C2C', '#4a0000', '#1a1a4e', '#2d2d2d', '#0a0a0a']
    
    if not palettes:
        palettes['Classic Art'] = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFD700', '#DDA0DD', '#2C3E50']
    
    return palettes


def _draw_style_pattern(draw, x, y, w, h, style_name, seed):
    """Draw a visual pattern representing the art style."""
    random.seed(seed + 42)
    
    if 'abstract' in style_name:
        for _ in range(15):
            sx, sy = x + random.randint(0, w), y + random.randint(0, h)
            size = random.randint(5, 25)
            c = random.choice(['#FF6B6B', '#4ECDC4', '#FFD700', '#DDA0DD', '#FFFFFF'])
            draw.rectangle([sx, sy, sx+size, sy+size], fill=c, outline='')
    
    elif 'minimal' in style_name:
        draw.line([(x, y+h//2), (x+w, y+h//2)], fill='#FFFFFF', width=1)
        draw.line([(x+w//2, y), (x+w//2, y+h)], fill='#FFFFFF', width=1)
        draw.ellipse([x+w//2-8, y+h//2-8, x+w//2+8, y+h//2+8], outline='#FFFFFF', width=1)
    
    elif 'geometric' in style_name or 'cubist' in style_name:
        for _ in range(8):
            pts = [(x+random.randint(0,w), y+random.randint(0,h)) for _ in range(random.randint(3,6))]
            c = random.choice(['#FF6B6B', '#4ECDC4', '#FFD700', '#FFFFFF'])
            if pts: draw.polygon(pts, fill=c, outline='#FFFFFF')
    
    elif 'impressionist' in style_name or 'watercolor' in style_name:
        for _ in range(20):
            sx, sy = x + random.randint(0, w), y + random.randint(0, h)
            sr = random.randint(5, 20)
            c = random.choice(['#FFB6C1', '#87CEEB', '#98FB98', '#FFD700', '#DDA0DD'])
            draw.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=c, outline='')
    
    elif 'pixel' in style_name or '8bit' in style_name:
        ps = 8
        for py in range(y, y+h, ps):
            for px in range(x, x+w, ps):
                if random.random() > 0.5:
                    c = random.choice(['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FFFFFF'])
                    draw.rectangle([px, py, px+ps, py+ps], fill=c)
    
    elif 'noir' in style_name or 'dark' in style_name:
        for _ in range(5):
            lx = x + random.randint(0, w)
            ly = y + random.randint(0, h)
            draw.line([(lx, y), (lx, y+h)], fill='#FFFFFF', width=random.randint(1, 3))
        draw.rectangle([x+10, y+10, x+60, y+60], fill='#FF0000')
    
    elif 'art nouveau' in style_name or 'organic' in style_name:
        for _ in range(4):
            cx, cy = x + random.randint(30, w-30), y + random.randint(20, h-20)
            for angle in range(0, 360, 15):
                r = 20 + 10*math.sin(angle*0.1)
                px = cx + int(r*math.cos(math.radians(angle)))
                py = cy + int(r*math.sin(math.radians(angle)))
                draw.point((px, py), fill='#FFFFFF')
    
    else:
        for _ in range(10):
            sx, sy = x + random.randint(5, w-5), y + random.randint(5, h-5)
            ex, ey = x + random.randint(5, w-5), y + random.randint(5, h-5)
            draw.line([(sx, sy), (ex, ey)], fill='#FFFFFF', width=random.randint(1, 2))