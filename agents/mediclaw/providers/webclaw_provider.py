"""Webclaw Provider"""

from config.settings import Config

class WebclawProvider:
    def __init__(self):
        self.path = Config.WEBCLAW_PATH
    
    def list_specialties(self):
        if self.path.exists():
            return sorted([d.name for d in self.path.iterdir() if d.is_dir()])
        return []
    
    def search(self, term):
        results = []
        term_lower = term.lower()
        if not self.path.exists():
            return results
        for specialty in self.path.iterdir():
            if specialty.is_dir():
                for md in specialty.glob("*.md"):
                    try:
                        if term_lower in md.read_text(encoding='utf-8').lower():
                            results.append(specialty.name)
                    except:
                        pass
        return list(set(results))
