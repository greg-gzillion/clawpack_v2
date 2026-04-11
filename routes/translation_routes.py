"""Interpretclaw routing with language learning"""
class TranslationRoutes:
    commands = ['translate', 'speak', '/listen', '/lesson', '/vocab']
    agent = 'interpretclaw'
    
    @staticmethod
    def get_help():
        return """
🌐 TRANSLATION & LANGUAGE:
  translate <text> to <lang>  - Translate text
  speak <text>                - Text-to-speech
  /listen                     - Speech to text
  /lesson <lang> <topic>      - Language lesson
  /vocab <lang> <word>        - Vocabulary lookup
"""
