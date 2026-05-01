"""Memory Poisoning Defense — Prevents hallucinations from becoming truth.

   CONSTITUTIONAL LAW: Not all information deserves to be remembered.
   
   - Inference-only facts NEVER persist to unified memory
   - Low-confidence facts (<0.75) NEVER persist
   - Only web_verified and chronicle sources may write to memory
"""
from typing import Dict

MEMORY_WRITE_THRESHOLD = 0.75

ALLOWED_MEMORY_SOURCES = {"web_verified", "chronicle"}

BLOCKED_MEMORY_SOURCES = {"inference", "memory"}


def should_persist(source_type: str, confidence: float) -> bool:
    """Determine if a fact should be written to unified memory.
    
    Args:
        source_type: web_verified, chronicle, memory, inference
        confidence: 0.0 - 1.0
        
    Returns:
        True if the fact is trustworthy enough to remember
    """
    if source_type in BLOCKED_MEMORY_SOURCES:
        return False
    
    if confidence < MEMORY_WRITE_THRESHOLD:
        return False
    
    return source_type in ALLOWED_MEMORY_SOURCES


def sanitize_memory_write(agent: str, fact: str, source_type: str, confidence: float) -> Dict:
    """Check and potentially block a memory write.
    
    Returns dict with allowed, reason.
    """
    if source_type in BLOCKED_MEMORY_SOURCES:
        return {
            "allowed": False,
            "reason": f"Source type '{source_type}' is blocked from memory persistence",
        }
    
    if confidence < MEMORY_WRITE_THRESHOLD:
        return {
            "allowed": False,
            "reason": f"Confidence {confidence} below threshold {MEMORY_WRITE_THRESHOLD}",
        }
    
    return {"allowed": True, "reason": "Passed memory write checks"}


__all__ = ["should_persist", "sanitize_memory_write", "MEMORY_WRITE_THRESHOLD"]