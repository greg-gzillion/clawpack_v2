name = "/interpret"
def run(args, agent=None):
    from shared.accessibility import listen, detect_language, translate, speak
    print("=" * 50)
    print("  INTERPRETER MODE ACTIVE")
    print("  Speak in any language. Type exit to stop.")
    print("=" * 50)
    last_lang = None
    conversation = []
    while True:
        try:
            text = listen(timeout=8, phrase_limit=15)
            if text.startswith('[STT]'):
                continue
            if text.lower().strip() in ['exit', 'quit', 'stop', 'salir']:
                result = "INTERPRETER SESSION\n" + "=" * 40 + "\n"
                for entry in conversation:
                    result += f"[{entry['lang'].upper()}] {entry['original']}\n  -> {entry['translated']}\n\n"
                return result
            lang = detect_language(text)
            if last_lang and last_lang != lang:
                target = last_lang
            elif lang != 'en':
                target = 'en'
            else:
                target = 'es'
            translated = translate(text, target, lang) if lang != target else text
            conversation.append({'lang': lang, 'original': text, 'translated': translated, 'target': target})
            print(f"\n[{lang.upper()} -> {target.upper()}]\n  Original: {text[:200]}\n  Translation: {translated[:200]}")
            speak(translated, target)
            last_lang = lang
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[INTERPRETER] Error: {str(e)[:100]}")
            continue
    return "Interpreter session complete."
