"""Liberateclaw routing"""
class LiberateclawRoutes:
    commands = ['/liberate', '/liberated', '/use']
    agent = 'liberateclaw'
    
    @staticmethod
    def get_help():
        return """
🦞 LIBERATECLAW:
  /liberate <model>       - Liberate a model
  /liberated              - List liberated models
  /use <model> <prompt>   - Use a liberated model
"""
