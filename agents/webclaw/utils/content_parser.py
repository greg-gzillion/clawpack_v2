# Fix for line 17 - Replace dangerous regex with proper HTML parser

import re
from bs4 import BeautifulSoup
from html import escape
from typing import Optional

class ContentParser:
    """Safe HTML content parser"""
    
    # REMOVE dangerous regex (line 17)
    # BAD:  re.sub(r'<(?!\/?a(?=>|\s.*>))\/?.*?>', '', html)
    
    # REPLACE with BeautifulSoup (safe)
    @staticmethod
    def clean_html(html: str, allowed_tags: Optional[list] = None) -> str:
        """Safely clean HTML using BeautifulSoup"""
        if not html:
            return ""
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Default allowed tags
        if allowed_tags is None:
            allowed_tags = ['a', 'p', 'br', 'strong', 'em', 'ul', 'ol', 'li']
        
        # Remove script and style tags completely
        for tag in soup(['script', 'style', 'iframe', 'object', 'embed']):
            tag.decompose()
        
        # Only keep allowed tags
        for tag in soup.find_all(True):
            if tag.name not in allowed_tags:
                tag.unwrap()  # Remove tag but keep content
        
        # Sanitize attributes
        for tag in soup.find_all('a'):
            href = tag.get('href', '')
            # Only allow http/https links
            if not href.startswith(('http://', 'https://', '/')):
                tag['href'] = '#'
            tag['rel'] = 'noopener noreferrer'
        
        return str(soup)
    
    @staticmethod
    def extract_text(html: str) -> str:
        """Safely extract plain text from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
