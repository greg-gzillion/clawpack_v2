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
        return "Usage: /practice <language>\nExample: /practice spanish"
    
    language = args.lower().strip()
    
    from core.lesson_engine import LessonEngine
    engine = LessonEngine(language)
    result = engine.get_practice()
    
    return f"📝 PRACTICE: {language.upper()}\n\n{result}"
