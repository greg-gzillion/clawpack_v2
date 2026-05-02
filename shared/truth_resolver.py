"""Truth Resolver — Enforced source hierarchy for all agents.

   CONSTITUTIONAL LAW: Not all sources are equal.
   
   WebClaw verified sources > Chronicle references > Agent memory > LLM inference.
   
   This file defines what the system is allowed to believe.
   It is the epistemological constitution of Clawpack V2.
"""
from typing import Dict, List, Optional, Any

TRUTH_PRIORITY = {
    "web_verified": 4,
    "chronicle": 3,
    "memory": 2,
    "inference": 1,
}

def resolve_truth(candidates: List[Dict]) -> Dict[str, Any]:
    """Resolve truth from multiple candidate sources.

    Args:
        candidates: List of dicts with value, source_type, confidence, source
        
    Returns:
        Dict with resolved value, confidence, conflicts, and status
    
    Example:
        candidates = [
            {"value": "Exclusionary rule applies to 4th Amendment",
             "source_type": "web_verified", "confidence": 0.92,
             "source": "law.cornell.edu"},
            {"value": "Exclusionary rule is optional",
             "source_type": "inference", "confidence": 0.4,
             "source": "llm"},
        ]
        result = resolve_truth(candidates)
        # result["resolved"] == "Exclusionary rule applies..."
        # result["status"] == "conflict_detected"
    """
    if not candidates:
        return {
            "resolved": None,
            "confidence": 0,
            "source_type": "none",
            "source": None,
            "conflicts": [],
            "status": "uncertain",
        }

    ranked = sorted(
        candidates,
        key=lambda x: (
            TRUTH_PRIORITY.get(x.get("source_type", "inference"), 0),
            x.get("confidence", 0),
        ),
        reverse=True,
    )

    top = ranked[0]
    conflicts = [
        c for c in ranked[1:]
        if c.get("value") != top.get("value")
    ]

    return {
        "resolved": top.get("value"),
        "confidence": top.get("confidence", 0),
        "source_type": top.get("source_type"),
        "source": top.get("source"),
        "conflicts": conflicts,
        "status": "resolved" if not conflicts else "conflict_detected",
    }


def classify_source(url_or_origin: str) -> str:
    """Classify a source into a truth priority tier."""
    web_domains = [
        "law.cornell.edu", "supremecourt.gov", "justice.gov",
        "nih.gov", "cdc.gov", "who.int", "arxiv.org",
        "github.com", "wikipedia.org",
        "nist.gov", "iso.org", "cisecurity.org", "isaca.org",
        "owasp.org", "gdpr-info.eu", "cvedetails.com", "first.org",
        "eur-lex.europa.eu", "hhs.gov", "aicpa.org",
        # Economic & market intelligence
        "iea.org", "worldbank.org", "imf.org", "oecd.org", "un.org",
        "bls.gov", "bea.gov", "fred.stlouisfed.org", "federalreserve.gov",
        "sec.gov", "eia.gov", "epa.gov", "ftc.gov", "census.gov",
        "irs.gov", "treasury.gov",
    ]
    for domain in web_domains:
        if domain in url_or_origin:
            return "web_verified"
    if "chronicle" in url_or_origin.lower():
        return "chronicle"
    if "memory" in url_or_origin.lower():
        return "memory"
    return "inference"


def merge_with_retriever(retriever_results: List[Dict], 
                         memory_results: List[Dict] = None,
                         llm_inference: str = None,
                         llm_confidence: float = 0.5) -> Dict[str, Any]:
    """Merge results from WebClaw retriever, agent memory, and LLM inference.
    
    This is the primary integration point for BaseAgent.smart_ask().
    """
    candidates = []
    
    for r in (retriever_results or []):
        candidates.append({
            "value": r.get("context", "")[:500],
            "source_type": classify_source(r.get("url", "")),
            "confidence": r.get("final_score", 0.5),
            "source": r.get("url", ""),
        })
    
    for m in (memory_results or []):
        candidates.append({
            "value": m.get("value", ""),
            "source_type": "memory",
            "confidence": 0.6,
            "source": f"memory:{m.get('agent', 'unknown')}",
        })
    
    if llm_inference:
        candidates.append({
            "value": llm_inference,
            "source_type": "inference",
            "confidence": llm_confidence,
            "source": "llm",
        })
    
    return resolve_truth(candidates)


__all__ = [
    "TRUTH_PRIORITY",
    "resolve_truth",
    "classify_source", 
    "merge_with_retriever",
]