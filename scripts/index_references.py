#!/usr/bin/env python3
"""Index ALL files + ALL URLs into SQLite chronicle - FULL content, NO truncation, NO limits"""
import sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from agents.webclaw.core.chronicle_ledger import get_chronicle

def index_file(file_path):
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')
        results = []
        title = ''
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        if not title:
            title = file_path.stem.replace('_', ' ').replace('-', ' ')
        
        # FULL body text - every character, no truncation
        body_lines = [l.strip() for l in lines if l.strip() and not l.startswith('#')]
        body_text = ' '.join(body_lines)
        
        # Index the file itself with FULL content
        file_context = f"{title}: {body_text}" if body_text else title
        results.append((f"file://{file_path}", file_context))
        
        # Index URLs with surrounding context - NO truncation
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
                results.append((url, ctx))
        return results
    except:
        return [("file://" + str(file_path), file_path.stem)]

def main():
    print('Indexing ALL files + URLs with FULL content...')
    chronicle = get_chronicle()
    refs = Path('agents/webclaw/references')
    total = 0
    files_done = 0
    for md_file in refs.rglob('*.md'):
        category = str(md_file.relative_to(refs).parent)
        entries = index_file(md_file)
        for url, ctx in entries:
            chronicle.record_fetch(url=url, context=ctx, source=category, metadata={'file': str(md_file)})
            total += 1
        files_done += 1
        if files_done % 500 == 0:
            print(f'  {files_done} files, {total} entries...')
    print(f'\nDone. {files_done} files, {total} entries')
    stats = chronicle.get_stats()
    print(f'Total cards: {stats["total_cards"]}')

if __name__ == '__main__':
    main()