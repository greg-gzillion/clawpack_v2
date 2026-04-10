#!/usr/bin/env python3
"""LawClaw - Reads actual court reference files"""
import sys
from pathlib import Path

def process_command(cmd: str) -> str:
    cmd = cmd.strip()
    
    # Parse /court command
    if cmd.startswith("/court"):
        parts = cmd.split()
        if len(parts) >= 3:
            state = parts[1].upper()
            county = ' '.join(parts[2:])
            
            # Path to the reference files
            ref_path = Path(f"agents/webclaw/references/lawclaw/jurisdictions/{state}/{county}")
            
            if ref_path.exists():
                # Read all .md files in the directory
                output = [f"\n📚 {county} County, {state} Courts:\n"]
                
                for md_file in ref_path.glob("*.md"):
                    content = md_file.read_text(encoding='utf-8', errors='ignore')
                    
                    # Extract court name from filename
                    court_name = md_file.stem.replace('_', ' ').title()
                    output.append(f"\n🏛️ {court_name}:")
                    
                    # Extract URLs and descriptions
                    for line in content.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if 'http' in line:
                                output.append(f"  🔗 {line}")
                            elif len(line) < 200:
                                output.append(f"  📝 {line}")
                
                if len(output) > 2:
                    return '\n'.join(output)
                else:
                    return f"⚠️ No court information found for {county} County"
            else:
                # List available counties
                state_path = Path(f"agents/webclaw/references/lawclaw/jurisdictions/{state}")
                if state_path.exists():
                    counties = [d.name for d in state_path.iterdir() if d.is_dir()]
                    return f"❌ County '{county}' not found.\nAvailable counties in {state}:\n  " + "\n  ".join(sorted(counties)[:20])
                else:
                    return f"❌ State '{state}' not found"
    
    elif cmd == "/list":
        # List available states
        jurisdictions = Path("agents/webclaw/references/lawclaw/jurisdictions")
        states = [d.name for d in jurisdictions.iterdir() if d.is_dir()]
        return "Available states:\n  " + "\n  ".join(sorted(states))
    
    elif cmd == "/help":
        return "Commands: /court <state> <county>, /list, /help, /quit"
    
    else:
        return f"Unknown: {cmd}"

def main():
    if len(sys.argv) > 1:
        cmd = ' '.join(sys.argv[1:])
        print(process_command(cmd))
        return
    
    if not sys.stdin.isatty():
        for line in sys.stdin:
            cmd = line.strip()
            if cmd and cmd != "/quit":
                print(process_command(cmd))
        return
    
    print("\n⚖️ LAWCLAW - Judicial Research")
    print("Commands: /court <state> <county>, /list, /help, /quit")
    
    while True:
        try:
            cmd = input("\n⚖️ > ").strip()
            if cmd == "/quit":
                break
            if cmd:
                print(process_command(cmd))
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == "__main__":
    main()
