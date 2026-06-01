# agents/_universal_voice.py - Drop-in voice command for any agent
# Import this in any agent handler's if/elif chain
name = "/voice"

def run(args, agent=None):
    from shared.accessibility import toggle_voice as toggle
    return toggle(agent)
