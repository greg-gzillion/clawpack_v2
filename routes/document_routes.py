"""Docuclaw routing"""
class DocumentRoutes:
    commands = ['doc', '/read', '/convert', '/export']
    agent = 'docuclaw'
    
    @staticmethod
    def get_help():
        return """
📄 DOCUMENTS:
  /read <file>              - Read document
  /convert <file> to <fmt>  - Convert format
  /export <file>            - Export document
"""
