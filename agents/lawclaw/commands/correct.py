# agents/lawclaw/commands/correct.py
"""correct command - Community correction of facts and URLs via consensus engine"""
name = "/correct"

from agents.lawclaw.commands._memory import show_prior, remember


def run(args):
    if not args:
        return (
            "[CORRECT] Usage: /correct <fact_or_url> <corrected_value>\n"
            "  /correct salazar-limon url https://www.oyez.org/cases/2016/15-617\n"
            "  /correct 'Qualified immunity always applies' 'Qualified immunity has exceptions per Harlow v Fitzgerald'\n"
            "\n"
            "Corrections are validated and recorded. Consensus builds truth over time."
        )

    out = []
    out.append("")
    out.append("=" * 60)
    out.append(f"CORRECT: {args[:100]}{'...' if len(args) > 100 else ''}")
    out.append("=" * 60)

    prior = show_prior(args, out)

    try:
        parts = args.split(maxsplit=1)
        if len(parts) < 2:
            out.append("  Usage: /correct <original> <correction>")
            return "\n".join(out)

        original = parts[0].strip()
        correction = parts[1].strip()

        # Detect if this is a URL correction
        is_url_correction = original.startswith("http") or correction.startswith("http")
        is_case_correction = "url" in correction.lower() or any(
            domain in correction.lower()
            for domain in ["courtlistener.com", "oyez.org", "supremecourt.gov", "law.cornell.edu"]
        )

        # Validate: if correcting a URL, verify the new URL resolves
        verified = False
        if correction.startswith("http"):
            out.append("")
            out.append("[VERIFY] Checking corrected URL...")
            try:
                from agents.lawclaw.commands._helpers import webclaw
                html = webclaw(correction)
                if html and len(html) > 100:
                    verified = True
                    out.append(f"  URL verified: {correction[:80]}...")
                else:
                    out.append(f"  WARNING: URL could not be verified. Recording anyway.")
            except Exception as e:
                out.append(f"  WARNING: URL verification failed: {str(e)[:100]}")

        # Record correction in consensus engine
        out.append("")
        out.append("[CONSENSUS] Recording correction...")
        try:
            from shared.consensus_engine import record_correction
            result = record_correction(
                fact_value=original,
                corrected_value=correction,
                corrected_url=correction if correction.startswith("http") else "",
                agent_name="lawclaw",
                reason="user_correction",
            )
            out.append(f"  Correction recorded. New truth score: {result.get('truth_score', 'N/A')}")
            out.append(f"  Confirmations: {len(result.get('confirmations', []))}")
        except Exception as e:
            out.append(f"  Error recording correction: {str(e)[:200]}")
            return "\n".join(out)

        # Learn the anti-pattern if this is a recurring correction
        try:
            from shared.memory.procedural_memory import get_memory
            mem = get_memory("lawclaw")
            if is_case_correction:
                mem.add_rule(
                    content=f"Verify case URLs against multiple sources. CourtListener URLs may need Oyez fallback.",
                    category="url_verification",
                    importance=0.8,
                )
            if verified:
                mem.add_rule(
                    content=f"Prefer {correction[:60]} as verified source for {original[:40]}",
                    category="source_preference",
                    importance=0.7,
                )
        except Exception:
            pass

        # Write to shared memory for cross-command recall
        remember(
            command="/correct",
            query=original[:200],
            result_summary=f"Corrected: {original[:100]} → {correction[:200]}",
            source_type="web_verified" if verified else "memory",
            confidence=0.90 if verified else 0.75,
            metadata={"original": original, "correction": correction, "verified": verified},
        )

        out.append("")
        out.append("=" * 60)
        out.append(f"  Original: {original[:200]}")
        out.append(f"  Corrected: {correction[:200]}")
        if verified:
            out.append(f"  Status: VERIFIED ✓")
        else:
            out.append(f"  Status: RECORDED (pending verification)")
        out.append("")
        out.append("  Corrections build consensus over time.")
        out.append("  Multiple confirmations increase truth score.")
        out.append("=" * 60)

        return "\n".join(out)

    except Exception as e:
        out.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(out)