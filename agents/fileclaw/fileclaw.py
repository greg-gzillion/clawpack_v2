#!/usr/bin/env python3
"""FileClaw - Intelligent File Management Agent"""

import sys
import os
import json
import hashlib
import mimetypes
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from shared.base_agent import BaseAgent

class FileClawCore:
    """Core file handling logic - same pattern as other agents"""
    
    def __init__(self):
        self.supported_formats = {
            'document': ['.pdf', '.docx', '.txt', '.md', '.rtf', '.odt', '.html', '.xml'],
            'spreadsheet': ['.csv', '.xlsx', '.xls', '.ods'],
            'image': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp', '.tiff'],
            'code': ['.py', '.js', '.ts', '.rs', '.go', '.cpp', '.c', '.java', '.rb', '.php'],
            'data': ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg'],
            'archive': ['.zip', '.tar', '.gz', '.bz2', '.7z', '.rar'],
            'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
            'video': ['.mp4', '.mkv', '.avi', '.mov', '.wmv'],
        }
        self.llm = None
        self._init_llm()
    
    def _init_llm(self):
        try:
            from core.llm_manager import get_llm_manager
            self.llm = get_llm_manager()
        except:
            pass
    
    def analyze_file(self, file_path: str) -> Dict:
        """AI-powered file analysis - returns structured data"""
        path = Path(file_path)
        if not path.exists():
            return {'error': f'File not found: {file_path}'}
        
        # Basic metadata
        stat = path.stat()
        file_type = self._detect_type(path)
        
        result = {
            'name': path.name,
            'path': str(path.absolute()),
            'size_bytes': stat.st_size,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'type': file_type,
            'extension': path.suffix,
            'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'hash': self._calculate_hash(path),
            'readable': os.access(path, os.R_OK),
            'writable': os.access(path, os.W_OK),
        }
        
        # Deep analysis with AI
        if self.llm and file_type in ['document', 'code', 'data']:
            try:
                content = path.read_text(encoding='utf-8', errors='ignore')
                prompt = f"""Analyze this {file_type} file:

Filename: {path.name}
Content preview:
{content}

Provide a concise analysis:
1. What this file contains
2. Key information to extract
3. Recommended actions
4. Any issues or concerns

Keep it brief and practical."""
                
                ai_analysis = self.llm.chat_sync(prompt, task_type="analysis")
                result['ai_analysis'] = ai_analysis
            except:
                result['ai_analysis'] = "AI analysis not available"
        
        return result
    
    def convert_file(self, input_path: str, target_format: str) -> Dict:
        """Convert file between formats"""
        input_path = Path(input_path)
        if not input_path.exists():
            return {'error': f'File not found: {input_path}'}
        
        source_format = input_path.suffix[1:].lower()
        output_path = input_path.with_suffix(f'.{target_format}')
        
        try:
            # CSV ? JSON
            if source_format == 'csv' and target_format == 'json':
                import csv
                with open(input_path, 'r') as f:
                    data = list(csv.DictReader(f))
                output_path.write_text(json.dumps(data, indent=2))
                return {'success': True, 'output': str(output_path), 'rows': len(data)}
            
            elif source_format == 'json' and target_format == 'csv':
                import csv
                data = json.loads(input_path.read_text())
                if isinstance(data, list) and data:
                    with open(output_path, 'w', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=data[0].keys())
                        writer.writeheader()
                        writer.writerows(data)
                    return {'success': True, 'output': str(output_path), 'rows': len(data)}
            
            # Markdown ? Text
            elif source_format == 'md' and target_format == 'txt':
                output_path.write_text(input_path.read_text())
                return {'success': True, 'output': str(output_path)}
            
            else:
                return {'error': f'Conversion from {source_format} to {target_format} not yet supported'}
        
        except Exception as e:
            return {'error': str(e)}
    
    def batch_process(self, directory: str, operation: str) -> Dict:
        """Process multiple files in a directory"""
        dir_path = Path(directory)
        if not dir_path.exists() or not dir_path.is_dir():
            return {'error': f'Directory not found: {directory}'}
        
        files = [f for f in dir_path.iterdir() if f.is_file()]
        results = []
        
        for f in files:  # Limit to 20 files
            if operation == 'info':
                info = self.analyze_file(str(f))
                results.append({
                    'name': f.name,
                    'type': info.get('type', 'unknown'),
                    'size': info.get('size_mb', 0)
                })
            elif operation == 'analyze':
                info = self.analyze_file(str(f))
                results.append(info)
        
        return {
            'directory': str(dir_path),
            'total_files': len(files),
            'operation': operation,
            'processed': len(results),
            'results': results
        }
    
    def find_files(self, query: str, search_path: str = None) -> List[Dict]:
        """Find files by name, type, or content"""
        search_root = Path(search_path) if search_path else Path.home()
        results = []
        
        query_lower = query.lower()
        
        # Search by type
        if query_lower.startswith('type:'):
            file_type = query_lower.split(':')[1]
            for category, exts in self.supported_formats.items():
                if file_type in category or file_type in exts:
                    for f in search_root.rglob('*'):
                        if f.is_file() and f.suffix.lower() in exts:
                            results.append({
                                'name': f.name,
                                'path': str(f),
                                'size': f.stat().st_size,
                                'type': category
                            })
                            if len(results) >= 20:
                                break
                    break
        
        # Search by name pattern
        else:
            for f in search_root.rglob(f'*{query}*'):
                if f.is_file():
                    results.append({
                        'name': f.name,
                        'path': str(f),
                        'size': f.stat().st_size
                    })
                    if len(results) >= 20:
                        break
        
        return results
    
    def _detect_type(self, path: Path) -> str:
        """Detect file type"""
        suffix = path.suffix.lower()
        for file_type, extensions in self.supported_formats.items():
            if suffix in extensions:
                return file_type
        return 'unknown'
    
    def _calculate_hash(self, path: Path) -> str:
        """Calculate file hash"""
        try:
            with open(path, 'rb') as f:
                return hashlib.md5(f.read(1024*1024)).hexdigest()
        except:
            return 'N/A'

