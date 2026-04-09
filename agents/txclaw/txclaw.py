"""TXclaw - TX Blockchain Reference Agent"""

import sys
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cli.interface import TXclawCLI

def main():
    """Main entry point for TXclaw"""
    cli = TXclawCLI()
    cli.run()

if __name__ == "__main__":
    main()
