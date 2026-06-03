"""Create document from template - works in CLI and A2A modes"""
name = "/create"

def run(args, agent=None):
    if not args:
        return "Usage: /create business/letter\nAvailable templates: use /templates to list"
    
    from pathlib import Path
    from datetime import datetime
    
    template_path = Path(__file__).parent.parent / "templates" / f"{args}.md"
    if not template_path.exists():
        return f"Template '{args}' not found. Use /templates to list available templates."
    
    content = template_path.read_text(encoding="utf-8")
    
    import re
    variables = re.findall(r'{{(.*?)}}', content)
    
    # Auto-fill variables - use system values where possible
    from datetime import datetime
    values = {}
    for var in variables:
        var_lower = var.lower().strip()
        if var_lower in ('date', 'today', 'current_date'):
            values[var] = datetime.now().strftime('%B %d, %Y')
        elif var_lower in ('year', 'current_year'):
            values[var] = datetime.now().strftime('%Y')
        elif var_lower in ('time', 'current_time'):
            values[var] = datetime.now().strftime('%I:%M %p')
        elif var_lower in ('datetime', 'current_datetime'):
            values[var] = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        else:
            values[var] = f"[{var.upper()}]"
    
    for var, val in values.items():
        content = content.replace(f"{{{{{var}}}}}", val)
    
    output_path = Path.home() / f"{args.replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    output_path.write_text(content, encoding="utf-8")
    
    return f"Document created: {output_path}\n\n{content[:500]}..."
