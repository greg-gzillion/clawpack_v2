"""Canvas command - Interactive drawing window with tools"""
import sys, os
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

def run(args):
    try:
        import tkinter as tk
        from tkinter import colorchooser, messagebox, simpledialog
    except:
        return 'Tkinter not available. Windows drawing requires tkinter.'

    root = tk.Tk()
    root.title('DrawClaw - Interactive Canvas')
    root.geometry('1000x700')

    # State
    current_color = '#000000'
    current_size = 3
    tool = tk.StringVar(value='pen')
    fill_mode = tk.BooleanVar(value=False)
    shapes = []
    undo_stack = []

    # Toolbar
    toolbar = tk.Frame(root, height=45, bg='#2d2d2d')
    toolbar.pack(fill='x')

    def set_color():
        nonlocal current_color
        c = colorchooser.askcolor(color=current_color)
        if c[1]: current_color = c[1]

    def set_tool(t):
        tool.set(t)
        if t in ('pen', 'eraser', 'spray'):
            canvas.config(cursor='crosshair')
        elif t in ('rect', 'circle', 'line'):
            canvas.config(cursor='cross')
        elif t == 'text':
            canvas.config(cursor='xterm')
        elif t == 'fill':
            canvas.config(cursor='spraycan')
        elif t == 'picker':
            canvas.config(cursor='target')

    def clear_canvas():
        undo_stack.clear()
        shapes.clear()
        canvas.delete('all')

    def undo():
        if shapes:
            item = shapes.pop()
            canvas.delete(item)

    def save_drawing():
        from PIL import Image, ImageDraw
        # Render to PIL by screenshot
        canvas.update()
        x = root.winfo_rootx() + canvas.winfo_x()
        y = root.winfo_rooty() + canvas.winfo_y()
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        from PIL import ImageGrab
        img = ImageGrab.grab(bbox=(x+2, y+2, x+w, y+h))
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        path = Path('exports') / f'canvas_{ts}.png'
        img.save(str(path))
        os.startfile(str(path))
        messagebox.showinfo('Saved', f'Saved: {path.name}')

    def add_text():
        txt = simpledialog.askstring('Text', 'Enter text:')
        if txt:
            item = canvas.create_text(400, 270, text=txt, fill=current_color, font=('Arial', current_size*4))
            shapes.append(item)

    # Tool buttons
    tools = [
        ('✏ Pen', 'pen'), ('◻ Rect', 'rect'), ('○ Circle', 'circle'),
        ('╱ Line', 'line'), ('🖌 Fill', 'fill'), ('💧 Spray', 'spray'),
        ('T Text', 'text'), ('◉ Pick', 'picker'), ('◻ Eraser', 'eraser')
    ]
    for label, t in tools:
        bg = '#555' if tool.get() != t else '#888'
        btn = tk.Button(toolbar, text=label, command=lambda x=t: set_tool(x), bg='#444', fg='white',
                        relief='flat', padx=6, pady=2)
        btn.pack(side='left', padx=1, pady=3)

    # Fill toggle
    tk.Checkbutton(toolbar, text='Fill', variable=fill_mode, bg='#2d2d2d', fg='white',
                   selectcolor='#2d2d2d').pack(side='left', padx=5)

    # Size
    tk.Label(toolbar, text='Size:', bg='#2d2d2d', fg='#aaa').pack(side='left', padx=(10, 2))
    tk.Scale(toolbar, from_=1, to=15, orient='horizontal', command=lambda s: setattr(type(current_size), 'current_size', int(s)) if False else None,
             bg='#444', fg='white', length=80, showvalue=False)
    
    def update_size(s):
        global current_size
        current_size = int(s)
    size_scale = tk.Scale(toolbar, from_=1, to=15, orient='horizontal', command=update_size,
                          bg='#444', fg='white', length=80, showvalue=False)
    size_scale.set(3)
    size_scale.pack(side='left', padx=2)

    # Color preview
    color_preview = tk.Label(toolbar, text='   ', bg=current_color, width=4)
    color_preview.pack(side='left', padx=5)
    tk.Button(toolbar, text='Color', command=lambda: [set_color(), color_preview.config(bg=current_color)],
              bg='#444', fg='white').pack(side='left', padx=2)

    # Actions
    tk.Button(toolbar, text='↩ Undo', command=undo, bg='#944', fg='white', relief='flat').pack(side='left', padx=2)
    tk.Button(toolbar, text='Clear', command=clear_canvas, bg='#944', fg='white', relief='flat').pack(side='left', padx=2)
    tk.Button(toolbar, text='💾 Save', command=save_drawing, bg='#494', fg='white', relief='flat').pack(side='left', padx=2)

    # Status
    status = tk.Label(toolbar, textvariable=tool, bg='#2d2d2d', fg='#aaa', width=12)
    status.pack(side='right', padx=10)

    # Canvas
    canvas = tk.Canvas(root, width=800, height=550, bg='white', cursor='crosshair')
    canvas.pack(fill='both', expand=True)

    # Drawing state
    start_x = start_y = 0
    current_shape = None

    def on_press(event):
        nonlocal start_x, start_y, current_shape
        start_x, start_y = event.x, event.y
        
        t = tool.get()
        fill = current_color if fill_mode.get() else ''
        
        if t == 'rect':
            current_shape = canvas.create_rectangle(start_x, start_y, start_x, start_y,
                                                     outline=current_color, fill=fill, width=current_size)
        elif t == 'circle':
            current_shape = canvas.create_oval(start_x, start_y, start_x, start_y,
                                                outline=current_color, fill=fill, width=current_size)
        elif t == 'line':
            current_shape = canvas.create_line(start_x, start_y, start_x, start_y,
                                                fill=current_color, width=current_size, capstyle='round')
        elif t == 'fill':
            # Flood fill - simplify by filling a large rectangle with transparency trick
            pass
        elif t == 'picker':
            # Simplistic color picker from canvas
            pass
        elif t == 'spray':
            spray_dots(event)
        elif t == 'pen':
            canvas._last_x = event.x
            canvas._last_y = event.y

    def on_drag(event):
        nonlocal current_shape
        t = tool.get()
        
        if t == 'pen' or t == 'eraser':
            x1, y1 = getattr(canvas, '_last_x', event.x), getattr(canvas, '_last_y', event.y)
            color = 'white' if t == 'eraser' else current_color
            item = canvas.create_line(x1, y1, event.x, event.y, fill=color, width=current_size*2,
                                      capstyle='round', smooth=True)
            shapes.append(item)
            canvas._last_x = event.x
            canvas._last_y = event.y
        
        elif t in ('rect', 'circle', 'line') and current_shape:
            canvas.coords(current_shape, start_x, start_y, event.x, event.y)
        
        elif t == 'spray':
            spray_dots(event)

    def on_release(event):
        nonlocal current_shape
        if current_shape:
            if tool.get() in ('rect', 'circle', 'line'):
                shapes.append(current_shape)
            current_shape = None

    def spray_dots(event):
        import random
        for _ in range(current_size * 3):
            rx = event.x + random.randint(-current_size*5, current_size*5)
            ry = event.y + random.randint(-current_size*5, current_size*5)
            item = canvas.create_oval(rx, ry, rx+2, ry+2, fill=current_color, outline='')
            shapes.append(item)

    # Keyboard shortcuts
    def on_key(event):
        if event.keysym == 'z' and event.state & 4:  # Ctrl+Z
            undo()
        elif event.keysym == 's' and event.state & 4:  # Ctrl+S
            save_drawing()
        elif event.keysym == 'Escape':
            clear_canvas()

    canvas.bind('<Button-1>', on_press)
    canvas.bind('<B1-Motion>', on_drag)
    canvas.bind('<ButtonRelease-1>', on_release)
    root.bind('<Key>', on_key)

    root.mainloop()
    return 'DrawClaw canvas closed. Use /canvas to open again.'