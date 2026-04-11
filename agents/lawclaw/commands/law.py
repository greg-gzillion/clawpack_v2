def run(args):
    """Law research using LLM + chronicle URLs"""
    if not args:
        return "Usage: /law <topic>\nExample: /law contract"
    
    import sys
    import subprocess
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))
    
    # Search chronicle
    from shared.chronicle_helper import search_chronicle
    results = search_chronicle(args, 3)
    
    if not results:
        return f"No information found for '{args}'"
    
    # Fetch content
    webclaw = project_root / "agents/webclaw/webclaw.py"
    contents = []
    for card in results:
        result = subprocess.run(
            [sys.executable, str(webclaw), "fetch", card.url],
            capture_output=True, text=True, timeout=30
        )
        if result.stdout and "Error" not in result.stdout:
            contents.append(f"Source: {card.url}\n{result.stdout[:1000]}")
    
    if not contents:
        return f"Could not fetch content for '{args}'"
    
    # Use LLM to answer
    from core.llm_manager import LLMManager
    llm = LLMManager()
    
    prompt = f"""Based on the following information, answer: {args}

{chr(10).join(contents)}

Provide a clear, helpful answer."""
    
    response = llm.chat_sync(prompt)
    
    return f"📚 {args.upper()}\n\n{response}\n\n🔗 Sources:\n" + "\n".join([f"  • {c.url}" for c in results[:3]])
