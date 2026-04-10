"""Quit command - Exit WebClaw"""

def quit_command(args=None):
    """Exit the application"""
    print("Goodbye!")
    return True  # Return True to signal exit

name = "/quit"
run = quit_command
