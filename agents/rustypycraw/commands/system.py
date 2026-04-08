def test_command(args=None):
    print("RUSTYPYCRAW is working!")

def help_command(args=None):
    print(f"\nRUSTYPYCRAW - Rust/Python Bridge")
    print("Commands:")
    print("  /test              - Test agent")
    print("  /help              - Show help")
    print("  /quit              - Exit")

def quit_command(args=None):
    return "QUIT"