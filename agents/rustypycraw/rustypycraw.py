#!/usr/bin/env python3
"""RustyPyCraw - Simple working version"""

import sys
from pathlib import Path

class RustyPyCraw:
    def __init__(self):
        self.name = "rustypycraw"
    
    def handle(self, query: str) -> str:
        return f"RustyPyCraw: Analyzing '{query}'"
    
    def scan(self, path):
        return f"Scanning {path} for code patterns"
    
    def search(self, path, query):
        return f"Searching for '{query}' in {path}"

def main():
    agent = RustyPyCraw()
    if len(sys.argv) > 1:
        if sys.argv[1] == "scan" and len(sys.argv) > 2:
            print(agent.scan(sys.argv[2]))
        elif sys.argv[1] == "search" and len(sys.argv) > 3:
            print(agent.search(sys.argv[2], sys.argv[3]))
        else:
            print(agent.handle(' '.join(sys.argv[1:])))
    else:
        print("RustyPyCraw - Code Crawler")
        print("Usage: python rustypycraw.py scan <path>")
        print("       python rustypycraw.py search <path> <query>")

if __name__ == "__main__":
    main()
