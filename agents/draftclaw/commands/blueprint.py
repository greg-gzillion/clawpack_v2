"""Blueprint command - Generate architectural floor plans from query specifications"""
import os, re
from pathlib import Path

name = "blueprint"
description = "Generate architectural floor plan from query specifications"

def parse_dimensions(args):
    """Extract dimensions like '100x200' or '100ft x 200ft'"""
    dims = re.findall(r'(\d+)\s*[xX]\s*(\d+)', args)
    if dims:
        return int(dims[0][0]), int(dims[0][1])
    dims = re.findall(r'(\d+)\s*ft', args)
    if len(dims) >= 2:
        return int(dims[0]), int(dims[1])
    return None, None

def detect_type(args):
    """Determine building type from keywords"""
    args_lower = args.lower()
    if any(kw in args_lower for kw in ['warehouse','storage','distribution','industrial','logistics']):
        return 'warehouse'
    if any(kw in args_lower for kw in ['office','commercial','business','coworking']):
        return 'office'
    if any(kw in args_lower for kw in ['retail','store','shop','restaurant','cafe']):
        return 'retail'
    if any(kw in args_lower for kw in ['house','home','apartment','residential','condo','living']):
        return 'residential'
    if any(kw in args_lower for kw in ['garage','parking','auto','vehicle']):
        return 'garage'
    if any(kw in args_lower for kw in ['manufacturing','factory','plant','production']):
        return 'manufacturing'
    return 'general'

def detect_features(args):
    """Detect requested features like loading docks, offices, etc."""
    features = []
    args_lower = args.lower()
    if any(kw in args_lower for kw in ['loading dock','dock','truck','shipping']):
        features.append('loading_docks')
    if any(kw in args_lower for kw in ['office','admin','administration']):
        features.append('office_area')
    if any(kw in args_lower for kw in ['restroom','bathroom','toilet']):
        features.append('restrooms')
    if any(kw in args_lower for kw in ['break room','kitchenette','lunch']):
        features.append('break_room')
    if any(kw in args_lower for kw in ['mezzanine','upper','second level']):
        features.append('mezzanine')
    if any(kw in args_lower for kw in ['crane','bridge crane','overhead']):
        features.append('crane')
    if any(kw in args_lower for kw in ['clear height','clear span']):
        height = re.findall(r'(\d+)\s*ft\s*clear', args_lower)
        if height:
            features.append(f'clear_height_{height[0]}ft')
    return features

