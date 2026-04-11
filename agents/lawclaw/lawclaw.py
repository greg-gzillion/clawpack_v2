#!/usr/bin/env python3
"""LawClaw - LawClaw Research Assistant (CLI-first)"""

import sys
import urllib.parse
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
REFERENCES_PATH = PROJECT_ROOT / "agents/webclaw/references/lawclaw/jurisdictions"

class LawClawAgent:
    def __init__(self):
        self.name = "lawclaw"
        self.description = "LawClaw research assistant"
    
    def handle(self, cmd: str) -> str:
        cmd = cmd.strip()
        
        if cmd.startswith("/court"):
            return self._court(cmd)
        elif cmd.startswith("/search"):
            return self._search_online(cmd)
        elif cmd.startswith("/help"):
            return self._help()
        else:
            return self._help()
    
    def _court(self, cmd: str) -> str:
        parts = cmd.split()
        if len(parts) < 3:
            return "Usage: /court <STATE> <county>\nExample: /court CO Clear Creek"
        
        state = parts[1].upper()
        location = ' '.join(parts[2:])
        
        state_dir = REFERENCES_PATH / state
        if not state_dir.exists():
            return f"No state directory found for {state}"
        
        # Find county
        found_dir = None
        for d in state_dir.iterdir():
            if d.is_dir() and d.name.lower() == location.lower():
                found_dir = d
                break
        
        if not found_dir:
            return f"No court info found for {state} - {location}"
        
        # Build CLI output
        output = f"""
╔══════════════════════════════════════════════════════════════════╗
║  {state} - {found_dir.name} Courts
╚══════════════════════════════════════════════════════════════════╝
"""
        for md in found_dir.glob("*.md"):
            content = md.read_text()
            court_name = md.stem.replace('_', ' ').title()
            output += f"\n📋 {court_name}\n{'-'*50}\n"
            
            # Extract and format key info
            lines = content.split('\n')
            for line in lines:
                if 'Phone:' in line or 'Address:' in line or 'Hours:' in line or 'Website:' in line:
                    # Make URLs clickable in terminals that support it
                    if 'http' in line:
                        url = line.split(': ', 1)[1]
                        output += f"   {line.split(':')[0]}: \033]8;;{url}\033\\{url}\033]8;;\033\\\n"
                    else:
                        output += f"   {line}\n"
                elif 'Jurisdiction:' in line:
                    output += f"\n   ⚖️ Jurisdiction:\n"
                elif line.strip().startswith('- ') and 'Jurisdiction' not in content[:100]:
                    output += f"      • {line.strip()[2:]}\n"
        
        return output
    
    def _search_online(self, cmd: str) -> str:
        """Search online LawClaw resources"""
        query = cmd[7:].strip()
        if not query:
            return "Usage: /search <law topic>\nExample: /search fourth amendment"
        
        encoded = urllib.parse.quote(query)
        
        # Free legal research resources
        resources = [
            ("Google Scholar", f"https://scholar.google.com/scholar?q={encoded}"),
            ("CourtListener", f"https://www.courtlistener.com/search/?q={encoded}&type=o"),
            ("Cornell LII", f"https://www.law.cornell.edu/search?q={encoded}"),
            ("Justia", f"https://law.justia.com/search?q={encoded}"),
            ("FindLaw", f"https://caselaw.findlaw.com/search?q={encoded}"),
            ("PACER", f"https://pacer.uscourts.gov/search?q={encoded}"),
        ]
        
        output = f"""
╔══════════════════════════════════════════════════════════════════╗
║  LEGAL SEARCH: {query}
╚══════════════════════════════════════════════════════════════════╝

🔍 FREE LEGAL DATABASES (click to search):

"""
        for name, url in resources:
            output += f"  📚 {name}: \033]8;;{url}\033\\{url}\033]8;;\033\\\n"
        
        output += """

💡 These are FREE public law databases - no fees required
💡 Click any URL to open in your browser
💡 Copy and paste if your terminal doesn't support clickable links
"""
        return output
    
    def _help(self):
        return """
╔══════════════════════════════════════════════════════════════════╗
║  LAWCLAW - Legal Research Assistant                              ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  COMMANDS:                                                       ║
║    /court <STATE> <county>  - Display local court info          ║
║    /search <topic>          - Search online legal resources     ║
║                                                                  ║
║  EXAMPLES:                                                       ║
║    /court CO Clear Creek                                        ║
║    /court VA Bedford                                            ║
║    /search fourth amendment                                     ║
║    /search contract law                                         ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝"""

def main():
    agent = LawClawAgent()
    if len(sys.argv) > 1:
        print(agent.handle(' '.join(sys.argv[1:])))
    else:
        print(agent._help())

if __name__ == "__main__":
    main()
