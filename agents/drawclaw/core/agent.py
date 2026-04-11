"""Drawclaw Core Logic - Casual drawing"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

class drawclawCore:
    """Core processing for casual/freeform drawing"""
    
    def process(self, query: str) -> str:
        """Process drawing commands"""
        query_lower = query.lower()
        
        if "sketch" in query_lower:
            return self._sketch(query)
        elif "doodle" in query_lower:
            return self._doodle(query)
        elif "paint" in query_lower:
            return self._paint(query)
        elif "illustration" in query_lower:
            return self._illustrate(query)
        elif "comic" in query_lower or "cartoon" in query_lower:
            return self._cartoon(query)
        elif "meme" in query_lower:
            return self._meme(query)
        else:
            return f"[drawclaw] Creating casual drawing: {query[:50]}..."
    
    def _sketch(self, query: str) -> str:
        return f"✏️ Sketching: {query}"
    
    def _doodle(self, query: str) -> str:
        return f"🎨 Doodling: {query}"
    
    def _paint(self, query: str) -> str:
        return f"🖌️ Painting: {query}"
    
    def _illustrate(self, query: str) -> str:
        return f"📖 Illustrating: {query}"
    
    def _cartoon(self, query: str) -> str:
        return f"😊 Creating cartoon: {query}"
    
    def _meme(self, query: str) -> str:
        return f"🔥 Generating meme: {query}"
    
    def _help(self) -> str:
        return """
🎨 DRAWCLAW COMMANDS:
  sketch <description>    - Quick sketch
  doodle <description>    - Casual doodle
  paint <description>     - Digital painting
  illustrate <scene>      - Detailed illustration
  cartoon <character>     - Cartoon style
  meme <concept>          - Meme generation
  /help                   - This menu
"""
