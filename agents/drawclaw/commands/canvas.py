"""Canvas command - Interactive drawing window with mouse"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

def run(args):
    try:
        import tkinter as tk
        from tkinter import colorchooser, messagebox
    except:
        return 'Tkinter not available. Windows drawing requires tkinter.'

    root = tk.Tk()
    root.title('DrawClaw - Interactive Canvas')
    root.geometry('900x700')
    
    # Toolbar
    toolbar = tk.Frame(root, height=40, bg='#2d2d2d')
    toolbar.pack(fill='x')
    
    current_color = '#000000'
    current_size = 3
    tool = tk.StringVar(value='pen')
    
    def set_color():
        nonlocal current_color
        c = colorchooser.askcolor(color=current_color)
        if c[1]: current_color = c[1]
    
    def set_size(s):
        nonlocal current_size
        current_size = int(s)
    
    def set_tool(t):
        tool.set(t)
    
    def clear_canvas():
        canvas.delete('all')
    
    def save_drawing():
        from datetime import datetime
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (800, 540), color='white')
        canvas.postscript(file='_temp.ps', colormode='color')
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        path = Path('exports') / f'canvas_{ts}.png'
        try:
            img.save(str(path))
            messagebox.showinfo('Saved', f'Saved: {path.name}')
        except:
            messagebox.showerror('Error', 'Could not save as PNG')
    
    # Buttons
    tk.Button(toolbar, text='Color', command=set_color, bg='#444', fg='white').pack(side='left', padx=2, pady=2)
    tk.Button(toolbar, text='Pen', command=lambda: set_tool('pen'), bg='#444', fg='white').pack(side='left', padx=2)
    tk.Button(toolbar, text='Eraser', command=lambda: set_tool('eraser'), bg='#444', fg='white').pack(side='left', padx=2)
    tk.Scale(toolbar, from_=1, to=10, orient='horizontal', command=set_size, bg='#444', fg='white', length=100).pack(side='left', padx=5)
    tk.Button(toolbar, text='Clear', command=clear_canvas, bg='#944', fg='white').pack(side='left', padx=2)
    tk.Button(toolbar, text='Save', command=save_drawing, bg='#494', fg='white').pack(side='left', padx=2)
    tk.Label(toolbar, textvariable=tool, bg='#2d2d2d', fg='#aaa', width=10).pack(side='right', padx=10)
    
    # Canvas
    canvas = tk.Canvas(root, width=800, height=540, bg='white', cursor='crosshair')
    canvas.pack(fill='both', expand=True)
    
    def on_press(event):
        canvas._last_x = event.x
        canvas._last_y = event.y
    
    def on_drag(event):
        x1, y1 = canvas._last_x, canvas._last_y
        x2, y2 = event.x, event.y
        color = 'white' if tool.get() == 'eraser' else current_color
        canvas.create_line(x1, y1, x2, y2, fill=color, width=current_size, capstyle='round', smooth=True)
        canvas._last_x = x2
        canvas._last_y = y2
    
    canvas.bind('<Button-1>', on_press)
    canvas.bind('<B1-Motion>', on_drag)
    
    root.mainloop()
    return 'DrawClaw canvas closed. Use /canvas to open again.'
