#!/usr/bin/env python3
"""Claw - One file to rule them all"""

import sys
import subprocess
from pathlib import Path

AGENTS = {
    "lang": "agents/langclaw/langclaw.py",
    "poly": "agents/interpretclaw/interpretclaw.py",
    "tx": "agents/txclaw/txclaw.py",
    "med": "agents/mediclaw/mediclaw.py",
    "law": "agents/lawclaw/lawclaw.py",
    "math": "agents/mathematicaclaw/mathematicaclaw.py",
    "data": "agents/dataclaw/dataclaw.py",
    "doc": "agents/docuclaw/docuclaw.py",
    "web": "agents/webclaw/webclaw.py",
    "plot": "agents/plotclaw/plotclaw.py",
    "dream": "agents/dreamclaw/dreamclaw.py",
    "flow": "agents/flowclaw/flowclaw.py",
    "draft": "agents/draftclaw/draftclaw.py",
    "design": "agents/designclaw/designclaw.py"
}

def main():
    if len(sys.argv) < 2:
        print("=" * 50)
        print("🦞 CLAW - 14 Agent Ecosystem")
        print("=" * 50)
        print("\nUsage: python claw.py <agent>")
        print("\n🎯 LANGUAGE AGENTS:")
        print("  lang   - Langclaw (Language Teacher)")
        print("  poly   - Polyclaw (Translator)")
        print("\n💼 BUSINESS AGENTS:")
        print("  tx     - TXclaw (Blockchain)")
        print("  med    - Mediclaw (Medical)")
        print("  law    - Lawclaw (Legal)")
        print("\n📐 TECHNICAL AGENTS:")
        print("  math   - Mathematicaclaw (Math)")
        print("  data   - Dataclaw (Data)")
        print("  doc    - Docuclaw (Documents)")
        print("  web    - Webclaw (Web)")
        print("\n🎨 VISUALIZATION AGENTS:")
        print("  plot   - Plotclaw (Charts & Graphs)")
        print("  dream  - Dreamclaw (AI Images)")
        print("  flow   - Flowclaw (Diagrams)")
        print("  draft  - Draftclaw (Technical Drawings)")
        print("  design - Designclaw (Graphic Design)")
        print("\n📖 Example: python claw.py plot")
        return
    
    agent = sys.argv[1].lower()
    
    if agent not in AGENTS:
        print(f"❌ Unknown: {agent}")
        return
    
    path = AGENTS[agent]
    if not Path(path).exists():
        print(f"❌ Agent not found: {path}")
        return
    
    print(f"🦞 Starting {agent}...\n")
    subprocess.run([sys.executable, path])

if __name__ == "__main__":
    main()
