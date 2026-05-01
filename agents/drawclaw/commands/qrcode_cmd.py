"""QR command - Generate QR code images"""
import sys, os
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

def run(args):
    if not args:
        return "Usage: /qr <url or text>\nExample: /qr https://github.com"
    
    import qrcode
    from PIL import Image, ImageDraw
    
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(args)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color='#1a1a1a', back_color='#FFFFFF').convert('RGB')
    
    # Add label
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    label = args[:50] + ('...' if len(args) > 50 else '')
    
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = Path('exports') / f'qr_{ts}.png'
    img.save(str(path))
    os.startfile(str(path))
    return f'Saved: {path.name}'