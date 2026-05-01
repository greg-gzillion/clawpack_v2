#!/usr/bin/env python3
"""FlowClaw - Complete Edition with All Features"""

import sys
import webbrowser
import tempfile
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

class FlowClawComplete:
    def __init__(self):
        self.output_path = Path(__file__).parent / "output"
        self.output_path.mkdir(exist_ok=True)
        self._init_llm()
    
    # ============================================
    # FEATURE 1: LLM INTEGRATION
    # ============================================
    def _init_llm(self):
        try:
            from shared.llm import get_llm_client
            self.llm = get_llm_manager()
            print("🤖 LLM Connected - AI-powered diagrams available", file=sys.stderr)
        except:
            self.llm = None
            print("⚠️ LLM not available - using templates", file=sys.stderr)
    
    def generate_with_ai(self, description):
        """Generate diagram using AI"""
        if self.llm:
            prompt = f"""Create a Mermaid flowchart for: {description}
Use flowchart TD syntax. Include decision points.
Output ONLY the Mermaid code."""
            try:
                code = self.llm.chat_sync(prompt, task_type="diagram")
                if code and len(code) > 20:
                    return code
            except:
                pass
        return None
    
    # ============================================
    # FEATURE 2: MORE TEMPLATES
    # ============================================
    def get_template(self, template_name, custom_desc=""):
        templates = {
            'login': '''flowchart TD
    A[Start] --> B[Enter Email]
    B --> C[Enter Password]
    C --> D{Valid Credentials?}
    D -->|Yes| E[Dashboard]
    D -->|No| F[Show Error]
    F --> B
    E --> G[Welcome]''',
    
            'decision': '''flowchart TD
    A[Start] --> B{Make Choice}
    B -->|Option 1| C[Path 1]
    B -->|Option 2| D[Path 2]
    B -->|Option 3| E[Path 3]
    C --> F[End]
    D --> F
    E --> F''',
    
            'user_journey': '''journey
    title User Journey
    section Research
      Visit site: 5: User
      Compare products: 3: User
    section Decision
      Select item: 5: User
      Add to cart: 4: User
    section Purchase
      Checkout: 5: User
      Payment: 5: User
      Complete: 5: User''',
    
            'gantt': f'''gantt
    title {custom_desc if custom_desc else "Project Timeline"}
    dateFormat YYYY-MM-DD
    section Planning
    Research :a1, 2024-01-01, 7d
    Design :after a1, 5d
    section Development
    Coding :2024-01-15, 14d
    Testing :2024-01-29, 7d
    section Deployment
    Launch :2024-02-05, 3d
    Monitoring :2024-02-08, 5d''',
    
            'sequence': '''sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Database
    
    User->>Frontend: Click Login
    Frontend->>API: POST /login
    API->>Database: Query user
    Database-->>API: User data
    API-->>Frontend: Auth token
    Frontend-->>User: Redirect to dashboard''',
    
            'architecture': '''flowchart TB
    subgraph Frontend
        A[React App]
        B[State Management]
    end
    subgraph Backend
        C[API Gateway]
        D[Microservices]
        E[Message Queue]
    end
    subgraph Data
        F[(Database)]
        G[(Cache)]
        H[Object Storage]
    end
    A --> C
    B --> C
    C --> D
    D --> F
    D --> G
    D --> H
    E --> D''',
    
            'mindmap': '''mindmap
    root((Project))
        Planning
            Requirements
            Timeline
            Resources
        Development
            Frontend
            Backend
            Database
        Testing
            Unit Tests
            Integration
            QA
        Deployment
            Staging
            Production
            Monitoring''',
    
            'git': '''gitGraph
    commit id: "Initial commit"
    branch develop
    checkout develop
    commit id: "Add feature"
    checkout main
    merge develop
    commit id: "Release v1.0"
    branch hotfix
    checkout hotfix
    commit id: "Fix bug"
    checkout main
    merge hotfix
    commit id: "Release v1.1"''',
    
            'pie': '''pie title Project Status
    "Completed" : 45
    "In Progress" : 35
    "Not Started" : 15
    "Blocked" : 5''',
    
            'state': '''stateDiagram-v2
    [*] --> Draft
    Draft --> Review : Submit
    Review --> Draft : Changes Needed
    Review --> Approved : Approve
    Approved --> Published : Publish
    Published --> [*]''',
    
            'class': '''classDiagram
    class User {
        +String name
        +String email
        +login()
        +logout()
    }
    class Order {
        +int id
        +Date date
        +process()
    }
    class Product {
        +String name
        +float price
        +getDetails()
    }
    User "1" -- "*" Order
    Order "*" -- "*" Product''',
    
            'er': '''erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : includes
    CUSTOMER {
        int id PK
        string name
        string email
    }
    ORDER {
        int id PK
        date order_date
        string status
    }
    PRODUCT {
        int id PK
        string name
        float price
    }'''
        }
        return templates.get(template_name, templates['login'])
    
    # ============================================
    # FEATURE 3: EXPORT TO PNG/PDF
    # ============================================
    def export_to_png(self, code, output_path):
        """Save diagram as PNG (via HTML)"""
        html = f'''<!DOCTYPE html>
<html><head><title>Export</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
</head><body><pre class="mermaid">{code}</pre>
<script>
mermaid.initialize({{startOnLoad:true}});
setTimeout(() => {{
    const svg = document.querySelector('svg');
    if(svg) {{
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const data = new XMLSerializer().serializeToString(svg);
        const img = new Image();
        img.onload = () => {{
            canvas.width = img.width * 2;
            canvas.height = img.height * 2;
            ctx.scale(2, 2);
            ctx.drawImage(img, 0, 0);
            const link = document.createElement('a');
            link.download = 'diagram.png';
            link.href = canvas.toDataURL();
            link.click();
        }};
        img.src = 'data:image/svg+xml;base64,' + btoa(data);
    }}
}}, 1000);
</script></body></html>'''
        temp_file = self.output_path / "temp_export.html"
        temp_file.write_text(html)
        webbrowser.open(f'file://{temp_file}')
        return f"PNG export opened in browser - save manually"
    
    # ============================================
    # FEATURE 4: CUSTOM DESCRIPTIONS
    # ============================================
    def generate_custom(self, description):
        """Generate custom diagram from description"""
        # Try AI first
        ai_code = self.generate_with_ai(description)
        if ai_code:
            return ai_code
        
        # Fallback to template-based generation
        words = description.lower().split()
        if 'login' in description.lower() or 'auth' in description.lower():
            return self.get_template('login')
        elif 'decision' in description.lower():
            return self.get_template('decision')
        elif 'timeline' in description.lower() or 'project' in description.lower():
            return self.get_template('gantt', description)
        elif 'architecture' in description.lower() or 'cloud' in description.lower():
            return self.get_template('architecture')
        else:
            # Generic flowchart
            steps = [f"Step {i+1}" for i in range(4)]
            return f'''flowchart TD
    A[Start: {description}]
    B[{steps[0]}]
    C{{Decision?}}
    D[{steps[1]}]
    E[{steps[2]}]
    F[End]
    A --> B --> C
    C -->|Yes| D --> F
    C -->|No| E --> F'''
    
    # ============================================
    # RENDERER
    # ============================================
    def render(self, code, title):
        html = f'''<!DOCTYPE html>
<html>
<head>
    <title>{title} - FlowClaw</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
        }}
        .header h1 {{ margin: 0; font-size: 24px; }}
        .diagram-container {{
            padding: 40px;
            background: #f8f9fa;
            text-align: center;
            min-height: 500px;
        }}
        .toolbar {{
            padding: 15px 30px;
            background: white;
            border-top: 1px solid #e0e0e0;
            text-align: center;
        }}
        button {{
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            margin: 0 5px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
        }}
        button:hover {{ background: #5a67d8; transform: translateY(-2px); }}
        .btn-success {{ background: #28a745; }}
        .btn-success:hover {{ background: #218838; }}
        .mermaid {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            display: inline-block;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .footer {{
            padding: 15px;
            background: #f8f9fa;
            text-align: center;
            font-size: 12px;
            color: #666;
        }}
        select {{
            padding: 8px;
            margin: 0 5px;
            border-radius: 6px;
            border: 1px solid #ddd;
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🎨 {title}</h1>
        <p>FlowClaw Complete Edition</p>
    </div>
    <div class="diagram-container">
        <pre class="mermaid">
{code}
        </pre>
    </div>
    <div class="toolbar">
        <button onclick="copyCode()">📋 Copy Code</button>
        <button onclick="saveAsPNG()">📸 Save PNG</button>
        <button onclick="window.print()">🖨️ Print / PDF</button>
        <button onclick="downloadMMD()">💾 Download .mmd</button>
        <button onclick="location.reload()">🔄 Refresh</button>
    </div>
    <div class="footer">
        🤖 AI-Powered | 📊 15+ Templates | 📸 PNG Export | 🎨 Custom Generation
    </div>
</div>
<script>
    mermaid.initialize({{
        startOnLoad: true,
        theme: 'base',
        themeVariables: {{
            'primaryColor': '#667eea',
            'primaryBorderColor': '#764ba2',
        }},
        flowchart: {{ useMaxWidth: true, htmlLabels: true }},
        securityLevel: 'loose'
    }});
    
    function copyCode() {{
        const code = document.querySelector('.mermaid').textContent;
        navigator.clipboard.writeText(code);
        alert('✅ Code copied!');
    }}
    
    function downloadMMD() {{
        const code = document.querySelector('.mermaid').textContent;
        const blob = new Blob([code], {{type: 'text/plain'}});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'flowclaw_diagram.mmd';
        a.click();
        URL.revokeObjectURL(url);
        alert('✅ File downloaded!');
    }}
    
    async function saveAsPNG() {{
        const svg = document.querySelector('.mermaid svg');
        if (!svg) {{ alert('Wait for diagram to render'); return; }}
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const data = new XMLSerializer().serializeToString(svg);
        const img = new Image();
        img.onload = () => {{
            canvas.width = img.width * 2;
            canvas.height = img.height * 2;
            ctx.scale(2, 2);
            ctx.drawImage(img, 0, 0);
            const a = document.createElement('a');
            a.download = 'flowclaw_diagram.png';
            a.href = canvas.toDataURL();
            a.click();
            alert('✅ PNG saved!');
        }};
        img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(data)));
    }}
    
    setTimeout(() => mermaid.contentLoaded(), 100);
</script>
</body>
</html>'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html)
            temp_path = f.name
        
        webbrowser.open(f'file://{temp_path}')
        return temp_path
    
    # ============================================
    # MAIN COMMANDS
    # ============================================
    def view(self, template=None, description=""):
        if template and template in ['login', 'decision', 'user_journey', 'gantt', 'sequence', 'architecture', 'mindmap', 'git', 'pie', 'state', 'class', 'er']:
            code = self.get_template(template, description)
        elif description:
            code = self.generate_custom(description)
        else:
            code = self.get_template('login')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_path / f"diagram_{timestamp}.mmd"
        filename.write_text(code)
        
        self.render(code, f"FlowClaw: {template or 'Custom'}")
        return f"✅ Diagram saved: {filename}\n🌐 Browser opened with diagram"
    
    def list_templates(self):
        templates = ['login', 'decision', 'user_journey', 'gantt', 'sequence', 'architecture', 'mindmap', 'git', 'pie', 'state', 'class', 'er']
        return "Available templates:\n" + "\n".join(f"  • {t}" for t in templates)
    
    def process(self, cmd, *args):
        if cmd == "view":
            template = args[0] if args else None
            description = ' '.join(args[1:]) if len(args) > 1 else ""
            return self.view(template, description)
        elif cmd == "templates":
            return self.list_templates()
        elif cmd == "ai":
            description = ' '.join(args) if args else "process flow"
            code = self.generate_with_ai(description)
            if code:
                self.render(code, f"AI Generated: {description}")
                return "✅ AI-generated diagram opened in browser"
            return "❌ AI not available - using template"
        else:
            return self.help()
    
    def help(self):
        return """
🎨 FLOWCLAW - COMPLETE EDITION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FEATURES:
  ✓ 12+ Built-in Templates
  ✓ AI-Powered Generation (when LLM available)
  ✓ PNG Export (high resolution)
  ✓ Custom Description Generation
  ✓ Local Rendering in Browser

COMMANDS:
  view <template>           - Use a template
  view custom "<desc>"      - Generate from description
  ai "<description>"        - Use AI generation
  templates                 - List all templates

TEMPLATES:
  login, decision, user_journey, gantt, sequence
  architecture, mindmap, git, pie, state, class, er

EXAMPLES:
  python flowclaw_complete.py view login
  python flowclaw_complete.py view gantt "My Project"
  python flowclaw_complete.py view custom "user registration flow"
  python flowclaw_complete.py ai "e-commerce checkout process"
  python flowclaw_complete.py templates

OUTPUT: Browser popup with rendered diagram + Save as PNG/PDF/MMD
"""

def main():
    agent = FlowClawComplete()
    if len(sys.argv) < 2:
        print(agent.help())
        return
    result = agent.process(sys.argv[1], *sys.argv[2:])
    print(result)

if __name__ == "__main__":
    main()
