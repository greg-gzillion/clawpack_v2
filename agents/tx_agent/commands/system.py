def test_command(args=None):
    print("TX-AGENT is working!")

def help_command(args=None):
    print(f"\nTX-AGENT - TX Blockchain Agent")
    print("Commands:")
    print("  /test              - Test agent")
    print("  /help              - Show help")
    print("  /quit              - Exit")

def quit_command(args=None):
    return "QUIT"