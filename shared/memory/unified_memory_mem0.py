"""mem0-backed unified memory — v5 (empty-query fallback to get_all)."""
import os
os.environ.setdefault("MEM0_TELEMETRY", "false")
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")

from pathlib import Path
from typing import Optional, List, Dict, Any

KNOWN_AGENTS = [
    "lawclaw", "claw_coder", "crustyclaw", "mediclaw", "designclaw",
    "draftclaw", "dreamclaw", "interpretclaw", "langclaw", "liberateclaw",
    "dataclaw", "drawclaw", "flowclaw", "docuclaw", "llmclaw",
    "mathematicaclaw", "plotclaw", "rustypycraw", "txclaw", "webclaw", "fileclaw",
]


def _log_err(context: str, detail: str) -> None:
    try:
        from shared._agent_helpers import log_err
        log_err("unified_memory", context, detail[:200])
    except Exception:
        pass


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MEM0_DIR = PROJECT_ROOT / "runtime" / "mem0"
MEM0_DIR.mkdir(parents=True, exist_ok=True)


def _normalize(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Translate mem0 result to legacy shape (key/value/agent/source)."""
    out = dict(raw)
    md = raw.get("metadata") or {}
    if not isinstance(md, dict):
        md = {}
    out.setdefault("key", md.get("key", ""))
    out.setdefault("value", raw.get("memory", ""))
    out.setdefault("agent", md.get("agent", ""))
    out.setdefault("source", md.get("source_type", ""))
    out.setdefault("source_type", md.get("source_type", ""))
    out.setdefault("confidence", md.get("confidence", 0.0))
    return out


class UnifiedMemory:
    """mem0-backed cross-agent memory."""

    def __init__(self, embedder_model: str = "BAAI/bge-small-en-v1.5",
                 collection: str = "clawpack"):
        from mem0 import Memory
        config = {
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "path": str(MEM0_DIR / "qdrant"),
                    "collection_name": collection,
                    "embedding_model_dims": 384,
                },
            },
            "embedder": {
                "provider": "fastembed",
                "config": {"model": embedder_model},
            },
            "history_db_path": str(MEM0_DIR / "history.db"),
        }
        self._m = Memory.from_config(config)
        self._collection = collection

    def learn(self, agent: str, key: str, value: str,
              source: str = "web_verified", confidence: float = 0.85,
              urls: Optional[List[str]] = None,
              **extra: Any) -> bool:
        try:
            metadata = {
                "key": key,
                "agent": agent,
                "source_type": source,
                "confidence": confidence,
            }
            if urls:
                metadata["urls"] = urls
            if extra:
                metadata.update(extra)
            self._m.add(
                messages=[{"role": "user", "content": value}],
                user_id=agent,
                agent_id=agent,
                infer=False,
                metadata=metadata,
            )
            return True
        except Exception as e:
            _log_err("learn", f"agent={agent} key={key} error={e}")
            return False

    def learn_from_interaction(self, agent: str, query: str, response: str) -> bool:
        key = f"interaction:{query[:40]}"
        value = f"{query} -> {response[:200]}"
        return self.learn(agent, key, value, source="agent_learned", confidence=0.85)

    def recall(self, query: str, limit: int = 5,
               agent: Optional[str] = None) -> List[Dict[str, Any]]:
        try:
            # Empty query -> use get_all (list) instead of semantic search
            if not query or not query.strip():
                return self.get_all(agent=agent, limit=limit)

            if agent:
                result = self._m.search(query=query, top_k=limit,
                                        filters={"user_id": agent})
                return [_normalize(r) for r in result.get("results", [])]
            all_results = []
            per_agent = max(1, limit // 2)
            for a in KNOWN_AGENTS:
                try:
                    result = self._m.search(query=query, top_k=per_agent,
                                            filters={"user_id": a})
                    all_results.extend([_normalize(r) for r in result.get("results", [])])
                except Exception:
                    continue
            all_results.sort(key=lambda x: x.get("score", 0) or 0, reverse=True)
            return all_results[:limit]
        except Exception as e:
            _log_err("recall", f"query={query[:40]} error={e}")
            return []

    def get_all(self, agent: Optional[str] = None,
                limit: int = 100) -> List[Dict[str, Any]]:
        try:
            if agent:
                result = self._m.get_all(top_k=limit, filters={"user_id": agent})
                return [_normalize(r) for r in result.get("results", [])]
            all_results = []
            for a in KNOWN_AGENTS:
                try:
                    result = self._m.get_all(top_k=limit, filters={"user_id": a})
                    all_results.extend([_normalize(r) for r in result.get("results", [])])
                except Exception:
                    continue
            return all_results[:limit]
        except Exception as e:
            _log_err("get_all", f"agent={agent} error={e}")
            return []

    def delete(self, memory_id: str) -> bool:
        try:
            self._m.delete(memory_id)
            return True
        except Exception as e:
            _log_err("delete", f"id={memory_id} error={e}")
            return False

    def reset(self, agent: Optional[str] = None) -> bool:
        try:
            self._m.reset()
            return True
        except Exception as e:
            _log_err("reset", f"agent={agent} error={e}")
            return False

    def stats(self) -> Dict[str, Any]:
        try:
            by_agent = {}
            total = 0
            for a in KNOWN_AGENTS:
                try:
                    result = self._m.get_all(top_k=10000, filters={"user_id": a})
                    n = len(result.get("results", []))
                    if n > 0:
                        by_agent[a] = n
                        total += n
                except Exception:
                    continue
            return {
                "total": total,
                "by_agent": by_agent,
                "collection": self._collection,
                "path": str(MEM0_DIR),
            }
        except Exception as e:
            _log_err("stats", str(e))
            return {"error": str(e)}


import threading

_instance: Optional[UnifiedMemory] = None
_instance_lock = threading.Lock()


def get_memory() -> UnifiedMemory:
    """Thread-safe singleton.

    Qdrant embedded storage holds a file lock. If two threads each
    create a UnifiedMemory(), the second one blocks forever waiting
    for the lock. Double-checked locking ensures only one instance
    is ever created per process.
    """
    global _instance
    if _instance is None:
        with _instance_lock:
            if _instance is None:
                _instance = UnifiedMemory()
    return _instance
