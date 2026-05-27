import requests, json
from pathlib import Path

env = Path(".env").read_text()
token = ""
for line in env.split("\n"):
    if "COURTLISTENER_TOKEN" in line and "=" in line:
        token = line.split("=", 1)[1].strip().strip('"').strip("'")
        break

headers = {"Authorization": f"Token {token}"}
r = requests.get("https://www.courtlistener.com/api/rest/v4/docket-entries/", params={"docket": "67876857"}, headers=headers, timeout=15)
data = r.json()
if data.get("results"):
    print(json.dumps(data["results"][0], indent=2))
else:
    print("No results")
