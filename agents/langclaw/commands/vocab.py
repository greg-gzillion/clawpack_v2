def run(args):
    import sys
    from pathlib import Path
    
    # Add paths
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    # Parse arguments based on command
    cmd_name = Path(__file__).stem
    if not args:
        return "Usage: /vocab <language> <word>\nExample: /vocab spanish hola"
    
    parts = args.split(maxsplit=1)
    language = parts[0].lower()
    word = parts[1] if len(parts) > 1 else ""
    
    if not word:
        return f"Usage: /vocab {language} <word>"
    
    from core.lesson_engine import LessonEngine
    engine = LessonEngine(language)
    result = engine.get_vocab(word)
    
    return f"📖 VOCAB: {language.upper()} - {word}\n\n{result}"
