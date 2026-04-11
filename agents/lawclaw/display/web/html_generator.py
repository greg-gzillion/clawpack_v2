"""Generate HTML webpage for court information"""

import webbrowser
from pathlib import Path
from datetime import datetime

class HTMLGenerator:
    def __init__(self):
        self.output_dir = Path.home() / ".clawpack" / "web_output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_court_page(self, jurisdiction: str, location: str, court_data: list) -> Path:
        """Generate HTML page for court information"""
        
        court_cards = ""
        for court in court_data:
            # Make website clickable
            website_html = court.get('website', 'N/A')
            if website_html != 'N/A' and website_html.startswith('http'):
                website_html = f'<a href="{website_html}" target="_blank">{website_html}</a>'
            
            court_cards += f"""
            <div class="court-card">
                <h3>🏛️ {court['name']}</h3>
                <div class="court-details">
                    <p><strong>📞 Phone:</strong> {court.get('phone', 'N/A')}</p>
                    <p><strong>📍 Address:</strong> {court.get('address', 'N/A')}</p>
                    <p><strong>⏰ Hours:</strong> {court.get('hours', 'N/A')}</p>
                    <p><strong>⚖️ Jurisdiction:</strong> <span style="white-space: pre-line;">{court.get('jurisdiction', 'N/A')}</span></p>
                    <p><strong>👨‍⚖️ Presiding Judge:</strong> {court.get('judge', 'N/A')}</p>
                    <p><strong>🌐 Website:</strong> {website_html}</p>
                </div>
            </div>
            """
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Court Information - {jurisdiction} - {location}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 16px;
            margin-bottom: 20px;
            text-align: center;
        }}
        .header h1 {{ font-size: 32px; margin-bottom: 10px; }}
        .court-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .court-card {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        .court-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        .court-card h3 {{
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }}
        .court-details p {{
            margin: 8px 0;
            color: #333;
            line-height: 1.4;
        }}
        .court-details a {{
            color: #667eea;
            text-decoration: none;
        }}
        .court-details a:hover {{
            text-decoration: underline;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #888;
            font-size: 12px;
        }}
        .meta {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 12px;
            margin-top: 20px;
            font-size: 12px;
            color: #666;
            text-align: center;
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>⚖️ {jurisdiction} - {location}</h1>
        <p>Court Information System | Powered by Clawpack</p>
    </div>
    <div class="court-grid">
        {court_cards}
    </div>
    <div class="meta">
        <p>📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>🦞 Clawpack Legal Research System</p>
        <p>💡 Click website links to visit official court pages</p>
    </div>
    <div class="footer">
        <p>© 2026 Clawpack - AI Agent Ecosystem</p>
    </div>
</div>
</body>
</html>"""
        
        html_file = self.output_dir / f"court_{jurisdiction}_{location.replace(' ', '_')}.html"
        html_file.write_text(html)
        return html_file

html_generator = HTMLGenerator()
