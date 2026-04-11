"""List templates command"""
name = "/templates"
def run(args):
    from pathlib import Path
    templates_dir = Path(__file__).parent.parent / "templates"
    print("\n📁 Document Templates:\n")
    for category in templates_dir.iterdir():
        if category.is_dir():
            print(f"\n  📂 {category.name.upper()}:")
            for template in category.glob("*.md"):
                print(f"     📄 {template.stem}")
