# docker/orchestrator/orchestrator.py
"""Clawpack Orchestrator - Coordinates all agents"""

import os
import time
import redis
import requests
from typing import Dict, List
import json

class ClawpackOrchestrator:
    def __init__(self):
        self.redis = redis.Redis(
            host=os.getenv('REDIS_HOST', 'redis'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            decode_responses=True
        )
        self.agents = {
            'webclaw': 'http://webclaw:5000',
            'langclaw': None,  # CLI agent
            'mathematicaclaw': None,  # CLI agent
            'drawclaw': None,  # CLI agent
            'txclaw': None,  # CLI agent
        }
        self.ready_agents = set()
    
    def check_health(self) -> Dict:
        """Check health of all agents"""
        status = {}
        
        # Check webclaw
        try:
            resp = requests.get(f"{self.agents['webclaw']}/health", timeout=5)
            status['webclaw'] = resp.status_code == 200
        except:
            status['webclaw'] = False
        
        # Check Redis
        try:
            self.redis.ping()
            status['redis'] = True
        except:
            status['redis'] = False
        
        return status
    
    def get_shared_knowledge(self, key: str) -> str:
        """Get knowledge from shared memory"""
        return self.redis.get(f"knowledge:{key}")
    
    def set_shared_knowledge(self, key: str, value: str):
        """Store knowledge in shared memory"""
        self.redis.set(f"knowledge:{key}", value)
    
    def coordinate_task(self, task: Dict) -> Dict:
        """Coordinate a task across agents"""
        task_type = task.get('type')
        result = {'status': 'pending', 'results': []}
        
        if task_type == 'translate_and_draw':
            # Langclaw translates, Drawclaw draws
            pass
        elif task_type == 'analyze_and_document':
            # Dataclaw analyzes, Docuclaw documents
            pass
        
        return result
    
    def run(self):
        """Main orchestrator loop"""
        print("🦞 Clawpack Orchestrator starting...")
        
        while True:
            health = self.check_health()
            print(f"Health: {health}")
            
            # Check for pending tasks in Redis
            tasks = self.redis.lrange('tasks:pending', 0, -1)
            for task_json in tasks:
                task = json.loads(task_json)
                result = self.coordinate_task(task)
                self.redis.lpush('tasks:completed', json.dumps(result))
                self.redis.lrem('tasks:pending', 1, task_json)
            
            time.sleep(5)

if __name__ == '__main__':
    orchestrator = ClawpackOrchestrator()
    orchestrator.run()
