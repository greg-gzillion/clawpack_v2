"""Practice command - Exercise practice"""

name = "practice"
description = "Practice with exercises"

def run(args):
    if not args:
        return "Usage: /practice <language> <topic>\nExample: /practice es greetings"
    
    parts = args.split()
    if len(parts) >= 2:
        lang = parts[0]
        topic = parts[1]
    else:
        return "Please specify language and topic"
    
    return f"""
📝 **Practice: {lang.upper()} - {topic}**

Exercise 1: Translate to {lang.upper()}
"Hello, how are you?"
(Type your answer)

Exercise 2: Fill in the blank
"_____ días" (Good morning)
(Type your answer)

Type /check to verify your answers!
"""