class FileClawAgent(BaseAgent):
    """FileClaw Agent - follows BaseAgent pattern"""
    
    def __init__(self):
        super().__init__("fileclaw")
        self.core = FileClawCore()
        self.description = "Intelligent file management and conversion"
    
    def handle(self, query: str) -> str:
        """Handle fileclaw commands"""
        query = query.strip().lower()
        
        if query.startswith("/analyze"):
            return self._analyze(query)
        elif query.startswith("/convert"):
            return self._convert(query)
        elif query.startswith("/batch"):
            return self._batch(query)
        elif query.startswith("/find"):
            return self._find(query)
        elif query.startswith("/info"):
            return self._info(query)
        else:
            return self._help()
    
    def _analyze(self, cmd: str) -> str:
        parts = cmd.split(maxsplit=1)
        if len(parts) < 2:
            return "Usage: /analyze <file_path>"
        
        result = self.core.analyze_file(parts[1])
        if 'error' in result:
            return f"? {result['error']}"
        
        output = f"""
+------------------------------------------------------------------+
¦  FILE ANALYSIS: {result['name']}
+------------------------------------------------------------------+

?? BASIC INFO:
    Type: {result['type']}
    Size: {result['size_mb']} MB
    Modified: {result['modified']}
    Hash: {result['hash']}

"""
        if 'ai_analysis' in result:
            output += f"?? AI INSIGHTS:\n{result['ai_analysis']}\n"
        
        output += "\n?? Use /convert to change format, /batch for multiple files"
        return output
    
    def _convert(self, cmd: str) -> str:
        parts = cmd.split()
        if len(parts) < 3:
            return "Usage: /convert <input> <output_format>\nExample: /convert data.csv json"
        
        result = self.core.convert_file(parts[1], parts[2])
        if 'error' in result:
            return f"? {result['error']}"
        
        return f"? Converted successfully!\n?? Output: {result['output']}\n?? Rows: {result.get('rows', 'N/A')}"
    
    def _batch(self, cmd: str) -> str:
        parts = cmd.split(maxsplit=2)
        if len(parts) < 3:
            return "Usage: /batch <directory> <operation>\nOperations: info, analyze"
        
        result = self.core.batch_process(parts[1], parts[2])
        if 'error' in result:
            return f"? {result['error']}"
        
        output = f"""
+------------------------------------------------------------------+
¦  BATCH PROCESSING: {Path(result['directory']).name}
+------------------------------------------------------------------+

?? Total files: {result['total_files']}
?? Operation: {result['operation']}
? Processed: {result['processed']}

{'-' * 50}
"""
        for r in result['results']:
            if isinstance(r, dict):
                output += f"   {r.get('name', 'unknown')} ({r.get('type', '?')}, {r.get('size', 0)} MB)\n"
        
        return output
    
    def _find(self, cmd: str) -> str:
        parts = cmd.split(maxsplit=2)
        if len(parts) < 2:
            return "Usage: /find <query> [search_path]\nExample: /find type:image\n       /find report.pdf"
        
        query = parts[1]
        search_path = parts[2] if len(parts) > 2 else None
        
        results = self.core.find_files(query, search_path)
        if not results:
            return f"No files found matching: {query}"
        
        output = f"?? FOUND {len(results)} FILES:\n"
        for r in results:
            size_mb = r.get('size', 0) / (1024 * 1024)
            output += f"   {r['name']} ({size_mb:.2f} MB)\n"
            output += f"    {r['path']}\n"
        
        return output
    
    def _info(self, cmd: str) -> str:
        parts = cmd.split(maxsplit=1)
        if len(parts) < 2:
            return "Usage: /info <file_path>"
        
        result = self.core.analyze_file(parts[1])
        if 'error' in result:
            return f"? {result['error']}"
        
        return f"""
?? {result['name']}
   Type: {result['type']}
   Size: {result['size_mb']} MB
   Modified: {result['modified']}
   Path: {result['path']}
"""
    

    def collaborate(self, target_agent: str, task: str) -> str:
        """Collaborate with another agent via A2A"""
        try:
            import requests
            response = requests.post(
                f"http://127.0.0.1:8766/v1/message/{target_agent}",
                json={"task": task},
                timeout=60
            )
            if response.status_code == 200:
                result = response.json()
                return f"?? {target_agent.upper()} responded:
{result.get('result', 'No result')}"
            return f"? Agent {target_agent} not responding"
        except Exception as e:
            return f"? Collaboration error: {e}"

    def _help(self):
        return """
+------------------------------------------------------------------+
¦  FILECLAW - Intelligent File Management Agent                    ¦
¦------------------------------------------------------------------¦
¦                                                                  ¦
¦  COMMANDS:                                                       ¦
¦    /analyze <file>     - AI-powered file analysis               ¦
¦    /convert <in> <out> - Convert between formats                ¦
¦    /batch <dir> <op>   - Batch process directory                ¦
¦    /find <query>       - Find files by name/type                ¦
¦    /info <file>        - Quick file info                        ¦
¦                                                                  ¦
¦  SUPPORTED FORMATS: 50+ file types across 8 categories          ¦
¦  AI INTEGRATION:    Uses LLM for deep file analysis             ¦
¦                                                                  ¦
¦  EXAMPLES:                                                      ¦
¦    /analyze contract.pdf                                        ¦
¦    /convert data.csv json                                       ¦
¦    /batch ./docs analyze                                        ¦
¦    /find type:image                                             ¦
¦                                                                  ¦
+------------------------------------------------------------------+"""

def main():
    agent = FileClawAgent()
    if len(sys.argv) > 1:
        print(agent.handle(' '.join(sys.argv[1:])))
    else:
        print(agent._help())

if __name__ == "__main__":
    main()
