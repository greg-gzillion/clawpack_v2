"""Blueprint command - Create architectural floor plans"""
import os
from pathlib import Path

name = "blueprint"
description = "Create architectural floor plan"

def run(args):
    if not args:
        return "Usage: /blueprint <specs>\nExample: /blueprint living room 12x15 with sofa TV dining"

    try:
        from PIL import Image, ImageDraw, ImageFont
        
        parts = args.split()
        label = args
        
        # Try to find a font
        try:
            font_title = ImageFont.truetype("arial.ttf", 16)
            font_label = ImageFont.truetype("arial.ttf", 12)
            font_small = ImageFont.truetype("arial.ttf", 10)
        except:
            font_title = ImageFont.load_default()
            font_label = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # Canvas
        width, height = 1000, 700
        img = Image.new('RGB', (width, height), color='#f5f0e8')
        draw = ImageDraw.Draw(img)

        # === TITLE BLOCK (top) ===
        draw.rectangle([0, 0, width, 70], fill='#1a3a5c')
        draw.text((20, 10), "DRAFTCLAW ARCHITECTURAL", fill='#ffffff', font=font_title)
        draw.text((20, 35), label[:80], fill='#7ab8ff', font=font_label)
        draw.text((width-200, 10), f"Scale: 1/4 in = 1 ft", fill='#7ab8ff', font=font_small)
        draw.text((width-200, 35), "Date: 2026-04-24", fill='#7ab8ff', font=font_small)

        # === GRID ===
        for x in range(0, width, 40):
            draw.line([(x, 70), (x, height)], fill='#e8e0d5', width=1)
        for y in range(70, height, 40):
            draw.line([(0, y), (width, y)], fill='#e8e0d5', width=1)

        # === OUTER WALLS ===
        margin = 60
        draw.rectangle([margin, 100, width-margin, height-margin], outline='#2d2d2d', width=4)

        # === LIVING ROOM (left side) ===
        lx, ly, lw, lh = margin+5, 105, 500, 400
        draw.rectangle([lx, ly, lx+lw, ly+lh], outline='#555555', width=2)
        draw.text((lx+10, ly+10), "LIVING ROOM", fill='#1a3a5c', font=font_label)
        draw.text((lx+10, ly+30), "15'-0\" x 20 ft", fill='#666666', font=font_small)
        
        # Sofa
        draw.rectangle([lx+40, ly+lh-80, lx+200, ly+lh-30], fill='#8B7355', outline='#5a4a35', width=2)
        draw.text((lx+70, ly+lh-65), "SOFA", fill='#ffffff', font=font_small)
        
        # Coffee table
        draw.rectangle([lx+80, ly+lh-150, lx+160, ly+lh-120], fill='#A0522D', outline='#6b3410', width=1)
        draw.text((lx+85, ly+lh-140), "TABLE", fill='#ffffff', font=font_small)
        
        # TV
        draw.line([(lx+lw-20, ly+100), (lx+lw-20, ly+250)], fill='#333333', width=6)
        draw.text((lx+lw-60, ly+160), "TV", fill='#333333', font=font_small)

        # === DINING ROOM (right side) ===
        dx, dy, dw, dh = lx+lw+20, 105, width-margin-lx-lw-25, 250
        draw.rectangle([dx, dy, dx+dw, dy+dh], outline='#555555', width=2)
        draw.text((dx+10, dy+10), "DINING ROOM", fill='#1a3a5c', font=font_label)
        draw.text((dx+10, dy+30), "10'-0\" x 12 ft", fill='#666666', font=font_small)
        
        # Dining table
        draw.rectangle([dx+30, dy+dh-100, dx+dw-30, dy+dh-40], fill='#8B6914', outline='#5a4410', width=2)
        draw.text((dx+50, dy+dh-80), "DINING TABLE", fill='#ffffff', font=font_small)
        
        # Chairs (small squares around table)
        for cx in [dx+15, dx+dw-55]:
            for cy in [dy+dh-130, dy+dh-20]:
                draw.rectangle([cx, cy, cx+30, cy+20], fill='#A0826D', outline='#705040', width=1)

        # === KITCHEN (right side bottom) ===
        kx, ky, kw, kh = dx, dy+dh+20, dw, height-margin-dy-dh-25
        draw.rectangle([kx, ky, kx+kw, ky+kh], outline='#555555', width=2)
        draw.text((kx+10, ky+10), "KITCHEN", fill='#1a3a5c', font=font_label)
        
        # Counter
        draw.rectangle([kx+10, ky+50, kx+kw-10, ky+80], fill='#C0C0C0', outline='#888888', width=2)
        draw.text((kx+30, ky+58), "COUNTER / CABINETS", fill='#333333', font=font_small)
        
        # Stove
        draw.rectangle([kx+100, ky+90, kx+160, ky+120], fill='#444444', outline='#222222', width=2)
        draw.text((kx+105, ky+98), "STOVE", fill='#ffffff', font=font_small)
        
        # Sink
        draw.rectangle([kx+200, ky+90, kx+260, ky+120], fill='#87CEEB', outline='#5a8aab', width=2)
        draw.text((kx+210, ky+98), "SINK", fill='#333333', font=font_small)

        # === DOORS (arc indicators) ===
        # Living room door
        draw.arc([lx-15, ly+150, lx+25, ly+190], start=0, end=90, fill='#666666', width=3)
        # Dining door
        draw.arc([dx-15, dy+80, dx+25, dy+120], start=0, end=90, fill='#666666', width=3)

        # === DIMENSION LINES ===
        dim_y = ly+lh+15
        draw.line([(lx, dim_y), (lx+lw, dim_y)], fill='#cc3333', width=1)
        draw.line([(lx, dim_y-10), (lx, dim_y+10)], fill='#cc3333', width=1)
        draw.line([(lx+lw, dim_y-10), (lx+lw, dim_y+10)], fill='#cc3333', width=1)
        draw.text((lx+lw//2-30, dim_y+5), "20 ft", fill='#cc3333', font=font_small)

        # === BOTTOM TITLE BLOCK ===
        draw.rectangle([0, height-40, width, height], fill='#1a3a5c')
        draw.text((20, height-30), "DRAFTCLAW V2 | Architectural Blueprint | NOT FOR CONSTRUCTION", fill='#7ab8ff', font=font_small)

        # === COMPASS ROSE (bottom right) ===
        cx, cy = width-60, height-80
        draw.text((cx-15, cy-35), "N", fill='#cc3333', font=font_label)
        draw.line([(cx, cy-30), (cx, cy+10)], fill='#cc3333', width=3)
        draw.line([(cx-15, cy-10), (cx+15, cy-10)], fill='#333333', width=1)
        draw.polygon([(cx, cy-30), (cx-8, cy-15), (cx+8, cy-15)], fill='#cc3333')

        # Save
        agent_dir = Path(__file__).parent.parent
        exports_dir = agent_dir / "exports"
        exports_dir.mkdir(exist_ok=True)
        path = exports_dir / f"blueprint_{abs(hash(args))%100000}.png"
        img.save(str(path))
        os.startfile(str(path))
        return f"Architectural blueprint created: {label}\nSaved: {path.name}\nOpening..."

    except ImportError:
        return "PIL not installed. Run: pip install pillow"
    except Exception as e:
        return f"Error: {e}"
