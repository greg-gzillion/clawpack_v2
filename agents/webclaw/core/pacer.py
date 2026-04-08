"""PACER (Public Access to Court Electronic Records) integration"""

import re
from typing import Optional, Dict, List

class PacerHandler:
    """Handle PACER-specific requests and parsing"""
    
    # PACER court codes mapping
    COURT_CODES = {
        "SCOTUS": "supreme",
        "1CA": "ca01", "2CA": "ca02", "3CA": "ca03", "4CA": "ca04",
        "5CA": "ca05", "6CA": "ca06", "7CA": "ca07", "8CA": "ca08",
        "9CA": "ca09", "10CA": "ca10", "11CA": "ca11", "FED": "cafc",
        "DC": "dcd",
    }
    
    @staticmethod
    def is_pacer_url(url: str) -> bool:
        """Check if URL is from PACER"""
        pacer_patterns = [
            r'pacer\.uscourts\.gov',
            r'ecf\.[^\.]+\.uscourts\.gov',
            r'courtlistener\.com.*pacer',
            r'archive\.recapthelaw\.org'
        ]
        url_lower = url.lower()
        return any(re.search(pattern, url_lower) for pattern in pacer_patterns)
    
    @staticmethod
    def extract_case_number(text: str) -> Optional[str]:
        """Extract case number from text"""
        patterns = [
            r'Case\s*No\.?\s*:?\s*(\d{2,4}-[a-zA-Z]+-\d+)',
            r'Docket\s*No\.?\s*:?\s*(\d{2,4}-[a-zA-Z]+-\d+)',
            r'(\d{2,4}-\w+-\d{5,6})',
            r'(\d{2,4}-\w+-\d{2,5})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    
    @staticmethod
    def get_pacer_base_url(court_code: str) -> str:
        """Get PACER base URL for court"""
        court = PacerHandler.COURT_CODES.get(court_code.upper(), court_code.lower())
        return f"https://ecf.{court}.uscourts.gov"
    
    @staticmethod
    def format_pacer_docket(case_number: str) -> str:
        """Format PACER docket URL"""
        # Try to extract district code
        match = re.match(r'(\d{2,4})-([a-zA-Z]+)-(\d+)', case_number)
        if match:
            _, district, _ = match.groups()
            return f"https://www.courtlistener.com/docket/?q={case_number}"
        
        return f"https://www.courtlistener.com/search/?q={case_number}"
    
    @staticmethod
    def extract_judge_name(text: str) -> Optional[str]:
        """Extract judge name from text"""
        patterns = [
            r'Judge\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'Presiding\s+Judge:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'Magistrate\s+Judge:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    
    @staticmethod
    def extract_filing_date(text: str) -> Optional[str]:
        """Extract filing date from text"""
        patterns = [
            r'Filed:\s*(\d{1,2}/\d{1,2}/\d{2,4})',
            r'Date\s+Filed:\s*(\d{1,2}/\d{1,2}/\d{2,4})',
            r'(\d{4}-\d{2}-\d{2})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

# Singleton
_pacer = None

def get_pacer():
    global _pacer
    if _pacer is None:
        _pacer = PacerHandler()
    return _pacer
