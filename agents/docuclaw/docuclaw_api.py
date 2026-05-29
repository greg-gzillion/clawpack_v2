'''DocuClaw API - call this for any document.'''
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).resolve().parent.parent / 'exports'
OUTPUT_DIR.mkdir(exist_ok=True)

def create_document(title, content, agent='unknown', doc_type='document'):
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = OUTPUT_DIR / f'{agent}_{doc_type}_{ts}.md'
    date_str = datetime.now().strftime('%B %d, %Y')
    text = f'# {title}' + chr(10)*2 + f'**Created by:** {agent}' + chr(10) + f'**Date:** {date_str}' + chr(10) + f'**Type:** {doc_type}' + chr(10)*2 + '---' + chr(10)*2 + content + chr(10)*2 + '---' + chr(10) + '*Document created by DocuClaw*'
    filename.write_text(text)
    return {'status': 'success', 'path': str(filename), 'agent': agent, 'type': doc_type}

__all__ = ['create_document']