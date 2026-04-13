"""Three-tier memory system - working, semantic, procedural"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field

@dataclass
class WorkingMemory:
    """Active session context - high volatility"""
    messages: List[Dict] = field(default_factory=list)
    token_count: int = 0
    max_tokens: int = 8000
    
    def add(self, role: str, content: str):
        self.messages.append({'role': role, 'content': content, 'timestamp': datetime.now().isoformat()})
        self.token_count += len(content) // 4
    
    def compress(self) -> str:
        """Compress when >90% capacity"""
        if self.token_count > self.max_tokens * 0.9:
            # Summarize older messages
            old_messages = self.messages[:-5]
            self.messages = self.messages[-5:]
            return f"Previous context compressed: {len(old_messages)} messages"
        return ""

@dataclass
class SemanticMemory:
    """Knowledge graph - relationships between entities"""
    entities: Dict[str, List[str]] = field(default_factory=dict)
    facts: List[Dict] = field(default_factory=list)
    
    def add_entity(self, name: str, attributes: List[str]):
        self.entities[name] = attributes
    
    def add_fact(self, subject: str, predicate: str, object: str):
        self.facts.append({'subject': subject, 'predicate': predicate, 'object': object, 'timestamp': datetime.now().isoformat()})
    
    def query(self, entity: str) -> List[str]:
        return self.entities.get(entity, [])

@dataclass
class ProceduralMemory:
    """Skills and how-to knowledge"""
    skills: Dict[str, str] = field(default_factory=dict)
    patterns: List[Dict] = field(default_factory=list)
    
    def add_skill(self, name: str, description: str, code: str):
        self.skills[name] = f"{description}\n\n```\n{code}\n```"
    
    def find_pattern(self, task: str) -> Optional[str]:
        task_lower = task.lower()
        for pattern in self.patterns:
            if pattern['trigger'] in task_lower:
                return pattern['solution']
        return None

class ThreeTierMemory:
    """Unified memory system"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.working = WorkingMemory()
        self.semantic = SemanticMemory()
        self.procedural = ProceduralMemory()
        self.storage_path = Path.home() / f".clawpack/memory/{agent_name}"
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._load()
    
    def _load(self):
        """Load persisted memory"""
        working_file = self.storage_path / "working.json"
        if working_file.exists():
            data = json.loads(working_file.read_text())
            self.working.messages = data.get('messages', [])
            self.working.token_count = data.get('token_count', 0)
        
        semantic_file = self.storage_path / "semantic.json"
        if semantic_file.exists():
            data = json.loads(semantic_file.read_text())
            self.semantic.entities = data.get('entities', {})
            self.semantic.facts = data.get('facts', [])
        
        procedural_file = self.storage_path / "procedural.json"
        if procedural_file.exists():
            data = json.loads(procedural_file.read_text())
            self.procedural.skills = data.get('skills', {})
            self.procedural.patterns = data.get('patterns', [])
    
    def _save(self):
        """Persist memory to disk"""
        working_file = self.storage_path / "working.json"
        working_file.write_text(json.dumps({
            'messages': self.working.messages,
            'token_count': self.working.token_count
        }, indent=2))
        
        semantic_file = self.storage_path / "semantic.json"
        semantic_file.write_text(json.dumps({
            'entities': self.semantic.entities,
            'facts': self.semantic.facts
        }, indent=2))
        
        procedural_file = self.storage_path / "procedural.json"
        procedural_file.write_text(json.dumps({
            'skills': self.procedural.skills,
            'patterns': self.procedural.patterns
        }, indent=2))
    
    def get_context(self, query: str, limit: int = 10) -> str:
        """Get relevant context from all memory tiers"""
        context = []
        
        # Working memory (recent)
        context.append("Recent conversation:")
        for msg in self.working.messages[-5:]:
            context.append(f"[{msg['role']}]: {msg['content'][:200]}")
        
        # Semantic memory (entities)
        context.append("\nKnown entities:")
        for entity, attrs in list(self.semantic.entities.items())[:5]:
            context.append(f"- {entity}: {', '.join(attrs)}")
        
        # Procedural memory (skills)
        context.append("\nAvailable skills:")
        for skill in list(self.procedural.skills.keys())[:5]:
            context.append(f"- {skill}")
        
        return "\n".join(context)

# Global memory instances
_memories = {}

def get_memory(agent_name: str) -> ThreeTierMemory:
    if agent_name not in _memories:
        _memories[agent_name] = ThreeTierMemory(agent_name)
    return _memories[agent_name]
