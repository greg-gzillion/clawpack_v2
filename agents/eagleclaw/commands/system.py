def test_command(args=None):
    print("EAGLECLAW is working!")

def help_command(args=None):
    print(f"\nEAGLECLAW - Main AI Assistant")
    print("Commands:")
    print("  /test              - Test agent")
    print("  /help              - Show help")
    print("  /quit              - Exit")

def quit_command(args=None):
    return "QUIT"