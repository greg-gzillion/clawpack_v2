import sys, re
from pathlib import Path

filepath = Path(r"C:\Users\greg\dev\clawpack_v2\agents\webclaw\core\chronicle_ledger.py")
content = filepath.read_text()

old = """            except:
                pass
            # Fallback LIKE search with source filter"""

new = """            except:
                pass
            # If FTS5 returned empty, extract keywords and retry
            if not rows:
                keywords = ' OR '.join([w for w in re.findall(r'[a-zA-Z0-9]{3,}', query) 
                    if w.lower() not in ('the','and','for','what','where','when','who','how','why','are','was','did','does','has','had','can','will','is','court','county','city','state','municipal')])
                if keywords:
                    try:
                        if source_filter:
                            rows = conn.execute(
                                \"\"\"SELECT c.* FROM chronicle c JOIN chronicle_fts f ON c.id = f.rowid WHERE chronicle_fts MATCH ? AND c.source LIKE ? ORDER BY rank LIMIT ?\"\"\",
                                (keywords, f\"%{source_filter}%\", limit)).fetchall()
                        else:
                            rows = conn.execute(
                                \"\"\"SELECT c.* FROM chronicle c JOIN chronicle_fts f ON c.id = f.rowid WHERE chronicle_fts MATCH ? ORDER BY rank LIMIT ?\"\"\",
                                (keywords, limit)).fetchall()
                        if rows:
                            return [dict(r) for r in rows]
                    except:
                        pass
            # Fallback LIKE search with source filter"""

if old in content:
    content = content.replace(old, new)
    filepath.write_text(content)
    print("Patched successfully")
else:
    print("Pattern not found - checking...")
    if "Fallback LIKE" in content:
        print("Found 'Fallback LIKE' but surrounding text differs")
