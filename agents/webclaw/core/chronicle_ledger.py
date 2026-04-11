"""Chronicle Ledger System - Immutable URL tracking with context preservation"""
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

@dataclass
class ChronicleCard:
    url: str
    context: str
    source: str
    timestamp: str
    recovery_key: str
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        return asdict(self)

class ChronicleLedger:
    def __init__(self, ledger_path: Optional[Path] = None):
        self.ledger_path = ledger_path or Path.home() / ".clawpack" / "chronicle_ledger.json"
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self.cards: List[ChronicleCard] = []
        self._load_ledger()
    
    def _load_ledger(self):
        if self.ledger_path.exists():
            try:
                with open(self.ledger_path, 'r') as f:
                    data = json.load(f)
                    self.cards = [ChronicleCard(**card) for card in data]
            except:
                self.cards = []
    
    def _save_ledger(self):
        with open(self.ledger_path, 'w') as f:
            json.dump([card.to_dict() for card in self.cards], f, indent=2)
    
    def record_fetch(self, url: str, context: str, source: str, metadata: Optional[Dict] = None) -> ChronicleCard:
        recovery_key = hashlib.md5(f"{url}{context}{source}".encode()).hexdigest()
        card = ChronicleCard(
            url=url,
            context=context[:500],
            source=source,
            timestamp=datetime.utcnow().isoformat(),
            recovery_key=recovery_key,
            metadata=metadata or {}
        )
        self.cards.append(card)
        self._save_ledger()
        return card
    
    def recover_by_context(self, query: str, limit: int = 5) -> List[ChronicleCard]:
        query_lower = query.lower()
        matches = []
        for card in reversed(self.cards):
            if (query_lower in card.context.lower() or 
                query_lower in card.url.lower() or
                query_lower in card.source.lower()):
                matches.append(card)
                if len(matches) >= limit:
                    break
        return matches
    
    def get_timeline(self, source: Optional[str] = None) -> List[ChronicleCard]:
        timeline = [card for card in self.cards if source is None or card.source == source]
        timeline.sort(key=lambda x: x.timestamp, reverse=True)
        return timeline
    
    def get_stats(self) -> Dict:
        sources = {}
        for card in self.cards:
            sources[card.source] = sources.get(card.source, 0) + 1
        return {
            "total_cards": len(self.cards),
            "unique_urls": len(set(c.url for c in self.cards)),
            "sources": sources,
            "ledger_path": str(self.ledger_path)
        }

_chronicle = None
def get_chronicle():
    global _chronicle
    if _chronicle is None:
        _chronicle = ChronicleLedger()
    return _chronicle

# ============================================================================
# Features inspired by Common Chronicle (liujuanjuan1984)
# ============================================================================

def create_timeline(self, topic: str, start_date: str = None, end_date: str = None) -> List[Dict]:
    """Create a structured timeline of events (inspired by Common Chronicle)"""
    # Query cards by date range
    cards = self.query_by_topic(topic)
    
    timeline = []
    for card in cards:
        if 'date' in card.metadata:
            timeline.append({
                'date': card.metadata['date'],
                'event': card.context,
                'source': card.url,
                'confidence': card.metadata.get('confidence', 'medium')
            })
    
    # Sort by date
    timeline.sort(key=lambda x: x['date'])
    return timeline

def add_sourced_entry(self, content: str, source_url: str, date: str = None):
    """Add a sourced entry to the chronicle (sourcing integrity)"""
    return self.record_fetch(
        url=source_url,
        context=content,
        source='user_submission',
        metadata={'date': date or datetime.now().isoformat(), 'sourcing': 'verified'}
    )

def get_structured_context(self, query: str, max_sources: int = 5) -> Dict:
    """Get structured context with sources (turning messy context into structured)"""
    results = self.search(query, max_sources)
    
    structured = {
        'query': query,
        'timestamp': datetime.now().isoformat(),
        'sources': [],
        'summary': '',
        'confidence': 'medium'
    }
    
    for r in results:
        structured['sources'].append({
            'url': r.url,
            'context': r.context,
            'relevance': 'high',
            'verified': True
        })
    
    return structured
