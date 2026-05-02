"""DocuClaw Source Validator v2 - Constitutional truth adjudication.

Integrates shared/truth_resolver.py and shared/source_registry.py
to provide trust-weighted claim validation with source authority mapping.

v2: Trust scores now drive confidence. Sources are adjudicated, not just detected.
"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from shared.truth_resolver import classify_source, TRUTH_PRIORITY
from shared.source_registry import get_trust, classify_trust

CLAIM_INDICATORS = [
    "according to", "reports", "reported by", "study by", "research from",
    "data from", "source:", "reference:", "citing", "per", "pursuant to",
    "https://", "http://", "www.", ".gov", ".edu", ".org",
    "%", "CAGR", "growth rate", "market size", "valued at",
    "billion", "million", "trillion", "percent",
]

def validate_claims(content, domain=None):
    """Scan document for claims, adjudicate sources, compute trust-weighted confidence.
    
    Returns:
        claims: list of detected claims with trust scores
        trust_summary: overall trust assessment with weighted confidence
        source_map: authority mapping of all sources
    """
    lines = content.split(chr(10))
    claims = []
    all_scores = []
    source_map = {}
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        for ind in CLAIM_INDICATORS:
            if ind in line_lower and len(line) > 20:
                urls = []
                for w in line.split():
                    if w.startswith("http"):
                        urls.append(w.strip(".,;:()[]{}"))
                
                # Adjudicate each source
                source_scores = []
                for url in urls:
                    score = get_trust(url, domain)
                    tier = classify_trust(score)
                    source_scores.append({"url": url, "score": score, "tier": tier})
                    source_map[url] = {"score": score, "tier": tier}
                    all_scores.append(score)
                
                source_type = classify_source(line)
                avg_source_score = sum(s["score"] for s in source_scores) / len(source_scores) if source_scores else 0.3
                
                claims.append({
                    "line": i + 1,
                    "text": line.strip()[:200],
                    "source_type": source_type,
                    "priority": TRUTH_PRIORITY.get(source_type, 0),
                    "sources": source_scores,
                    "has_source": len(urls) > 0,
                    "avg_trust_score": round(avg_source_score, 2),
                })
                break
    
    # Trust-weighted confidence adjudication
    if not claims:
        trust_summary = {
            "level": "unverified",
            "tier": "inference",
            "confidence": 0.3,
            "avg_source_trust": 0.0,
            "recommendation": "WARNING: No verifiable sources or claims detected. Document is LLM-generated content with no epistemic grounding.",
        }
    else:
        avg_trust = sum(all_scores) / len(all_scores) if all_scores else 0.0
        has_authoritative = any(s.get("tier") == "authoritative" for c in claims for s in c.get("sources", []))
        has_verified = any(s.get("tier") in ("authoritative", "verified") for c in claims for s in c.get("sources", []))
        has_any_source = any(c["has_source"] for c in claims)
        
        if avg_trust >= 0.90:
            level, confidence, recommendation = "verified", 0.95, "Multiple authoritative primary sources cited. High epistemic confidence."
        elif avg_trust >= 0.70:
            level, confidence, recommendation = "verified", 0.80, "Verified secondary sources cited. Moderate-to-high confidence."
        elif avg_trust >= 0.50:
            level, confidence, recommendation = "moderate", 0.60, "Sources cited but none from authoritative primary domains. Verify key claims."
        elif has_any_source:
            level, confidence, recommendation = "weak", 0.40, "Sources detected but trust scores are low. Independent verification strongly recommended."
        else:
            level, confidence, recommendation = "unverified", 0.25, "Claims detected but no URLs or citations. Treat as unverified inference."
        
        trust_summary = {
            "level": level,
            "confidence": confidence,
            "avg_source_trust": round(avg_trust, 2),
            "has_authoritative": has_authoritative,
            "has_verified": has_verified,
            "recommendation": recommendation,
        }
    
    return {
        "claims": claims,
        "claim_count": len(claims),
        "trust_summary": trust_summary,
        "source_map": source_map,
    }

def generate_trust_footer(validation_result):
    """Generate a constitutional trust footer with source adjudication details."""
    ts = validation_result["trust_summary"]
    sm = validation_result.get("source_map", {})
    nl = chr(10)
    footer = nl + "---" + nl
    footer += "## Constitutional Source Validation" + nl + nl
    footer += "| Metric | Value |" + nl
    footer += "|--------|-------|" + nl
    footer += "| **Trust Level** | " + ts["level"].upper() + " |" + nl
    footer += "| **Confidence** | " + str(int(ts["confidence"]*100)) + "% |" + nl
    footer += "| **Avg Source Trust** | " + str(ts.get("avg_source_trust", 0)) + " |" + nl
    footer += "| **Claims Analyzed** | " + str(validation_result["claim_count"]) + " |" + nl
    footer += "| **Authoritative Sources** | " + ("Yes" if ts.get("has_authoritative") else "No") + " |" + nl
    
    if sm:
        footer += nl + "### Source Authority Map" + nl + nl
        footer += "| Source | Trust Score | Tier |" + nl
        footer += "|--------|-------------|------|" + nl
        for url, info in list(sm.items())[:10]:
            short_url = url[:60] + "..." if len(url) > 60 else url
            footer += "| " + short_url + " | " + str(info["score"]) + " | " + info["tier"] + " |" + nl
    
    footer += nl + ts["recommendation"] + nl
    footer += nl + "*Validated by DocuClaw Constitutional Engine v2.0*" + nl
    footer += "*Truth: web_verified > chronicle > memory > inference*" + nl
    footer += "*Source Trust: shared/source_registry.py*" + nl
    return footer

__all__ = ["validate_claims", "generate_trust_footer"]