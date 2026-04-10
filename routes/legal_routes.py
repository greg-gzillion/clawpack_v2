"""Lawclaw routing"""
class LegalRoutes:
    commands = ['/court', '/law', '/legal', '/case', '/statute']
    agent = 'lawclaw'
    
    @staticmethod
    def get_help():
        return """
⚖️ LEGAL:
  /court <state> <county>   - Court information
  /law <query>              - Legal research
  /case <name>              - Case law lookup
"""
