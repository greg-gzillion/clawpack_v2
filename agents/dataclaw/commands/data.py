"""data command - Constitutional local data search with memory + Chronicle indexing"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
name = "data"

def run(args: str, agent=None) -> str:
    from agents.dataclaw.commands._memory import recall, remember, show_prior
    from agents.dataclaw.commands._helpers import search_local_files, search_data_files, index_to_chronicle
    
    query = args.strip()
    if not query:
        return "Usage: /search <query>"
    
    # Check memory for prior searches
    prior = recall(query, limit=3)
    
    # Search local files and data
    file_results = search_local_files(query, max_results=10)
    data_results = search_data_files(query)
    
    # Build output
    lines = [f"Search: {query}", "=" * 50]
    
    if prior:
        lines.append(f"  [MEMORY] {len(prior)} prior related search(es)")
    
    if file_results:
        lines.append(f"\n### Local Files ({len(file_results)} found)")
        for r in file_results:
            lines.append(f"\n  {r['file']} ({r['size']:,}B)")
            lines.append(f"     {r['match']}")
            # Index to Chronicle for cross-agent visibility
            index_to_chronicle(r['file'], r.get('match', ''), agent=agent)
    
    if data_results:
        lines.append(f"\n### Data Files ({len(data_results)} found)")
        for r in data_results:
            lines.append(f"\n  {r['file']}")
            if 'key' in r:
                lines.append(f"     {r['key']}: {r['value']}")
            elif 'item' in r:
                lines.append(f"     {r['item']}")
    
    # Chronicle search
    if agent and hasattr(agent, 'search_chronicle'):
        chronicle_results = agent.search_chronicle(query, limit=5)
        if chronicle_results:
            lines.append(f"\n### Chronicle ({len(chronicle_results)} references)")
            for c in chronicle_results:
                ctx = c.get('context', '')[:150] if isinstance(c, dict) else str(c)[:150]
                if ctx:
                    lines.append(f"\n  {ctx}")
    
    if not file_results and not data_results:
        lines.append("\nNo local results found.")
    
    result = "\n".join(lines)
    
    # Remember for future
    remember(command="search", query=query,
             result_summary=f"Found {len(file_results)} files, {len(data_results)} data matches for: {query[:100]}",
             source_type="chronicle", confidence=0.85,
             metadata={"files_found": len(file_results), "data_found": len(data_results)})
    
    return result


def run_export(args: str, agent=None) -> str:
    """Export search results to a file."""
    from agents.dataclaw.commands._helpers import search_local_files, search_data_files, export_results
    
    parts = args.split(maxsplit=1)
    fmt = parts[0] if len(parts) > 1 and parts[0] in ('json', 'csv', 'txt') else "json"
    data_query = parts[1] if len(parts) > 1 else parts[0]
    
    file_results = search_local_files(data_query, max_results=5)
    data_results = search_data_files(data_query)
    fn = export_results(data_query, file_results, data_results, fmt)
    return f"Exported: {fn}"
