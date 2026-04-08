def format_result(content, max_lines=30):
    lines = content.split('\n')[:max_lines]
    return '\n'.join(lines)

def truncate(text, max_length=800):
    if len(text) > max_length:
        return text[:max_length] + "\n... (truncated)"
    return text
