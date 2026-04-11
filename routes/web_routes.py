"""Webclaw routing"""
class WebRoutes:
    commands = ['search', 'material', 'fetch', 'browse', '/chronicle']
    agent = 'webclaw'
    
    @staticmethod
    def get_help():
        return """
🔍 WEBCLAW:
  search python     - Search reference URLs
  material python   - Fetch content from URL
  fetch <url>       - Fetch specific URL
  /chronicle stats|timeline|search - URL context recovery ledger
"""
