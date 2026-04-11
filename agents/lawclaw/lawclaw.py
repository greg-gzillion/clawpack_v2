#!/usr/bin/env python3
"""LawClaw - LawClaw Research Agent"""
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
            
            ref_path = Path(f"agents/webclaw/references/lawclaw/jurisdictions/{state}/{county}")
            
            if ref_path.exists():
                output = [f"\n📚 {county} County, {state} Courts:\n"]
                for md_file in ref_path.glob("*.md"):
                    content = md_file.read_text(encoding='utf-8', errors='ignore')
                    court_name = md_file.stem.replace('_', ' ').title()
                    output.append(f"\n🏛️ {court_name}:")
                    for line in content.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if 'http' in line:
                                output.append(f"  🔗 {line}")
                            elif len(line) < 200:
                                output.append(f"  📝 {line}")
                return '\n'.join(output) if len(output) > 2 else f"⚠️ No court information found for {county} County"
            else:
                state_path = Path(f"agents/webclaw/references/lawclaw/jurisdictions/{state}")
                if state_path.exists():
                    counties = [d.name for d in state_path.iterdir() if d.is_dir()]
                    return f"❌ County '{county}' not found.\nAvailable counties in {state}:\n  " + "\n  ".join(sorted(counties)[:20])
                else:
                    return f"❌ State '{state}' not found"
    
    # Parse /law command
    elif cmd.startswith("/law "):
        topic = cmd[5:].strip()
        from commands.law import run
        return run(topic)
    
    # Parse /list command
    elif cmd == "/list":
        law_dir = Path("agents/webclaw/references/lawclaw")
        if law_dir.exists():
            topics = [d.name for d in law_dir.iterdir() if d.is_dir() and d.name != "jurisdictions"]
            return "Available law topics:\n  " + "\n  ".join(sorted(topics)[:30])
        return "No law topics found"
    
    # Parse /help command
    elif cmd == "/help":
        return """
⚖️ LAWCLAW COMMANDS:
  /court <state> <county>   - Court information
  /law <topic>              - LawClaw research (contract, criminal, property, etc.)
  /list                     - Available law topics
  /help                     - This help
  /quit                     - Exit
"""
    
    # Parse /quit command
    elif cmd == "/quit":
        return "QUIT"
    
    # Unknown command
    else:
        return f"Unknown: {cmd}. Type /help"

def main():
    if len(sys.argv) > 1:
        print(process_command(' '.join(sys.argv[1:])))
        return
    
    print("\n⚖️ LawClaw Research Agent")
    print("Type /help for commands, /quit to exit\n")
    
    while True:
        try:
            cmd = input("⚖️ > ").strip()
            if not cmd:
                continue
            result = process_command(cmd)
            print(result)
            if result == "QUIT":
                break
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()

    def _search_chronicle(self, query):
        from shared.chronicle_helper import search_chronicle
        results = search_chronicle(query)
        if results:
            return "\n".join([f"  • {r.url}" for r in results[:5]])
        return "  No results found"
