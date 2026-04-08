#!/usr/bin/env python3
"""DATACLAW - Local Data Reference Agent"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

class DataClaw:
    def __init__(self):
        self.references_path = Path(__file__).parent / "references"
        self.references_path.mkdir(exist_ok=True)
        self.db_path = self.references_path / "data_index.db"
        self._init_db()
        self.running = True

    def _init_db(self):
        """Initialize SQLite index for references"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS data_refs (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE,
                    category TEXT,
                    file_path TEXT,
                    size INTEGER,
                    created TEXT,
                    tags TEXT
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_category ON data_refs(category)")

    def _index_references(self):
        """Index all .md and .json files in references folder"""
        indexed = 0
        for file in self.references_path.rglob("*"):
            if file.suffix in ['.md', '.json', '.txt', '.csv']:
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute("""
                        INSERT OR REPLACE INTO data_refs (name, category, file_path, size, created, tags)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (file.name, file.parent.name, str(file), file.stat().st_size, 
                          datetime.now().isoformat(), ""))
                indexed += 1
        return indexed

    def print_welcome(self):
        print("\n" + "█"*70)
        print("█" + " "*68 + "█")
        print("█" + " "*15 + "📊 DATACLAW - LOCAL DATA REFERENCE AGENT 📊" + " "*15 + "█")
        print("█" + " "*68 + "█")
        print("█"*70)
        self.print_help()

    def print_help(self):
        print("\n" + "="*60)
        print("COMMANDS")
        print("="*60)
        print("  /stats          - Show statistics")
        print("  /list           - List categories")
        print("  /search <term>  - Search references")
        print("  /add <file>     - Add reference file")
        print("  /get <name>     - Get reference content")
        print("  /index          - Re-index references folder")
        print("  /help           - This menu")
        print("  /quit           - Exit")
        print("="*60)

    def run(self):
        self.print_welcome()
        
        count = self._index_references()
        print(f"\n📊 Indexed {count} reference files")

        while self.running:
            try:
                cmd = input("\n📊 dataclaw> ").strip().lower()
                if not cmd:
                    continue
                
                if cmd == '/quit':
                    print("Goodbye!")
                    break
                elif cmd == '/help':
                    self.print_help()
                elif cmd == '/stats':
                    self.stats()
                elif cmd == '/list':
                    self.list_categories()
                elif cmd.startswith('/search'):
                    self.search(cmd[7:].strip())
                elif cmd.startswith('/get'):
                    self.get_reference(cmd[4:].strip())
                elif cmd == '/index':
                    count = self._index_references()
                    print(f"✅ Re-indexed {count} files")
                else:
                    print("Unknown. Type /help")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break

    def stats(self):
        print("\n" + "="*40)
        print("DATACLAW STATS")
        print("="*40)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM data_refs")
            count = cursor.fetchone()[0]
            print(f"Indexed files: {count}")
            
            cursor = conn.execute("SELECT DISTINCT category FROM data_refs")
            categories = cursor.fetchall()
            print(f"Categories: {len(categories)}")
        print(f"References folder: {self.references_path}")
        print("="*40)

    def list_categories(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT DISTINCT category FROM data_refs ORDER BY category")
            categories = cursor.fetchall()
            print(f"\n📁 Categories ({len(categories)}):\n")
            for cat in categories:
                cursor2 = conn.execute("SELECT COUNT(*) FROM data_refs WHERE category = ?", (cat[0],))
                count = cursor2.fetchone()[0]
                print(f"  • {cat[0]}: {count} files")

    def search(self, term):
        if not term:
            print("Usage: /search <term>")
            return
        
        print(f"\n🔍 Searching for '{term}'...\n")
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT name, category, file_path FROM data_refs 
                WHERE name LIKE ? OR tags LIKE ?
                LIMIT 20
            """, (f"%{term}%", f"%{term}%"))
            results = cursor.fetchall()
        
        if results:
            for name, category, path in results:
                print(f"  📄 {name} [{category}]")
        else:
            print("  No results found")

    def get_reference(self, name):
        if not name:
            print("Usage: /get <filename>")
            return
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT file_path FROM data_refs WHERE name = ?", (name,))
            result = cursor.fetchone()
        
        if result:
            file_path = Path(result[0])
            if file_path.exists():
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                print(f"\n📄 {name}:\n")
                print(content[:2000])
                if len(content) > 2000:
                    print("\n... (truncated)")
            else:
                print(f"❌ File not found: {file_path}")
        else:
            print(f"❌ Reference '{name}' not found")

if __name__ == "__main__":
    DataClaw().run()
