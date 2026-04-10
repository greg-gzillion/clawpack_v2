"""Webclaw routing"""
class WebRoutes:
    commands = ['search', 'material', 'fetch', 'browse']
    agent = 'webclaw'
    
    @staticmethod
    def get_help():
        return """
🔍 WEB:
  search python     - Search reference URLs
  material python   - Fetch content from URL
  fetch <url>       - Fetch specific URL
"""
