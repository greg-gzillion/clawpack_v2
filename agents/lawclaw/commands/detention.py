"""detention command - Jail/detention facility lookup via Chronicle FTS5"""
import re
from pathlib import Path

name = "/detention"
from agents.lawclaw.commands._memory import show_prior, remember


def run(args, agent=None):
    if not args:
        return "[DETENTION] Usage: /detention [city] [state]\n  /detention Daytona Beach FL"

    out = []
    out.append("")
    out.append("=" * 60)
    out.append(f"DETENTION: {args}")
    out.append("=" * 60)

    prior = show_prior(args, out)

    try:
        # Use Chronicle FTS5 via agent — instant, no LLM needed
        if agent and hasattr(agent, 'lookup_jurisdiction'):
            result = agent.lookup_jurisdiction(args, "all")
            if result.get("police"):
                out.append("\n### Jail/Detention Facilities")
                for line in result["police"]:
                    if any(kw in line.lower() for kw in ["jail", "detention", "correction", "inmate"]):
                        out.append(f"  {line}")
            if result.get("urls"):
                out.append(f"\n### URLs ({len(result['urls'])})")
                for url in result["urls"][:10]:
                    out.append(f"  {url}")
        else:
            out.append("  Agent context not available — cannot look up jurisdiction data")
        
        if len(out) <= 4:  # Only header lines
            out.append(f"  No detention facilities found for {args}")
        
        remember(command="/detention", query=args, result_summary="\n".join(out)[:400],
                 source_type="chronicle", confidence=0.90)
        return "\n".join(out)
    except Exception as e:
        out.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(out)
