"""Interpretclaw routing"""
class TranslationRoutes:
    commands = ['translate', 'speak', '/listen']
    agent = 'interpretclaw'
    
    @staticmethod
    def get_help():
        return """
🌐 TRANSLATION & SPEECH:
  translate hello to spanish   - Translate text
  speak hello                  - Speak text
  speak hello to spanish       - Translate then speak
  /listen                      - Speech to text
  /listen to spanish           - Listen, translate, speak
"""
