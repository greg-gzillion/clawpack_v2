"""Share command - Query all agents' knowledge"""

def share_command(args):
    if not args:
        print("Usage: /share [query]")
        return

    import sqlite3
    from pathlib import Path
    
    SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"
    
    if not SHARED_DB.exists():
        print("No shared memory database found. Other agents haven't saved knowledge yet.")
        return
    
    conn = sqlite3.connect(str(SHARED_DB))
    conn.row_factory = sqlite3.Row
    
    # Get all agent tables
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%_knowledge'")
    tables = [row[0] for row in cursor.fetchall()]
    
    results = {}
    for table in tables:
        try:
            cursor = conn.execute(f'''
                SELECT query, response, source_agent, timestamp
                FROM {table}
                WHERE query LIKE ?
                ORDER BY timestamp DESC
                LIMIT 3
            ''', (f'%{args}%',))
            rows = cursor.fetchall()
            if rows:
                agent_name = table.replace('_knowledge', '')
                results[agent_name] = [dict(row) for row in rows]
        except sqlite3.OperationalError as e:
            # Table might have different schema
            pass
    
    conn.close()
    
    if results:
        print(f"\n📚 SHARED KNOWLEDGE: '{args}'\n")
        for agent, items in results.items():
            print(f"   🔗 From {agent}:")
            for item in items[:2]:
                print(f"      📖 {item['query'][:60]}...")
                if 'response' in item:
                    print(f"         {item['response'][:150]}...")
                print()
    else:
        print(f"No shared knowledge found for: {args}")
        print("💡 Other agents may not have saved this information yet.")
        print("   Try running the same query in LawClaw or MedicLaw first.")
