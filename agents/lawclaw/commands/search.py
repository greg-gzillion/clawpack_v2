"""search command - Search local legal references"""
from pathlib import Path

name = "/search"

from agents.lawclaw.commands._helpers import log

LAW_REFS = Path(__file__).parent.parent.parent.parent / "agents" / "webclaw" / "references" / "lawclaw"


def run(args):
    if not args:
        return "[SEARCH] Usage: /search [case name, citation, or keyword]"

    out = []
    out.append("")
    out.append("=" * 60)
    out.append(f"SEARCH: {args}")
    out.append("=" * 60)

    # Memory recall
    try:
        from agents.lawclaw.commands._memory import show_prior, remember
        prior = show_prior(args, out)
    except Exception:
        pass

    try:
        results = []
        if LAW_REFS.exists():
            for md_file in LAW_REFS.rglob("*.md"):
                try:
                    content = md_file.read_text(encoding='utf-8', errors='ignore')
                    if args.lower() in content.lower():
                        rel = md_file.relative_to(LAW_REFS)
                        results.append((str(rel), content))
                        if len(results) >= 8:
                            break
                except:
                    pass

        if results:
            out.append(f"  Found {len(results)} reference files:")
            out.append("")
            for rel_path, content in results:
                out.append("-" * 60)
                out.append(f"  {rel_path}")
                out.append("-" * 60)
                out.append(content[:1500])
                if len(content) > 1500:
                    out.append(f"  ... ({len(content) - 1500} more chars)")
                out.append("")

            # Write to shared memory
            try:
                remember(
                    command="/search",
                    query=args,
                    result_summary=f"Found {len(results)} files matching '{args}'",
                    source_type="chronicle",
                    confidence=0.90,
                )
            except Exception:
                pass
        else:
            out.append("  No local reference files found.")
            out.append("  Try: /law [topic] for legal research with CourtListener")

        return "\n".join(out)

    except Exception as e:
        log("search_run_error", str(e)[:300])
        out.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(out)