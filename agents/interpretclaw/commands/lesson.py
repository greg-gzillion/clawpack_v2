def run(args):
    """Get language lesson from chronicle references"""
    if not args:
        return "Usage: /lesson <language> <topic>\nExample: /lesson spanish greetings"
    
    import sys
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))
    
    from shared.chronicle_helper import search_chronicle
    from core.llm_manager import LLMManager
    
    results = search_chronicle(args, 5)
    
    if not results:
        return f"No language references found for '{args}'"
    
    llm = LLMManager()
    prompt = f"""Based on these language learning resources, create a brief lesson about {args}:

Resources:
{chr(10).join([f'- {r.url}' for r in results[:3]])}

Provide a helpful language lesson with examples."""
    
    response = llm.chat_sync(prompt)
    
    output = f"📚 LANGUAGE LESSON: {args.upper()}\n\n{response}\n\n📖 References:\n"
    for r in results[:3]:
        output += f"   🔗 {r.url}\n"
    
    return output
