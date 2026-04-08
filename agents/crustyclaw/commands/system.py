def test_command(args=None):
    print("CRUSTYCLAW is working!")

def help_command(args=None):
    print(f"\nCRUSTYCLAW - Web Scraping Agent")
    print("Commands:")
    print("  /test              - Test agent")
    print("  /help              - Show help")
    print("  /quit              - Exit")

def quit_command(args=None):
    return "QUIT"