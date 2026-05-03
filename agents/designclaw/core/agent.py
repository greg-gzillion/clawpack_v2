"""Designclaw Core - AI-Powered Design Assistant"""
import sys
from pathlib import Path

# Add root to path
root_path = Path(__file__).parent.parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from shared.llm import LLMManager

class designclawCore:
    """Creative design assistant with AI"""
    
    def __init__(self):
        self.llm = LLMManager()
        self.exports_dir = Path("str(PROJECT_ROOT)/exports/designclaw")
        self.exports_dir.mkdir(parents=True, exist_ok=True)
    
    def process(self, query: str) -> str:
        """Process design queries with AI"""
        q = query.lower()
        
        if "/interactive" in q:
            return self._interactive_mode()
        elif "/help" in q:
            return self._help()
        elif "brand" in q or "logo" in q or "identity" in q:
            return self._ai_brand_identity(query)
        elif "color" in q or "palette" in q:
            return self._ai_color_palette(query)
        elif "mood" in q or "aesthetic" in q:
            return self._ai_mood(query)
        elif "typography" in q or "font" in q:
            return self._ai_typography(query)
        elif "slogan" in q or "tagline" in q:
            return self._ai_copywriting(query)
        else:
            return self._ai_general(query)
    
    def _ai_brand_identity(self, query: str) -> str:
        prompt = f"""You are a professional brand designer. Create a concise brand identity based on: "{query}"

Provide:
1. Brand essence (1 sentence)
2. Logo concept (2-3 sentences)
3. Color palette (3-4 hex codes with names)
4. Typography recommendation (header + body font)

Keep it practical and specific."""
        
        try:
            response = self.llm.chat_sync(prompt)
            return f"🎨 BRAND IDENTITY\n\n{response}"
        except:
            return self._fallback_brand(query)
    
    def _ai_color_palette(self, query: str) -> str:
        prompt = f"""Create a cohesive color palette for: "{query}"
Provide 4-5 hex codes with descriptive names and brief usage notes."""
        
        try:
            response = self.llm.chat_sync(prompt)
            return f"🎨 COLOR PALETTE\n\n{response}"
        except:
            return "Colors: #0066FF (Primary), #1E1E2E (Dark), #FFFFFF (Light), #00D4AA (Accent)"
    
    def _ai_mood(self, query: str) -> str:
        prompt = f"""Describe an aesthetic/mood direction for: "{query}"
Include: Vibe (2-3 words), Color story, Texture/feel, Typography style, Reference imagery."""
        
        try:
            response = self.llm.chat_sync(prompt)
            return f"🎭 MOOD DIRECTION\n\n{response}"
        except:
            return "Mood: Minimal, clean, airy. Colors: Neutrals with one bold accent."
    
    def _ai_typography(self, query: str) -> str:
        prompt = f"""Recommend font pairings for: "{query}"
Include header font, body font, and brief reasoning."""
        
        try:
            response = self.llm.chat_sync(prompt)
            return f"✍️ TYPOGRAPHY\n\n{response}"
        except:
            return "Typography: Inter (headers) + Open Sans (body) - clean and modern."
    
    def _ai_copywriting(self, query: str) -> str:
        prompt = f"""Create brand copy for: "{query}"
Provide: Tagline (5-7 words), Value proposition (1 sentence), Brand voice (3 adjectives)."""
        
        try:
            response = self.llm.chat_sync(prompt)
            return f"✍️ COPYWRITING\n\n{response}"
        except:
            return "Tagline: Design that works. Voice: Professional, clear, approachable."
    
    def _ai_general(self, query: str) -> str:
        prompt = f"""You are a senior design consultant. Answer concisely: "{query}" """
        
        try:
            response = self.llm.chat_sync(prompt)
            return f"💡 DESIGN ADVICE\n\n{response}"
        except:
            return f"[designclaw] Processing: {query}\n\nTip: Try 'brand identity for...' or 'color palette for...'"
    
    def _fallback_brand(self, query: str) -> str:
        return f"""
🎨 BRAND IDENTITY

Essence: Modern, trustworthy, innovative
Logo: Clean wordmark with geometric symbol
Colors: #0066FF (Primary), #1E1E2E (Secondary), #FFFFFF (Light)
Typography: Inter (headers) + Open Sans (body)
"""
    
    def _interactive_mode(self) -> str:
        print("\n🎨 DESIGNCLAW INTERACTIVE")
        print("=" * 40)
        name = input("Brand/Project name: ").strip()
        industry = input("Industry (tech/health/luxury/creative): ").strip()
        mood = input("Mood/vibe: ").strip()
        
        query = f"brand identity for {name} - {industry} industry, {mood} vibe"
        return self._ai_brand_identity(query)
    
    def _help(self) -> str:
        return """
🎨 DESIGNCLAW COMMANDS:

  brand identity for [name]     - AI brand concept
  color palette for [mood]      - AI color scheme  
  mood [aesthetic]              - AI mood board direction
  typography for [style]        - Font recommendations
  slogan for [brand]            - Copywriting help
  /interactive                  - Guided design brief
  /help                         - This menu
  /quit                         - Exit

Examples:
  brand identity for eco-friendly fashion startup
  color palette for luxury spa
  mood dark academia
"""
