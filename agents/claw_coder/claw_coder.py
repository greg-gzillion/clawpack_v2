#!/usr/bin/env python3
"""claw_coder - Universal CLI wrapper"""
import sys
import subprocess
from pathlib import Path

def process_command(cmd: str) -> str:
    """Process a command"""
    cmd = cmd.strip()
    
    if cmd == "/help":
        return "claw_coder Commands: /help, /stats, /quit"
    elif cmd == "/stats":
        return "claw_coder - Ready"
    elif cmd == "/quit":
        return ""
    elif cmd:
        # Try to route to webclaw for search
        try:
            webclaw = Path(__file__).parent.parent / "webclaw" / "webclaw.py"
            if webclaw.exists():
                result = subprocess.run(
                    [sys.executable, str(webclaw), "search", cmd],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                output = result.stdout.strip()
                if output and "No URLs found" not in output:
                    return f"[claw_coder] {output[:500]}"
        except:
            pass
        
        return f"[claw_coder] Processing: {cmd}"
    
    return ""

def main():
    # CLI mode - single command
    if len(sys.argv) > 1:
        cmd = ' '.join(sys.argv[1:])
        result = process_command(cmd)
        if result:
            print(result)
        return
    
    # Piped input mode
    if not sys.stdin.isatty():
        for line in sys.stdin:
            cmd = line.strip()
            if cmd and cmd != "/quit":
                result = process_command(cmd)
                if result:
                    print(result)
        return
    
    # Interactive mode
    print(f"\nclaw_coder - Interactive Mode")
    print("Type /help for commands, /quit to exit")
    
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
