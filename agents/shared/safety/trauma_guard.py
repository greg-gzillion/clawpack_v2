"""Trauma Guard - Prevent dangerous operations (inspired by cass-memory)"""

import re
from pathlib import Path
from datetime import datetime
from typing import Dict

class TraumaGuard:
    """Prevent dangerous operations - completely optional, zero cost when not used"""
    
    DANGEROUS_PATTERNS = [
        (r'rm\s+-rf\s+/?', 'FATAL', 'Recursive delete of root directory'),
        (r'rm\s+-rf\s+~', 'HIGH', 'Recursive delete of home directory'),
        (r'drop\s+database', 'FATAL', 'Database deletion'),
        (r'truncate\s+table', 'HIGH', 'Table truncation without WHERE'),
        (r'git\s+push\s+--force', 'HIGH', 'Force push to remote'),
        (r'chmod\s+777', 'MEDIUM', 'Overly permissive permissions'),
    ]
    
    def __init__(self):
        self.enabled = False  # OFF by default
        self.trauma_log = Path.home() / ".clawpack/trauma.log"
    
    def enable(self):
        """Enable trauma guard"""
        self.enabled = True
        self.trauma_log.parent.mkdir(parents=True, exist_ok=True)
    
    def check_command(self, command: str) -> Dict:
        """Check if command is dangerous"""
        if not self.enabled:
            return {'blocked': False}
        
        for pattern, severity, reason in self.DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                self._log(command, severity, reason)
                return {'blocked': True, 'severity': severity, 'reason': reason}
        
        return {'blocked': False}
    
    def _log(self, command: str, severity: str, reason: str):
        import json
        entry = {'timestamp': datetime.now().isoformat(), 'command': command, 'severity': severity, 'reason': reason}
        with open(self.trauma_log, 'a') as f:
            f.write(json.dumps(entry) + '\n')

trauma_guard = TraumaGuard()
