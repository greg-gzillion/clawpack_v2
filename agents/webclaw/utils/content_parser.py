"""Content extraction utilities"""
from typing import Callable, Optional
import re

def get_extractor(url: str) -> Optional[Callable]:
    """Get appropriate content extractor for URL"""
    # Simple extractor that works for most HTML
    def default_extractor(content: str) -> str:
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', content)
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    return default_extractor

def extract_content(content: str, content_type: str = 'html') -> str:
    """Extract clean text from content"""
    if 'html' in content_type.lower():
        # Remove scripts and styles
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', content)
        # Clean whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    return content
