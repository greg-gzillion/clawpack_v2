#!/usr/bin/env python3
"""Claw - Dynamic Agent Launcher (Auto-discovers all agents)"""

import sys
import subprocess
from pathlib import Path

def discover_agents():
    """Auto-discover all agents in the agents/ directory"""
    agents_dir = Path("agents")
    agents = {}
    
    for agent_dir in agents_dir.iterdir():
        if not agent_dir.is_dir():
            continue
        if agent_dir.name.startswith(('_', 'shared', 'langclaw_backup')):
            continue
        
        agent_file = agent_dir / f"{agent_dir.name}.py"
        if agent_file.exists():
            # Use folder name as the command
            name = agent_dir.name.replace('claw', '')
            if not name:
                name = agent_dir.name
            agents[name] = str(agent_file)
    
    return agents

def main():
    AGENTS = discover_agents()
    
    if len(sys.argv) < 2:
        print("=" * 50)
        print("CLAW - Dynamic Agent Launcher")
        print("=" * 50)
        print(f"\nDiscovered {len(AGENTS)} agents:\n")
        
        # Group by category
        categories = {
            "CREATIVE": ["design", "draw", "draft", "dream", "plot", "flow"],
            "DATA": ["data", "math", "web", "docu"],
            "LANGUAGE": ["lang", "interpret"],
            "DOMAIN": ["law", "med", "tx"],
            "SYSTEM": ["liberate", "_coder"]
        }
        
        for category, patterns in categories.items():
            print(f"\n{category}:")
            for name, path in sorted(AGENTS.items()):
                if any(p in name for p in patterns):
                    print(f"  {name:12} -> {Path(path).parent.name}")
        
        print("\n" + "=" * 50)
        print("Usage: python claw.py <agent>")
        print("Example: python claw.py design")
        return

    agent = sys.argv[1].lower()
    
    # Find matching agent
    if agent in AGENTS:
        path = AGENTS[agent]
    else:
        # Try partial match
        matches = [a for a in AGENTS if agent in a]
        if len(matches) == 1:
            path = AGENTS[matches[0]]
            agent = matches[0]
        else:
            print(f"Unknown agent: {agent}")
            print(f"Available: {', '.join(sorted(AGENTS.keys()))}")
            return

    if not Path(path).exists():
        print(f"Agent not found: {path}")
        return

    print(f"Starting {agent}...\n")
    subprocess.run([sys.executable, path])

if __name__ == "__main__":
    main()
