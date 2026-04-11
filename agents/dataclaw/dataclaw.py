#!/usr/bin/env python3
"""DataClaw - Local Reference Manager for PDFs, Ebooks, Videos, Music"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent to path
CLAWPACK_ROOT = Path("/home/greg/dev/clawpack_v2")
sys.path.insert(0, str(CLAWPACK_ROOT))

from modules.scanner.file_scanner import FileScanner
from modules.indexer.local_indexer import LocalIndexer
from modules.search.local_search import LocalSearch
from modules.metadata.extractor import MetadataExtractor

class DataClaw:
    def __init__(self):
        self.scanner = FileScanner()
        self.indexer = LocalIndexer()
        self.searcher = LocalSearch()
        self.metadata = MetadataExtractor()
    
    def scan(self, directory=None):
        """Scan a directory for media files"""
        if directory:
            results = self.scanner.scan_directory(Path(directory))
        else:
            results = self.scanner.scan_all_data_dirs()
        
        return self._format_scan_results(results)
    
    def index(self, directory=None):
        """Index local files into chronicle"""
        files = self.scanner.scan_directory(Path(directory)) if directory else []
        
        indexed = 0
        for file_info in files:
            if self.indexer.index_file(file_info):
                indexed += 1
        
        return f"✅ Indexed {indexed} of {len(files)} files into chronicle"
    
    def search(self, query, file_type=None):
        """Search local files"""
        results = self.searcher.search_files(query, file_type)
        if not results:
            return "No files found"
        
        output = f"🔍 Found {len(results)} files matching '{query}':\n"
        for r in results[:10]:
            output += f"  • {r['name']} ({r['size_mb']} MB)\n"
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
    
    def add_reference(self, file_path, category=None):
        """Add a file to local reference library"""
        src = Path(file_path)
        if not src.exists():
            return f"❌ File not found: {file_path}"
        
        # Determine category
        if not category:
            suffix = src.suffix.lower()
            for cat, exts in self.scanner.SUPPORTED_TYPES.items():
                if suffix in exts:
                    category = cat
                    break
        
        if not category:
            return f"❌ Unknown file type: {suffix}"
        
        # Copy to data directory
        dest = self.scanner.data_root / category / src.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        import shutil
        shutil.copy2(src, dest)
        
        # Index the file
        file_info = self.scanner.get_file_info(dest)
        self.indexer.index_file(file_info)
        
        return f"✅ Added {src.name} to {category} library\n   Location: {dest}"
    
    def help(self):
        return """
╔══════════════════════════════════════════════════════════════════╗
║                      DATACLAW - Local Reference Manager          ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  COMMANDS:                                                       ║
║    scan [directory]         - Scan for media files              ║
║    index [directory]        - Index files into chronicle        ║
║    search <query> [type]    - Search local files                ║
║    search-content <query>   - Search within file contents       ║
║    add <file> [category]    - Add file to reference library     ║
║    stats                    - Show statistics                   ║
║                                                                  ║
║  CATEGORIES: documents, ebooks, videos, music, images           ║
║                                                                  ║
║  INTEGRATION COMMANDS:                                           ║
║    sync                     - Sync with webclaw chronicle        ║
║    agents                   - List all connected agents          ║
║    share <agent> <file>     - Share file with another agent      ║
║    agent-context <agent> <q> - Get context for agent             ║
║    unified-search <query>   - Search local + chronicle          ║
║                                                                  ║
║  EXAMPLES:                                                       ║
║    python dataclaw.py add ~/Downloads/thesis.pdf documents      ║
║    python dataclaw.py scan ~/MyDocuments                        ║
║    python dataclaw.py search "blockchain"                       ║
║    python dataclaw.py sync                                      ║
║    python dataclaw.py agents                                    ║
║    python dataclaw.py share flowclaw my_diagram.png             ║
║    python dataclaw.py unified-search "smart contract"           ║
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
    
    if cmd == "scan":
        directory = args[0] if args else None
        print(agent.scan(directory))
    
    elif cmd == "index":
        directory = args[0] if args else None
        print(agent.index(directory))
    
    elif cmd == "search":
        if not args:
            print("Usage: search <query> [file_type]")
            return
        query = args[0]
        file_type = args[1] if len(args) > 1 else None
        print(agent.search(query, file_type))
    
    elif cmd == "search-content":
        if not args:
            print("Usage: search-content <query> [directory]")
            return
        query = args[0]
        directory = args[1] if len(args) > 1 else None
        print(agent.search_content(query, directory))
    
    elif cmd == "add":
        if not args:
            print("Usage: add <file_path> [category]")
            return
        file_path = args[0]
        category = args[1] if len(args) > 1 else None
        print(agent.add_reference(file_path, category))
    

    elif cmd == "sync":
        print(agent.sync_with_webclaw())
    
    elif cmd == "agents":
        print(agent.list_agents())
    
    elif cmd == "share" and len(args) >= 2:
        print(agent.share_with_agent(args[0], args[1]))
    
    elif cmd == "agent-context" and len(args) >= 2:
        print(agent.get_agent_context(args[0], args[1]))
    
    elif cmd == "unified-search" and args:
        print(agent.unified_search(' '.join(args)))

    elif cmd == "stats":
        print(agent.stats())
    
    else:
        print(agent.help())

