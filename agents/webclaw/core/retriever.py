"""WebClaw Retriever — BM25-ranked retrieval with source confidence.

   All agents query this for references.
   Ranks by relevance, source quality, and freshness.
"""
import json
import math
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional
from collections import Counter

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DB_PATH = PROJECT_ROOT / "data" / "chronicle.db"

from shared.source_registry import get_trust as get_source_weight

class BM25:
    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.documents = []
        self.doc_lengths = []
        self.avg_doc_length = 0
        self.doc_freqs = Counter()
        self.N = 0

    def tokenize(self, text: str) -> List[str]:
        return re.findall(r'[a-z0-9]+', text.lower())

    def index(self, documents: List[Dict], text_field="context"):
        self.documents = documents
        self.N = len(documents)
        self.doc_lengths = []
        self.doc_freqs.clear()
        for doc in documents:
            text = doc.get(text_field, "")
            tokens = self.tokenize(text)
            self.doc_lengths.append(len(tokens))
            for term in set(tokens):
                self.doc_freqs[term] += 1
        self.avg_doc_length = sum(self.doc_lengths) / max(1, self.N)

    def score(self, query: str, doc_idx: int) -> float:
        doc_len = self.doc_lengths[doc_idx]
        score = 0.0
        for term in set(self.tokenize(query)):
            df = self.doc_freqs.get(term, 0)
            if df == 0:
                continue
            idf = math.log((self.N - df + 0.5) / (df + 0.5) + 1.0)
            tf = self.tokenize(self.documents[doc_idx].get("context", "")).count(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / max(1, self.avg_doc_length))
            score += idf * numerator / max(0.1, denominator)
        return score

    def search(self, query: str, top_k=10) -> List[Dict]:
        scored = [(self.score(query, i), self.documents[i]) for i in range(self.N)]
        scored.sort(key=lambda x: x[0], reverse=True)
        results = []
        for score, doc in scored[:top_k]:
            if score > 0:
                doc = dict(doc)
                doc["bm25_score"] = round(score, 4)
                doc["source_weight"] = get_source_weight(doc.get("url", ""))
                doc["final_score"] = round(score * doc["source_weight"], 4)
                results.append(doc)
        results.sort(key=lambda x: x["final_score"], reverse=True)
        return results

class Retriever:
    def __init__(self):
        self.bm25 = BM25()
        self._loaded = False

    def load_chronicle(self):
        if not DB_PATH.exists():
            return
        import sqlite3
        db = sqlite3.connect(str(DB_PATH))
        db.row_factory = sqlite3.Row
        rows = db.execute('SELECT url, context, source, timestamp FROM chronicle').fetchall()
        refs = []
        for r in rows:
            refs.append({"url": r["url"], "context": r["context"], "source": r["source"], "timestamp": r["timestamp"]})
        db.close()
        self.bm25.index(refs)
        self._loaded = True

    def search(self, query: str, top_k=10) -> Dict:
        if not self._loaded:
            self.load_chronicle()
        results = self.bm25.search(query, top_k)
        return {
            "query": query,
            "results": results,
            "count": len(results),
            "top_source": results[0].get("url", "")[:80] if results else None,
            "confidence": round(max(r.get("final_score", 0) for r in results) if results else 0, 4),
        }

_retriever = None
def get_retriever() -> Retriever:
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever

def search(query: str, top_k=10) -> Dict:
    return get_retriever().search(query, top_k)

__all__ = ["Retriever", "get_retriever", "search", "BM25"]