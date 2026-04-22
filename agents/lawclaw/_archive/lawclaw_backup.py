#!/usr/bin/env python3
"""LawClaw - Pure Logic Legal Agent
Queries WebClaw (31,686+ legal files) via A2A, enhances with LLM.
"""

import sys
import json
import requests
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import modules (with fallbacks)
try:
    from cli.parser import parse_command
except ImportError:
    def parse_command(cmd):
        parts = cmd.strip().split(' ', 1)
        return parts[0].lower(), parts[1] if len(parts) > 1 else ""

try:
    from queries import WebClawQueryBuilder
except ImportError:
    class WebClawQueryBuilder:
        def build(self, cmd, args): return f"{cmd} {args}"

try:
    from synthesis import LegalSynthesizer
except ImportError:
    class LegalSynthesizer:
        def synthesize(self, q, c, ctx=""): return c
        def ask_with_context(self, q, c): return f"Q: {q}"
        def analyze_legal_text(self, t): return f"Analysis: {t[:100]}"
        def is_available(self): return False

try:
    from utils.display import display
except ImportError:
    class Display:
        def banner(self, t, i=""): print(f"\n{t}\n" + "="*50)
    display = Display()

# Configuration
A2A_URL = "http://127.0.0.1:8766/v1/message/webclaw"
TIMEOUT = 30

class LawClaw:
    def __init__(self):
        self.query_builder = WebClawQueryBuilder()
        self.synthesizer = LegalSynthesizer()
        self.history = []
    
    def _call_webclaw(self, query: str) -> str:
        """Call WebClaw A2A endpoint"""
        try:
            payload = {"task": query, "agent": "lawclaw"}
            resp = requests.post(A2A_URL, json=payload, timeout=TIMEOUT)
            
            if resp.status_code == 200:
                data = resp.json()
                return data.get("result", "")
            return f"WebClaw error: {resp.status_code}"
        except requests.exceptions.ConnectionError:
            return "ERROR: WebClaw server not running (port 8766)"
        except Exception as e:
            return f"ERROR: {e}"
    
    def _execute(self, cmd: str, args: str) -> str:
        """Execute a command"""
        query = self.query_builder.build(cmd.replace('/', ''), args)
        raw = self._call_webclaw(query)
        
        if raw.startswith("ERROR"):
            return raw
        
        return self.synthesizer.synthesize(query, raw, f"Command: {cmd} {args}")
    
    def handle(self, cmd_input: str) -> str:
        """Main command handler"""
        if not cmd_input.strip():
            return ""
        
        cmd, args = parse_command(cmd_input)
        self.history.append({"cmd": cmd, "args": args, "time": datetime.now()})
        
        # Commands that use WebClaw + LLM
        webclaw_commands = [
            '/court', '/federal', '/state', '/search', '/cite', '/statute',
            '/precedent', '/docket', '/judge', '/brief', '/jurisdiction',
            '/oral', '/clerk', '/calendar', '/filing', '/fees', '/forms',
            '/contact', '/address', '/hours', '/online', '/efile', '/pacer',
            '/statistics', '/trends', '/landmark', '/news', '/cle',
            '/resources', '/links', '/browse', '/list'
        ]
        
        if cmd in webclaw_commands:
            return self._execute(cmd, args)
        
        # Special commands
        if cmd == '/ask':
            raw = self._call_webclaw(args)
            return self.synthesizer.ask_with_context(args, raw)
        
        if cmd == '/analyze':
            return self.synthesizer.analyze_legal_text(args)
        
        if cmd == '/stats':
            return self._stats()
        
        if cmd == '/help':
            return self._help()
        
        return f"Unknown: {cmd}\nType /help for commands"
    
    def _stats(self) -> str:
        return f"""
📊 LAWCLAW STATS
========================================
Queries this session: {len(self.history)}
WebClaw references: 31,686+ legal files
LLM Available: {'Yes' if self.synthesizer.is_available() else 'No'}
A2A Server: http://127.0.0.1:8766
========================================
"""
    
    def _help(self) -> str:
        return """
╔══════════════════════════════════════════════════════════════════╗
║                    ⚖️ LAWCLAW COMMANDS ⚖️                        ║
╠══════════════════════════════════════════════════════════════════╣
║ COURT RESEARCH:                                                  ║
║   /court <state> <county>  - County court info                  ║
║   /federal [circuit]       - Federal courts                     ║
║   /state <state>           - State court overview               ║
║   /browse <state>          - Browse state courts                ║
╠══════════════════════════════════════════════════════════════════╣
║ LEGAL RESEARCH:                                                  ║
║   /search <query>          - Search legal topics                ║
║   /ask <question>          - AI legal Q&A                       ║
║   /cite <citation>         - Parse citation                     ║
║   /statute <statute>       - Look up statute                    ║
║   /precedent <case>        - Find precedents                    ║
╠══════════════════════════════════════════════════════════════════╣
║ CASE INFO:                                                       ║
║   /docket <number>         - Court docket                       ║
║   /judge <name>            - Judge info                         ║
║   /brief <case>            - Legal briefs                       ║
║   /oral <case>             - Oral arguments                     ║
║   /analyze <text>          - Analyze legal text                 ║
╠══════════════════════════════════════════════════════════════════╣
║ ADMINISTRATION:                                                  ║
║   /clerk, /calendar, /filing, /fees, /forms                     ║
║   /contact, /address, /hours, /online, /efile, /pacer           ║
╠══════════════════════════════════════════════════════════════════╣
║ SYSTEM:                                                          ║
║   /stats                   - Statistics                         ║
║   /help                    - This help                          ║
║   /quit                    - Exit                               ║
╚══════════════════════════════════════════════════════════════════╝
"""
    
    def run(self):
        """Interactive mode"""
        display.banner("LAWCLAW - AI Legal Research", "⚖️")
        print("Connected to WebClaw: 31,686+ legal files")
        print("LLM: " + ("Available" if self.synthesizer.is_available() else "Unavailable"))
        print("\nType /help for commands, /quit to exit\n")
        
        while True:
            try:
                cmd = input("⚖️ lawclaw> ").strip()
                if cmd.lower() in ['/quit', '/exit', 'quit']:
                    print("Goodbye!")
                    break
                if cmd:
                    print("\n" + self.handle(cmd) + "\n")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}\n")

def main():
    LawClaw().run()

if __name__ == "__main__":
    main()

