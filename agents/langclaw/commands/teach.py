"""Teach command - Interactive teaching mode"""

name = "teach"
description = "Start interactive teaching session"

def run(args):
    if not args:
        return "Usage: /teach <language>\nExample: /teach es"
    
    lang = args.split()[0]
    return f"""
🎓 **Interactive Teaching Mode: {lang.upper()}**

Available commands in teach mode:
  /next - Next lesson
  /repeat - Repeat current lesson
  /quiz - Take a quiz
  /progress - Show your progress
  /exit - Exit teach mode

Starting with beginner lesson...
Type /next to begin!
"""
