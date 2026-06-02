# shared/consensus_engine.py
"""
Consensus Truth Engine — reputation-based fact verification.

CONSTITUTIONAL LAW: Truth is not declared. It is earned through consensus.

A fact's truth score rises as:
  - Multiple independent sources confirm it (consensus)
  - High-trust sources verify it (source_registry)
  - Multiple agents agree on it (cross-agent consensus)
  - Corrections refine it over time (self-healing)

Formula:
  TRUTH_SCORE = (source_trust * 0.35) + (consensus_count * 0.25) +
                (recency * 0.15) + (verification_count * 0.15) +
                (cross_agent_agreement * 0.10)

The more consensus, the truer it is.
"""
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any


# ── Storage ──────────────────────────────────────────────────────────────────

CONSENSUS_PATH = Path(__file__).resolve().parent.parent / "runtime" / "indexes" / "consensus_index.json"


def _load_consensus() -> Dict:
    """Load the consensus index from disk."""
    if CONSENSUS_PATH.exists():
        try:
            return json.loads(CONSENSUS_PATH.read_text())
        except Exception:
            pass
    return {"facts": {}, "corrections": [], "updated_at": None}


def _save_consensus(data: Dict) -> None:
    """Persist the consensus index."""
    CONSENSUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    CONSENSUS_PATH.write_text(json.dumps(data, indent=2, default=str))


# ── Fact Hashing ─────────────────────────────────────────────────────────────

def _fact_hash(value: str) -> str:
    """Create a stable hash for a fact to track consensus across sources."""
    normalized = value.strip().lower()[:500]
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


# ── Claim Extraction ─────────────────────────────────────────────────────────

def _extract_claims(result: str, args: str = "") -> List[Dict]:
    """
    Extract structured claims from a command result.
    Returns list of {value, url, source_type, confidence} dicts.
    Prevents consensus pollution from raw markdown responses.
    """
    claims = []

    # Extract URLs from the result
    urls = re.findall(r'https?://[^\s\)\]\<\>\"]+', result)

    # Extract case citations (e.g., "Miranda v. Arizona, 384 U.S. 436 (1966)")
    citations = re.findall(
        r'([A-Z][a-z]+(?:\s+v\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)?,?\s+\d+\s+U\.S\.\s+\d+\s*\(\d{4}\))',
        result
    )

    # Extract key legal concepts (lines starting with ** or ##)
    concepts = re.findall(r'(?:\*\*|##)\s*(.+?)(?:\*\*|##)', result)

    # Claim 1: The primary topic/query
    if args:
        claims.append({
            "value": f"query:{args.strip()[:200]}",
            "source_type": "memory",
            "confidence": 0.85,
        })

    # Claim 2: Each case citation found
    for cite in citations[:5]:
        claims.append({
            "value": f"citation:{cite.strip()[:200]}",
            "url": urls[0] if urls else "",
            "source_type": "web_verified",
            "confidence": 0.90,
        })

    # Claim 3: Key concepts extracted
    for concept in concepts[:5]:
        cleaned = concept.strip()[:200]
        if len(cleaned) > 10:
            claims.append({
                "value": f"concept:{cleaned}",
                "source_type": "web_verified",
                "confidence": 0.80,
            })

    # Claim 4: Source URLs as verified endpoints
    for url in urls[:5]:
        claims.append({
            "value": f"source_url:{url}",
            "url": url,
            "source_type": "web_verified",
            "confidence": 0.85,
        })

    # Fallback: if no structured claims extracted, use first 200 chars
    if not claims:
        claims.append({
            "value": result[:200].replace('\n', ' ').strip(),
            "source_type": "web_verified",
            "confidence": 0.80,
        })

    return claims


# ── Scoring ──────────────────────────────────────────────────────────────────

