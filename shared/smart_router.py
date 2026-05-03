"""Four-tier intelligent command routing - inspired by Citadel"""

import re
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class RoutingTier(Enum):
    DIRECT = 0      # 0 tokens - regex pattern match
    SESSION = 1     # 0 tokens - active session context
    KEYWORD = 2     # 0 tokens - keyword lookup
    LLM = 3         # ~500 tokens - fallback

@dataclass
class RouteResult:
    tier: RoutingTier
    handler: str
    confidence: float
    tokens_saved: int

class SmartRouter:
    """Route commands to cheapest possible handler"""
    
    def __init__(self):
        self.patterns = self._load_patterns()
        self.keyword_index = self._build_keyword_index()
        self.active_sessions = {}
    
    def _load_patterns(self):
        """Load regex patterns for direct matching"""
        return {
            r'^fix (typo|spelling|grammar)': 'direct_edit',
            r'^add (comment|docstring)': 'direct_edit',
            r'^format (code|file)': 'direct_format',
            r'^explain (this|that)': 'session_context',
            r'^what is': 'session_context',
            r'^show me': 'session_context',
            r'^list (agents|templates|skills)': 'keyword_list',
            r'^status': 'keyword_status',
            r'^help': 'keyword_help',
        }
    
    def _build_keyword_index(self):
        """Build keyword index for fast lookup"""
        return {
            'agents': 'list_agents',
            'templates': 'list_templates', 
            'skills': 'list_skills',
            'status': 'get_status',
            'stats': 'get_stats',
            'help': 'show_help',
        }
    
    def route(self, command: str, session_context: Optional[Dict] = None) -> RouteResult:
        """Route command to appropriate handler"""
        command_lower = command.lower().strip()
        
        # Tier 0: Direct regex match
        for pattern, handler in self.patterns.items():
            if re.match(pattern, command_lower):
                return RouteResult(
                    tier=RoutingTier.DIRECT,
                    handler=handler,
                    confidence=0.95,
                    tokens_saved=500
                )
        
        # Tier 1: Active session context
        if session_context and command_lower in session_context.get('recent_commands', []):
            return RouteResult(
                tier=RoutingTier.SESSION,
                handler='session_handler',
                confidence=0.85,
                tokens_saved=500
            )
        
        # Tier 2: Keyword lookup
        for keyword, handler in self.keyword_index.items():
            if keyword in command_lower:
                return RouteResult(
                    tier=RoutingTier.KEYWORD,
                    handler=handler,
                    confidence=0.75,
                    tokens_saved=500
                )
        
        # Tier 3: LLM fallback
        return RouteResult(
            tier=RoutingTier.LLM,
            handler='llm_handler',
            confidence=0.5,
            tokens_saved=0
        )
    
    def get_stats(self) -> Dict:
        """Get routing statistics"""
        return {
            'tiers': [t.value for t in RoutingTier],
            'patterns': len(self.patterns),
            'keywords': len(self.keyword_index)
        }

# Global instance
smart_router = SmartRouter()
