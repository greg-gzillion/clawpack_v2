#!/usr/bin/env python3
"""LLMClaw - Model Management Agent for Clawpack"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def main():
    # If called with arguments from A2A
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        args = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        
        if cmd == "/llm":
            from commands.llm import run
            print(run(args))
            return
        elif cmd == "/list":
            from commands.list import run
            print(run(args))
            return
        elif cmd == "/use":
            from commands.use import run
            print(run(args))
            return
        elif cmd == "/normal":
            from commands.normal import run
            print(run(args))
            return
        elif cmd == "/obliterated":
            from commands.obliterated import run
            print(run(args))
            return
    
    # Otherwise show interactive menu
    from agents.llmclaw.cli.interface import main_menu
    main_menu()

if __name__ == "__main__":
    main()
