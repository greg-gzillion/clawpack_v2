"""MCP Server Registry - manage MCP tools"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class MCPServer:
    name: str
    command: str
    args: List[str]
    enabled: bool = True
    description: str = ""

class MCPRegistry:
    """Manage MCP servers and tools"""
    
    # Popular MCP servers
    BUILTIN_SERVERS = {
        'filesystem': {
            'command': 'npx',
            'args': ['-y', '@modelcontextprotocol/server-filesystem', '/tmp'],
            'description': 'File system operations'
        },
        'github': {
            'command': 'npx',
            'args': ['-y', '@modelcontextprotocol/server-github'],
            'description': 'GitHub API integration'
        },
        'brave-search': {
            'command': 'npx',
            'args': ['-y', '@modelcontextprotocol/server-brave-search'],
            'description': 'Web search via Brave'
        },
        'postgres': {
            'command': 'npx',
            'args': ['-y', '@modelcontextprotocol/server-postgres'],
            'description': 'PostgreSQL database access'
        },
        'sqlite': {
            'command': 'npx',
            'args': ['-y', '@modelcontextprotocol/server-sqlite'],
            'description': 'SQLite database access'
        }
    }
    
    def __init__(self):
        self.servers: Dict[str, MCPServer] = {}
        self.config_path = Path.home() / ".clawpack/mcp/servers.json"
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self._load()
    
    def _load(self):
        if self.config_path.exists():
            data = json.loads(self.config_path.read_text())
            for name, server_data in data.items():
                self.servers[name] = MCPServer(
                    name=name,
                    command=server_data['command'],
                    args=server_data.get('args', []),
                    enabled=server_data.get('enabled', True),
                    description=server_data.get('description', '')
                )
    
    def _save(self):
        data = {}
        for name, server in self.servers.items():
            data[name] = {
                'command': server.command,
                'args': server.args,
                'enabled': server.enabled,
                'description': server.description
            }
        self.config_path.write_text(json.dumps(data, indent=2))
    
    def install(self, name: str) -> str:
        """Install an MCP server"""
        if name in self.BUILTIN_SERVERS:
            server_data = self.BUILTIN_SERVERS[name]
            self.servers[name] = MCPServer(
                name=name,
                command=server_data['command'],
                args=server_data['args'],
                description=server_data['description']
            )
            self._save()
            return f"✅ Installed MCP server: {name}"
        return f"❌ Unknown MCP server: {name}"
    
    def list_servers(self) -> str:
        """List all installed MCP servers"""
        if not self.servers:
            return "No MCP servers installed. Run: mcp install <name>"
        
        output = "📦 MCP Servers:\n"
        for name, server in self.servers.items():
            status = "✅" if server.enabled else "❌"
            output += f"  {status} {name}: {server.description}\n"
        return output
    
    def enable(self, name: str) -> str:
        if name in self.servers:
            self.servers[name].enabled = True
            self._save()
            return f"✅ Enabled MCP server: {name}"
        return f"❌ Server not found: {name}"
    
    def disable(self, name: str) -> str:
        if name in self.servers:
            self.servers[name].enabled = False
            self._save()
            return f"✅ Disabled MCP server: {name}"
        return f"❌ Server not found: {name}"

mcp_registry = MCPRegistry()
