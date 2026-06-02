with open('shared/accessibility.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Only print Listening indicator when it hasn't been printed recently
old_listen = '''    while _voice_active:
        try:
            if awake:
                print("\\n[VOICE] ? Listening...", flush=True)
            else:
                print("\\n[VOICE] ? Sleeping (say 'start listening')", flush=True)'''

new_listen = '''    last_indicator = ''
    while _voice_active:
        try:
            indicator = '?' if awake else '?'
            if indicator != last_indicator:
                print(f"\\n[VOICE] {indicator} {'Listening...' if awake else 'Sleeping (say start listening)'}", flush=True)
                last_indicator = indicator'''

content = content.replace(old_listen, new_listen)

with open('shared/accessibility.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Silent listening - only prints on state change')
