def test_command(args=None):
    print("LAWCLAW is working!")
    from core.data import get_data_path
    data_path = get_data_path()
    if data_path.exists():
        print(f"Data path: {data_path}")
        refs = len(list(data_path.glob("**/*.md")))
        print(f"Reference files: {refs}")

def help_command(args=None):
    print("\nLAWCLAW - Judicial Research Agent")
    print("Commands:")
    print("  /test              - Test agent")
    print("  /list              - List reference topics")
    print("  /search [query]    - Search references")
    print("  /browse [state]    - Browse state courts")
    print("  /court [state]     - Court information")
    print("  /court [state]/[county] - Specific county")
    print("  /help              - Show help")
    print("  /quit              - Exit")

def quit_command(args=None):
    return "QUIT"

def list_command(args=None):
    from core.data import get_data_path
    data_path = get_data_path()
    if not data_path.exists():
        print(f"Data path not found: {data_path}")
        return
    topics = [d.name for d in data_path.iterdir() if d.is_dir() and d.name != "jurisdictions"]
    print(f"\nReference topics ({len(topics)}):")
    for topic in sorted(topics)[:20]:
        print(f"  {topic}")
    if len(topics) > 20:
        print(f"  ... and {len(topics)-20} more")