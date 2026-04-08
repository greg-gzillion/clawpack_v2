def test_command(args=None):
    print("KNOWLEDGE is working!")

def help_command(args=None):
    print(f"\nKNOWLEDGE - Knowledge Persistence")
    print("Commands:")
    print("  /test              - Test agent")
    print("  /help              - Show help")
    print("  /quit              - Exit")

def quit_command(args=None):
    return "QUIT"