"""Webclaw Agent - Web crawling and references"""

import sys
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.agent import BaseAgent
from shared.loop import ToolSafety
from shared.memory import MemoryType


class WebclawAgent(BaseAgent):
    """Web crawling and reference agent"""
    
    def __init__(self, project_root: Optional[Path] = None):
        super().__init__("Webclaw", project_root)
        
        # Load all references
        references_path = Path("str(PROJECT_ROOT)/agents/webclaw/references")
        self.load_references(references_path)
    
    def _register_tools(self):
        """Register web tools"""
        self.register_tool("search_references", self.search_references_tool, ToolSafety.READ_ONLY)
        self.register_tool("fetch_url", self.fetch_url, ToolSafety.READ_ONLY)
        self.register_tool("list_references", self.list_references, ToolSafety.READ_ONLY)
    
    def search_references_tool(self, query: str, max_results: int = 10) -> Dict:
        """Search across all reference files"""
        results = self.search_references(query, max_results)
        return {
            "query": query,
            "results": results,
            "total": len(results)
        }
    
    def fetch_url(self, url: str) -> Dict:
        """Fetch and extract content from URL"""
        # This would actually fetch the URL
        return {
            "url": url,
            "status": 200,
            "content_length": 1500,
            "extracted": "Sample content from URL..."
        }
    
    def list_references(self, category: str = "all") -> Dict:
        """List all reference files by category"""
        if self.reference_index:
            stats = self.reference_index.get_stats()
            return {
                "total": stats['total_items'],
                "category": category,
                "memory_bytes": stats['memory_bytes']
            }
        return {"total": 0}


# Register the agent
from shared.agent import ClawpackAgentRegistry
ClawpackAgentRegistry.register("webclaw", WebclawAgent)
