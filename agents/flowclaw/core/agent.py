"""flowclaw Core Logic"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class flowclawCore:
    """Core processing logic for flowclaw"""
    
    def process(self, query: str) -> str:
        """Process a query"""
        # Original logic from the simple agent
        #!/usr/bin/env python3
import sys

def process_command(cmd):
    cmd = cmd.strip()
    if cmd == "/help":
        return "Commands: /help, /quit, /flowchart test"
    elif cmd == "/quit":
        return ""
    elif cmd:
        return "[flowclaw] Processed: Test-Path 'C:\Program Files\LocalAI'"
    return ""

def main():
    if len(sys.argv) > 1:
        cmd = ' '.join(sys.argv[1:])
        result = process_command(cmd)
        if result:
            print(result)
        return
    
    if not sys.stdin.isatty():
        for line in sys.stdin:
            cmd = line.strip()
            if cmd and cmd != "/quit":
                result = process_command(cmd)
                if result:
                    print(result)
        return
    
    while True:
        try:
            cmd = input("> ").strip()
            if cmd == "/quit":
                break
            if cmd:
                result = process_command(cmd)
                if result:
                    print(result)
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == "__main__":
    main()

        return f"[flowclaw] Processing: {query}"

    def _help(self) -> str:
        return "flowclaw Commands: /help, /stats, /quit"
