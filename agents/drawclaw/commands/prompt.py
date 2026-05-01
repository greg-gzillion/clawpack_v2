def run(args):
    if not args:
        return "Usage: /prompt <concept>\nExample: /prompt cyberpunk city at night"
    
    from agents.drawclaw.agent_handler import _agent
    from PIL import Image, ImageDraw, ImageFont
    from pathlib import Path
    from datetime import datetime
    import os, textwrap, json

    # Get AI prompt from LLM
    prompt = _agent.ask_llm(
        f"Create a detailed AI image generation prompt. Include: subject, style, lighting, composition, colors, mood, camera angle.\n\nTopic: {args}"
    )
    
    # Also get variations
    variations = _agent.ask_llm(
        f"Create 3 ALTERNATIVE AI image generation prompts for the same concept, each with different artistic styles (e.g. photorealistic, oil painting, anime, cyberpunk, watercolor, minimalist). Return as numbered list.\n\nConcept: {args}"
    )
    
    # Also get platform-specific formats
    platforms = _agent.ask_llm(
        f"Convert this into optimized prompts for: 1) Midjourney (use --ar, --style, --v parameters), 2) DALL-E 3, 3) Stable Diffusion. Keep each under 200 chars.\n\nConcept: {args}"
    )
    
    # Create prompt card image
    img = Image.new('RGB', (1000, 1000), color='#0d0d1a')
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("arial.ttf", 32)
        heading_font = ImageFont.truetype("arial.ttf", 20)
        body_font = ImageFont.truetype("arial.ttf", 14)
        small_font = ImageFont.truetype("arial.ttf", 12)
    except:
        title_font = ImageFont.load_default()
        heading_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Header
    draw.rectangle([0, 0, 1000, 80], fill='#1a1a3e')
    draw.text((30, 15), f'AI IMAGE PROMPT', fill='#e94560', font=title_font)
    draw.text((30, 50), f'Concept: {args[:60]}', fill='#8888aa', font=small_font)
    
    y = 95
    
    # Main prompt
    draw.text((30, y), 'MAIN PROMPT', fill='#e94560', font=heading_font)
    y += 28
    
    wrapper = textwrap.TextWrapper(width=95)
    for line in wrapper.wrap(prompt):
        draw.text((30, y), line, fill='#E0E0E0', font=body_font)
        y += 20
        if y > 420:
            draw.text((30, y), '...', fill='#666666', font=body_font)
            break
    
    y = 440
    
    # Variations
    draw.rectangle([20, y-5, 980, y+2], fill='#1a1a3e')
    draw.text((30, y+5), 'STYLE VARIATIONS', fill='#FFD700', font=heading_font)
    y += 35
    
    for line in variations.split('\n'):
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('-')):
            for wline in textwrap.wrap(line, width=95):
                draw.text((40, y), wline, fill='#CCCCCC', font=body_font)
                y += 18
                if y > 700:
                    break
        if y > 700:
            break
    
    y = 720
    
    # Platform-specific prompts
    draw.rectangle([20, y-5, 980, y+2], fill='#1a1a3e')
    draw.text((30, y+5), 'PLATFORM-OPTIMIZED', fill='#00CED1', font=heading_font)
    y += 35
    
    current_platform = ""
    for line in platforms.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('1)') or line.startswith('2)') or line.startswith('3)'):
            current_platform = line[:30]
            draw.text((40, y), line[:95], fill='#87CEEB', font=body_font)
        elif line:
            for wline in textwrap.wrap(line, width=90):
                draw.text((60, y), wline, fill='#AAAAAA', font=small_font)
                y += 16
        y += 20
        if y > 900:
            break
    
    # Copy button hint
    y = max(y+20, 930)
    draw.rectangle([20, y, 980, y+35], fill='#1a1a3e')
    draw.text((30, y+8), '[ Copy any prompt above and paste into Midjourney / DALL-E / Stable Diffusion ]', 
              fill='#666666', font=small_font)
    
    # Save
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = Path('exports') / f'prompt_{ts}.png'
    img.save(str(path))
    os.startfile(str(path))
    
    return f"Saved: {path.name}\n\n{prompt[:1000]}"