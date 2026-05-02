"""DocuClaw Source Validator v3.1 - Multi-claim, semantic grouping, authority-tied messaging.

v3.1: Detects multiple claims per line, semantically groups conflicts,
confidence messaging tied to actual source authority, classify_source expanded.
"""
import sys, re
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

# Semantic categories for conflict grouping
SEMANTIC_CATEGORIES = {
    "market_size": ["market", "valued", "size", "worth", "billion", "million", "trillion"],
    "growth_rate": ["growth", "CAGR", "increase", "rate", "percent", "%"],
    "revenue": ["revenue", "sales", "income", "earnings"],
    "employment": ["jobs", "employed", "workforce", "labor", "workers"],
    "cost": ["cost", "price", "expense", "spending", "investment"],
    "regulation": ["compliance", "regulatory", "law", "statute", "amendment", "rule"],
}

def _categorize_claim(text):
    """Map a claim to a semantic category for conflict grouping."""
    text_lower = text.lower()
    for category, keywords in SEMANTIC_CATEGORIES.items():
        if any(kw in text_lower for kw in keywords):
            return category
    return "other"

def validate_claims(content, domain=None):
    """Scan, adjudicate, and detect conflicts in document claims.
    
    v3.1: Multi-claim detection (no early break), semantic grouping,
    authority-tied confidence messaging.
    """
    lines = content.split(chr(10))
    claims = []
    all_scores = []
    source_map = {}
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        # Extract ALL URLs from the line first
        urls = []
        for w in line.split():
            if w.startswith("http"):
                urls.append(w.strip(".,;:()[]{}"))
        
        if not urls and not any(ind in line_lower for ind in CLAIM_INDICATORS if ind not in ("https://", "http://")):
            continue
        
        # Check if line contains claim-like content
        has_claim = len(urls) > 0 or any(ind in line_lower for ind in CLAIM_INDICATORS)
        if not has_claim or len(line) < 20:
            continue
        
        # Adjudicate each URL (URL-level classification)
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
        
        if not urls:
            best_source_type = classify_source(line)
        
        avg_source_score = sum(s["score"] for s in source_scores) / len(source_scores) if source_scores else 0.0
        category = _categorize_claim(line)
        
        claims.append({
            "line": i + 1,
            "text": line.strip()[:200],
            "source_type": best_source_type,
            "priority": best_priority,
            "sources": source_scores,
            "has_source": len(urls) > 0,
            "avg_trust_score": round(avg_source_score, 2),
            "category": category,
        })
    
    # Semantic conflict detection
    conflicts = []
    if len(claims) >= 2:
        category_groups = {}
        for claim in claims:
            cat = claim.get("category", "other")
            if cat not in category_groups:
                category_groups[cat] = []
            category_groups[cat].append(claim)
        
        for cat, group in category_groups.items():
            if cat == "other" or len(group) < 2:
                continue
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
                conflicts.append({"category": cat, "claims": group, "resolution": resolved})
    
    # Authority-tied confidence adjudication
    if not claims:
        trust_summary = {
            "level": "unverified",
            "confidence": 0.3,
            "avg_source_trust": 0.0,
            "has_authoritative": False,
            "conflicts_detected": 0,
            "recommendation": "No verifiable sources detected. Document is LLM-generated with no epistemic grounding.",
        }
    else:
        avg_trust = sum(all_scores) / len(all_scores) if all_scores else 0.0
        has_authoritative = any(s.get("tier") == "authoritative" for c in claims for s in c.get("sources", []))
        has_verified = any(s.get("tier") in ("authoritative", "verified") for c in claims for s in c.get("sources", []))
        has_any_source = any(c["has_source"] for c in claims)
        
        if conflicts:
            level, confidence = "conflict", 0.50
            if has_authoritative:
                recommendation = "EPISTEMIC CONFLICT DETECTED: Multiple sources disagree. Authoritative sources have been prioritized per Truth Resolver hierarchy. Review conflicting claims."
            else:
                recommendation = "EPISTEMIC CONFLICT DETECTED: Multiple sources disagree. No authoritative sources present to resolve. Independent verification required."
        elif has_authoritative:
            level, confidence, recommendation = "verified", 0.90, "Authoritative primary sources cited. High epistemic confidence. Document is grounded in verified institutional knowledge."
        elif has_verified:
            level, confidence, recommendation = "verified", 0.80, "Verified secondary sources cited. Moderate-to-high confidence. Key claims are source-backed."
        elif avg_trust >= 0.50:
            level, confidence, recommendation = "moderate", 0.60, "Sources cited but none from authoritative domains. Verify key claims before relying on this document."
        elif has_any_source:
            level, confidence, recommendation = "weak", 0.40, "Sources detected but trust scores are low. Independent verification strongly recommended."
        else:
            level, confidence, recommendation = "unverified", 0.25, "Claims detected but no URLs or citations. Treat as unverified inference only."
        
        trust_summary = {
            "level": level,
            "confidence": confidence,
            "avg_source_trust": round(avg_trust, 2),
            "has_authoritative": has_authoritative,
            "has_verified": has_verified,
            "conflicts_detected": len(conflicts),
            "recommendation": recommendation,
        }
    
    return {"claims": claims, "claim_count": len(claims), "conflicts": conflicts, "conflict_count": len(conflicts), "trust_summary": trust_summary, "source_map": source_map}

def generate_trust_footer(validation_result):
    ts = validation_result["trust_summary"]
    sm = validation_result.get("source_map", {})
    conflicts = validation_result.get("conflicts", [])
    nl = chr(10)
    footer = nl + "---" + nl + "## Constitutional Source Validation" + nl + nl
    footer += "| Metric | Value |" + nl + "|--------|-------|" + nl
    footer += "| **Trust Level** | " + ts["level"].upper() + " |" + nl
    footer += "| **Confidence** | " + str(int(ts["confidence"]*100)) + "% |" + nl
    footer += "| **Avg Source Trust** | " + str(ts.get("avg_source_trust", 0)) + " |" + nl
    footer += "| **Claims Analyzed** | " + str(validation_result["claim_count"]) + " |" + nl
    footer += "| **Conflicts** | " + str(ts.get("conflicts_detected", 0)) + " |" + nl
    footer += "| **Authoritative** | " + ("Yes" if ts.get("has_authoritative") else "No") + " |" + nl
    if conflicts:
        footer += nl + "### Epistemic Conflicts" + nl
        for conflict in conflicts:
            res = conflict["resolution"]
            footer += "- **Category:** " + conflict.get("category", "") + nl
            footer += "  - Resolved: " + str(res.get("resolved", ""))[:120] + nl
            footer += "  - Source: " + str(res.get("source", "")) + nl
    if sm:
        footer += nl + "### Source Authority Map" + nl + nl
        footer += "| Source | Trust | Tier | Type |" + nl + "|--------|-------|------|------|" + nl
        for url, info in list(sm.items())[:10]:
            short = url[:45] + "..." if len(url) > 45 else url
            footer += "| " + short + " | " + str(info["score"]) + " | " + info.get("tier", "") + " | " + info.get("source_type", "") + " |" + nl
    footer += nl + ts["recommendation"] + nl
    footer += nl + "*DocuClaw Constitutional Engine v3.1 | Truth: web_verified > chronicle > memory > inference*" + nl
    return footer

__all__ = ["validate_claims", "generate_trust_footer"]