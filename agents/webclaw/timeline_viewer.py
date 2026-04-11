"""Timeline Viewer - Inspired by Common Chronicle"""

import json
from datetime import datetime
from typing import List, Dict

class TimelineViewer:
    """Visualize structured timelines (Common Chronicle pattern)"""
    
    @staticmethod
    def render_timeline(timeline: List[Dict]) -> str:
        """Render timeline in markdown format"""
        if not timeline:
            return "No timeline events found"
        
        output = "# Structured Timeline\n\n"
        output += "| Date | Event | Source |\n"
        output += "|------|-------|--------|\n"
        
        for event in timeline:
            output += f"| {event.get('date', 'Unknown')} | {event.get('event', '')[:50]} | {event.get('source', '')[:40]} |\n"
        
        return output
    
    @staticmethod
    def render_sources(structured_context: Dict) -> str:
        """Render structured sources"""
        output = f"# Structured Context: {structured_context.get('query', '')}\n\n"
        output += f"*Generated: {structured_context.get('timestamp', '')}*\n\n"
        
        for i, source in enumerate(structured_context.get('sources', []), 1):
            output += f"## Source {i}\n"
            output += f"- **URL**: {source.get('url', '')}\n"
            output += f"- **Context**: {source.get('context', '')}\n"
            output += f"- **Relevance**: {source.get('relevance', '')}\n\n"
        
        return output
