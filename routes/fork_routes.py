"""Fork agent routing"""
class ForkRoutes:
    commands = ['/fork', '/forks']
    agent = 'fork'
    
    @staticmethod
    def get_help():
        return """
🔀 FORK AGENTS:
  /fork "<task>"            - Spawn parallel sub-agent
  /forks                    - List active forks
"""
