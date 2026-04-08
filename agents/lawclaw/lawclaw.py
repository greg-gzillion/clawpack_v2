#!/usr/bin/env python3
"""LAWCLAW - Judicial Research System using WebClaw for web requests"""

import sys
import os
import json
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path
import requests

ROOT_DIR = Path(r"C:\Users\greg\dev\clawpack_v2")
SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"
LAW_REFS = ROOT_DIR / "agents" / "webclaw" / "references" / "lawclaw"

# Load API key
env_path = ROOT_DIR / ".env"
if env_path.exists():
    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                os.environ[k] = v

WEBCLAW_URL = "http://localhost:5000"

def fetch_via_webclaw(url):
    """Fetch URL content using WebClaw API"""
    try:
        response = requests.get(f"{WEBCLAW_URL}/fetch", params={"url": url}, timeout=30)
        if response.status_code == 200:
            return response.json().get("content", "")
    except:
        pass
    return None

class LawClaw:
    def __init__(self):
        self.init_db()
        self.print_welcome()

    def init_db(self):
        SHARED_DB.parent.mkdir(exist_ok=True)
        conn = sqlite3.connect(str(SHARED_DB))
        conn.execute('''CREATE TABLE IF NOT EXISTS law_memory 
                        (id INTEGER PRIMARY KEY, query TEXT UNIQUE, 
                         response TEXT, timestamp TEXT)''')
        conn.close()

    def print_welcome(self):
        print("\n" + "█"*80)
        print("█" + " "*78 + "█")
        print("█" + " "*18 + "⚖️  LAWCLAW - JUDICIAL RESEARCH  ⚖️" + " "*18 + "█")
        print("█" + " "*78 + "█")
        print("█"*80)
        self.print_help()

    def print_help(self):
        print("\n" + "="*50)
        print("COMMANDS")
        print("="*50)
        print("  /stats     - System info")
        print("  /list      - Available states")
        print("  /search    - Search law references (uses WebClaw)")
        print("  /browse    - Browse state courts")
        print("  /court     - Court details")
        print("  /ask       - Ask AI (via WebClaw)")
        print("  /help      - This menu")
        print("  /quit      - Exit")
        print("\n" + "="*50)

    def run(self):
        while True:
            try:
                cmd = input("\n⚖️ lawclaw> ").strip().lower()
                if not cmd:
                    continue
                if cmd == '/quit':
                    print("Goodbye!")
                    break
                elif cmd == '/help':
                    self.print_help()
                elif cmd == '/stats':
                    self.stats()
                elif cmd == '/list':
                    self.list_states()
                elif cmd.startswith('/search'):
                    self.search(cmd[7:].strip())
                elif cmd.startswith('/browse'):
                    self.browse(cmd[7:].strip().upper())
                elif cmd.startswith('/court'):
                    self.court(cmd[6:].strip().upper())
                elif cmd.startswith('/ask'):
                    self.ask(cmd[4:].strip())
                else:
                    print("Unknown. Type /help")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break

    def stats(self):
        print("\n" + "="*40)
        print("SYSTEM STATS")
        print("="*40)
        api_key = os.environ.get('OPENROUTER_API_KEY')
        print(f"API: {'✅' if api_key else '❌'}")
        print(f"WebClaw: {'✅' if self._check_webclaw() else '❌'}")
        if LAW_REFS.exists():
            files = len(list(LAW_REFS.rglob("*.md")))
            print(f"References: {files} files")
        print("="*40)

    def _check_webclaw(self):
        try:
            r = requests.get(f"{WEBCLAW_URL}/health", timeout=5)
            return r.status_code == 200
        except:
            return False

    def list_states(self):
        juris = LAW_REFS / "jurisdictions"
        if not juris.exists():
            print("No jurisdictions found")
            return
        states = sorted([d.name for d in juris.iterdir() if d.is_dir()])
        print(f"\n{len(states)} states:\n")
        for i, s in enumerate(states, 1):
            print(f"  {s}", end="  ")
            if i % 8 == 0:
                print()
        print()

    def search(self, query):
        if not query:
            print("Usage: /search [term]")
            return
        print(f"\nSearching: {query}\n")
        results = []
        for md in LAW_REFS.rglob("*.md"):
            try:
                content = md.read_text(encoding='utf-8', errors='ignore')
                if query.lower() in content.lower():
                    results.append(md)
                    if len(results) >= 5:
                        break
            except:
                pass
        if results:
            for r in results:
                print(f"  📄 {r.name}")
                # Extract URLs from the file
                content = r.read_text(encoding='utf-8', errors='ignore')
                import re
                urls = re.findall(r'https?://[^\s\)\]>]+', content)
                if urls:
                    print(f"     🔗 {urls[0]}")
        else:
            print("  No results found")
        print("\n💡 Use /ask for AI-powered legal research")

    def browse(self, state):
        if not state:
            print("Usage: /browse TX")
            return
        state_path = LAW_REFS / "jurisdictions" / state
        if not state_path.exists():
            print(f"State '{state}' not found")
            return
        counties = [d.name for d in state_path.iterdir() if d.is_dir()]
        print(f"\n{state} - {len(counties)} counties:\n")
        for i, c in enumerate(counties[:20], 1):
            print(f"  {i}. {c}")
        if len(counties) > 20:
            print(f"  ... and {len(counties)-20} more")

    def court(self, location):
        if not location or '/' not in location:
            print("Usage: /court TX/DALLAS")
            return
        state, county = location.split('/', 1)
        county_path = LAW_REFS / "jurisdictions" / state / county
        if not county_path.exists():
            # Try case-insensitive
            state_path = LAW_REFS / "jurisdictions" / state
            for d in state_path.iterdir():
                if d.is_dir() and d.name.upper() == county.upper():
                    county_path = d
                    break
        if not county_path or not county_path.exists():
            print(f"County '{county}' not found")
            return
        print(f"\n{county_path.name.upper()} COUNTY, {state}\n")
        for cf in county_path.glob("*.md"):
            name = cf.stem.replace('_', ' ').title()
            print(f"  📌 {name}")

    def ask(self, question):
        if not question:
            print("Usage: /ask [your legal question]")
            return
        print(f"\nQuestion: {question}\n")
        if not self._check_webclaw():
            print("⚠️ WebClaw not running. Start it with: python webclaw_agent.py")
            return
        try:
            response = requests.post(f"{WEBCLAW_URL}/llm", json={"question": question}, timeout=60)
            if response.status_code == 200:
                print(response.json().get("response", "No response"))
            else:
                print(f"Error: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    LawClaw().run()
