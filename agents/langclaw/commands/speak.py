# agents/langclaw/commands/speak.py
name = "/speak"
def run(args, agent=None):
    '''Convert text to speech'''
    from shared.accessibility import speak
    if not args:
        return "Usage: /speak <text>"
    return speak(args)
