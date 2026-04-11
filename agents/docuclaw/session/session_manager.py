"""Session continuity for document processing"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class SessionManager:
    """Persistent session management"""
    
    def __init__(self, agent_name: str):
        self.session_path = Path.home() / f".clawpack/sessions/{agent_name}"
        self.session_path.mkdir(parents=True, exist_ok=True)
        self.current_session = None
    
    def start_session(self, topic: str, metadata: Dict = None) -> str:
        """Start a new session"""
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_session = {
            'id': session_id,
            'topic': topic,
            'started': datetime.now().isoformat(),
            'messages': [],
            'metadata': metadata or {},
            'status': 'active'
        }
        return session_id
    
    def add_message(self, role: str, content: str):
        """Add a message to current session"""
        if self.current_session:
            self.current_session['messages'].append({
                'role': role,
                'content': content,
                'timestamp': datetime.now().isoformat()
            })
            self._save()
    
    def end_session(self, summary: str = None):
        """End current session"""
        if self.current_session:
            self.current_session['ended'] = datetime.now().isoformat()
            self.current_session['summary'] = summary
            self.current_session['status'] = 'completed'
            self._save()
    
    def _save(self):
        """Save session to disk"""
        if self.current_session:
            file_path = self.session_path / f"{self.current_session['id']}.json"
            file_path.write_text(json.dumps(self.current_session, indent=2))
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """Get recent session history"""
        sessions = sorted(self.session_path.glob("*.json"), reverse=True)
        history = []
        for session_file in sessions[:limit]:
            session = json.loads(session_file.read_text())
            history.append({
                'id': session['id'],
                'topic': session.get('topic', ''),
                'started': session.get('started', ''),
                'summary': session.get('summary', '')
            })
        return history
