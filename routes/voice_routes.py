"""Voice/STT routing (uses interpretclaw)"""
class VoiceRoutes:
    commands = ['/listen']
    agent = 'interpretclaw'
    
    @staticmethod
    def get_help():
        return """
🎤 VOICE:
  /listen                   - Speech to text
  /listen to <lang>         - Listen, translate, speak
"""
