"""unified_memory.py — now delegates to mem0-backed implementation.

The dormant legacy UnifiedMemory is preserved at unified_memory_legacy.py.
This module redirects all imports to the mem0-backed version.

Constitutional note: the mem0 implementation uses infer=False on writes,
so no LLM calls are made (Article I compliant). All exceptions are logged
via log_err (Article VII compliant).
"""
from shared.memory.unified_memory_mem0 import UnifiedMemory, get_memory

__all__ = ["UnifiedMemory", "get_memory"]
