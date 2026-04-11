"""LLM Wrapper - Direct import from project root"""
import sys
from pathlib import Path

# Get project root (clawpack_v2 directory)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Direct import
try:
    from core.llm_manager import get_llm_manager as _get_llm_manager
    LLMManager = _get_llm_manager
except ImportError:
    # Fallback for when running as script
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "llm_manager",
        PROJECT_ROOT / "core" / "llm_manager.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    LLMManager = module.get_llm_manager

def get_llm_manager():
    return LLMManager()
