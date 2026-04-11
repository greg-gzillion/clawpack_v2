#!/usr/bin/env python3
"""RustyPyCraw - Hybrid Code Crawler Agent for Clawpack v2"""

import sys
import asyncio
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.scanner.code_scanner import CodeScanner
from modules.analyzer.code_analyzer import CodeAnalyzer
from modules.llm.groq_client import GroqClient
from modules.crawler.ast_crawler import ASTCrawler
from modules.indexer.chronicle_indexer import ChronicleIndexer
from a2a.client import A2AClient

class RustyPyCraw:
    """Hybrid Rust+Python code crawler with A2A and chronicle integration"""
    
    def __init__(self):
        self.scanner = CodeScanner()
        self.analyzer = CodeAnalyzer()
        self.llm = GroqClient()
        self.crawler = ASTCrawler()
        self.indexer = ChronicleIndexer()
        self.a2a = A2AClient()
        self._init_components()
    
    def _init_components(self):
        """Initialize all components"""
        print("🦀 RustyPyCraw Agent Initializing...")
        self.scanner.init()
        self.analyzer.init()
        self.indexer.init()
        print("✅ RustyPyCraw Ready")
    
    def scan_codebase(self, path: str, language: str = None) -> Dict:
        """Scan a codebase for analysis"""
        return self.scanner.scan(path, language)
    
    def analyze(self, path: str, analysis_type: str = "stats") -> Dict:
        """Analyze codebase structure"""
        return self.analyzer.analyze(path, analysis_type)
    
    def search(self, path: str, query: str) -> List[Dict]:
        """Search codebase for patterns"""
        return self.crawler.search(path, query)
    
    def pinch(self, path: str) -> List[str]:
        """Find unnecessary clone() calls in Rust"""
        return self.analyzer.find_unnecessary_clones(path)
    
    def ask(self, question: str, context: str = None) -> str:
        """Ask LLM about code"""
        return self.llm.ask(question, context)
    
    def index_codebase(self, path: str) -> Dict:
        """Index codebase into chronicle"""
        return self.indexer.index_codebase(path)
    
    def search_index(self, query: str, limit: int = 10) -> List[Dict]:
        """Search chronicle for code references"""
        return self.indexer.search(query, limit)
    
    def a2a_health(self) -> Dict:
        """Check A2A server health"""
        return self.a2a.health()
    
    def a2a_chat(self, task: str) -> Dict:
        """Send task to other agents via A2A"""
        return self.a2a.chat(task)
    
    def process(self, command: str, *args) -> str:
        """Process commands"""
        if command == "scan" and args:
            result = self.scan_codebase(args[0])
            return self._format_result(result)
        
        elif command == "analyze" and len(args) >= 1:
            analysis_type = args[1] if len(args) > 1 else "stats"
            result = self.analyze(args[0], analysis_type)
            return self._format_result(result)
        
        elif command == "search" and len(args) >= 2:
            result = self.search(args[0], args[1])
            return self._format_search_results(result)
        
        elif command == "pinch" and args:
            result = self.pinch(args[0])
            return self._format_pinch_results(result)
        
        elif command == "ask" and args:
            question = ' '.join(args)
            result = self.ask(question)
            return result
        
        elif command == "index" and args:
            result = self.index_codebase(args[0])
            return f"✅ Indexed {result.get('files', 0)} files to chronicle"
        
        elif command == "search-index" and args:
            result = self.search_index(' '.join(args))
            return self._format_index_results(result)
        
        elif command == "a2a-status":
            result = self.a2a_health()
            return f"📡 A2A Server: {result.get('status', 'unknown')}"
        
        elif command == "a2a-chat" and args:
            result = self.a2a_chat(' '.join(args))
            return f"🦞 A2A Response: {result.get('message', 'No response')}"
        
        else:
            return self.help()
    
    def _format_result(self, result: Dict) -> str:
        """Format analysis result for display"""
        if not result:
            return "No results found"
        
        output = f"📊 Analysis Results:\n"
        output += f"   Files: {result.get('files', 0)}\n"
        output += f"   Lines: {result.get('lines', 0)}\n"
        output += f"   Languages: {', '.join(result.get('languages', []))}\n"
        return output
    
    def _format_search_results(self, results: List[Dict]) -> str:
        """Format search results"""
        if not results:
            return "No matches found"
        
        output = f"🔍 Found {len(results)} matches:\n"
        for r in results[:10]:
            output += f"   • {r.get('file', 'unknown')}:{r.get('line', 0)}\n"
            output += f"     {r.get('content', '')[:80]}...\n"
        return output
    
    def _format_pinch_results(self, results: List[str]) -> str:
        """Format pinch mode results"""
        if not results:
            return "🦞 No unnecessary .clone() calls found!"
        
        output = f"🔧 Found {len(results)} potential optimizations:\n"
        for r in results[:10]:
            output += f"   • {r}\n"
        return output
    
    def _format_index_results(self, results: List[Dict]) -> str:
        """Format index search results"""
        if not results:
            return "No indexed results found"
        
        output = f"📚 Found {len(results)} indexed references:\n"
        for r in results[:5]:
            output += f"   • {r.get('path', 'unknown')}\n"
        return output
    
    def help(self) -> str:
        return """
╔══════════════════════════════════════════════════════════════════╗
║              RUSTYPYCRAW - Hybrid Code Crawler Agent             ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  COMMANDS:                                                       ║
║    scan <path>              - Scan codebase for analysis        ║
║    analyze <path> [type]    - Analyze code structure            ║
║    search <path> <query>    - Search for patterns               ║
║    pinch <path>             - Find unnecessary .clone() calls   ║
║    ask <question>           - Ask LLM about code                ║
║    index <path>             - Index codebase to chronicle       ║
║    search-index <query>     - Search chronicle index            ║
║    a2a-status               - Check A2A server status           ║
║    a2a-chat <task>          - Chat with other agents via A2A    ║
║                                                                  ║
║  ANALYSIS TYPES: stats, security, dependencies, complexity      ║
║                                                                  ║
║  EXAMPLES:                                                       ║
║    python rustypycraw.py scan ~/dev/TX                          ║
║    python rustypycraw.py pinch ~/dev/TX/contracts               ║
║    python rustypycraw.py ask "What does this function do?"      ║
║    python rustypycraw.py index ~/dev/TX                         ║
║    python rustypycraw.py a2a-chat "analyze my code"             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝"""

def main():
    agent = RustyPyCraw()
    
    if len(sys.argv) < 2:
        print(agent.help())
        return
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    result = agent.process(command, *args)
    print(result)

if __name__ == "__main__":
    main()
