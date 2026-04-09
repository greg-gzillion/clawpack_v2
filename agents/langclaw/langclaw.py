"""Langclaw - Language Learning Agent with TTS/STT"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cli.interface import LangclawCLI

def main():
    cli = LangclawCLI()
    cli.run()

if __name__ == "__main__":
    main()
