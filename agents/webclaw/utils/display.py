"""Display utilities for WebClaw"""

def display_banner(title="WEBCLAW - WEB RESEARCH & SECURITY", icon="🌐"):
    """Display welcome banner"""
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print(f"█{' '*35}{icon}{' '*35}█")
    print(f"█{' '*15}{title}{' '*15}█")
    print("█" + " "*78 + "█")
    print("█"*80)

def display_categories(categories):
    """Display categories in columns"""
    print("\n📚 CATEGORIES")
    print("-"*50)
    for i, cat in enumerate(categories):
        if i % 5 == 0 and i > 0:
            print()
        print(f"  • {cat:<20}", end="")
    print("\n" + "-"*50)

def display_commands(commands_list):
    """Display commands in columns"""
    print("\n🎯 COMMANDS")
    print("-"*50)
    for i, (cmd, desc) in enumerate(commands_list):
        if i % 3 == 0 and i > 0:
            print()
        print(f"  {cmd:<12} - {desc:<25}", end="")
    print("\n" + "-"*50)

def display_header(text):
    """Display section header"""
    print("\n" + "="*50)
    print(text)
    print("="*50)
