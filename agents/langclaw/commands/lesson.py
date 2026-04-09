"""Lesson command for Langclaw"""

name = "lesson"
description = "Start a language lesson"

def run(args):
    from teacher.core import teacher
    
    if not args:
        return "Usage: /lesson <language> <topic> [level]\nExample: /lesson es greetings beginner"
    
    parts = args.split()
    if len(parts) >= 2:
        lang = parts[0]
        topic = parts[1]
        level = parts[2] if len(parts) > 2 else "beginner"
    else:
        return "Please specify language and topic"
    
    lesson = teacher.get_lesson(lang, topic, level)
    if lesson:
        return f"📚 **{lesson.title.upper()}** ({lang.upper()} - {level})\n\n{lesson.content}\n\n📝 Vocabulary:\n" + \
               '\n'.join([f"  • {k} = {v}" for k, v in lesson.vocabulary.items()])
    else:
        return f"Lesson not found: {lang}/{topic}/{level}"
