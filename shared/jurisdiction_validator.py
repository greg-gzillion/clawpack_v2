# shared/jurisdiction_validator.py
"""Centralized jurisdiction path validation for all agents.
Import this instead of duplicating ALLOWED_STATES across commands."""

import re
from pathlib import Path

# Hardcoded whitelist — single source of truth
ALLOWED_STATES = frozenset({
    "ak","al","ar","az","ca","co","ct","dc","de","fl","ga","hi","ia","id","il","in",
    "ks","ky","la","ma","md","me","mi","mn","mo","ms","mt","nc","nd","ne","nh","nj",
    "nm","nv","ny","oh","ok","or","pa","pr","ri","sc","sd","tn","tx","ut","va","vt",
    "wa","wi","wv","wy"
})

def validate_state(raw: str) -> str | None:
    """Return lowercase 2-letter state code if valid, else None."""
    if not raw:
        return None
    safe = re.sub(r'[^a-zA-Z]', '', str(raw).strip())[:2]
    if len(safe) != 2:
        return None
    if safe.lower() not in ALLOWED_STATES:
        return None
    return safe.lower()

def sanitize_component(raw: str, max_len: int = 80) -> str:
    """Return sanitized path component string."""
    if not raw:
        return ""
    s = str(raw).replace('..', '').replace('\\', '').replace('/', ' ')
    return re.sub(r'[^a-zA-Z0-9\s\-\']', '', s.strip())[:max_len]

def safe_path_join(base: Path, component: str, max_len: int = 80) -> Path | None:
    """Join and resolve a path component under base. Returns None if invalid."""
    safe = sanitize_component(component, max_len)
    if not safe:
        return None
    candidate = (base / safe).resolve()
    try:
        candidate.relative_to(base.resolve())
        return candidate
    except ValueError:
        return None