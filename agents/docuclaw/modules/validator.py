"""DocuClaw Source Validator v3.3 - Canonical claim normalization + epistemic adjudication.

v3.3: Canonical claim normalization recognizes semantically identical claims
expressed in different phrasing. URL proximity binding prevents false
authority inheritance. Numeric extraction enables quantitative comparison.

Integrates shared/truth_resolver.py and shared/source_registry.py.
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

SEMANTIC_CATEGORIES = {
    "market_size": ["market", "valued", "size", "worth", "billion", "million", "trillion", "sector"],
    "growth_rate": ["growth", "CAGR", "increase", "rate", "percent", "%", "growing"],
    "revenue": ["revenue", "sales", "income", "earnings"],
    "employment": ["jobs", "employed", "workforce", "labor", "workers"],
    "cost": ["cost", "price", "expense", "spending", "investment"],
    "regulation": ["compliance", "regulatory", "law", "statute", "amendment", "rule"],
}

# Canonical form templates for normalizing claims
CANONICAL_FORMS = {
    "market_size": "market_size:{numeric}",
    "growth_rate": "growth_rate:{numeric}%",
    "revenue": "revenue:{numeric}",
    "employment": "employment:{numeric}",
    "cost": "cost:{numeric}",
}

def _categorize_claim(text):
    """Map a claim to a semantic category."""
    text_lower = text.lower()
    for category, keywords in SEMANTIC_CATEGORIES.items():
        if any(kw in text_lower for kw in keywords):
            return category
    return "other"

def _extract_numeric(text):
    """Extract the first numeric value, scaling for billion/million/thousand."""
    numbers = re.findall(r"[\d,.]+", text)
    for n in numbers:
        try:
            val = float(n.replace(",", ""))
            if val > 0:
                t = text.lower()
                if "trillion" in t: val *= 1e12
                elif "billion" in t: val *= 1e9
                elif "million" in t: val *= 1e6
                elif "thousand" in t: val *= 1e3
                return val
        except:
            pass
    return None

def _format_numeric(val):
    """Format a numeric value back to human-readable form for canonical keys."""
    if val is None:
        return "unknown"
    if val >= 1e12:
        return str(round(val / 1e12, 1)) + "T"
    elif val >= 1e9:
        return str(round(val / 1e9, 1)) + "B"
    elif val >= 1e6:
        return str(round(val / 1e6, 1)) + "M"
    else:
        return str(round(val, 1))

def _canonical_form(category, numeric_value):
    """Generate a canonical key for a claim, normalizing different phrasings."""
    if category == "other" or numeric_value is None:
        return None
    template = CANONICAL_FORMS.get(category, "{category}:{numeric}")
    return template.replace("{category}", category).replace("{numeric}", _format_numeric(numeric_value))

def validate_claims(content, domain=None):
    """Scan, adjudicate, and detect conflicts in document claims.

    v3.3: Canonical claim normalization groups semantically identical claims
    expressed in different phrasing. URL proximity binding. Numeric comparison.
    """
    text_lines = content.split(chr(10))
    claims = []
    all_scores = []
    source_map = {}

    for i, line in enumerate(text_lines):
        if len(line) < 20:
            continue

        # Split into assertions at sentence boundaries and contrast markers
        parts = re.split(
            r"(?<=[.!?])\s*(?=[A-Z])|\s*(?:However|however|But|but|Although|although|while|Whereas|whereas)\s+",
            line
        )

        for assertion in parts:
            assertion = assertion.strip()
            if len(assertion) < 20:
                continue

            # Extract URLs from THIS assertion only (proximity binding)
            assertion_urls = []
            for w in assertion.split():
                if w.startswith("http"):
                    assertion_urls.append(w.strip(".,;:()[]{}"))

            # URL proximity: only inherit if assertion names a source
            if not assertion_urls:
                attr_match = re.search(
                    r"(?:according to|per|reported by|study by|data from|citing|pursuant to)\s+(\S+)",
                    assertion.lower()
                )
                if attr_match:
                    ref_name = attr_match.group(1).strip(".,;:()[]")
                    if ref_name:
                        for w in line.split():
                            if w.startswith("http") and ref_name in w.lower():
                                assertion_urls.append(w.strip(".,;:()[]{}"))

            has_indicator = any(ind in assertion.lower() for ind in CLAIM_INDICATORS)
            if not has_indicator and not assertion_urls:
                continue

            # Adjudicate URLs
            source_scores = []
            best_source_type = "inference"
            best_priority = 0
            for url in assertion_urls:
                score = get_trust(url, domain)
                tier = classify_trust(score)
                url_type = classify_source(url)
                url_priority = TRUTH_PRIORITY.get(url_type, 0)
                source_scores.append({
                    "url": url, "score": score, "tier": tier, "source_type": url_type
                })
                source_map[url] = {"score": score, "tier": tier, "source_type": url_type}
                all_scores.append(score)
                if url_priority > best_priority:
                    best_source_type = url_type
                    best_priority = url_priority

            if not assertion_urls:
                best_source_type = classify_source(assertion)

            avg_source_score = (
                sum(s["score"] for s in source_scores) / len(source_scores)
                if source_scores else 0.0
            )
            category = _categorize_claim(assertion)
            numeric_value = _extract_numeric(assertion)
            canonical = _canonical_form(category, numeric_value)

            claims.append({
                "line": i + 1,
                "text": assertion[:200],
                "source_type": best_source_type,
                "priority": best_priority,
                "sources": source_scores,
                "has_source": len(assertion_urls) > 0,
                "avg_trust_score": round(avg_source_score, 2),
                "category": category,
                "numeric_value": numeric_value,
                "canonical_form": canonical,
            })

    # Canonical conflict detection
    conflicts = []
    if len(claims) >= 2:
        # Group by canonical form first, then by category
        canonical_groups = {}
        for claim in claims:
            cf = claim.get("canonical_form")
            key = cf if cf else claim.get("category", "other")
            if key not in canonical_groups:
                canonical_groups[key] = []
            canonical_groups[key].append(claim)

        for key, group in canonical_groups.items():
            if len(group) < 2:
                continue

            # Check for numeric conflicts
            has_numeric_conflict = False
            nums = [c.get("numeric_value") for c in group if c.get("numeric_value") is not None]
            if len(nums) >= 2:
                max_val, min_val = max(nums), min(nums)
                if min_val > 0 and (max_val / min_val) > 1.2:
                    has_numeric_conflict = True

            candidates = []
            for claim in group:
                candidates.append({
                    "value": claim["text"][:100],
                    "source_type": claim["source_type"],
                    "confidence": claim["avg_trust_score"] if claim["avg_trust_score"] > 0 else 0.3,
                    "source": claim["sources"][0]["url"] if claim["sources"] else "text",
                })
            resolved = resolve_truth(candidates)
            if resolved["status"] == "conflict_detected" or has_numeric_conflict:
                conflicts.append({
                    "canonical_key": key,
                    "claims": group,
                    "resolution": resolved,
                    "numeric_conflict": has_numeric_conflict,
                })

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
        has_authoritative = any(
            s.get("tier") == "authoritative"
            for c in claims
            for s in c.get("sources", [])
        )
        has_verified = any(
            s.get("tier") in ("authoritative", "verified")
            for c in claims
            for s in c.get("sources", [])
        )
        has_any_source = any(c["has_source"] for c in claims)

        if conflicts:
            level, confidence = "conflict", 0.50
            if has_authoritative:
                recommendation = "EPISTEMIC CONFLICT DETECTED. Authoritative sources prioritized per Truth Resolver hierarchy. Review conflicting claims."
            else:
                recommendation = "EPISTEMIC CONFLICT DETECTED. No authoritative sources present to resolve disagreement. Independent verification required."
        elif has_authoritative:
            level, confidence = "verified", 0.90
            recommendation = "Authoritative primary sources cited. High epistemic confidence. Document grounded in verified institutional knowledge."
        elif has_verified:
            level, confidence = "verified", 0.80
            recommendation = "Verified secondary sources cited. Moderate-to-high confidence. Key claims are source-backed."
        elif avg_trust >= 0.50:
            level, confidence = "moderate", 0.60
            recommendation = "Sources cited but none from authoritative domains. Verify key claims before relying on this document."
        elif has_any_source:
            level, confidence = "weak", 0.40
            recommendation = "Sources detected but trust scores are low. Independent verification strongly recommended."
        else:
            level, confidence = "unverified", 0.25
            recommendation = "Claims detected but no URLs or citations. Treat as unverified inference only."

        trust_summary = {
            "level": level,
            "confidence": confidence,
            "avg_source_trust": round(avg_trust, 2),
            "has_authoritative": has_authoritative,
            "has_verified": has_verified,
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
    """Generate a constitutional trust footer with canonical conflict details."""
    ts = validation_result["trust_summary"]
    sm = validation_result.get("source_map", {})
    conflicts = validation_result.get("conflicts", [])
    nl = chr(10)
    footer = nl + "---" + nl
    footer += "## Constitutional Source Validation" + nl + nl
    footer += "| Metric | Value |" + nl
    footer += "|--------|-------|" + nl
    footer += "| **Trust Level** | " + ts["level"].upper() + " |" + nl
    footer += "| **Confidence** | " + str(int(ts["confidence"] * 100)) + "% |" + nl
    footer += "| **Avg Source Trust** | " + str(ts.get("avg_source_trust", 0)) + " |" + nl
    footer += "| **Claims Analyzed** | " + str(validation_result["claim_count"]) + " |" + nl
    footer += "| **Conflicts Detected** | " + str(ts.get("conflicts_detected", 0)) + " |" + nl
    footer += "| **Authoritative Sources** | " + ("Yes" if ts.get("has_authoritative") else "No") + " |" + nl

    if conflicts:
        footer += nl + "### Epistemic Conflicts" + nl
        for conflict in conflicts:
            res = conflict["resolution"]
            footer += "- **Canonical Key:** " + str(conflict.get("canonical_key", "")) + nl
            footer += "  - Resolved: " + str(res.get("resolved", ""))[:120] + nl
            footer += "  - Source: " + str(res.get("source", "")) + nl
            footer += "  - Numeric Conflict: " + str(conflict.get("numeric_conflict", False)) + nl

    if sm:
        footer += nl + "### Source Authority Map" + nl + nl
        footer += "| Source | Trust | Tier | Classification |" + nl
        footer += "|--------|-------|------|----------------|" + nl
        for url, info in list(sm.items())[:10]:
            short_url = url[:45] + "..." if len(url) > 45 else url
            footer += "| " + short_url + " | " + str(info["score"]) + " | " + info.get("tier", "") + " | " + info.get("source_type", "") + " |" + nl

    footer += nl + ts["recommendation"] + nl
    footer += nl + "*DocuClaw Constitutional Engine v3.3 | Truth: web_verified > chronicle > memory > inference*" + nl
    return footer

__all__ = ["validate_claims", "generate_trust_footer"]