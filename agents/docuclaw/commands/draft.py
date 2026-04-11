"""Draft a document using templates"""
name = "/draft"

def run(args):
    if not args:
        print("Usage: /draft <type> [topic]")
        print("Types: letter, memo, report, proposal, email, blog, notes")
        return
    
    from pathlib import Path
    from datetime import datetime
    
    parts = args.split(' ', 1)
    doc_type = parts[0].lower()
    topic = parts[1] if len(parts) > 1 else ""
    
    templates = {
        "letter": f"# Letter\n\nDate: {datetime.now().strftime('%B %d, %Y')}\nTo: [Recipient]\nFrom: [You]\n\nDear [Recipient],\n\n{topic if topic else '[Your message]'}\n\nSincerely,\n[Your name]",
        "memo": f"# MEMORANDUM\n\nTo: [Recipients]\nFrom: [Sender]\nDate: {datetime.now().strftime('%B %d, %Y')}\nSubject: {topic if topic else '[Subject]'}\n\n## Purpose\n[State purpose]\n\n## Discussion\n[Details]\n\n## Action Items\n- [ ] Item 1\n- [ ] Item 2",
        "notes": f"# Notes: {topic if topic else datetime.now().strftime('%Y-%m-%d')}\n\n## Key Points\n- Point 1\n- Point 2\n\n## Action Items\n- [ ] Task 1\n- [ ] Task 2"
    }
    
    if doc_type not in templates:
        print(f"Available: {', '.join(templates.keys())}")
        return
    
    output_path = Path(f"{doc_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
    output_path.write_text(templates[doc_type])
    print(f"✅ Drafted {doc_type} -> {output_path}")
