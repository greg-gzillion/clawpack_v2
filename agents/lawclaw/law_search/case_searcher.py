"""Law case search module - searches US court cases for free"""

import urllib.parse
from datetime import datetime
from typing import Dict, List, Optional

class LawCaseSearcher:
    """Search US court cases across free law databases"""
    
    # Free law databases (no API key required)
    LAW_DATABASES = {
        'courtlistener': {
            'name': 'CourtListener',
            'url': 'https://www.courtlistener.com/search/?q={query}&type=o',
            'description': 'Free law database with millions of opinions'
        },
        'google_scholar': {
            'name': 'Google Scholar',
            'url': 'https://scholar.google.com/scholar?q={query}&as_sdt=4,11',
            'description': 'Search case law and scholarly articles'
        },
        'cornell_lii': {
            'name': 'Cornell LII',
            'url': 'https://www.law.cornell.edu/search?q={query}',
            'description': 'Free law source from Cornell'
        },
        'justia': {
            'name': 'Justia',
            'url': 'https://law.justia.com/search?q={query}',
            'description': 'Free case law information'
        },
        'findlaw': {
            'name': 'FindLaw',
            'url': 'https://caselaw.findlaw.com/search?q={query}',
            'description': 'Free case law database'
        },
        'pacer': {
            'name': 'PACER',
            'url': 'https://pacer.uscourts.gov/search?q={query}',
            'description': 'Public Access to Court Electronic Records'
        }
    }
    
    def search_case(self, case_name: str, court: Optional[str] = None) -> Dict:
        """Search for a case by name across all law databases"""
        encoded = urllib.parse.quote(case_name)
        
        results = {
            'case': case_name,
            'court': court,
            'timestamp': datetime.now().isoformat(),
            'searches': []
        }
        
        for key, db in self.LAW_DATABASES.items():
            results['searches'].append({
                'source': db['name'],
                'url': db['url'].format(query=encoded),
                'description': db['description']
            })
        
        return results
    
    def search_by_citation(self, citation: str) -> Dict:
        """Search by law citation (e.g., '123 F.3d 456')"""
        encoded = urllib.parse.quote(citation)
        
        return {
            'citation': citation,
            'timestamp': datetime.now().isoformat(),
            'searches': [
                {'source': 'Google Scholar', 'url': f'https://scholar.google.com/scholar?q={encoded}'},
                {'source': 'CourtListener', 'url': f'https://www.courtlistener.com/search/?q={encoded}'},
                {'source': 'Cornell LII', 'url': f'https://www.law.cornell.edu/search?q={encoded}'}
            ]
        }
    
    def search_docket(self, docket_number: str, court: str = "federal") -> Dict:
        """Search court dockets"""
        encoded = urllib.parse.quote(f"{court} {docket_number}")
        
        return {
            'docket': docket_number,
            'court': court,
            'searches': [
                {'source': 'PACER', 'url': f'https://pacer.uscourts.gov/search?q={encoded}'},
                {'source': 'CourtListener', 'url': f'https://www.courtlistener.com/docket/?q={encoded}'},
                {'source': 'RECAP', 'url': f'https://www.courtlistener.com/recap/?q={encoded}'}
            ]
        }

# Global instance
law_searcher = LawCaseSearcher()
