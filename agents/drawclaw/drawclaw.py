#!/usr/bin/env python3
"""Drawclaw - Complex Drawing and Visualization AI Agent"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from cli.interface import DrawclawCLI

def main():
    cli = DrawclawCLI()
    cli.run()

if __name__ == "__main__":
    main()
