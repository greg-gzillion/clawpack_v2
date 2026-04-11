#!/usr/bin/env python3
"""LLM-Powered LawClaw Research with Chronicle Search"""

import sys
import re
import webbrowser
import urllib.parse
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
REFERENCES_PATH = PROJECT_ROOT / "agents/webclaw/references/lawclaw/jurisdictions"

class LawClawAgent:
    def __init__(self):
        self.name = "lawclaw"
        self.llm_searcher = None
        self._init_llm()
    
    def _init_llm(self):
        try:
            law_search_path = Path(__file__).parent / "law_search"
            if str(law_search_path) not in sys.path:
                sys.path.insert(0, str(law_search_path))
            from llm_searcher import llm_searcher
            self.llm_searcher = llm_searcher
        except Exception as e:
            print(f"⚠️ LLM searcher error: {e}", file=sys.stderr)
    
    def handle(self, cmd: str) -> str:
        cmd = cmd.strip()
        
        if cmd.startswith("/searchcase"):
            return self._searchcase(cmd)
        elif cmd.startswith("/searchindex"):
            # Use split to get the query - everything after the command
            parts = cmd.split(maxsplit=1)
            if len(parts) < 2:
                return "Usage: /searchindex <query>"
            query = parts[1].strip()
            return self._search_index(query)
        elif cmd.startswith("/court"):
            return self._court(cmd)
        elif cmd.startswith("/citation"):
            return self._citation(cmd)
        elif cmd.startswith("/docket"):
            return self._docket(cmd)
        else:
            return self._help()
    
    def _search_index(self, query: str) -> str:
        """Search the chronicle index for LawClaw information"""
        # Remove quotes if present
        query = query.strip().strip('"')
        if not query:
            return "Usage: /searchindex <query>\nExample: /searchindex Clear Creek"
        
        try:
            from shared.chronicle_helper import search_chronicle
            results = search_chronicle(query, 10)
            
            if not results:
                return f"📚 No results found for '{query}' in chronicle index"
            
            output = f"""
╔══════════════════════════════════════════════════════════════════╗
║  CHRONICLE SEARCH: {query}
╚══════════════════════════════════════════════════════════════════╝

📚 Found {len(results)} results:

"""
            for i, r in enumerate(results, 1):
                url = getattr(r, 'url', 'unknown')
                context = getattr(r, 'context', '')[:300]
                source = getattr(r, 'source', 'chronicle')
                output += f"""
{i}. 📄 Source: {source}
   🔗 URL: {url}
   📝 Context: {context}...
"""
            return output
        except Exception as e:
            return f"Search error: {e}"
    
    def _markdown_to_html(self, text: str) -> str:
        """Convert markdown links to HTML links"""
        text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank">\1</a>', text)
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
        text = re.sub(r'(https?://[^\s]+)', r'<a href="\1" target="_blank">\1</a>', text)
        return text
    
    def _court(self, cmd: str) -> str:
        parts = cmd.split()
        if len(parts) < 2:
            return "Usage: /court <STATE> <location>\nExample: /court CO Clear Creek"
        
        state = parts[1].upper()
        location = ' '.join(parts[2:]) if len(parts) > 2 else ""
        
        if not location:
            state_dir = REFERENCES_PATH / state
            if state_dir.exists():
                locations = [d.name for d in state_dir.iterdir() if d.is_dir()]
                if locations:
                    return f"📍 {state} - Available locations:\n" + "\n".join(f"   • {loc}" for loc in sorted(locations)[:20])
            return f"Usage: /court {state} <location>"
        
        state_dir = REFERENCES_PATH / state
        if not state_dir.exists():
            return f"No state directory found for {state}"
        
        found_dir = None
        location_lower = location.lower()
        for d in state_dir.iterdir():
            if d.is_dir() and d.name.lower() == location_lower:
                found_dir = d
                break
        
        if not found_dir:
            locations = [d.name for d in state_dir.iterdir() if d.is_dir()]
            similar = [loc for loc in locations if location_lower in loc.lower()]
            if similar:
                return f"No exact match for '{location}'. Did you mean:\n" + "\n".join(f"   • {s}" for s in similar[:5])
            return f"No location '{location}' found in {state}. Available: {', '.join(locations[:10])}"
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{state} - {found_dir.name} Courts</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f0f2f5; }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        h1 {{ color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
        .court-card {{ background: white; border-radius: 12px; padding: 20px; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .court-card h2 {{ color: #667eea; margin-top: 0; }}
        .court-details {{ line-height: 1.6; }}
        .court-details a {{ color: #667eea; text-decoration: none; }}
        .court-details a:hover {{ text-decoration: underline; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
<div class="container">
    <h1>⚖️ {state} - {found_dir.name} Courts</h1>
"""
        for md in found_dir.glob("*.md"):
            content = md.read_text()
            html_content = self._markdown_to_html(content)
            html += f"""
    <div class="court-card">
        <h2>{md.stem.replace('_', ' ').title()}</h2>
        <div class="court-details">
            {html_content.replace(chr(10), '<br>')}
        </div>
    </div>
"""
        
        html += f"""
    <div class="footer">
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>🦞 Clawpack LawClaw Research System</p>
    </div>
</div>
</body>
</html>"""
        
        output = Path.home() / f".clawpack/court_{state}_{found_dir.name}.html"
        output.parent.mkdir(exist_ok=True)
        output.write_text(html)
        webbrowser.open(f'file://{output}')
        
        return f"📂 Court info for {state} - {found_dir.name}\n🌐 Browser opened with formatted HTML"
    
    def _searchcase(self, cmd: str) -> str:
        query = cmd[11:].strip().strip('"')
        if not query:
            return "Usage: /searchcase \"case name\""
        
        if self.llm_searcher:
            return self.llm_searcher.search_case_law(query)
        
        encoded = urllib.parse.quote(query)
        return f"Search: https://scholar.google.com/scholar?q={encoded}"
    
    def _citation(self, cmd: str) -> str:
        citation = cmd[10:].strip().strip('"')
        if not citation:
            return "Usage: /citation \"123 F.3d 456\""
        
        if self.llm_searcher:
            return self.llm_searcher.search_case_law(f"citation {citation}")
        
        encoded = urllib.parse.quote(citation)
        return f"Citation search: https://scholar.google.com/scholar?q={encoded}"
    
    def _docket(self, cmd: str) -> str:
        docket = cmd[8:].strip().strip('"')
        if not docket:
            return "Usage: /docket <number>"
        
        encoded = urllib.parse.quote(docket)
        return f"Docket search: https://www.courtlistener.com/docket/?q={encoded}"
    
    def _help(self):
        return """
LAWCLAW - LawClaw Research Assistant

COMMANDS:
  /searchindex Clear Creek   - Search chronicle index
  /court CO Clear Creek      - Display court info in browser
  /searchcase "Roe v Wade"   - AI case law analysis
  /citation "123 F.3d 456"   - Citation search
  /docket "1:23-cv-45678"    - Docket search

EXAMPLES:
  /searchindex Clear Creek
  /searchindex Leon County
"""

def main():
    agent = LawClawAgent()
    if len(sys.argv) > 1:
        print(agent.handle(' '.join(sys.argv[1:])))
    else:
        print(agent._help())

if __name__ == "__main__":
    main()
