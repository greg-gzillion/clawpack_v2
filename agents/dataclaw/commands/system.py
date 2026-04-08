def test_command(args=None):
    print("DATACLAW is working!")

def help_command(args=None):
    print(f"\nDATACLAW - Local Data Agent")
    print("Commands:")
    print("  /test              - Test agent")
    print("  /help              - Show help")
    print("  /quit              - Exit")

def quit_command(args=None):
    return "QUIT"