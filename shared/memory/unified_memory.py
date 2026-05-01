'''Unified Shared Memory — Chronicle-backed, cross-agent knowledge store.

   CONSTITUTIONAL PRINCIPLE: Knowledge learned by one agent belongs to all.
   No agent shall hoard facts in isolated JSON files.

   Replace the fragmented per-agent shared_memory.json pattern with
   a single Chronicle-backed memory system that all 21 agents share.
'''
import json
import hashlib
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CHRONICLE_PATH = PROJECT_ROOT / 'data' / 'chronicle_ledger.json'
MEMORY_INDEX_PATH = PROJECT_ROOT / 'data' / 'memory_index.json'


class UnifiedMemory:
    '''Chronicle-backed shared memory for all 21 agents.

    Facts are extracted, indexed, and retrievable across agents.
    No per-agent JSON files. One memory. One empire.
    '''

    def __init__(self):
        self.chronicle_path = CHRONICLE_PATH
        self.index_path = MEMORY_INDEX_PATH
        self._index: Dict[str, List[Dict]] = {}
        self._facts: List[Dict] = []
        self._load_index()

    # =========================================================================
    # INDEX MANAGEMENT
    # =========================================================================

    def _load_index(self):
        '''Load the memory index from disk.'''
        if self.index_path.exists():
            try:
                data = json.loads(self.index_path.read_text())
                self._facts = data.get('facts', [])
                self._index = data.get('index', {})
            except (json.JSONDecodeError, KeyError):
                self._facts = []
                self._index = {}
        else:
            self._facts = []
            self._index = {}

    def _save_index(self):
        '''Persist the memory index to disk.'''
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(json.dumps({
            'facts': self._facts[-10000:],  # Keep last 10K facts
            'index': self._index,
            'updated_at': datetime.now(timezone.utc).isoformat(),
        }, indent=2))

    # =========================================================================
    # FACT EXTRACTION
    # =========================================================================

    def extract_facts(self, query: str, response: str, agent: str) -> List[str]:
        '''Extract key facts from an LLM interaction.

        Simple heuristics — no LLM call needed for extraction.
        - Lines with key indicators (is, are, means, defined as)
        - Lines with citations
        - Lines with numbers/statistics
        '''
        facts = []
        lines = response.split('\n')

        for line in lines:
            line = line.strip()
            if len(line) < 20 or len(line) > 500:
                continue

            # Heuristic fact indicators
            lower = line.lower()
            is_fact = any([
                lower.startswith('- ') and len(line) > 30,
                lower.startswith('* ') and len(line) > 30,
                ' is ' in lower and len(line) < 200,
                ' means ' in lower and len(line) < 200,
                ' defined as ' in lower,
                ' refers to ' in lower,
                ' requires ' in lower,
                ' must ' in lower and len(line) < 200,
                re.search(r'\d+%', line),  # Contains percentage
                re.search(r'\d{4}', line) and 'court' in lower,  # Case citation
            ])

            if is_fact:
                facts.append(line.strip('- *').strip())

        return facts[:5]  # Max 5 facts per interaction

    # =========================================================================
    # LEARNING
    # =========================================================================

    def learn(self, agent: str, key: str, value: str, source: str = 'interaction'):
        '''Store a fact in unified memory.'''
        fact = {
            'key': key,
            'value': value,
            'agent': agent,
            'source': source,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'hash': hashlib.sha256(f'{agent}:{key}:{value}'.encode()).hexdigest()[:16],
        }

        # Deduplicate
        for existing in self._facts:
            if existing['hash'] == fact['hash']:
                existing['recall_count'] = existing.get('recall_count', 0) + 1
                existing['last_recalled'] = fact['timestamp']
                self._save_index()
                return

        fact['recall_count'] = 0
        fact['last_recalled'] = None
        self._facts.append(fact)

        # Update index
        for word in key.lower().split():
            if len(word) > 2:
                if word not in self._index:
                    self._index[word] = []
                self._index[word].append(fact['hash'])

        self._save_index()

    def learn_from_interaction(self, agent: str, query: str, response: str):
        '''Extract and store facts from an LLM interaction automatically.'''
        facts = self.extract_facts(query, response, agent)
        for fact in facts:
            # Use first 80 chars as key, full text as value
            key = fact[:80]
            self.learn(agent, key, fact, source='auto_extraction')

    # =========================================================================
    # RECALL
    # =========================================================================

    def recall(self, query: str, limit: int = 5) -> List[Dict]:
        '''Search unified memory for relevant facts.'''
        query_words = set(query.lower().split())
        candidates = {}

        # Index lookup
        for word in query_words:
            if len(word) <= 2:
                continue
            if word in self._index:
                for fact_hash in self._index[word]:
                    candidates[fact_hash] = candidates.get(fact_hash, 0) + 1

        # Score and sort
        scored = []
        for fact in self._facts:
            if fact['hash'] in candidates:
                score = candidates[fact['hash']]
                # Boost by recency
                if fact.get('last_recalled'):
                    score += 1
                # Boost by recall count
                score += fact.get('recall_count', 0) * 0.5
                scored.append((score, fact))

        scored.sort(key=lambda x: x[0], reverse=True)
        results = [f for _, f in scored[:limit]]

        # Update recall stats
        for fact in results:
            fact['recall_count'] = fact.get('recall_count', 0) + 1
            fact['last_recalled'] = datetime.now(timezone.utc).isoformat()

        if results:
            self._save_index()

        return results

    def search_chronicle(self, query: str, limit: int = 10) -> List[Dict]:
        '''Search Chronicle for relevant context.'''
        if not self.chronicle_path.exists():
            return []

        try:
            data = json.loads(self.chronicle_path.read_text())
            entries = data if isinstance(data, list) else data.get('entries', [])
        except (json.JSONDecodeError, KeyError):
            return []

        query_lower = query.lower()
        results = []

        for entry in reversed(entries):
            ctx = entry.get('context', '') or entry.get('url', '')
            if any(word in ctx.lower() for word in query_lower.split() if len(word) > 3):
                results.append(entry)
                if len(results) >= limit:
                    break

        return results

    # =========================================================================
    # STATS
    # =========================================================================

    def get_stats(self) -> Dict[str, Any]:
        '''Get memory statistics.'''
        agents = {}
        for fact in self._facts:
            agent = fact.get('agent', 'unknown')
            agents[agent] = agents.get(agent, 0) + 1

        return {
            'total_facts': len(self._facts),
            'indexed_terms': len(self._index),
            'by_agent': agents,
            'chronicle_entries': 0,  # Set by caller if needed
        }


# Singleton
_memory: Optional[UnifiedMemory] = None

def get_memory() -> UnifiedMemory:
    '''Get THE unified memory. There is only ONE.'''
    global _memory
    if _memory is None:
        _memory = UnifiedMemory()
    return _memory


__all__ = ['UnifiedMemory', 'get_memory']
