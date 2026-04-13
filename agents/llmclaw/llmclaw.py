#!/usr/bin/env python3
"""LLMClaw - Model Management Agent for Clawpack"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.llmclaw.cli.interface import main_menu

if __name__ == "__main__":
    main_menu()
