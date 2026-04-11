"""Lawclaw routing"""
class LawclawRoutes:
    commands = ['/court', '/law', '/case', '/statute', 'court']
    agent = 'lawclaw'
    
    @staticmethod
    def get_help():
        return """
⚖️ LAWCLAW:
  /court <state> <county>   - Court information
  /law <query>              - Law research
  /case <name>              - Case law lookup
"""
