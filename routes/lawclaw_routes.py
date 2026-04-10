"""Lawclaw routing"""
class LawclawRoutes:
    commands = ['/court', '/law', '/case', '/statute', 'court',
                '/search', '/browse', '/ask', '/stats', '/list']
    agent = 'lawclaw'
    
    @staticmethod
    def get_help():
        return """
⚖️ LAWCLAW:
  /court <state> <county>   - Court information
  /law <query>              - Law research
  /case <name>              - Case law lookup
  /search <query>           - Search law references
  /browse <state>           - Browse state courts
  /ask <question>           - Ask AI legal question
"""
