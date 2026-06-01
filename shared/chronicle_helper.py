"""Chronicle helper - search across all indexed references"""
from shared._agent_helpers import log_err
import sys
from pathlib import Path

def search_chronicle(query: str, limit: int = 10):
    """Search the chronicle index for URLs matching query"""
    try:
        # Project root is parent of shared directory
        project_root = Path(__file__).parent.parent
        chronicle_path = project_root / "agents/webclaw/core/chronicle_ledger.py"
        
        # Chronicle path resolved silently
        
        import importlib.util
        spec = importlib.util.spec_from_file_location("chronicle_ledger", chronicle_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        chronicle = module.get_chronicle()
        results = []
        query_lower = query.lower()
        
        for card in chronicle.recover_by_context(query, limit=20):
            if (query_lower in card.url.lower() or 
                query_lower in card.source.lower() or 
                query_lower in card.context.lower()):
                results.append(card)
                if len(results) >= limit:
                    break
        return results
    except Exception as e:
        log_err("chronicle_helper", "search_error", str(e)[:200])
        return []

def get_chronicle_stats():
    try:
        project_root = Path(__file__).parent.parent
        chronicle_path = project_root / "agents/webclaw/core/chronicle_ledger.py"
        
        import importlib.util
        spec = importlib.util.spec_from_file_location("chronicle_ledger", chronicle_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        return module.get_chronicle().get_stats()
    except:
        return {"total_cards": 0}
