#!/usr/bin/env python3
"""DataClaw - Local Reference Manager for PDFs, Ebooks, Videos, Music, and Documentation"""

import sys
import shutil
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.scanner.file_scanner import FileScanner
from modules.indexer.local_indexer import LocalIndexer
from modules.search.local_search import LocalSearch

class DataClaw:
    def __init__(self):
        self.scanner = FileScanner()
        self.indexer = LocalIndexer()
        self.searcher = LocalSearch()
    
    def add_reference(self, path, category=None):
        """Add a file or directory to local reference library"""
        src_path = Path(path)
        if not src_path.exists():
            return f"❌ Path not found: {path}"
        
        # Determine category if not provided
        if not category:
            if src_path.is_file():
                suffix = src_path.suffix.lower()
                for cat, exts in self.scanner.SUPPORTED_TYPES.items():
                    if suffix in exts:
                        category = cat
                        break
            else:
                category = "documents"
        
        # Handle directories
        if src_path.is_dir():
            dest_dir = self.scanner.data_root / category / src_path.name
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            file_count = 0
            for file_path in src_path.rglob('*'):
                if file_path.is_file():
                    try:
                        shutil.copy2(file_path, dest_dir / file_path.name)
                        file_count += 1
                    except:
                        pass
            
            # Index the directory
            self.indexer.index_directory(dest_dir)
            
            return f"✅ Added directory '{src_path.name}' to {category}\n   📁 Copied {file_count} files\n   📍 Location: {dest_dir}"
        
        # Handle single file
        else:
            dest = self.scanner.data_root / category / src_path.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dest)
            
            file_info = self.scanner.get_file_info(dest)
            self.indexer.index_file(file_info)
            
            return f"✅ Added {src_path.name} to {category}\n   📁 Location: {dest}"
    
    def scan(self, directory=None):
        """Scan a directory for media files"""
        if directory:
            results = self.scanner.scan_directory(Path(directory))
        else:
            results = self.scanner.scan_all_data_dirs()
        return self._format_scan_results(results)
    
    def index(self, directory=None):
        """Index local files into chronicle"""
        if directory:
            path = Path(directory)
            if path.is_dir():
                return self.indexer.index_directory(path)
            else:
                files = self.scanner.scan_directory(path)
                indexed = 0
                for file_info in files:
                    if self.indexer.index_file(file_info):
                        indexed += 1
                return f"✅ Indexed {indexed} of {len(files)} files"
        else:
            return self.indexer.index_all()
    
    def search(self, query, file_type=None):
        """Search local files"""
        results = self.searcher.search_files(query, file_type)
        if not results:
            return f"No files found for '{query}'"
        
        output = f"🔍 Found {len(results)} files matching '{query}':\n"
        for r in results[:10]:
            output += f"  • {r['name']} ({r.get('size_mb', 0)} MB)\n"
            output += f"    {r['path']}\n"
        return output
    
    def search_content(self, query, directory=None):
        """Search within file contents"""
        results = self.searcher.full_text_search(query, Path(directory) if directory else None)
        if not results:
            return f"No content found for '{query}'"
        
        output = f"📄 Found {len(results)} matches for '{query}':\n"
        for r in results[:10]:
            output += f"  • {r['file']}\n"
            output += f"    Line {r['line']}: {r['context'][:80]}...\n"
        return output
    
    def stats(self):
        """Get statistics"""
        stats = self.scanner.get_statistics()
        output = f"""
╔══════════════════════════════════════════════════════════════════╗
║                      DATACLAW STATISTICS                         ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  📊 Total Files: {stats['total_files']}                                         ║
║  💾 Total Size: {stats['total_size_mb']:.2f} MB                                    ║
║                                                                  ║
"""
        for type_name, type_stats in stats['by_type'].items():
            output += f"  📁 {type_name.title()}: {type_stats['count']} files, {type_stats['size_mb']:.2f} MB\n"
        
        output += "╚══════════════════════════════════════════════════════════════════╝"
        return output
    
    def list_agents(self):
        """List connected agents"""
        agents = ['webclaw', 'flowclaw', 'docuclaw', 'txclaw', 'mathematicaclaw']
        return "🤝 Connected Agents:\n" + "\n".join(f"  • {a}" for a in agents)
    
    def help(self):
        return """
╔══════════════════════════════════════════════════════════════════╗
║                      DATACLAW - Local Reference Manager          ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  COMMANDS:                                                       ║
║    add <path> [category]     - Add file or directory            ║
║    scan [directory]          - Scan for media files              ║
║    index [directory]         - Index files into chronicle        ║
║    search <query> [type]     - Search local files                ║
║    search-content <query>    - Search within file contents       ║
║    stats                     - Show statistics                   ║
║    agents                    - List connected agents             ║
║                                                                  ║
║  CATEGORIES: documents, ebooks, videos, music, images           ║
║                                                                  ║
║  EXAMPLES:                                                       ║
║    python dataclaw.py add ~/TXdocumentation docs                ║
║    python dataclaw.py search "smart contract"                   ║
║    python dataclaw.py stats                                     ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝"""

def main():
    agent = DataClaw()
    
    if len(sys.argv) < 2:
        print(agent.help())
        return
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    if cmd == "add" and args:
        category = args[1] if len(args) > 1 else None
        print(agent.add_reference(args[0], category))
    
    elif cmd == "scan":
        directory = args[0] if args else None
        print(agent.scan(directory))
    
    elif cmd == "index":
        directory = args[0] if args else None
        print(agent.index(directory))
    
    elif cmd == "search" and args:
        query = args[0]
        file_type = args[1] if len(args) > 1 else None
        print(agent.search(query, file_type))
    
    elif cmd == "search-content" and args:
        query = args[0]
        directory = args[1] if len(args) > 1 else None
        print(agent.search_content(query, directory))
    
    elif cmd == "stats":
        print(agent.stats())
    
    elif cmd == "agents":
        print(agent.list_agents())
    
    else:
        print(agent.help())

if __name__ == "__main__":
    main()
