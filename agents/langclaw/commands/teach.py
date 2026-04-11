def run(args):
    if not args:
        return "Usage: /teach <language>\nExample: /teach spanish"
    
    import sys
    from pathlib import Path
    
    language = args.lower().strip()
    
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))
    
    from core.llm_manager import LLMManager
    llm = LLMManager()
    
    prompt = f"""You are an interactive language teacher for {language}. 
Start with a greeting, then teach one concept at a time.
Ask the user to repeat or answer questions.
Keep it simple and encouraging."""
    
    response = llm.chat_sync(prompt)
    return f"👩‍🏫 TEACHING {language.upper()}\n\n{response}\n\n(Type your response to continue)"
