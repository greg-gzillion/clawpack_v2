def run(args):
    if not args:
        return "Usage: /describe <visual>\nExample: /describe a misty forest at dawn"
    
    from agents.drawclaw.agent_handler import _agent
    from PIL import Image, ImageDraw, ImageFont
    from pathlib import Path
    from datetime import datetime
    import os, textwrap

    # Get rich visual description from AI
    description = _agent.ask_llm(
        f"Describe this visual concept in rich detail suitable for an artist or AI generator. Cover: atmosphere, colors, textures, lighting, mood, materials, spatial relationships, and sensory qualities.\n\nConcept: {args}"
    )
    
    # Create a visual reference card
    img = Image.new('RGB', (900, 900), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    # Try to load a font
    try:
        title_font = ImageFont.truetype("arial.ttf", 28)
        heading_font = ImageFont.truetype("arial.ttf", 18)
        body_font = ImageFont.truetype("arial.ttf", 14)
    except:
        title_font = ImageFont.load_default()
        heading_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
    
    # Header
    draw.rectangle([0, 0, 900, 80], fill='#16213e')
    draw.text((30, 20), f'VISUAL REFERENCE: {args[:50].upper()}', fill='#e94560', font=title_font)
    
    # Color palette extraction from description
    import re
    hex_colors = re.findall(r'#[0-9a-fA-F]{6}', description)
    if not hex_colors:
        # Infer colors from keywords
        color_map = {
            'gold': '#FFD700', 'blue': '#4169E1', 'red': '#FF4444', 'green': '#228B22',
            'purple': '#8B008B', 'orange': '#FF8C00', 'pink': '#FF69B4', 'brown': '#8B4513',
            'white': '#FFFFFF', 'black': '#1a1a1a', 'gray': '#808080', 'yellow': '#FFD700',
            'amber': '#FFBF00', 'crimson': '#DC143C', 'indigo': '#4B0082', 'teal': '#008080',
            'warm': '#FF7B42', 'cool': '#4A90D9', 'dark': '#2C2C2C', 'light': '#F5F0E8',
            'mist': '#D3D3D3', 'fog': '#B0C4DE', 'silver': '#C0C0C0', 'bronze': '#CD7F32'
        }
        hex_colors = []
        for word, color in color_map.items():
            if word in args.lower() or word in description.lower():
                hex_colors.append(color)
        if not hex_colors:
            hex_colors = ['#FF7B42', '#4A90D9', '#228B22', '#FFD700', '#8B4513']
    
    # Color swatches
    draw.text((30, 100), 'COLOR PALETTE', fill='#e94560', font=heading_font)
    for i, color in enumerate(hex_colors[:8]):
        x = 30 + i * 100
        y = 125
        draw.rectangle([x, y, x+85, y+60], fill=color, outline='#333333')
        draw.text((x+5, y+65), color, fill='#999999', font=body_font)
    
    # Mood indicators
    mood_keywords = {
        'serene': 'calm, peaceful', 'dramatic': 'intense, bold', 'mysterious': 'dark, enigmatic',
        'warm': 'cozy, inviting', 'cold': 'stark, harsh', 'nostalgic': 'vintage, soft',
        'futuristic': 'sleek, neon', 'natural': 'organic, earthy', 'elegant': 'refined, luxurious',
        'dark': 'moody, shadowy', 'bright': 'vibrant, energetic', 'soft': 'gentle, diffused'
    }
    
    detected_moods = []
    for word, desc in mood_keywords.items():
        if word in args.lower() or word in description.lower():
            detected_moods.append(f'{word}: {desc}')
    
    if detected_moods:
        draw.text((30, 200), 'MOOD & ATMOSPHERE', fill='#e94560', font=heading_font)
        for i, mood in enumerate(detected_moods[:5]):
            draw.text((30, 225 + i*22), f'• {mood}', fill='#CCCCCC', font=body_font)
    
    # Texture references
    texture_keywords = ['rough', 'smooth', 'glossy', 'matte', 'textured', 'polished', 
                        'weathered', 'crystalline', 'velvety', 'grainy', 'silky', 'metallic']
    textures = [w for w in texture_keywords if w in description.lower()]
    if textures:
        y = 340
        draw.text((30, y), 'TEXTURES & MATERIALS', fill='#e94560', font=heading_font)
        draw.text((30, y+22), ', '.join(textures[:10]).title(), fill='#CCCCCC', font=body_font)
    
    # Lighting info
    lighting_terms = ['golden hour', 'backlight', 'rim light', 'ambient', 'diffused', 
                      'directional', 'volumetric', 'soft', 'harsh', 'moody', 'cinematic']
    detected_lighting = [l for l in lighting_terms if l in description.lower()]
    if detected_lighting:
        y = 390
        draw.text((30, y), 'LIGHTING', fill='#e94560', font=heading_font)
        draw.text((30, y+22), ', '.join(detected_lighting).title(), fill='#CCCCCC', font=body_font)
    
    # Composition notes
    y = 440
    draw.text((30, y), 'COMPOSITION NOTES', fill='#e94560', font=heading_font)
    comp_terms = ['rule of thirds', 'symmetry', 'leading lines', 'framing', 'depth of field',
                  'foreground', 'middle ground', 'background', 'wide angle', 'close-up']
    detected_comp = [c for c in comp_terms if c in description.lower()]
    if detected_comp:
        draw.text((30, y+22), ', '.join(detected_comp).title(), fill='#CCCCCC', font=body_font)
    
    # Full description text
    y = 490
    draw.text((30, y), 'FULL ARTIST REFERENCE', fill='#e94560', font=heading_font)
    
    # Word-wrap the description
    wrapper = textwrap.TextWrapper(width=100)
    wrapped_lines = wrapper.wrap(description)
    
    for i, line in enumerate(wrapped_lines[:18]):
        if line.strip():
            draw.text((30, y+25 + i*20), line.strip(), fill='#E0E0E0', font=body_font)
    
    # Footer
    draw.rectangle([0, 870, 900, 900], fill='#16213e')
    draw.text((30, 878), f'DrawClaw Visual Reference Card | {args[:40]}', fill='#666666', font=body_font)
    
    # Save
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = Path('exports') / f'describe_{ts}.png'
    img.save(str(path))
    os.startfile(str(path))
    
    return f"Saved: {path.name} | Visual reference card generated\n\n{description[:500]}..."