def score_fact(
    fact_value: str,
    source_url: str = "",
    source_type: str = "web_verified",
    agent_name: str = "lawclaw",
    domain: str = "legal",
) -> float:
    """
    Calculate consensus-based truth score for a fact.

    Args:
        fact_value: The fact/claim being evaluated
        source_url: URL where the fact was found
        source_type: web_verified, chronicle, memory, inference
        agent_name: Agent reporting this fact
        domain: Domain context for trust overrides (legal, medical, code, math)

    Returns:
        Truth score 0.0 - 1.0
    """
    fact_id = _fact_hash(fact_value)
    consensus = _load_consensus()

    # ── 1. Source Trust (35%) ──────────────────────────────────────────
    source_trust = 0.5  # default
    try:
        from shared.source_registry import get_trust
        source_trust = get_trust(source_url, domain=domain)
    except Exception:
        pass

    # ── 2. Consensus Count (25%) ────────────────────────────────────────
    fact_entry = consensus["facts"].get(fact_id, {})
    confirmations = fact_entry.get("confirmations", [])
    consensus_count = len(confirmations)

    # Each additional confirmation increases consensus weight
    # 1 confirmation = 0.3, 3 = 0.6, 5 = 0.8, 10+ = 0.95
    consensus_score = min(0.95, 0.3 + (consensus_count * 0.07))

    # ── 3. Recency (15%) ────────────────────────────────────────────────
    last_updated = fact_entry.get("last_updated")
    if last_updated:
        try:
            last_dt = datetime.fromisoformat(last_updated)
            days_ago = (datetime.now(timezone.utc) - last_dt).days
            recency_score = 0.5 ** (days_ago / 90)  # 90-day half-life
        except Exception:
            recency_score = 0.3
    else:
        recency_score = 0.3  # new fact, moderate recency

    # ── 4. Verification Count (15%) ─────────────────────────────────────
    verifications = fact_entry.get("verifications", 0)
    verification_score = min(0.95, verifications * 0.2)

    # ── 5. Cross-Agent Agreement (10%) ──────────────────────────────────
    agents = set(c.get("agent", "") for c in confirmations)
    agents.add(agent_name)
    agent_count = len(agents)
    agreement_score = min(0.95, agent_count * 0.15) if agent_count > 1 else 0.1

    # ── FINAL SCORE ─────────────────────────────────────────────────────
    truth_score = (
        (source_trust * 0.35) +
        (consensus_score * 0.25) +
        (recency_score * 0.15) +
        (verification_score * 0.15) +
        (agreement_score * 0.10)
    )

    return round(min(1.0, truth_score), 4)


# ── Confirmation ─────────────────────────────────────────────────────────────

