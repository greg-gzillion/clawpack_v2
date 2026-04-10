"""Langclaw routing"""
class LanguageRoutes:
    commands = ['lang', '/lesson', '/practice', '/vocab']
    agent = 'langclaw'
    
    @staticmethod
    def get_help():
        return """
📚 LANGUAGE:
  /lesson <lang> <topic>    - Language lesson
  /practice <lang>          - Practice exercises
  /vocab <lang> <word>      - Vocabulary lookup
"""
