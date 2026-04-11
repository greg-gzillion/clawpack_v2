def run(args):
    """Medical research using LLM"""
    if not args:
        return "Usage: /med <condition>\nExample: /med diabetes symptoms"
    
    import sys
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))
    
    from core.llm_manager import LLMManager
    llm = LLMManager()
    
    prompt = f"""You are a medical information assistant. Answer the following medical question accurately and helpfully:

Question: {args}

Provide clear, factual information. Include relevant symptoms, causes, treatments, or prevention tips as appropriate. Note: This is for informational purposes only, not medical advice."""
    
    response = llm.chat_sync(prompt)
    
    if response and "Error" not in response:
        return f"🏥 MEDICAL INFO: {args.upper()}\n\n{response}"
    else:
        return f"Error: Could not get medical info for '{args}'"
