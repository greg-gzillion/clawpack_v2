'''File Analyzer — deep file analysis with optional AI enhancement.'''
from pathlib import Path
from typing import Dict
from .formats import get_metadata, detect_type

def analyze_file(file_path: str, use_ai: bool = False) -> Dict:
    '''Analyze a file with metadata and optional AI analysis.'''
    path = Path(file_path)
    result = get_metadata(path)
    if 'error' in result:
        return result

    if use_ai and result['type'] in ('document', 'code', 'data'):
        try:
            content = path.read_text(encoding='utf-8', errors='ignore')[:5000]
            from shared.llm import get_llm_client
            client = get_llm_client()
            prompt = f"Analyze this {result['type']} file: {path.name}\n\nContent preview:\n{content}\n\nProvide: 1. What this file contains 2. Key information 3. Recommended actions 4. Any issues. Keep it brief."
            response = client.call_sync(prompt=prompt, agent='fileclaw', capability='file_analysis')
            result['ai_analysis'] = response.content
        except Exception:
            result['ai_analysis'] = 'AI analysis not available'

    return result


__all__ = ['analyze_file']
