def test_command(args=None):
    print("interpretclaw is working!")

def help_command(args=None):
    print(f"\ninterpretclaw - Translation Agent")
    print("Commands:")
    print("  /test              - Test agent")
    print("  /help              - Show help")
    print("  /quit              - Exit")

def quit_command(args=None):
    return "QUIT"