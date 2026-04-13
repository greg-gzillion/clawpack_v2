"""LLM synthesis for legal responses - uses shared LLM infrastructure"""

import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class LegalSynthesizer:
    def __init__(self):
        self.available = self._check_ollama()
    
    def _check_ollama(self) -> bool:
        """Check if Ollama is available"""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def synthesize(self, query: str, content: str, context: str = "") -> str:
        """Synthesize response from WebClaw content using LLM"""
        if not content or content == "Agent executed":
            return f"No results found for: {query}"
        
        if not self.available:
            return self._format_raw(content, query)
        
        prompt = self._build_synthesis_prompt(query, content, context)
        response = self._query_ollama(prompt)
        
        if response:
            return f"\nSynthesized Response:\n{'='*50}\n\n{response}"
        
        return self._format_raw(content, query)
    
    def _build_synthesis_prompt(self, query: str, content: str, context: str) -> str:
        """Build prompt for legal synthesis"""
        return f"""You are a legal research assistant. Synthesize this information into a clear, accurate response.

Query: {query}
Context: {context[:200]}

Source Content:
{content[:1500]}

Provide a concise summary focusing on key legal information."""
    
    def _query_ollama(self, prompt: str, model: str = "tinyllama:1.1b") -> str:
        """Query Ollama model"""
        try:
            result = subprocess.run(
                ["ollama", "run", model, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return ""
    
    def _format_raw(self, content: str, query: str) -> str:
        """Format raw content when LLM unavailable"""
        lines = content.split('\n')[:30]
        result = f"\nResults for: {query}\n"
        result += "=" * 50 + "\n\n"
        
        for line in lines:
            if line.strip():
                result += line + "\n"
        
        if len(content.split('\n')) > 30:
            result += "\n... (truncated)\n"
        
        return result
    
    def ask_with_context(self, question: str, context: str) -> str:
        """Direct LLM query with legal context"""
        if not self.available:
            return f"LLM unavailable. Question: {question}"
        
        prompt = f"""Context from legal database:
{context[:1000]}

Question: {question}

Provide a helpful legal answer based on the context."""
        
        response = self._query_ollama(prompt)
        if response:
            return f"\nAnswer:\n{'='*50}\n\n{response}"
        return f"Unable to answer: {question}"
    
    def analyze_legal_text(self, text: str) -> str:
        """Analyze legal text directly with LLM"""
        if not self.available:
            return f"Legal text analysis (LLM unavailable):\n{text[:500]}..."
        
        prompt = f"""Analyze this legal text. Extract: parties, legal issues, holdings, reasoning.

Text: {text[:1500]}

Provide structured analysis."""
        
        response = self._query_ollama(prompt)
        if response:
            return f"\nLegal Analysis:\n{'='*50}\n\n{response}"
        return f"Analysis error for: {text[:200]}"
    
    def is_available(self) -> bool:
        return self.available
