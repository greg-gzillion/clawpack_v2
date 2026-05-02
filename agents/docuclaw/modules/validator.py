"""DocuClaw Source Validator v3 - Conflict-aware constitutional truth adjudication.

v3: URL-level source classification, trust-weighted confidence,
epistemic conflict detection via truth_resolver.resolve_truth().
"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from shared.truth_resolver import classify_source, resolve_truth, TRUTH_PRIORITY
from shared.source_registry import get_trust, classify_trust

CLAIM_INDICATORS = [
    "according to", "reports", "reported by", "study by", "research from",
    "data from", "source:", "reference:", "citing", "per", "pursuant to",
    "https://", "http://", "www.", ".gov", ".edu", ".org",
    "%", "CAGR", "growth rate", "market size", "valued at",
    "billion", "million", "trillion", "percent",
]

def validate_claims(content, domain=None):
    """Scan, adjudicate, and detect conflicts in document claims.
    
    v3 features:
    - URL-level source classification (not line-level)
    - Trust-weighted confidence from source_registry
    - Epistemic conflict detection via truth_resolver
    - Source authority map with per-source trust scores
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
                
                # URL-level classification: classify each URL, use strongest
                source_scores = []
                best_source_type = "inference"
                best_priority = 0
                for url in urls:
                    score = get_trust(url, domain)
                    tier = classify_trust(score)
                    url_type = classify_source(url)
                    url_priority = TRUTH_PRIORITY.get(url_type, 0)
                    source_scores.append({"url": url, "score": score, "tier": tier, "source_type": url_type})
                    source_map[url] = {"score": score, "tier": tier, "source_type": url_type}
                    all_scores.append(score)
                    if url_priority > best_priority:
                        best_source_type = url_type
                        best_priority = url_priority
                
                # Fallback: classify the line if no URLs found
                if not urls:
                    best_source_type = classify_source(line)
                
                avg_source_score = sum(s["score"] for s in source_scores) / len(source_scores) if source_scores else 0.0
                
                claims.append({
                    "line": i + 1,
                    "text": line.strip()[:200],
                    "source_type": best_source_type,
                    "priority": best_priority,
                    "sources": source_scores,
                    "has_source": len(urls) > 0,
                    "avg_trust_score": round(avg_source_score, 2),
                })
                break
    
    # Conflict detection via truth_resolver
    conflicts = []
    if len(claims) >= 2:
        # Group claims that make similar assertions (same numeric patterns)
        import re
        numeric_claims = {}
        for claim in claims:
            numbers = re.findall(r"[\d,.]+\s*(?:billion|million|trillion|%|percent)", claim["text"].lower())
            if numbers:
                key = str(sorted(numbers))
                if key not in numeric_claims:
                    numeric_claims[key] = []
                numeric_claims[key].append(claim)
        
        for key, group in numeric_claims.items():
            if len(group) >= 2:
                candidates = []
                for claim in group:
                    candidates.append({
                        "value": claim["text"][:100],
                        "source_type": claim["source_type"],
                        "confidence": claim["avg_trust_score"] if claim["avg_trust_score"] > 0 else 0.3,
                        "source": claim["sources"][0]["url"] if claim["sources"] else "text",
                    })
                resolved = resolve_truth(candidates)
                if resolved["status"] == "conflict_detected":
                    conflicts.append({
                        "claims": group,
                        "resolution": resolved,
                    })
    
    # Trust-weighted confidence adjudication
    if not claims:
        trust_summary = {
            "level": "unverified",
            "tier": "inference",
            "confidence": 0.3,
            "avg_source_trust": 0.0,
            "conflicts_detected": 0,
            "recommendation": "WARNING: No verifiable sources or claims detected. Document is LLM-generated content with no epistemic grounding.",
        }
    else:
        avg_trust = sum(all_scores) / len(all_scores) if all_scores else 0.0
        has_authoritative = any(s.get("tier") == "authoritative" for c in claims for s in c.get("sources", []))
        has_any_source = any(c["has_source"] for c in claims)
        
        if conflicts:
            level, confidence = "conflict", 0.50
            recommendation = "EPISTEMIC CONFLICT DETECTED: Multiple sources disagree. Higher-trust sources have been prioritized per Truth Resolver hierarchy."
        elif avg_trust >= 0.90:
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
            "has_verified": any(s.get("tier") in ("authoritative", "verified") for c in claims for s in c.get("sources", [])),
            "conflicts_detected": len(conflicts),
            "recommendation": recommendation,
        }
    
    return {
        "claims": claims,
        "claim_count": len(claims),
        "conflicts": conflicts,
        "conflict_count": len(conflicts),
        "trust_summary": trust_summary,
        "source_map": source_map,
    }

def generate_trust_footer(validation_result):
    ts = validation_result["trust_summary"]
    sm = validation_result.get("source_map", {})
    conflicts = validation_result.get("conflicts", [])
    nl = chr(10)
    footer = nl + "---" + nl
    footer += "## Constitutional Source Validation" + nl + nl
    footer += "| Metric | Value |" + nl
    footer += "|--------|-------|" + nl
    footer += "| **Trust Level** | " + ts["level"].upper() + " |" + nl
    footer += "| **Confidence** | " + str(int(ts["confidence"]*100)) + "% |" + nl
    footer += "| **Avg Source Trust** | " + str(ts.get("avg_source_trust", 0)) + " |" + nl
    footer += "| **Claims Analyzed** | " + str(validation_result["claim_count"]) + " |" + nl
    footer += "| **Conflicts Detected** | " + str(ts.get("conflicts_detected", 0)) + " |" + nl
    footer += "| **Authoritative Sources** | " + ("Yes" if ts.get("has_authoritative") else "No") + " |" + nl
    
    if conflicts:
        footer += nl + "### Epistemic Conflicts" + nl + nl
        for conflict in conflicts:
            res = conflict["resolution"]
            footer += "- **Resolved:** " + str(res.get("resolved", ""))[:100] + nl
            footer += "  - Source: " + str(res.get("source", "")) + nl
            footer += "  - Confidence: " + str(int(res.get("confidence", 0)*100)) + "%" + nl
            footer += "  - Status: " + res.get("status", "") + nl
    
    if sm:
        footer += nl + "### Source Authority Map" + nl + nl
        footer += "| Source | Trust | Tier | Classification |" + nl
        footer += "|--------|-------|------|----------------|" + nl
        for url, info in list(sm.items())[:10]:
            short_url = url[:50] + "..." if len(url) > 50 else url
            footer += "| " + short_url + " | " + str(info["score"]) + " | " + info.get("tier", "") + " | " + info.get("source_type", "") + " |" + nl
    
    footer += nl + ts["recommendation"] + nl
    footer += nl + "*Validated by DocuClaw Constitutional Engine v3.0*" + nl
    footer += "*Truth: web_verified > chronicle > memory > inference*" + nl
    return footer

__all__ = ["validate_claims", "generate_trust_footer"]