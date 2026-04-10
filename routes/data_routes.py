"""Dataclaw routing"""
class DataRoutes:
    commands = ['data', 'analyze', '/stats', '/query']
    agent = 'dataclaw'
    
    @staticmethod
    def get_help():
        return """
📊 DATA:
  analyze <file>            - Analyze data file
  /stats                    - Show statistics
  /query <sql>              - Run query
"""
