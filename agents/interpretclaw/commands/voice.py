name = '/voice'

def run(args, agent=None):

    from shared.accessibility import toggle_voice as toggle

    return toggle()

