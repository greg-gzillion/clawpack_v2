def test_command(args=None):
    print("MATHEMATICACLAW is working!")

def help_command(args=None):
    print(f"\nMATHEMATICACLAW - Math Calculations")
    print("Commands:")
    print("  /test              - Test agent")
    print("  /help              - Show help")
    print("  /quit              - Exit")

def quit_command(args=None):
    return "QUIT"