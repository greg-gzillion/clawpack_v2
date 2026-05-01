def run(args):
    if not args:
        return "Usage: /compose <scene>\nExample: /compose mountain lake at sunset with cabin"
    
    from PIL import Image, ImageDraw
    from pathlib import Path
    from datetime import datetime
    import os

    # Get AI composition guidance
    from agents.drawclaw.agent_handler import _agent
    guidance = _agent.ask_llm(
        f"Analyze this scene compositionally. Identify: focal point placement, rule of thirds, leading lines, depth layers, framing elements, and color harmony.\n\nScene: {args}"
    )
    
    # Render the scene with compositional overlays
    img = Image.new('RGB', (900, 700), color='#F5F0E8')
    draw = ImageDraw.Draw(img)
    
    # Canvas area
    canvas_x, canvas_y = 50, 80
    canvas_w, canvas_h = 800, 550
    
    # Draw actual scene from draw module
    from agents.drawclaw.commands.draw import run as draw_run
    scene_result = draw_run(args)
    
    # Load the generated scene as reference
    import glob
    scene_files = sorted(glob.glob('exports/draw_*.png'), key=os.path.getmtime, reverse=True)
    if scene_files:
        from PIL import Image as PILImage
        scene_img = PILImage.open(scene_files[0])
        scene_img = scene_img.resize((canvas_w, canvas_h))
        img.paste(scene_img, (canvas_x, canvas_y))
    
    # Composition grid overlay
    # Rule of thirds lines
    third_x = canvas_w // 3
    third_y = canvas_h // 3
    for i in range(1, 3):
        # Vertical thirds
        draw.line([(canvas_x + i*third_x, canvas_y), (canvas_x + i*third_x, canvas_y+canvas_h)], 
                  fill='#FF0000', width=1)
        # Horizontal thirds
        draw.line([(canvas_x, canvas_y + i*third_y), (canvas_x+canvas_w, canvas_y + i*third_y)], 
                  fill='#FF0000', width=1)
    
    # Golden ratio spiral (Fibonacci)
    import math
    cx, cy = canvas_x + canvas_w//2, canvas_y + canvas_h//2
    points = [(cx, cy)]
    for i in range(8):
        angle = i * math.pi/2
        radius = 13 * (1.618 ** i)
        px = cx + int(radius * math.cos(angle))
        py = cy + int(radius * math.sin(angle))
        points.append((px, py))
    for i in range(len(points)-1):
        # Arc approximation
        if i < len(points)-1:
            draw.line([points[i], points[i+1]], fill='#FFD700', width=2)
    
    # Focal point markers (intersection points)
    focal_color = '#00FF00'
    for fx, fy in [(canvas_x+third_x, canvas_y+third_y), 
                   (canvas_x+2*third_x, canvas_y+third_y),
                   (canvas_x+third_x, canvas_y+2*third_y),
                   (canvas_x+2*third_x, canvas_y+2*third_y)]:
        draw.ellipse([fx-10, fy-10, fx+10, fy+10], outline=focal_color, width=3)
        draw.ellipse([fx-3, fy-3, fx+3, fy+3], fill=focal_color)
    
    # Leading lines (diagonals)
    draw.line([(canvas_x, canvas_y), (canvas_x+canvas_w, canvas_y+canvas_h)], fill='#4169E1', width=1)
    draw.line([(canvas_x+canvas_w, canvas_y), (canvas_x, canvas_y+canvas_h)], fill='#4169E1', width=1)
    
    # Legend panel
    legend_x = 80
    legend_y = canvas_y + canvas_h + 15
    
    # Title
    draw.text((legend_x, legend_y), f"COMPOSITION ANALYSIS: {args[:60]}", fill='#1a1a1a')
    
    # Legend items
    items = [
        ('#FF0000', 'Rule of Thirds Grid'),
        ('#FFD700', 'Golden Ratio Spiral'),
        ('#00FF00', 'Focal Points (intersections)'),
        ('#4169E1', 'Leading Lines (diagonals)')
    ]
    
    for i, (color, label) in enumerate(items):
        y = legend_y + 25 + i*25
        draw.rectangle([legend_x, y, legend_x+20, y+15], fill=color)
        draw.text((legend_x+30, y-2), label, fill='#1a1a1a')
    
    # Composition notes summary
    note_y = legend_y + 130
    # Extract first 3 lines of guidance
    guidance_lines = [l.strip() for l in guidance.split('\n') if l.strip() and not l.startswith('#')][:4]
    for i, line in enumerate(guidance_lines):
        if len(line) > 80:
            line = line[:77] + '...'
        draw.text((legend_x, note_y + i*20), line, fill='#333333')
    
    # Save
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = Path('exports') / f'compose_{ts}.png'
    img.save(str(path))
    os.startfile(str(path))
    
    return f"Saved: {path.name} | Scene rendered with composition overlay\n\n{guidance[:600]}"