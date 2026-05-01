"""Filter command - Apply OpenCV filters to generated drawings"""
import sys, os
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

def run(args):
    if not args:
        return "Usage: /filter <style> <drawing>\nExample: /filter blur sketch\n         /filter edges cartoon\n         /filter cartoonize portrait"
    
    import cv2
    import numpy as np
    from PIL import Image
    
    d = args.lower()
    mode = 'blur'
    if any(w in d for w in ['edge', 'edges', 'outline']): mode = 'edges'
    elif any(w in d for w in ['cartoon', 'cartoonize', 'toon']): mode = 'cartoon'
    elif any(w in d for w in ['sharpen', 'sharp']): mode = 'sharpen'
    elif any(w in d for w in ['emboss', 'relief']): mode = 'emboss'
    elif any(w in d for w in ['pencil', 'sketch']): mode = 'pencil'
    elif any(w in d for w in ['invert', 'negative']): mode = 'invert'
    elif any(w in d for w in ['sepia', 'vintage', 'old']): mode = 'sepia'
    
    # Find the most recent drawing
    exp = Path('exports')
    files = sorted(exp.glob('*.png'), key=os.path.getmtime, reverse=True)
    if not files:
        return "No drawings found. Generate one first with /sketch, /draw, etc."
    
    img = cv2.imread(str(files[0]))
    if img is None:
        return "Could not read image."
    
    if mode == 'blur':
        result = cv2.GaussianBlur(img, (15, 15), 0)
    elif mode == 'edges':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        result = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    elif mode == 'cartoon':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(img, 9, 250, 250)
        result = cv2.bitwise_and(color, color, mask=edges)
    elif mode == 'sharpen':
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        result = cv2.filter2D(img, -1, kernel)
    elif mode == 'emboss':
        kernel = np.array([[-2,-1,0], [-1,1,1], [0,1,2]])
        result = cv2.filter2D(img, -1, kernel)
    elif mode == 'pencil':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        inv = 255 - gray
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        result = cv2.cvtColor(255 - cv2.divide(gray, 255-blur, scale=256), cv2.COLOR_GRAY2BGR)
    elif mode == 'invert':
        result = 255 - img
    elif mode == 'sepia':
        kernel = np.array([[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]])
        result = cv2.transform(img, kernel)
        result = np.clip(result, 0, 255).astype(np.uint8)
    
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = Path('exports') / f'filter_{mode}_{ts}.png'
    cv2.imwrite(str(path), result)
    os.startfile(str(path))
    return f'Saved: {path.name} | Filter: {mode}'