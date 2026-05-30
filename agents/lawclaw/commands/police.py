"""police command - Police department lookup via Chronicle FTS5"""
from pathlib import Path

name = "/police"
from agents.lawclaw.commands._memory import show_prior, remember


def run(args, agent=None):
    if not args:
        return "[POLICE] Usage: /police [city] [state]\n  /police Miami FL"

    out = []
    out.append("")
    out.append("=" * 60)
    out.append(f"POLICE: {args}")
    out.append("=" * 60)

    prior = show_prior(args, out)

    try:
        if agent and hasattr(agent, 'lookup_jurisdiction'):
            result = agent.lookup_jurisdiction(args, "police")
            if result.get("police"):
                out.append(f"\n### Police Department")
                for line in result["police"][:10]:
                    out.append(f"  {line}")
            if result.get("urls"):
                out.append(f"\n### URLs ({len(result['urls'])})")
                for url in result["urls"][:10]:
                    out.append(f"  {url}")
        else:
            out.append("  Agent context not available")
        
        if len(out) <= 4:
            out.append(f"  No police data found for {args}")
        
        remember(command="/police", query=args, result_summary="\n".join(out)[:400],
                 source_type="chronicle", confidence=0.92)
        return "\n".join(out)
    except Exception as e:
        out.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(out)
