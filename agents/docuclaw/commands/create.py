"""Create document from template"""
name = "/create"
def run(args):
    if not args:
        print("Usage: /create business/letter")
        return
    from pathlib import Path
    from datetime import datetime
    template_path = Path(__file__).parent.parent / "templates" / f"{args}.md"
    if not template_path.exists():
        print(f"Template '{args}' not found")
        return
    content = template_path.read_text()
    print(f"\n📝 Creating document from '{args}'")
    print("\nFill in the variables (press Enter to skip):\n")
    import re
    variables = re.findall(r'{{(.*?)}}', content)
    values = {}
    for var in variables:
        val = input(f"  {var}: ")
        if val:
            values[var] = val
    for var, val in values.items():
        content = content.replace(f"{{{{{var}}}}}", val)
    output_path = Path.home() / f"{args.replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    output_path.write_text(content)
    print(f"\n✅ Document saved to: {output_path}")
