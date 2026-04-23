"""Content extraction utilities"""
from typing import Callable, Optional
import re
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    """Extract text from HTML, stripping scripts and styles"""
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False
        self.skip_tag = None
    
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip = True
            self.skip_tag = tag
    
    def handle_endtag(self, tag):
        if self.skip and tag == self.skip_tag:
            self.skip = False
            self.skip_tag = None
    
    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)
    
    def get_text(self):
        return ' '.join(self.text)

def get_extractor(url: str) -> Optional[Callable]:
    """Get appropriate content extractor for URL"""
    def default_extractor(content: str) -> str:
        text = re.sub(r'<[^>]+>', ' ', content)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    return default_extractor

def extract_content(content: str, content_type: str = 'html') -> str:
    """Extract clean text from content using HTML parser"""
    if 'html' in content_type.lower():
        try:
            parser = TextExtractor()
            parser.feed(content)
            text = parser.get_text()
            text = re.sub(r'\s+', ' ', text)
            return text.strip()
        except Exception:
            # Fallback: simple tag removal
            text = re.sub(r'<[^>]+>', ' ', content)
            text = re.sub(r'\s+', ' ', text)
            return text.strip()
    return content
