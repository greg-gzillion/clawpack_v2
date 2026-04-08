"""Content extraction - strip HTML, extract main content"""

import re
from html.parser import HTMLParser
from urllib.parse import urlparse

class ContentExtractor:
    """Extract clean text from HTML content"""
    
    @staticmethod
    def strip_html(html_content: str, max_length: int = 5000) -> str:
        """Remove HTML tags, scripts, styles, return clean text"""
        if not html_content:
            return ""
        
        # Remove script and style tags with their content
        html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        html_content = re.sub(r'<nav[^>]*>.*?</nav>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        html_content = re.sub(r'<footer[^>]*>.*?</footer>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        html_content = re.sub(r'<header[^>]*>.*?</header>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Replace HTML tags with spaces
        html_content = re.sub(r'<[^>]+>', ' ', html_content)
        
        # Decode HTML entities
        html_content = html_content.replace('&nbsp;', ' ')
        html_content = html_content.replace('&amp;', '&')
        html_content = html_content.replace('&lt;', '<')
        html_content = html_content.replace('&gt;', '>')
        html_content = html_content.replace('&quot;', '"')
        
        # Collapse whitespace
        html_content = re.sub(r'\s+', ' ', html_content)
        
        # Strip leading/trailing spaces
        html_content = html_content.strip()
        
        # Limit length
        if len(html_content) > max_length:
            html_content = html_content[:max_length] + "..."
        
        return html_content
    
    @staticmethod
    def extract_links(html_content: str, base_url: str = "") -> list:
        """Extract all links from HTML content"""
        links = re.findall(r'href=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
        
        # Filter and normalize links
        valid_links = []
        for link in links:
            if link.startswith('http'):
                valid_links.append(link)
            elif link.startswith('/') and base_url:
                # Parse base URL to get domain
                parsed = urlparse(base_url)
                full_link = f"{parsed.scheme}://{parsed.netloc}{link}"
                valid_links.append(full_link)
        
        # Remove duplicates and limit
        return list(dict.fromkeys(valid_links))[:20]
    
    @staticmethod
    def extract_legal_citations(text: str) -> list:
        """Extract legal citations from text"""
        # Common citation patterns
        patterns = [
            r'\d+\s+U\.?S\.?\s+\d+',  # 410 U.S. 113
            r'\d+\s+F\.?\d*\s+\d+',    # 123 F.3d 456
            r'\d+\s+F\.\s+Supp\.?\s+\d+',  # 456 F. Supp. 2d 789
            r'\d+\s+S\.?\s+Ct\.?\s+\d+',   # 123 S. Ct. 456
            r'\d+\s+L\.?\s+Ed\.?\s+\d+',   # 123 L. Ed. 2d 456
            r'\d+\s+U\.?\s+S\.?\s+C\.?\s+§\s*\d+',  # 11 U.S.C. § 362
            r'§\s*\d+',  # § 362
        ]
        
        citations = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            citations.extend(matches)
        
        return list(dict.fromkeys(citations))[:20]

    @staticmethod
    def is_legal_site(url: str) -> bool:
        """Check if URL is from a legal domain"""
        legal_domains = [
            'court', 'law', 'uscourts', 'pacermonitor', 'courtlistener',
            'justia', 'findlaw', 'cornell.edu/law', 'law.cornell',
            'supremecourt', 'scotus', 'govinfo', 'federalregister'
        ]
        url_lower = url.lower()
        return any(domain in url_lower for domain in legal_domains)

# Create singleton
_extractor = None

def get_extractor():
    global _extractor
    if _extractor is None:
        _extractor = ContentExtractor()
    return _extractor
