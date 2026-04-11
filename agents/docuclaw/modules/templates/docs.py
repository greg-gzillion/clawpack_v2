"""Document templates"""
TEMPLATES = {'letter': 'Letter template', 'report': 'Report template'}
def get_template(name): return TEMPLATES.get(name, '')
def list_templates(): return list(TEMPLATES.keys())
