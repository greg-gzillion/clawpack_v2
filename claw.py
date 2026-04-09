#!/usr/bin/env python3
"""Claw - One file to rule them all"""

import sys
import subprocess
from pathlib import Path

AGENTS = {
    "lang": "agents/langclaw/langclaw.py",
    "tx": "agents/txclaw/txclaw.py",
    "med": "agents/mediclaw/mediclaw.py",
    "law": "agents/lawclaw/lawclaw.py",
    "math": "agents/mathematicaclaw/mathematicaclaw.py",
    "draw": "agents/drawclaw/drawclaw.py",
    "data": "agents/dataclaw/dataclaw.py",
    "doc": "agents/docuclaw/docuclaw.py",
    "int": "agents/interpretclaw/interpretclaw.py",
    "web": "agents/webclaw/webclaw.py"
}

def main():
    if len(sys.argv) < 2:
        print("=" * 40)
        print("🦞 CLAW")
        print("=" * 40)
        print("\nUsage: python claw.py <agent>")
        print("\nAgents:")
        for name, path in AGENTS.items():
            exists = "✅" if Path(path).exists() else "❌"
            print(f"  {exists} {name}")
        print("\nExample: python claw.py lang")
        return
    
    agent = sys.argv[1].lower()
    
    if agent not in AGENTS:
        print(f"❌ Unknown: {agent}")
        print(f"   Try: {', '.join(AGENTS.keys())}")
        return
    
    path = AGENTS[agent]
    if not Path(path).exists():
        print(f"❌ Agent not found: {path}")
        return
    
    print(f"🦞 Starting {agent}...\n")
    subprocess.run([sys.executable, path])

if __name__ == "__main__":
    main()
