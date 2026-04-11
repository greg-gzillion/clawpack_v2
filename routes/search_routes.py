"""General search routing using chronicle"""
class SearchRoutes:
    commands = ['search', '/search']
    agent = 'chronicle'  # Special handler in clawpack
    
    @staticmethod
    def get_help():
        return """
🔍 GENERAL SEARCH (Chronicle):
  search <query>    - Search across all indexed references
  /search <query>   - Same as above
"""
