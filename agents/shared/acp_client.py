"""ACP Client for agent-to-agent communication"""

import sys
import subprocess
import json
from pathlib import Path
from typing import Optional, Dict

class ACPClient:
    """Agent Client Protocol client - communicate with any ACP-compatible agent"""
    
    SUPPORTED_AGENTS = {
        'claude': 'claude-agent-acp',
        'codex': 'codex-acp',
        'pi': 'pi-acp',
        'gemini': 'gemini --acp',
        'qwen': 'qwen --acp'
    }
    
    def __init__(self, agent: str = 'claude'):
        self.agent = agent
        self.session_id = None
        self._check_availability()
    
    def _check_availability(self):
        """Check if agent is available"""
        agent_cmd = self.SUPPORTED_AGENTS.get(self.agent, self.agent)
        try:
            subprocess.run(['which', agent_cmd.split()[0]], capture_output=True, check=True)
            print(f"✅ ACP agent '{self.agent}' available", file=sys.stderr)
        except:
            print(f"⚠️ ACP agent '{self.agent}' not found (optional)", file=sys.stderr)
    
    def chat(self, message: str, session_id: Optional[str] = None) -> str:
        """Send message to ACP agent"""
        cmd = self.SUPPORTED_AGENTS.get(self.agent, self.agent).split()
        cmd.extend(['--acp', '--message', message])
        
        if session_id:
            cmd.extend(['--session', session_id])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return result.stdout if result.stdout else result.stderr
        except subprocess.TimeoutExpired:
            return "ACP request timed out"
        except Exception as e:
            return f"ACP error: {e}"
    
    def exec_one_shot(self, task: str) -> str:
        """One-shot execution (no session persistence)"""
        cmd = self.SUPPORTED_AGENTS.get(self.agent, self.agent).split()
        cmd.extend(['--acp', 'exec', task])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout
        except:
            return f"Failed to execute: {task}"

acp_client = ACPClient()
