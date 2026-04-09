#!/usr/bin/env python3
"""Mathematicaclaw - Mathematical Computation AI Agent"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from cli.interface import MathematicaclawCLI

def main():
    cli = MathematicaclawCLI()
    cli.run()

if __name__ == "__main__":
    main()
