import requests, json
from pathlib import Path

env = Path(".env").read_text()
token = ""
for line in env.split("\n"):
    if "COURTLISTENER_TOKEN" in line and "=" in line:
        token = line.split("=", 1)[1].strip().strip('"').strip("'")
        break

headers = {"Authorization": f"Token {token}"}
r = requests.get("https://www.courtlistener.com/api/rest/v4/courts/", params={"jurisdiction": "FD", "page_size": 5}, headers=headers, timeout=10)
data = r.json()

for c in data.get("results", []):
    print(f"Name: {c.get('short_name', '?')}")
    print(f"Circuit: {c.get('circuit')} (type: {type(c.get('circuit')).__name__})")
    print(f"Jurisdiction: {c.get('jurisdiction')}")
    print()
