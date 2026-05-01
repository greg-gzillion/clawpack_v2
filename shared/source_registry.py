"""Source Trust Registry — Centralized authority for source confidence.

   CONSTITUTIONAL LAW: Trust is not distributed. It is governed.
   
   This registry defines which sources the system trusts and at what level.
   Every agent queries this. No agent hardcodes trust.
"""
from typing import Dict, Optional

# =============================================================================
# TRUST REGISTRY — Single source of truth for source confidence
# =============================================================================

TRUST_REGISTRY: Dict[str, float] = {
    # === TIER 1: Authoritative Primary Sources (1.0 - 0.9) ===
    "law.cornell.edu": 1.0,
    "supremecourt.gov": 1.0,
    "justice.gov": 1.0,
    "congress.gov": 1.0,
    "govinfo.gov": 1.0,
    "uscode.house.gov": 1.0,
    "nih.gov": 0.95,
    "cdc.gov": 0.95,
    "fda.gov": 0.95,
    "who.int": 0.95,
    "arxiv.org": 0.90,
    
    # === TIER 2: Verified Secondary Sources (0.85 - 0.7) ===
    "github.com": 0.80,
    "wikipedia.org": 0.75,
    "stackoverflow.com": 0.70,
    "stackexchange.com": 0.70,
    "pypi.org": 0.75,
    "docs.python.org": 0.85,
    "developer.mozilla.org": 0.85,
    
    # === TIER 3: Unverified Sources (0.6 - 0.4) ===
    "medium.com": 0.50,
    "dev.to": 0.45,
    "blogspot.com": 0.40,
    "wordpress.com": 0.40,
    
    # === TIER 4: Low Trust (0.3 - 0.1) ===
    "reddit.com": 0.30,
    "twitter.com": 0.15,
    "x.com": 0.15,
    "facebook.com": 0.15,
    "tiktok.com": 0.10,
    
    # === DEFAULT ===
    "DEFAULT": 0.50,
}

# =============================================================================
# DOMAIN-SPECIFIC OVERRIDES
# =============================================================================

DOMAIN_OVERRIDES: Dict[str, Dict[str, float]] = {
    "medical": {
        "nih.gov": 1.0,
        "cdc.gov": 1.0,
        "fda.gov": 1.0,
        "who.int": 0.98,
        "mayoclinic.org": 0.90,
        "webmd.com": 0.60,
        "DEFAULT": 0.40,
    },
    "legal": {
        "law.cornell.edu": 1.0,
        "supremecourt.gov": 1.0,
        "justice.gov": 1.0,
        "findlaw.com": 0.75,
        "DEFAULT": 0.45,
    },
    "code": {
        "github.com": 0.90,
        "docs.python.org": 0.95,
        "stackoverflow.com": 0.75,
        "DEFAULT": 0.55,
    },
    "math": {
        "arxiv.org": 0.95,
        "wikipedia.org": 0.80,
        "DEFAULT": 0.50,
    },
}

# =============================================================================
# PUBLIC API
# =============================================================================

def get_trust(url: str, domain: str = None) -> float:
    """Get trust level for a source URL.
    
    Args:
        url: The source URL
        domain: Optional domain context (medical, legal, code, math)
        
    Returns:
        Trust score 0.0 - 1.0
    """
    # Check domain overrides first if context provided
    if domain and domain in DOMAIN_OVERRIDES:
        overrides = DOMAIN_OVERRIDES[domain]
        for key, weight in overrides.items():
            if key in url:
                return weight
        return overrides.get("DEFAULT", 0.50)
    
    # Check general registry
    for key, weight in TRUST_REGISTRY.items():
        if key in url:
            return weight
    
    return TRUST_REGISTRY["DEFAULT"]


def classify_trust(score: float) -> str:
    """Classify a trust score into a tier label."""
    if score >= 0.90:
        return "authoritative"
    elif score >= 0.70:
        return "verified"
    elif score >= 0.50:
        return "moderate"
    elif score >= 0.30:
        return "low"
    else:
        return "untrusted"


def list_registry() -> Dict:
    """List all registered sources and their trust levels."""
    return dict(TRUST_REGISTRY)


def add_source(url_fragment: str, trust: float, domain: str = None):
    """Register a new source or update an existing one."""
    if domain and domain in DOMAIN_OVERRIDES:
        DOMAIN_OVERRIDES[domain][url_fragment] = trust
    else:
        TRUST_REGISTRY[url_fragment] = trust


__all__ = [
    "TRUST_REGISTRY", "DOMAIN_OVERRIDES",
    "get_trust", "classify_trust", "list_registry", "add_source",
]