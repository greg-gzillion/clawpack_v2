import sqlite3
conn = sqlite3.connect('data/chronicle.db')
count = conn.execute("SELECT COUNT(*) FROM chronicle WHERE url LIKE '%TX-project%'").fetchone()[0]
print(f'TX-project entries in Chronicle: {count}')
total = conn.execute("SELECT COUNT(*) FROM chronicle WHERE source LIKE 'jurisdiction:%'").fetchone()[0]
print(f'Total jurisdiction entries: {total}')
conn.close()
