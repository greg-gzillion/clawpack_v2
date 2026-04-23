import sys, json, sqlite3, os
from pathlib import Path
from datetime import datetime

# Add .env loading
env_file = Path('.env')
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                os.environ[k] = v

sys.path.insert(0, str(Path.cwd()))

print('🦞 WebClaw Chronicle Rebuild & Test')
print('=' * 60)

# 1. REBUILD
cache_dir = Path('agents/webclaw/cache')
cache_dir.mkdir(parents=True, exist_ok=True)
ref_dir = Path('agents/webclaw/references')

# Count markdown files
md_count = len(list(ref_dir.rglob('*.md'))) if ref_dir.exists() else 0
print(f'\n📁 References found: {md_count:,} files')

# Build URL index
url_index = cache_dir / 'url_index.json'
index_data = {'urls': {}, 'total_entries': 0, 'last_updated': datetime.now().isoformat()}

if ref_dir.exists():
    for f in ref_dir.rglob('*.md'):
        rel = str(f.relative_to(ref_dir))
        index_data['urls'][rel] = {'path': rel, 'size': f.stat().st_size, 'indexed_at': datetime.now().isoformat()}
    index_data['total_entries'] = len(index_data['urls'])
    
with open(url_index, 'w') as f:
    json.dump(index_data, f)
print(f'✅ URL Index: {index_data["total_entries"]:,} entries ({url_index.stat().st_size:,} bytes)')

# Build SQLite
web_cache = cache_dir / 'web_cache.db'
conn = sqlite3.connect(web_cache)
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS web_cache')
c.execute('DROP TABLE IF EXISTS search_index')
c.execute('CREATE TABLE web_cache (url TEXT PRIMARY KEY, content TEXT, fetched_at TIMESTAMP)')
c.execute('CREATE TABLE search_index (term TEXT, url TEXT, frequency INTEGER, PRIMARY KEY (term, url))')

if ref_dir.exists():
    count = 0
    for f in ref_dir.rglob('*.md'):
        try:
            content = open(f, 'r', encoding='utf-8', errors='ignore').read()
            rel = str(f.relative_to(ref_dir))
            c.execute('INSERT OR REPLACE INTO web_cache VALUES (?, ?, ?)', (rel, content[:50000], datetime.now().isoformat()))
            for word in set(w.strip().lower() for w in content.split() if 3 < len(w) < 20):
                c.execute('INSERT OR REPLACE INTO search_index VALUES (?, ?, ?)', (word, rel, 1))
            count += 1
            if count % 1000 == 0:
                print(f'   Indexed {count:,} docs...')
        except Exception as e:
            pass
    conn.commit()
    print(f'✅ Search DB: {count:,} docs indexed ({web_cache.stat().st_size:,} bytes)')
conn.close()

# 2. TEST
print('\n' + '=' * 60)
print('🧪 Testing Integration...')

try:
    from agents.webclaw.core.agent import WebClawAgent
    agent = WebClawAgent()
    print('✅ WebClaw Agent initialized')
    
    # Try recall
    result = agent.recall('court')
    if result:
        print(f'✅ Recall working: found {len(str(result))} chars')
    else:
        print('⚠️ Recall returned empty (may need more data)')
        
except Exception as e:
    print(f'❌ Agent error: {e}')

try:
    from agents.llmclaw.providers.stock import StockProvider
    llm = StockProvider()
    response = llm.query('Say hello')
    print(f'✅ LLM Provider: {response[:50]}...')
except Exception as e:
    print(f'⚠️ LLM not configured: {e}')

print('\n' + '=' * 60)
print('✨ Complete! WebClaw is ready.')
