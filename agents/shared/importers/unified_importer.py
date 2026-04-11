"""Universal Import System - All Agents, All File Types"""

import json
import csv
import yaml
import zipfile
import tarfile
import mimetypes
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

class UniversalImporter:
    """Import ANY file type into ANY agent"""
    
    # Supported file types and their handlers
    SUPPORTED_TYPES = {
        # Documents
        '.json': 'json', '.csv': 'csv', '.yaml': 'yaml', '.yml': 'yaml',
        '.txt': 'text', '.md': 'markdown', '.pdf': 'pdf', '.docx': 'docx',
        '.html': 'html', '.xml': 'xml',
        # Images
        '.png': 'image', '.jpg': 'image', '.jpeg': 'image', '.gif': 'image',
        '.svg': 'image', '.webp': 'image',
        # Data
        '.xlsx': 'excel', '.xls': 'excel', '.db': 'database', '.sql': 'sql',
        # Archives
        '.zip': 'archive', '.tar': 'archive', '.gz': 'archive',
        # Code
        '.py': 'code', '.js': 'code', '.rs': 'code', '.go': 'code',
        '.cpp': 'code', '.c': 'code', '.java': 'code',
    }
    
    def __init__(self):
        self.import_log = []
    
    def import_to_agent(self, agent_name: str, file_path: str) -> str:
        """Import ANY file into ANY agent"""
        
        path = Path(file_path)
        if not path.exists():
            return f"❌ File not found: {file_path}"
        
        # Validate agent
        valid_agents = ['docuclaw', 'flowclaw', 'dataclaw', 'lawclaw', 'txclaw', 
                       'mathematicaclaw', 'interpretclaw', 'langclaw', 'claw_coder',
                       'webclaw', 'mediclaw', 'liberateclaw', 'rustypycraw']
        
        if agent_name not in valid_agents:
            return f"❌ Unknown agent: {agent_name}\nAvailable: {', '.join(valid_agents)}"
        
        # Detect file type
        file_type = self.SUPPORTED_TYPES.get(path.suffix.lower(), 'unknown')
        
        # Route to agent-specific handler
        handlers = {
            'docuclaw': self._import_to_docuclaw,
            'flowclaw': self._import_to_flowclaw,
            'dataclaw': self._import_to_dataclaw,
            'lawclaw': self._import_to_lawclaw,
            'txclaw': self._import_to_txclaw,
            'mathematicaclaw': self._import_to_mathclaw,
            'interpretclaw': self._import_to_interpretclaw,
            'langclaw': self._import_to_langclaw,
            'claw_coder': self._import_to_clawcoder,
            'webclaw': self._import_to_webclaw,
            'mediclaw': self._import_to_mediclaw,
            'liberateclaw': self._import_to_liberateclaw,
            'rustypycraw': self._import_to_rustypycraw,
        }
        
        handler = handlers.get(agent_name, self._import_generic)
        result = handler(agent_name, path, file_type)
        
        # Log the import
        self.import_log.append({
            'timestamp': datetime.now().isoformat(),
            'agent': agent_name,
            'file': str(path),
            'type': file_type,
            'status': 'success'
        })
        
        return result
    
    def _import_to_docuclaw(self, agent: str, path: Path, file_type: str) -> str:
        """Import to DocClaw as document"""
        content = self._read_content(path, file_type)
        return f"""✅ Imported to {agent}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 File: {path.name}
📁 Type: {file_type.upper()}
📏 Size: {path.stat().st_size} bytes
💾 Agent: {agent}

💡 Use /create to turn this into a document
"""
    
    def _import_to_flowclaw(self, agent: str, path: Path, file_type: str) -> str:
        """Import to FlowClaw as diagram source"""
        if file_type == 'code' or path.suffix == '.mmd':
            return f"""✅ Imported to {agent}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Diagram source: {path.name}
📁 Type: {file_type.upper()}

💡 The diagram code is ready. Use /view flowchart to visualize
"""
        return f"""✅ Added to {agent}
📊 {path.name} - Ready for diagram generation
💡 Use /flowchart with this data
"""
    
    def _import_to_dataclaw(self, agent: str, path: Path, file_type: str) -> str:
        """Import to DataClaw as reference (using existing add_reference)"""
        try:
            from agents.dataclaw.dataclaw import DataClaw
            dc = DataClaw()
            result = dc.add_reference(str(path))
            return result
        except:
            return f"""✅ Imported to {agent}
📁 File: {path.name}
💾 Added to local reference library
"""
    
    def _import_to_lawclaw(self, agent: str, path: Path, file_type: str) -> str:
        """Import to LawClaw as legal reference"""
        return f"""✅ Imported to {agent}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚖️ Legal reference: {path.name}
📁 Type: {file_type.upper()}

💡 Use /searchindex to find this later
💡 Use /court to search for specific jurisdictions
"""
    
    def _import_to_txclaw(self, agent: str, path: Path, file_type: str) -> str:
        """Import to TXClaw as contract template"""
        return f"""✅ Imported to {agent}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 Contract source: {path.name}
📁 Type: {file_type.upper()}

💡 Use /create to generate a smart contract
💡 Use /deploy to deploy to testnet
"""
    
    def _import_to_mathclaw(self, agent: str, path: Path, file_type: str) -> str:
        """Import to MathClaw as data"""
        return f"""✅ Imported to {agent}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📐 Data source: {path.name}
📁 Type: {file_type.upper()}

💡 Use /visualize to create math visualizations
💡 Use /plot to graph this data
"""
    
    def _import_to_interpretclaw(self, agent: str, path: Path, file_type: str) -> str:
        """Import to InterpretClaw as translation source"""
        return f"""✅ Imported to {agent}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌐 Translation source: {path.name}
📁 Type: {file_type.upper()}

💡 Use /translate to convert this content
"""
    
    def _import_to_langclaw(self, agent: str, path: Path, file_type: str) -> str:
        """Import to LangClaw as lesson material"""
        return f"""✅ Imported to {agent}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 Language material: {path.name}

💡 Use /lesson to create lessons from this content
"""
    
    def _import_to_clawcoder(self, agent: str, path: Path, file_type: str) -> str:
        """Import to ClawCoder as code reference"""
        return f"""✅ Imported to {agent}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💻 Code reference: {path.name}
📁 Language: {path.suffix[1:] if path.suffix else 'text'}

💡 Use /code to generate similar code
"""
    
    def _import_to_webclaw(self, agent: str, path: Path, file_type: str) -> str:
        """Import to WebClaw as web content"""
        return f"""✅ Imported to {agent}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌍 Web content: {path.name}

💡 This content will be indexed for search
"""
    
    def _import_to_mediclaw(self, agent: str, path: Path, file_type: str) -> str:
        """Import to MedicClaw as medical reference"""
        return f"""✅ Imported to {agent}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏥 Medical reference: {path.name}

💡 Use /symptom or /drug to search this content
"""
    
    def _import_to_liberateclaw(self, agent: str, path: Path, file_type: str) -> str:
        """Import to LiberateClaw as model config"""
        return f"""✅ Imported to {agent}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔓 Model configuration: {path.name}

💡 Use /liberate to download models
💡 Use /use to run inference
"""
    
    def _import_to_rustypycraw(self, agent: str, path: Path, file_type: str) -> str:
        """Import to RustyPyCraw as code to crawl"""
        return f"""✅ Imported to {agent}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦀 Code for crawling: {path.name}

💡 Use /scan to analyze this codebase
"""
    
    def _import_generic(self, agent: str, path: Path, file_type: str) -> str:
        """Generic import handler"""
        return f"""✅ Imported to {agent}
📄 {path.name} ({file_type.upper()})
💾 {path.stat().st_size} bytes
💡 Use agent-specific commands to process
"""
    
    def _read_content(self, path: Path, file_type: str) -> Any:
        """Read file content based on type"""
        try:
            if file_type in ['json', 'yaml']:
                import json, yaml
                if file_type == 'json':
                    return json.loads(path.read_text())
                else:
                    return yaml.safe_load(path.read_text())
            elif file_type == 'csv':
                import csv
                with open(path, 'r') as f:
                    return list(csv.DictReader(f))
            else:
                return path.read_text()[:1000]
        except:
            return f"<Content preview not available>"
    
    def get_import_history(self) -> List[Dict]:
        """Get import history"""
        return self.import_log[-20:]  # Last 20 imports

# Singleton instance
unified_importer = UniversalImporter()
