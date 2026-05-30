name = "/language"
def run(args, agent=None):
    """Set system-wide language preference. Example: /language es"""
    from shared.locale import set_language, list_languages
    if not args:
        return list_languages()
    return set_language(args.strip())
