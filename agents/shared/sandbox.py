"""Container sandbox for agent isolation - inspired by NanoClaw"""

import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Dict

class ContainerSandbox:
    """Run agents in isolated containers"""
    
    def __init__(self, image: str = "python:3.12-slim"):
        self.image = image
        self.container_name = None
        self._check_docker()
    
    def _check_docker(self):
        try:
            subprocess.run(['docker', '--version'], capture_output=True, check=True)
            print("✅ Docker available for sandboxing", file=sys.stderr)
        except:
            print("⚠️ Docker not available - sandbox disabled", file=sys.stderr)
    
    def create(self, name: str, workspace: Optional[Path] = None) -> Dict:
        """Create a sandbox container"""
        self.container_name = f"clawpack-sandbox-{name}"
        
        cmd = [
            'docker', 'run', '-d',
            '--name', self.container_name,
            '--rm'
        ]
        
        if workspace:
            cmd.extend(['-v', f'{workspace.absolute()}:/workspace'])
            cmd.extend(['-w', '/workspace'])
        
        cmd.append(self.image)
        cmd.append('tail', '-f', '/dev/null')
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return {
                'success': True,
                'container': self.container_name,
                'command': f'docker exec -it {self.container_name} /bin/bash'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def exec_command(self, command: str) -> str:
        """Execute command inside sandbox"""
        if not self.container_name:
            return "No sandbox active"
        
        cmd = ['docker', 'exec', self.container_name, 'bash', '-c', command]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout if result.stdout else result.stderr
        except:
            return "Command execution failed"
    
    def destroy(self):
        """Destroy the sandbox"""
        if self.container_name:
            subprocess.run(['docker', 'rm', '-f', self.container_name], capture_output=True)

sandbox = ContainerSandbox()
