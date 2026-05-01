"""API - AI and web requests

   CONSTITUTIONAL UPDATE: All AI requests now route through
   shared/llm/client.py — the sovereign gateway.
   
   This was the original bypass factory that taught other agents
   how to call models directly. Now it's an adapter that demonstrates
   constitutional compliance.
   
   No direct OpenRouter calls. No subprocess Ollama calls.
   Every legal query is audited, budgeted, and governed.
"""

import sys
import warnings
from pathlib import Path

# Project root for sovereign gateway access
_project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

warnings.warn(
    "lawclaw/core/api.py is DEPRECATED as an independent authority. "
    "All AI calls now route through shared/llm/client.py. "
    "This was the original bypass factory — now an adapter to the throne.",
    DeprecationWarning,
    stacklevel=2
)

import urllib.request
import json
import re

__all__ = ["ask_ai", "fetch_url"]


# Sovereign gateway — initialized on first use
_client = None

def _get_client():
    """Get THE sovereign gateway. There is only ONE."""
    global _client
    if _client is None:
        from shared.llm import get_llm_client
        _client = get_llm_client()
    return _client


def ask_ai(question):
    """Ask AI through the sovereign gateway — NOT direct provider calls.
    
    The throne handles:
    - Provider selection (no more "if key: OpenRouter else: Ollama")
    - API key management (no more get_api_key())
    - Model selection (respects llmclaw /use, no hardcoded models)
    - Budget enforcement
    - Chronicle audit logging
    
    This was the original bypass factory. Now it's a constitutional example.
    """
    try:
        response = _get_client().call_sync(
            prompt=question,
            agent="lawclaw",
            capability="legal_research",
        )
        return response.content
    except Exception as e:
        raise RuntimeError(
            f"SOVEREIGN GATEWAY FAILURE in lawclaw/core/api.py: "
            f"The throne is unreachable. Legal AI assistance cannot proceed "
            f"without constitutional authority. Underlying error: {e}"
        ) from e


def fetch_url(url):
    """Fetch a URL — web access, not model access. No sovereignty issue.
    
    This is preserved unchanged. HTTP requests to external websites
    are data retrieval, not intelligence generation. The sovereign
    gateway governs model access, not web browsing.
    """
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'LawClaw/1.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            text = re.sub(r'<[^>]+>', ' ', content)
            text = re.sub(r'\s+', ' ', text)
            return text
    except Exception as e:
        return f"Error: {e}"