def record_confirmation(
    fact_value: str,
    source_url: str = "",
    source_type: str = "web_verified",
    agent_name: str = "lawclaw",
    confidence: float = 0.85,
) -> Dict[str, Any]:
    """
    Record that an agent confirmed a fact. Builds consensus over time.

    Returns the updated fact entry with current truth score.
    """
    fact_id = _fact_hash(fact_value)
    consensus = _load_consensus()

    if fact_id not in consensus["facts"]:
        consensus["facts"][fact_id] = {
            "fact_id": fact_id,
            "fact_value": fact_value[:500],
            "confirmations": [],
            "verifications": 0,
            "corrections": [],
            "truth_score": 0.0,
            "first_seen": datetime.now(timezone.utc).isoformat(),
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }

    fact_entry = consensus["facts"][fact_id]

    # Add confirmation
    fact_entry["confirmations"].append({
        "agent": agent_name,
        "source_url": source_url,
        "source_type": source_type,
        "confidence": confidence,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    # Deduplicate confirmations from same agent+source
    seen = set()
    unique_confirmations = []
    for c in fact_entry["confirmations"]:
        key = (c.get("agent"), c.get("source_url"))
        if key not in seen:
            seen.add(key)
            unique_confirmations.append(c)
    fact_entry["confirmations"] = unique_confirmations

    # Increment verification count if from authoritative source
    try:
        from shared.source_registry import get_trust
        trust = get_trust(source_url)
        if trust >= 0.80:
            fact_entry["verifications"] += 1
    except Exception:
        pass

    fact_entry["last_updated"] = datetime.now(timezone.utc).isoformat()

    # Recalculate truth score
    fact_entry["truth_score"] = score_fact(
        fact_value, source_url, source_type, agent_name
    )

    _save_consensus(consensus)
    return fact_entry


# ── Correction ───────────────────────────────────────────────────────────────

def record_correction(
    fact_value: str,
    corrected_value: str,
    corrected_url: str = "",
    agent_name: str = "lawclaw",
    reason: str = "",
) -> Dict[str, Any]:
    """
    Record a correction to a previously confirmed fact.
    The corrected fact gets a fresh consensus entry.
    The original fact is marked as corrected and its truth score decays.
    """
    original_id = _fact_hash(fact_value)
    consensus = _load_consensus()

    # Mark original as corrected
    if original_id in consensus["facts"]:
        original = consensus["facts"][original_id]
        original["corrections"].append({
            "corrected_to": corrected_value[:200],
            "corrected_url": corrected_url,
            "agent": agent_name,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        original["truth_score"] = max(0.1, original.get("truth_score", 0.5) - 0.3)
        original["last_updated"] = datetime.now(timezone.utc).isoformat()

    # Log correction for audit
    consensus["corrections"].append({
        "original_fact": fact_value[:200],
        "corrected_fact": corrected_value[:200],
        "corrected_url": corrected_url,
        "agent": agent_name,
        "reason": reason,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    _save_consensus(consensus)

    # Record the corrected fact as a new consensus entry
    return record_confirmation(
        fact_value=corrected_value,
        source_url=corrected_url,
        source_type="web_verified",
        agent_name=agent_name,
        confidence=0.90,  # corrections start with higher confidence
    )


# ── Query ────────────────────────────────────────────────────────────────────

def get_consensus(fact_value: str) -> Dict[str, Any]:
    """Get the current consensus state for a fact."""
    fact_id = _fact_hash(fact_value)
    consensus = _load_consensus()
    return consensus["facts"].get(fact_id, {
        "fact_id": fact_id,
        "fact_value": fact_value[:200],
        "confirmations": [],
        "verifications": 0,
        "truth_score": 0.0,
    })


def get_high_confidence_facts(min_score: float = 0.7, limit: int = 20) -> List[Dict]:
    """Get facts with truth scores above the threshold."""
    consensus = _load_consensus()
    facts = [
        f for f in consensus["facts"].values()
        if f.get("truth_score", 0) >= min_score
    ]
    facts.sort(key=lambda x: x.get("truth_score", 0), reverse=True)
    return facts[:limit]


def get_recent_corrections(limit: int = 10) -> List[Dict]:
    """Get recent corrections for audit review."""
    consensus = _load_consensus()
    corrections = consensus.get("corrections", [])
    corrections.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return corrections[:limit]


# ── Constitutional Boundary Integration ──────────────────────────────────────

def constitutional_consensus_check(
    result: str,
    args: str = "",
    urls: List[str] = None,
    agent_name: str = "lawclaw",
) -> None:
    """
    Called from the handler's constitutional boundary.
    Normalizes facts before recording — stores structured claims,
    not raw markdown responses. Prevents consensus pollution.
    """
    if not result or len(result) < 50:
        return

    # Extract structured claims instead of dumping raw response
    claims = _extract_claims(result, args)

    # Record each claim as a separate consensus fact
    for claim in claims:
        record_confirmation(
            fact_value=claim["value"],
            source_url=claim.get("url", ""),
            source_type=claim.get("source_type", "web_verified"),
            agent_name=agent_name,
            confidence=claim.get("confidence", 0.85),
        )


__all__ = [
    "score_fact",
    "record_confirmation",
    "record_correction",
    "get_consensus",
    "get_high_confidence_facts",
    "get_recent_corrections",
    "constitutional_consensus_check",
    "_extract_claims",
]