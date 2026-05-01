"""Cartoon command - Expressive cartoon faces with variations"""
from pathlib import Path
from datetime import datetime
import sys, os, random
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

def run(args):
    from PIL import Image, ImageDraw

    img = Image.new('RGB', (800, 600), color='#f5f0e8')
    draw = ImageDraw.Draw(img)
    
    # Title bar
    draw.rectangle([0, 0, 800, 40], fill='#2d2d2d')
    draw.text((15, 10), f'DRAWCLAW CARTOON: {args[:70]}', fill='#ffffff')

    d = args.lower()
    
    # Detect mood from keywords
    mood = 'happy'
    if any(w in d for w in ['sad', 'cry', 'frown']):
        mood = 'sad'
    elif any(w in d for w in ['angry', 'mad', 'furious']):
        mood = 'angry'
    elif any(w in d for w in ['surprised', 'shock', 'wow']):
        mood = 'surprised'
    elif any(w in d for w in ['sleep', 'tired', 'bored']):
        mood = 'sleepy'
    elif any(w in d for w in ['cool', 'sunglass']):
        mood = 'cool'
    elif any(w in d for w in ['wink', 'mischievous']):
        mood = 'wink'

    # Detect style
    style = 'classic'
    if any(w in d for w in ['cat', 'kitty', 'feline']):
        style = 'cat'
    elif any(w in d for w in ['robot', 'bot', 'mech']):
        style = 'robot'
    elif any(w in d for w in ['alien', 'monster', 'creature']):
        style = 'alien'
    elif any(w in d for w in ['bear', 'teddy']):
        style = 'bear'

    # Skin/face colors
    colors = {
        'classic': '#FFE4C4',
        'cat': '#FFDAB9',
        'robot': '#C0C0C0',
        'alien': '#98FB98',
        'bear': '#D2691E'
    }
    face_color = colors.get(style, '#FFE4C4')

    # Head shape
    head_x, head_y = 200, 80
    head_w, head_h = 400, 440
    draw.ellipse([head_x, head_y, head_x+head_w, head_y+head_h], 
                 fill=face_color, outline='#333333', width=4)

    # Style-specific features
    if style == 'cat':
        # Cat ears
        draw.polygon([(head_x+40, head_y+60), (head_x, head_y-30), (head_x+100, head_y+20)], 
                     fill=face_color, outline='#333333', width=4)
        draw.polygon([(head_x+360, head_y+60), (head_x+400, head_y-30), (head_x+300, head_y+20)], 
                     fill=face_color, outline='#333333', width=4)
        # Inner ears
        draw.polygon([(head_x+45, head_y+50), (head_x+20, head_y-10), (head_x+85, head_y+25)], 
                     fill='#FFB6C1')
        draw.polygon([(head_x+355, head_y+50), (head_x+380, head_y-10), (head_x+315, head_y+25)], 
                     fill='#FFB6C1')
        # Whiskers
        for offset in [-1, 1]:
            for wy in [350, 370, 390]:
                draw.line([(head_x+80, wy), (head_x-20, wy+offset*20)], fill='#666666', width=2)
                draw.line([(head_x+320, wy), (head_x+420, wy+offset*20)], fill='#666666', width=2)
        # Nose
        draw.polygon([(head_x+190, 330), (head_x+210, 330), (head_x+200, 350)], fill='#FFB6C1')

    elif style == 'robot':
        # Square head
        head_x, head_y = 200, 100
        head_w, head_h = 400, 400
        draw.rectangle([head_x, head_y, head_x+head_w, head_y+head_h], 
                       fill='#C0C0C0', outline='#333333', width=4)
        # Antenna
        draw.line([(head_x+200, head_y), (head_x+200, head_y-40)], fill='#666666', width=3)
        draw.ellipse([head_x+190, head_y-50, head_x+210, head_y-30], fill='#FF0000')
        # Bolts
        for bx, by in [(head_x+20, head_y+20), (head_x+360, head_y+20), 
                       (head_x+20, head_y+360), (head_x+360, head_y+360)]:
            draw.ellipse([bx, by, bx+20, by+20], fill='#888888')
        face_color = '#C0C0C0'

    elif style == 'alien':
        face_color = '#98FB98'
        # Antennae
        draw.line([(head_x+150, head_y+30), (head_x+100, head_y-40)], fill='#228B22', width=3)
        draw.line([(head_x+250, head_y+30), (head_x+300, head_y-40)], fill='#228B22', width=3)
        draw.ellipse([head_x+90, head_y-50, head_x+110, head_y-30], fill='#FFD700')
        draw.ellipse([head_x+290, head_y-50, head_x+310, head_y-30], fill='#FFD700')
        # Big eyes
        draw.ellipse([head_x+120, head_y+160, head_x+200, head_y+260], fill='#FFFFFF', outline='#333', width=3)
        draw.ellipse([head_x+220, head_y+160, head_x+300, head_y+260], fill='#FFFFFF', outline='#333', width=3)
        draw.ellipse([head_x+155, head_y+195, head_x+175, head_y+230], fill='#000000')
        draw.ellipse([head_x+245, head_y+195, head_x+265, head_y+230], fill='#000000')

    elif style == 'bear':
        face_color = '#D2691E'
        # Round ears
        draw.ellipse([head_x-20, head_y-20, head_x+80, head_y+80], fill='#D2691E', outline='#333', width=4)
        draw.ellipse([head_x+340, head_y-20, head_x+440, head_y+80], fill='#D2691E', outline='#333', width=4)
        draw.ellipse([head_x+10, head_y+10, head_x+60, head_y+60], fill='#FFDAB9')
        draw.ellipse([head_x+360, head_y+10, head_x+410, head_y+60], fill='#FFDAB9')

    # Eyes (vary by mood)
    eye_y = 240
    left_eye_x = 300
    right_eye_x = 460
    
    if mood == 'happy':
        # Simple dots
        draw.ellipse([left_eye_x, eye_y, left_eye_x+50, eye_y+50], fill='#333333')
        draw.ellipse([right_eye_x, eye_y, right_eye_x+50, eye_y+50], fill='#333333')
        # Eyebrows raised
        draw.arc([left_eye_x-10, eye_y-30, left_eye_x+60, eye_y+10], start=200, end=340, fill='#333333', width=3)
        draw.arc([right_eye_x-10, eye_y-30, right_eye_x+60, eye_y+10], start=200, end=340, fill='#333333', width=3)
    
    elif mood == 'sad':
        draw.ellipse([left_eye_x, eye_y, left_eye_x+45, eye_y+45], fill='#333333')
        draw.ellipse([right_eye_x, eye_y, right_eye_x+45, eye_y+45], fill='#333333')
        # Tear
        draw.ellipse([left_eye_x+35, eye_y+40, left_eye_x+50, eye_y+65], fill='#87CEEB')
        # Sad eyebrows
        draw.arc([left_eye_x-10, eye_y+10, left_eye_x+60, eye_y+50], start=20, end=160, fill='#333333', width=3)
        draw.arc([right_eye_x-10, eye_y+10, right_eye_x+60, eye_y+50], start=20, end=160, fill='#333333', width=3)
    
    elif mood == 'angry':
        draw.ellipse([left_eye_x, eye_y, left_eye_x+45, eye_y+45], fill='#333333')
        draw.ellipse([right_eye_x, eye_y, right_eye_x+45, eye_y+45], fill='#333333')
        # Angry eyebrows
        draw.line([(left_eye_x-10, eye_y), (left_eye_x+60, eye_y-20)], fill='#333333', width=4)
        draw.line([(right_eye_x+60, eye_y), (right_eye_x-10, eye_y-20)], fill='#333333', width=4)
    
    elif mood == 'surprised':
        draw.ellipse([left_eye_x, eye_y+5, left_eye_x+50, eye_y+55], fill='#FFFFFF', outline='#333', width=3)
        draw.ellipse([right_eye_x, eye_y+5, right_eye_x+50, eye_y+55], fill='#FFFFFF', outline='#333', width=3)
        draw.ellipse([left_eye_x+15, eye_y+20, left_eye_x+30, eye_y+35], fill='#333333')
        draw.ellipse([right_eye_x+15, eye_y+20, right_eye_x+30, eye_y+35], fill='#333333')
    
    elif mood == 'sleepy':
        # Half-closed eyes
        draw.arc([left_eye_x, eye_y, left_eye_x+50, eye_y+50], start=0, end=180, fill='#333333', width=3)
        draw.arc([right_eye_x, eye_y, right_eye_x+50, eye_y+50], start=0, end=180, fill='#333333', width=3)
        # Zzz
        for i, (zx, zy) in enumerate([(620, 100), (650, 70), (680, 40)]):
            draw.text((zx, zy), 'Z', fill='#666666')
    
    elif mood == 'cool':
        # Sunglasses
        draw.rectangle([left_eye_x-15, eye_y-5, left_eye_x+65, eye_y+55], fill='#1a1a1a')
        draw.rectangle([right_eye_x-15, eye_y-5, right_eye_x+65, eye_y+55], fill='#1a1a1a')
        draw.line([(left_eye_x+65, eye_y+25), (right_eye_x-15, eye_y+25)], fill='#1a1a1a', width=4)
        # Lens shine
        draw.line([(left_eye_x+5, eye_y+10), (left_eye_x+20, eye_y+10)], fill='#666666', width=2)
        draw.line([(right_eye_x+5, eye_y+10), (right_eye_x+20, eye_y+10)], fill='#666666', width=2)
    
    elif mood == 'wink':
        draw.ellipse([left_eye_x, eye_y, left_eye_x+50, eye_y+50], fill='#333333')
        draw.arc([right_eye_x, eye_y, right_eye_x+50, eye_y+50], start=0, end=180, fill='#333333', width=3)

    # Mouth
    mouth_y = 380
    mouth_x = 340
    
    if mood == 'happy' or mood == 'cool' or mood == 'wink':
        draw.arc([mouth_x, mouth_y, mouth_x+120, mouth_y+80], start=0, end=180, fill='#333333', width=4)
    elif mood == 'sad':
        draw.arc([mouth_x, mouth_y+60, mouth_x+120, mouth_y+10], start=180, end=360, fill='#333333', width=4)
    elif mood == 'angry':
        draw.arc([mouth_x, mouth_y+65, mouth_x+120, mouth_y+15], start=180, end=360, fill='#333333', width=4)
    elif mood == 'surprised':
        draw.ellipse([mouth_x, mouth_y, mouth_x+120, mouth_y+60], fill='#333333')
    elif mood == 'sleepy':
        draw.ellipse([mouth_x, mouth_y, mouth_x+120, mouth_y+40], fill='#333333')

    # Cheeks (blush)
    if mood in ('happy', 'surprised', 'wink', 'cool'):
        draw.ellipse([head_x+50, 340, head_x+120, 380], fill='#FFB6C1', outline='')
        draw.ellipse([head_x+280, 340, head_x+350, 380], fill='#FFB6C1', outline='')

    # Hair (optional, random)
    if random.random() > 0.3:
        hair_colors = ['#4A3728', '#8B6914', '#FF6347', '#2C2C2C', '#FFD700']
        hc = random.choice(hair_colors)
        for i in range(0, 400, 20):
            offset = random.randint(-15, 15)
            draw.arc([head_x+i, head_y-30, head_x+i+80, head_y+40], 
                     start=random.randint(160, 200), end=random.randint(160, 200),
                     fill=hc, width=random.randint(3, 6))

    # Hair accessory
    if 'bow' in d:
        draw.polygon([(head_x+170, head_y-10), (head_x+140, head_y-40), (head_x+170, head_y-25)], fill='#FF69B4')
        draw.polygon([(head_x+230, head_y-10), (head_x+260, head_y-40), (head_x+230, head_y-25)], fill='#FF69B4')
        draw.ellipse([head_x+185, head_y-20, head_x+215, head_y+5], fill='#FF1493')
    if 'hat' in d or 'top hat' in d:
        draw.rectangle([head_x+120, head_y-60, head_x+280, head_y], fill='#1a1a1a')
        draw.rectangle([head_x+140, head_y-90, head_x+260, head_y-60], fill='#1a1a1a')
    if 'crown' in d:
        for i, cx in enumerate([head_x+130, head_x+180, head_x+230, head_x+280]):
            h = random.randint(30, 50)
            draw.polygon([(cx-15, head_y), (cx, head_y-h), (cx+15, head_y)], fill='#FFD700')

    # Save and open
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = Path('exports') / f'cartoon_{ts}.png'
    img.save(str(path))
    os.startfile(str(path))
    return f'Saved: {path.name} | mood={mood} style={style}'