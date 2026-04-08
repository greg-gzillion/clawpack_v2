#!/usr/bin/env python3
"""
LAWCLAW - Judicial Research & Court Information System
"""

import os
import sys
import json
import requests
import sqlite3
from pathlib import Path
from datetime import datetime

# Paths
ROOT_DIR = Path(r"C:\Users\greg\dev\clawpack_v2")
SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"
COURT_REFS = ROOT_DIR / "agents" / "webclaw" / "references" / "lawclaw"

# Load .env file
env_path = ROOT_DIR / ".env"
if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

API_KEY = os.environ.get("OPENROUTER_API_KEY")

class LawClaw:
    def __init__(self):
        self.shared_path = SHARED_DB
        self.init_db()
        self.print_welcome()

    def init_db(self):
        """Initialize shared memory database"""
        self.shared_path.parent.mkdir(exist_ok=True)
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS court_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT UNIQUE,
                response TEXT,
                topic TEXT,
                timestamp TEXT,
                source_agent TEXT
            )
        """)
        
        conn.commit()
        conn.close()

    def print_welcome(self):
        print("\n" + "="*70)
        print("⚖️ LAWCLAW - Judicial Research & Court Information")
        print("="*70)
        print(f"📁 Court References: {COURT_REFS}")
        print(f"🧠 Shared Memory: {self.shared_path}")
        print(f"🌐 API: {'Configured' if API_KEY else 'Not Configured'}")
        print("="*70)
        print("\n💡 Simply type your question about courts, judges, or judicial process")
        print("   Examples: 'What does the 1st amendment say?'")
        print("            'Find information about bankruptcy court'")
        print("            'Show me Texas court system'")
        print("            'What is habeas corpus?'")
        print("\nCommands: /stats, /quit")
        print("="*70)

    def search_local(self, query):
        """Search local court references"""
        results = []
        if COURT_REFS.exists():
            for md_file in COURT_REFS.rglob("*.md"):
                try:
                    content = md_file.read_text(encoding='utf-8', errors='ignore')
                    if query.lower() in content.lower():
                        results.append({
                            "file": md_file.name,
                            "preview": content[:500]
                        })
                        if len(results) >= 3:
                            break
                except:
                    pass
        return results

    def query_api(self, question):
        """Query OpenRouter API"""
        if not API_KEY:
            return "❌ API key not configured. Add OPENROUTER_API_KEY to .env file."
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "meta-llama/llama-3.3-70b-instruct",
                    "messages": [
                        {"role": "system", "content": "You are a judicial research assistant. Provide accurate, clear information about courts, judges, and judicial procedures."},
                        {"role": "user", "content": question}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 1000
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()['choices'][0]['message']['content']
                self.save_to_memory(question, result)
                return result
            else:
                return f"API Error: {response.status_code}"
        except Exception as e:
            return f"Error: {e}"

    def save_to_memory(self, query, response):
        """Save to shared memory"""
        try:
            conn = sqlite3.connect(str(self.shared_path))
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO court_knowledge (query, response, topic, timestamp, source_agent)
                VALUES (?, ?, ?, ?, ?)
            """, (query, response, "general", datetime.now().isoformat(), "LawClaw"))
            conn.commit()
            conn.close()
        except:
            pass

    def show_stats(self):
        """Show system statistics"""
        print("\n" + "="*50)
        print("📊 SYSTEM STATISTICS")
        print("="*50)
        print(f"API: {'✅ Configured' if API_KEY else '❌ Not configured'}")
        print(f"Court References: {COURT_REFS}")
        print(f"Shared Memory: {self.shared_path}")
        
        if COURT_REFS.exists():
            file_count = len(list(COURT_REFS.rglob("*.md")))
            print(f"Reference Files: {file_count}")
        
        if self.shared_path.exists():
            conn = sqlite3.connect(str(self.shared_path))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM court_knowledge")
            count = cursor.fetchone()[0]
            print(f"Shared Memory Entries: {count}")
            conn.close()
        print("="*50)

    def run(self):
        """Main loop"""
        self.print_welcome()
        while True:
            try:
                user_input = input("\n⚖️ lawclaw> ").strip()
                if not user_input:
                    continue
                
                if user_input.lower() == '/quit':
                    print("Goodbye!")
                    break
                elif user_input.lower() == '/stats':
                    self.show_stats()
                else:
                    print("\n🔍 Searching court references...")
                    local_results = self.search_local(user_input)
                    if local_results:
                        print("\n📚 Found in court references:")
                        for r in local_results:
                            print(f"\n📄 {r['file']}")
                            print("-"*40)
                            print(r['preview'])
                            if len(r['preview']) < 500:
                                print("...")
                    else:
                        print("\n🤖 No local results. Consulting judicial AI...")
                        answer = self.query_api(user_input)
                        print("\n" + "="*60)
                        print("🤖 RESPONSE:")
                        print("="*60)
                        print(answer)
                        print("="*60)
                        
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    agent = LawClaw()
    agent.run()