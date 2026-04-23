"""Index court information in chronicle"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class ChronicleIndexer:
    def __init__(self):
        self.chronicle = None
        self.ledger = None
        self._init_chronicle()
    
    def _init_chronicle(self):
        try:
            from shared.chronicle_helper import search_chronicle
            self.chronicle = search_chronicle
            from agents.webclaw.core.chronicle_ledger import get_chronicle
            self.ledger = get_chronicle()
            print("✅ Chronicle connected", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ Chronicle not available: {e}", file=sys.stderr)
    
    def index_court(self, jurisdiction: str, location: str, content: str, source_path: Path) -> bool:
        """Index court information in chronicle"""
        if not self.ledger:
            return False
        
        try:
            self.ledger.record_fetch(
                url=f"file://{source_path}",
                context=f"Court: {jurisdiction} - {location}\n{content}",
                source=f"lawclaw/jurisdictions/{jurisdiction}/{location}",
                metadata={
                    'jurisdiction': jurisdiction,
                    'location': location,
                    'type': 'court_info',
                    'indexed_at': datetime.now().isoformat()
                }
            )
            return True
        except Exception as e:
            print(f"Index error: {e}", file=sys.stderr)
            return False

chronicle_indexer = ChronicleIndexer()