if __name__ == "__main__":
    main()

    def sync_with_webclaw(self):
        """Sync local references with webclaw chronicle"""
        from modules.integration.agent_hub import agent_hub
        
        # Get all scanned files
        all_files = self.scanner.scan_all_data_dirs()
        
        synced = 0
        for file_type, files in all_files.items():
            for file_info in files:
                if agent_hub.sync_to_webclaw(file_info):
                    synced += 1
        
        return f"✅ Synced {synced} local files to webclaw chronicle"
    
    def get_agent_context(self, agent_name, query):
        """Get local reference context for another agent"""
        from modules.integration.agent_hub import agent_hub
        
        if agent_name not in agent_hub.get_agent_list():
            return f"Agent '{agent_name}' not found. Available: {', '.join(agent_hub.get_agent_list())}"
        
        context = agent_hub.provide_context_to_agent(agent_name, query)
        if context:
            return context
        return f"No local references found for '{query}' to share with {agent_name}"
    
    def list_agents(self):
        """List all available agents DataClaw can integrate with"""
        from modules.integration.agent_hub import agent_hub
        agents = agent_hub.get_agent_list()
        return "🤝 Connected Agents:\n" + "\n".join(f"  • {a}" for a in agents)
    
    def share_with_agent(self, agent_name, file_path):
        """Share a local file reference with another agent"""
        from modules.integration.agent_hub import agent_hub
        
        # First add the file locally
        result = self.add_reference(file_path)
        
        # Then sync with webclaw for the target agent
        agent_hub.sync_to_webclaw({'path': file_path, 'name': Path(file_path).name})
        
        return f"✅ Shared {Path(file_path).name} with {agent_name}\n   File added to local library and synced with chronicle"
    
    def unified_search(self, query):
        """Search across local files and webclaw chronicle"""
        from modules.integration.agent_hub import agent_hub
        from shared.chronicle_helper import search_chronicle
        
        # Search local files
        local_results = self.searcher.search_files(query, None)
        
        # Search chronicle
        chronicle_results = []
        try:
            chronicle_results = search_chronicle(query, 5)
        except:
            pass
        
        output = f"🔍 UNIFIED SEARCH RESULTS for '{query}':\n\n"
        
        output += "📁 LOCAL FILES:\n"
        if local_results:
            for r in local_results[:5]:
                output += f"  • {r['name']} ({r['size_mb']} MB)\n"
        else:
            output += "  No local files found\n"
        
        output += "\n🌐 CHRONICLE REFERENCES:\n"
        if chronicle_results:
            for r in chronicle_results[:5]:
                url = getattr(r, 'url', str(r))
                output += f"  • {url[:80]}...\n"
        else:
            output += "  No chronicle references found\n"
        
        return output
