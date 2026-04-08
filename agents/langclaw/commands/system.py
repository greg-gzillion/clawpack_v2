def test_command(args=None):
    print("LANGCLAW is working!")

def help_command(args=None):
    print(f"\nLANGCLAW - Language Learning")
    print("Commands:")
    print("  /test              - Test agent")
    print("  /help              - Show help")
    print("  /quit              - Exit")

def quit_command(args=None):
    return "QUIT"