def run(args):
    if not args:
        return "Usage: /blueprint <specs>\nExample: /blueprint warehouse 100x200 with loading docks and office"

    try:
        from PIL import Image, ImageDraw, ImageFont
        
        width_ft, length_ft = parse_dimensions(args)
        building_type = detect_type(args)
        features = detect_features(args)
        label = args[:80]
        
        if not width_ft:
            width_ft, length_ft = 60, 80
        
        # Try to find fonts
        try:
            font_title = ImageFont.truetype("arial.ttf", 14)
            font_label = ImageFont.truetype("arial.ttf", 11)
            font_small = ImageFont.truetype("arial.ttf", 9)
        except:
            font_title = ImageFont.load_default()
            font_label = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Scale: fit building in canvas
        canvas_w, canvas_h = 1200, 800
        margin = 60
        scale_x = (canvas_w - 2*margin) / length_ft
        scale_y = (canvas_h - 2*margin - 150) / width_ft
        scale = min(scale_x, scale_y)
        
        px_w = int(width_ft * scale)
        px_l = int(length_ft * scale)
        
        img = Image.new('RGB', (canvas_w, canvas_h), color='#fafaf5')
        draw = ImageDraw.Draw(img)
        
        # Title block
        draw.rectangle([0, 0, canvas_w, 55], fill='#1a2744')
        draw.text((15, 8), "DRAFTCLAW ARCHITECTURAL BLUEPRINT", fill='#ffffff', font=font_title)
        draw.text((15, 30), f"Type: {building_type.upper()} | {label}", fill='#7ab8ff', font=font_label)
        scale_text = f"Scale: 1\" = {int(length_ft * 12 / (canvas_w - 2*margin))}'"
        draw.text((canvas_w-280, 10), scale_text, fill='#7ab8ff', font=font_small)
        draw.text((canvas_w-280, 30), "NOT FOR CONSTRUCTION", fill='#ff6b6b', font=font_small)
        
        # Grid
        grid_spacing = 30
        for x in range(0, canvas_w, grid_spacing):
            draw.line([(x, 55), (x, canvas_h-30)], fill='#e8e4dc', width=1)
        for y in range(55, canvas_h-30, grid_spacing):
            draw.line([(0, y), (canvas_w, y)], fill='#e8e4dc', width=1)
        
        # Building outline
        bx, by = margin, 80
        draw.rectangle([bx, by, bx+px_l, by+px_w], outline='#2d2d2d', width=3, fill='#f0ede6')
        
        # Draw based on building type
        if building_type == 'warehouse':
            _draw_warehouse(draw, bx, by, px_l, px_w, width_ft, length_ft, features, font_label, font_small, scale)
        elif building_type == 'office':
            _draw_office(draw, bx, by, px_l, px_w, font_label, font_small)
        else:
            _draw_generic(draw, bx, by, px_l, px_w, font_label, font_small)
        
        # Dimension lines
        dim_y = by + px_w + 20
        draw.line([(bx, dim_y), (bx+px_l, dim_y)], fill='#cc3333', width=1)
        draw.line([(bx, dim_y-5), (bx, dim_y+5)], fill='#cc3333', width=1)
        draw.line([(bx+px_l, dim_y-5), (bx+px_l, dim_y+5)], fill='#cc3333', width=1)
        draw.text((bx + px_l//2 - 30, dim_y+3), f"{length_ft} ft", fill='#cc3333', font=font_small)
        
        dim_x = bx - 20
        draw.line([(dim_x, by), (dim_x, by+px_w)], fill='#cc3333', width=1)
        draw.line([(dim_x-5, by), (dim_x+5, by)], fill='#cc3333', width=1)
        draw.line([(dim_x-5, by+px_w), (dim_x+5, by+px_w)], fill='#cc3333', width=1)
        draw.text((dim_x-50, by + px_w//2 - 8), f"{width_ft} ft", fill='#cc3333', font=font_small)
        
        # Features list
        feature_y = by + px_w + 50
        draw.text((bx, feature_y), "Features:", fill='#1a2744', font=font_label)
        if features:
            for i, feat in enumerate(features):
                draw.text((bx+10, feature_y+18+i*16), f"- {feat.replace('_',' ').title()}", fill='#555555', font=font_small)
        else:
            draw.text((bx+10, feature_y+18), "- Open floor plan", fill='#555555', font=font_small)
        
        # Bottom bar
        draw.rectangle([0, canvas_h-30, canvas_w, canvas_h], fill='#1a2744')
        draw.text((15, canvas_h-22), "DRAFTCLAW V2 | Reference-Based Blueprint | Verify with AHJ", fill='#7ab8ff', font=font_small)
        
        # North arrow
        nx, ny = canvas_w-50, canvas_h-70
        draw.text((nx-10, ny-28), "N", fill='#cc3333', font=font_label)
        draw.line([(nx, ny-25), (nx, ny+5)], fill='#cc3333', width=3)
        draw.polygon([(nx, ny-25), (nx-6, ny-12), (nx+6, ny-12)], fill='#cc3333')
        
        # Save
        exports_dir = Path(__file__).parent.parent / "exports"
        exports_dir.mkdir(exist_ok=True)
        path = exports_dir / f"blueprint_{abs(hash(args))%100000}.png"
        img.save(str(path))
        os.startfile(str(path))
        return f"Architectural blueprint created: {label}\nSaved: {path.name}\nOpening..."
    
    except ImportError:
        return "PIL not installed. Run: pip install pillow"
    except Exception as e:
        return f"Error: {e}"

def _draw_warehouse(draw, bx, by, px_l, px_w, w_ft, l_ft, features, font_label, font_small, scale):
    """Draw warehouse layout with column grid, loading docks, and optional office"""
    # Column grid
    cols_x = max(3, l_ft // 25)
    cols_y = max(2, w_ft // 25)
    spacing_x = px_l / (cols_x)
    spacing_y = px_w / (cols_y)
    
    for cx in range(1, cols_x):
        for cy in range(1, cols_y):
            x = bx + int(cx * spacing_x)
            y = by + int(cy * spacing_y)
            # Column symbol (small filled square)
            col_size = max(4, min(8, px_l // 40))
            draw.rectangle([x-col_size, y-col_size, x+col_size, y+col_size], fill='#2d2d2d')
    
    # Column grid lines (dashed)
    for cx in range(1, cols_x):
        x = bx + int(cx * spacing_x)
        for cy in range(0, cols_y):
            y1 = by + int(cy * spacing_y)
            y2 = by + int(min(cy+1, cols_y) * spacing_y)
            draw.line([(x, y1), (x, y2)], fill='#999999', width=1)
    
    for cy in range(1, cols_y):
        y = by + int(cy * spacing_y)
        draw.line([(bx, y), (bx+px_l, y)], fill='#999999', width=1)
    
    # Column labels
    for cx in range(cols_x):
        x = bx + int((cx + 0.5) * spacing_x)
        draw.text((x-15, by-20), f"A{cx+1}", fill='#1a2744', font=font_small)
    for cy in range(cols_y):
        y = by + int((cy + 0.5) * spacing_y)
        draw.text((bx-30, y-6), f"B{cy+1}", fill='#1a2744', font=font_small)
    
    # Loading docks (if specified or for warehouses)
    if 'loading_docks' in features or True:  # Warehouses always get docks
        dock_count = min(4, max(1, l_ft // 40))
        dock_w = px_l // (dock_count + 2)
        for d in range(dock_count):
            dx = bx + int((d + 1.5) * dock_w)
            dy = by + px_w - 15
            draw.rectangle([dx-10, dy, dx+10, dy+15], outline='#333333', width=2, fill='#cccccc')
            draw.text((dx-8, dy+2), f"D{d+1}", fill='#555555', font=font_small)
        draw.text((bx+5, by+px_w-12), "LOADING DOCKS", fill='#1a2744', font=font_small)
    
    # Office area (if specified)
    if 'office_area' in features:
        off_w = max(px_l // 5, 80)
        draw.rectangle([bx+px_l-off_w, by, bx+px_l, by+60], outline='#555555', width=2)
        draw.text((bx+px_l-off_w+8, by+5), "OFFICE", fill='#1a2744', font=font_label)
        draw.text((bx+px_l-off_w+8, by+22), f'{int(off_w/scale)}x20', fill='#666666', font=font_small)
        
        draw.rectangle([bx+px_l-off_w, by+65, bx+px_l, by+110], outline='#555555', width=2)
        draw.text((bx+px_l-off_w+8, by+70), "RESTROOM", fill='#1a2744', font=font_label)
    
    # Clear height callout
    if any('clear_height' in f for f in features):
        for f in features:
            if 'clear_height' in f:
                height = f.split('_')[2]
                draw.text((bx+px_l//2-40, by+px_w//2-8), f"CLEAR HEIGHT: {height}", fill='#1a2744', font=font_label)
                break
    
    # Warehouse label
    draw.text((bx+10, by+10), "WAREHOUSE FLOOR", fill='#1a2744', font=font_label)
    draw.text((bx+10, by+26), f"{w_ft}' x {l_ft}'", fill='#666666', font=font_small)

def _draw_office(draw, bx, by, px_l, px_w, font_label, font_small):
    """Draw basic office layout"""
    draw.text((bx+10, by+10), "OFFICE LAYOUT", fill='#1a2744', font=font_label)
    # Open workspace
    draw.rectangle([bx+5, by+5, bx+px_l//2, by+px_w-5], outline='#999999', width=1)
    draw.text((bx+20, by+px_w//2), "OPEN OFFICE", fill='#888888', font=font_small)
    # Private offices
    off_w = px_l // 4
    for i in range(3):
        draw.rectangle([bx+px_l//2+5, by+5+i*60, bx+px_l-5, by+55+i*60], outline='#999999', width=1)
        draw.text((bx+px_l//2+15, by+20+i*60), f"OFFICE {i+1}", fill='#555555', font=font_small)

def _draw_generic(draw, bx, by, px_l, px_w, font_label, font_small):
    """Draw generic building outline"""
    w = int(px_w * 0.4)
    h = int(px_l * 0.4)
    draw.rectangle([bx+px_l//2-h//2, by+px_w//2-w//2, bx+px_l//2+h//2, by+px_w//2+w//2], outline='#999999', width=1)
    draw.text((bx+px_l//2-30, by+px_w//2-6), "BUILDING", fill='#888888', font=font_small)