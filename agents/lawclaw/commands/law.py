def run(args):
    """Law research using LLM"""
    if not args:
        return "Usage: /law <topic>\nExample: /law contract"
    
    import sys
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))
    
    # Import LLM
    try:
        from core.llm_manager import LLMManager
    except ImportError:
        try:
            from shared.llm.manager import LLMManager
        except ImportError:
            return "Error: LLMManager not found"
    
    llm = LLMManager()
    prompt = f"You are a legal research assistant. Answer: {args}"
    response = llm.chat_sync(prompt)
    
    return f"📚 LAW: {args.upper()}\n\n{response}"
