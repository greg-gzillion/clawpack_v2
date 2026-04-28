"""Main application - routes commands to modules"""

from .config import LAW_REFS
from .data import search_local, get_states, get_state_info, get_county_info
from .api import ask_ai, fetch_url

class LawClaw:
    def __init__(self):
        self.running = True
    
    def run(self):
        self._help()
        while self.running:
            try:
                cmd = input("\n⚖️ lawclaw> ").strip()
                if not cmd:
                    continue
                
                if cmd == '/quit':
                    print("Goodbye!")
                    break
                elif cmd == '/help':
                    self._help()
                elif cmd == '/stats':
                    self._stats()
                elif cmd == '/list':
                    self._list()
                elif cmd.startswith('/search'):
                    self._search(cmd[7:].strip())
                elif cmd.startswith('/browse'):
                    self._browse(cmd[7:].strip().upper())
                elif cmd.startswith('/court'):
                    self._court(cmd[6:].strip().upper())
                elif cmd.startswith('/ask'):
                    self._ask(cmd[4:].strip())
                elif cmd.startswith('/fetch'):
                    self._fetch(cmd[6:].strip())
                else:
                    print("Unknown. Type /help")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
    
    def _help(self):
        print("\n" + "="*50)
        print("⚖️  LAWCLAW  ⚖️")
        print("="*50)
        print("\nCOMMANDS:")
        print("  /stats          - System statistics")
        print("  /list           - All 50 states")
        print("  /search [term]  - Search law references")
        print("  /browse [ST]    - Browse state counties")
        print("  /court ST/CTY   - Court details")
        print("  /ask [question] - AI law question")
        print("  /fetch [url]    - Fetch web content")
        print("  /help           - This menu")
        print("  /quit           - Exit")
        print("\n" + "="*50)
    
    def _stats(self):
        print("\n" + "="*40)
        print("LAWCLAW STATS")
        print("="*40)
        if LAW_REFS.exists():
            files = len(list(LAW_REFS.rglob("*.md")))
            print(f"Reference files: {files}")
        states = len(get_states())
        print(f"States: {states}")
        print("="*40)
    
    def _list(self):
        states = get_states()
        print(f"\n{len(states)} states:\n")
        for i, s in enumerate(states, 1):
            print(f"  {s}", end="  ")
            if i % 8 == 0:
                print()
        print()
    
    def _search(self, query):
        if not query:
            print("Usage: /search [term]")
            return
        print(f"\nSearching: {query}\n")
        results = search_local(query)
        if results:
            for r in results:
                print(f"📄 {r['file']}")
                if r['urls']:
                    print(f"   URLs: {r['urls'][0]}")
                print(f"   {r['content'][:150]}...\n")
        else:
            print("No results found")
    
    def _browse(self, state):
        if not state:
            print("Usage: /browse TX")
            return
        info = get_state_info(state)
        if not info["exists"]:
            print(f"State '{state}' not found")
            return
        print(f"\n{state} - {info['total']} counties:\n")
        for i, c in enumerate(info['counties'], 1):
            print(f"  {i}. {c}")
        print(f"\nUse /court {state}/COUNTY for details")
    
    def _court(self, location):
        if not location or '/' not in location:
            print("Usage: /court TX/DALLAS")
            return
        state, county = location.split('/', 1)
        info = get_county_info(state, county)
        if not info:
            print(f"County '{county}' not found in {state}")
            return
        print(f"\n{info['county']} COUNTY, {state}\n")
        for court in info['courts']:
            print(f"  📌 {court['name']}")
    
    def _ask(self, question):
        if not question:
            print("Usage: /ask [your law question]")
            return
        print(f"\nQuestion: {question}\n")
        print(ask_ai(question))
    
    def _fetch(self, url):
        if not url:
            print("Usage: /fetch [url]")
            return
        print(f"\nFetching: {url}\n")
        print(fetch_url(url))
