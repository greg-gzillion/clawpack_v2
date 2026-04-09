"""API Provider for TXclaw - Handles LLM calls"""

import sys
import os
from pathlib import Path

# Get the absolute path to clawpack_v2 root
current_file = Path(__file__).resolve()
txclaw_dir = current_file.parent.parent  # agents/TXclaw
agents_dir = txclaw_dir.parent  # agents
root_dir = agents_dir.parent  # clawpack_v2

# Add root to Python path
sys.path.insert(0, str(root_dir))

# Try multiple import strategies
call = None

# Strategy 1: Direct import from shared.llm.api
try:
    from shared.llm.api import call
    print("✓ Using shared.llm.api")
except ImportError as e:
    print(f"Strategy 1 failed: {e}")

# Strategy 2: Import from llm.api (if shared is in path)
if call is None:
    try:
        sys.path.insert(0, str(root_dir / "shared"))
        from llm.api import call
        print("✓ Using llm.api")
    except ImportError as e:
        print(f"Strategy 2 failed: {e}")

# Strategy 3: Mock API (fallback)
if call is None:
    print("⚠️ No LLM API found - using fallback mode")
    def call(prompt, model=None):
        return f"[FALLBACK] TXclaw running without API.\nQuery: {prompt[:200]}..."

from config.settings import DEFAULT_MODEL

def api_call(prompt: str, model: str = None) -> str:
    """Make API call through shared LLM module"""
    model = model or DEFAULT_MODEL
    try:
        response = call(prompt, model=model)
        return response if response else "Unable to get response from API."
    except Exception as e:
        return f"API Error: {str(e)}"

def quick_call(prompt: str) -> str:
    """Simplified API call for common queries"""
    return api_call(prompt)
