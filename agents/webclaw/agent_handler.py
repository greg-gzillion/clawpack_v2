"""WebClaw A2A Message Handler - REAL INDEXES ONLY"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def process_task(task: str) -> str:
    """Process incoming A2A task using WebclawProvider index and Chronicle"""
    if not task:
        return "No task provided"
    
    task = task.strip()
    if task.startswith('search '):
        task = task[7:].strip()
    
    try:
        if task.startswith('/search') or not task.startswith('/'):
            args = task.replace('/search', '').strip() if task.startswith('/search') else task
            
            # USE THE REAL FUCKING INDEX
            from providers.webclaw_provider import WebclawProvider
            provider = WebclawProvider()
            results = provider.search(args)
            
            if results:
                output = [f"Found {len(results)} results for '{args}':\n"]
                for r in results[:10]:
                    output.append(f"  • {r}")
                return "\n".join(output)
            return f"No results for: {args}"
            
        elif task.startswith('/chronicle'):
            args = task.replace('/chronicle', '').strip()
            from commands.chronicle import run as chronicle_run
            return chronicle_run(args) or "Chronicle query complete"
            
        elif task.startswith('/stats'):
            from providers.webclaw_provider import WebclawProvider
            provider = WebclawProvider()
            stats = provider.get_stats()
            return f"WebClaw Index Stats:\n  Files indexed: {stats.get('total_files', 'N/A')}\n  Index size: {stats.get('index_size', 'N/A')}"
            
        else:
            return f"Unknown command: {task}"
            
    except Exception as e:
        import traceback
        return f"Error: {str(e)}\n{traceback.format_exc()}"
