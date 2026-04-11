def run(args):
    """Translate text using LLM (same as lawclaw)"""
    if not args:
        return "Usage: translate <text> to <lang>\nExample: translate hello to spanish"
    
    import sys
    from pathlib import Path
    
    # Parse command
    text = args
    target_lang = "spanish"
    
    if " to " in args.lower():
        text = args.split(" to ")[0].strip()
        target_lang = args.split(" to ")[1].strip()
    
    # Add project root to path
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))
    
    # Import LLM the same way lawclaw does
    from core.llm_manager import LLMManager
    llm = LLMManager()
    
    # Create prompt for translation
    prompt = f"Translate the following text to {target_lang}. Only output the translation, nothing else.\n\nText: {text}"
    
    # Get translation (lawclaw uses chat_sync successfully)
    response = llm.chat_sync(prompt)
    
    if response and "Error" not in response:
        return f"🌐 {target_lang.upper()}: {response.strip()}"
    else:
        return f"Translation error: Could not translate '{text}' to {target_lang}"
