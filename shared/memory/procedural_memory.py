"""Procedural memory for AI agents - inspired by cass-memory"""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class ProceduralMemory:
    """Agent memory with confidence decay and anti-pattern learning"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.memory_path = Path.home() / f".clawpack/memory/{agent_name}"
        self.memory_path.mkdir(parents=True, exist_ok=True)
        self._load_memory()
    
    def _load_memory(self):
        self.rules = []
        self.anti_patterns = []
        self.feedback_log = []
        
        rules_file = self.memory_path / "rules.json"
        if rules_file.exists():
            self.rules = json.loads(rules_file.read_text())
    
    def add_rule(self, content: str, category: str, importance: float = 0.5):
        """Add a new rule with confidence tracking"""
        rule_id = hashlib.md5(content.encode()).hexdigest()[:8]
        
        rule = {
            'id': rule_id,
            'content': content,
            'category': category,
            'importance': importance,
            'helpful_count': 0,
            'harmful_count': 0,
            'created_at': datetime.now().isoformat(),
            'last_used': None,
            'maturity': 'candidate'
        }
        self.rules.append(rule)
        self._save()
        return rule_id
    
    def record_feedback(self, rule_id: str, helpful: bool):
        """Record feedback for confidence adjustment"""
        for rule in self.rules:
            if rule['id'] == rule_id:
                if helpful:
                    rule['helpful_count'] += 1
                else:
                    rule['harmful_count'] += 1
                
                # Check for anti-pattern conversion
                harmful_ratio = rule['harmful_count'] / (rule['helpful_count'] + rule['harmful_count'] + 1)
                if harmful_ratio > 0.5 and rule['harmful_count'] >= 3:
                    self._convert_to_anti_pattern(rule)
                
                self._update_maturity(rule)
                break
        
        self._save()
    
    def _convert_to_anti_pattern(self, rule: Dict):
        """Convert harmful rule to anti-pattern"""
        anti_pattern = {
            'id': f"anti-{rule['id']}",
            'original_rule': rule['content'],
            'content': f"PITFALL: Avoid - {rule['content']}",
            'category': rule['category'],
            'created_at': datetime.now().isoformat()
        }
        self.anti_patterns.append(anti_pattern)
        
        # Deprecate original
        rule['maturity'] = 'deprecated'
    
    def _update_maturity(self, rule: Dict):
        """Update rule maturity based on feedback"""
        total = rule['helpful_count'] + rule['harmful_count']
        harmful_ratio = rule['harmful_count'] / total if total > 0 else 0
        
        if rule['maturity'] == 'candidate' and rule['helpful_count'] >= 3 and harmful_ratio < 0.25:
            rule['maturity'] = 'established'
        elif rule['maturity'] == 'established' and rule['helpful_count'] >= 10 and harmful_ratio < 0.1:
            rule['maturity'] = 'proven'
        elif harmful_ratio > 0.25:
            rule['maturity'] = 'deprecated'
    
    def get_relevant_rules(self, task: str, limit: int = 10) -> List[Dict]:
        """Get rules relevant to current task with confidence scoring"""
        task_lower = task.lower()
        
        scored = []
        for rule in self.rules:
            if rule.get('maturity') in ['deprecated', 'retired']:
                continue
            
            # Simple relevance scoring
            relevance = 0
            if any(word in task_lower for word in rule['content'].lower().split()[:5]):
                relevance += 0.5
            
            # Calculate effective score with decay
            days_since_creation = (datetime.now() - datetime.fromisoformat(rule['created_at'])).days
            decay = 0.5 ** (days_since_creation / 90)  # 90-day half-life
            
            helpful_weight = rule['helpful_count'] * decay
            harmful_weight = rule['harmful_count'] * 4 * decay  # 4x multiplier for harmful
            
            confidence = helpful_weight - harmful_weight
            
            scored.append({
                **rule,
                'relevance_score': relevance,
                'confidence_score': confidence,
                'effective_score': relevance * confidence
            })
        
        scored.sort(key=lambda x: x['effective_score'], reverse=True)
        return scored[:limit]
    
    def _save(self):
        rules_file = self.memory_path / "rules.json"
        rules_file.write_text(json.dumps(self.rules, indent=2))
        
        anti_file = self.memory_path / "anti_patterns.json"
        anti_file.write_text(json.dumps(self.anti_patterns, indent=2))

# Global instance for all agents
_memory_instances = {}

def get_memory(agent_name: str) -> ProceduralMemory:
    if agent_name not in _memory_instances:
        _memory_instances[agent_name] = ProceduralMemory(agent_name)
    return _memory_instances[agent_name]
