"""Drawclaw CLI Interface"""

import os
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.agent import DrawclawAgent

class DrawclawCLI:
    def __init__(self):
        self.agent = DrawclawAgent()
    
    def run(self):
        self._show_header()
        while True:
            try:
                cmd = input("\n🎨 Draw > ").strip()
                if not cmd:
                    continue
                
                if cmd == "/quit":
                    print("Goodbye!")
                    break
                elif cmd == "/clear":
                    os.system('cls')
                    self._show_header()
                elif cmd == "/help":
                    self._show_help()
                elif cmd == "/stats":
                    self._show_stats()
                elif cmd == "/list":
                    self._list_drawings()
                elif cmd.startswith("/plot"):
                    self._plot(cmd[5:].strip())
                elif cmd.startswith("/draw"):
                    self._draw(cmd[5:].strip())
                elif cmd.startswith("/chart"):
                    self._chart(cmd[6:].strip())
                elif cmd.startswith("/diagram"):
                    self._diagram(cmd[8:].strip())
                elif cmd.startswith("/geometry"):
                    self._geometry(cmd[9:].strip())
                elif cmd.startswith("/export"):
                    self._export(cmd[7:].strip())
                elif cmd.startswith("/save"):
                    self._save(cmd[5:].strip())
                else:
                    print("Unknown command. Type /help")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def _show_header(self):
        print("\n" + "="*60)
        print("DRAWCLAW - Complex Drawing & Visualization Agent".center(60))
        print("="*60)
        print("SVG • Matplotlib • Diagrams • Geometry • Charts".center(60))
        print("="*60)
        self._show_help()
    
    def _show_help(self):
        print("""
🎨 DRAWING COMMANDS:
  /plot <function> [range]      - Plot mathematical function
  /draw <type> <specs>          - Draw SVG graphics
  /chart <type> <data>          - Create charts (bar/pie/line/scatter)
  /diagram <type> <elements>    - Draw diagrams (flowchart/network/tree)
  /geometry <shape> <params>    - Draw geometric shapes
  /export <id> <format>         - Export to Docuclaw
  /save <name>                  - Save current drawing
  /list                         - List all drawings
  /stats                        - Session statistics
  /help                         - Show help
  /quit                         - Exit

📐 EXAMPLES:
  /plot sin(x)
  /plot x**2
  /chart bar [10,20,15,30] --labels A,B,C,D
  /chart pie [30,20,50] --labels Red,Blue,Green
  /geometry circle radius=2
  /geometry rectangle width=4 height=3
  /save my_drawing
  /export my_drawing png
""")
    
    def _show_stats(self):
        stats = self.agent.get_stats()
        print(f"\n📊 Session Statistics:")
        print(f"   Total queries: {stats['total_queries']}")
        print(f"   Total drawings: {stats['total_drawings']}")
        if stats.get('recent_drawings'):
            print("   Recent drawings:")
            for d in stats['recent_drawings']:
                print(f"     • {d['name']}")
    
    def _list_drawings(self):
        result = self.agent.list_drawings()
        if result.get("success"):
            drawings = result.get("drawings", [])
            if drawings:
                print(f"\n📁 Saved Drawings ({len(drawings)}):")
                for d in drawings:
                    print(f"   • {d['name']} - {d['filepath']}")
            else:
                print("\n📁 No drawings saved yet.")
        else:
            print(f"\n❌ Error: {result.get('error')}")
    
    def _plot(self, arg):
        """Plot a mathematical function"""
        if not arg:
            print("Usage: /plot <expression> [x_min,x_max]")
            print("Example: /plot sin(x)")
            return
        
        parts = arg.split()
        expression = parts[0]
        x_range = (-10, 10)
        
        if len(parts) > 1:
            range_str = parts[1].strip('[]()')
            if ',' in range_str:
                try:
                    x_range = tuple(map(float, range_str.split(',')))
                except:
                    pass
        
        print(f"\n📈 Plotting: {expression} over {x_range}")
        result = self.agent.plot_function(expression, x_range)
        
        if result.get("success"):
            print(f"✅ Plot created successfully!")
            print(f"   Type: {result.get('type', 'matplotlib')}")
        else:
            print(f"❌ Error: {result.get('error')}")
    
    def _draw(self, arg):
        print("🎨 SVG Drawing - Use /create svg with specifications")
    
    def _chart(self, arg):
        print("📊 Chart Creation - Types: bar, pie, line, scatter")
        print("   Example: /chart bar [10,20,30] --labels A,B,C")
    
    def _diagram(self, arg):
        print("🔷 Diagram Creation - Types: flowchart, network, tree")
    
    def _geometry(self, arg):
        print("📐 Geometry Drawing - Shapes: circle, rectangle, triangle")
        print("   Example: /geometry circle radius=3")
    
    def _export(self, arg):
        parts = arg.split()
        if len(parts) >= 2:
            drawing_id = parts[0]
            format = parts[1]
            result = self.agent.export_to_docuclaw(drawing_id, format)
            if result.get("success"):
                print(f"✅ {result.get('message')}")
            else:
                print(f"❌ Error: {result.get('error')}")
        else:
            print("Usage: /export <drawing_id> <format>")
    
    def _save(self, arg):
        """Save current drawing"""
        if arg:
            print(f"💾 Saving drawing as: {arg}")
            result = self.agent.save_drawing(arg)
            if result.get("success"):
                print(f"✅ Saved to: {result['filepath']}")
            else:
                print(f"❌ Error: {result.get('error')}")
        else:
            print("Usage: /save <name>")
