# agents/interpretclaw/commands/braille.py
name = "/braille"
def run(args, agent=None):
    '''Convert text to Braille (opt-in)'''
    from shared.accessibility import to_braille
    if not args:
        return "Usage: /braille <text>  - converts text to Braille (opt-in)"
    return to_braille(args)
