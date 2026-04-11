"""LLM Wrapper - re-export from project root"""
import sys
import os
from pathlib import Path

# Get project root (clawpack_v2 directory)
# This file is at: clawpack_v2/agents/langclaw/core/llm_wrapper.py
# Go up 4 levels to reach project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

# Add to path
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Also add the core directory
core_path = PROJECT_ROOT / "core"
if str(core_path) not in sys.path:
    sys.path.insert(0, str(core_path))

# Now try to import
try:
    from core.llm_manager import LLMManager
    print(f"✅ LLMManager imported from {core_path}", file=sys.stderr)
except ImportError as e:
    print(f"❌ Import error: {e}", file=sys.stderr)
    # Fallback: try direct import
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "llm_manager", 
        PROJECT_ROOT / "core" / "llm_manager.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    LLMManager = module.LLMManager
    print(f"✅ LLMManager loaded via fallback", file=sys.stderr)

__all__ = ['LLMManager']
