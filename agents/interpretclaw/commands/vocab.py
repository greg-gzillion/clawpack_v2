def run(args):
    """Look up vocabulary using chronicle references"""
    if not args:
        return "Usage: /vocab <language> <word>\nExample: /vocab spanish hola"
    
    import sys
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))
    
    from shared.chronicle_helper import search_chronicle
    from shared.llm import LLMManager
    
    results = search_chronicle(args, 3)
    
    llm = LLMManager()
    prompt = f"Provide the definition and usage of the word/phrase: {args}\nInclude pronunciation tips and example sentences."
    
    response = llm.chat_sync(prompt)
    
    output = f"📖 VOCABULARY: {args.upper()}\n\n{response}"
    
    if results:
        output += "\n\n🔗 References:\n"
        for r in results:
            output += f"   {r.url}\n"
    
    return output
