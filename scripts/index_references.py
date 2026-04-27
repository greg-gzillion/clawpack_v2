#!/usr/bin/env python3
"""Index all references into SQLite chronicle with full context"""
import sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from agents.webclaw.core.chronicle_ledger import get_chronicle

def extract_urls_with_context(file_path):
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')
        results = []
        title = ''
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        current_heading = title
        current_paragraph = []
        for line in lines:
            if line.startswith('## ') or line.startswith('# '):
                current_heading = line.lstrip('#').strip()
                current_paragraph = []
                continue
            if line.strip():
                current_paragraph.append(line.strip())
            else:
                current_paragraph = []
            urls = re.findall(r'https?://[^\s<>"\')\]]+', line)
            for url in urls:
                url = url.rstrip('.,;:!?')
                para_text = ' '.join(current_paragraph[-3:])
                ctx = f'{title} | {current_heading}: {para_text}' if title else f'{current_heading}: {para_text}'
                if len(ctx) > 500: ctx = ctx[:497] + '...'
                results.append((url, ctx))
        return results
    except:
        return []

def main():
    print('Indexing references into SQLite chronicle...')
    chronicle = get_chronicle()
    refs = Path('agents/webclaw/references')
    total = 0
    for md_file in refs.rglob('*.md'):
        category = str(md_file.relative_to(refs).parent)
        entries = extract_urls_with_context(md_file)
        for url, ctx in entries:
            chronicle.record_fetch(url=url, context=ctx, source=category, metadata={'file': str(md_file)})
            total += 1
            if total % 100 == 0: print(f'  Indexed {total} URLs...')
    print(f'\nDone. Indexed {total} URLs')
    print(f'Total cards: {chronicle.get_stats()["total_cards"]}')

if __name__ == '__main__':
    main()