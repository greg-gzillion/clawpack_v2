"""Document Formatting Module"""
STYLES = {
    'professional': {'font': 'Times New Roman', 'size': '12pt', 'spacing': '1.5', 'margin': '1in'},
    'modern': {'font': 'Arial', 'size': '11pt', 'spacing': '1.4', 'margin': '0.75in'},
    'academic': {'font': 'Georgia', 'size': '12pt', 'spacing': '2.0', 'margin': '1.25in'},
    'business': {'font': 'Calibri', 'size': '11pt', 'spacing': '1.15', 'margin': '0.5in'},
}

class Formatter:
    @staticmethod
    def apply(content, style='professional'):
        s = STYLES.get(style, STYLES['professional'])
        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>body{{font-family:{s['font']};font-size:{s['size']};line-height:{s['spacing']};margin:{s['margin']}}}</style>
</head><body>
{content.replace(chr(10), '<br>')}
</body></html>"""
    
    @staticmethod
    def list_styles():
        return list(STYLES.keys())
