"""library command - Public library lookup via Chronicle FTS5"""
from pathlib import Path

name = "/library"
from agents.lawclaw.commands._memory import show_prior, remember


def run(args, agent=None):
    if not args:
        return "[LIBRARY] Usage: /library [city] [state]\n  /library Tampa FL"

    out = []
    out.append("")
    out.append("=" * 60)
    out.append(f"LIBRARY: {args}")
    out.append("=" * 60)

    prior = show_prior(args, out)

    try:
        if agent and hasattr(agent, 'lookup_jurisdiction'):
            result = agent.lookup_jurisdiction(args, "library")
            if result.get("libraries"):
                out.append(f"\n### Public Libraries ({len(result['libraries'])} found)")
                for lib in result["libraries"][:10]:
                    out.append(f"  {lib}")
            if result.get("urls"):
                out.append(f"\n### URLs ({len(result['urls'])})")
                for url in result["urls"][:10]:
                    out.append(f"  {url}")
        else:
            out.append("  Agent context not available")
        
        if len(out) <= 4:
            out.append(f"  No libraries found for {args}")
        
        remember(command="/library", query=args, result_summary="\n".join(out)[:400],
                 source_type="chronicle", confidence=0.92)
        return "\n".join(out)
    except Exception as e:
        out.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(out)
