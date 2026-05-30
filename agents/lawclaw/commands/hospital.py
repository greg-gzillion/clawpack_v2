"""hospital command - Hospital lookup via Chronicle FTS5"""
from pathlib import Path

name = "/hospital"
from agents.lawclaw.commands._memory import show_prior, remember


def run(args, agent=None):
    if not args:
        return "[HOSPITAL] Usage: /hospital [city] [state]\n  /hospital Daytona Beach FL"

    out = []
    out.append("")
    out.append("=" * 60)
    out.append(f"HOSPITALS: {args}")
    out.append("=" * 60)

    prior = show_prior(args, out)

    try:
        if agent and hasattr(agent, 'lookup_jurisdiction'):
            result = agent.lookup_jurisdiction(args, "hospital")
            if result.get("hospitals"):
                out.append(f"\n### Hospitals ({len(result['hospitals'])} found)")
                for h in result["hospitals"][:10]:
                    out.append(f"  {h}")
            if result.get("urls"):
                out.append(f"\n### URLs ({len(result['urls'])})")
                for url in result["urls"][:10]:
                    out.append(f"  {url}")
        else:
            out.append("  Agent context not available")
        
        if len(out) <= 4:
            out.append(f"  No hospitals found for {args}")
        
        remember(command="/hospital", query=args, result_summary="\n".join(out)[:400],
                 source_type="chronicle", confidence=0.92)
        return "\n".join(out)
    except Exception as e:
        out.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(out)
