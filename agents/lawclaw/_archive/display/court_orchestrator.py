"""Orchestrator for court information display"""

import re
from pathlib import Path
from .index.chronicle_indexer import chronicle_indexer
from .web.html_generator import html_generator
from .file.markdown_exporter import markdown_exporter

class CourtOrchestrator:
    def __init__(self):
        self.indexer = chronicle_indexer
        self.web = html_generator
        self.file_exporter = markdown_exporter
    
    def process_court_info(self, jurisdiction: str, location: str, court_files: list) -> dict:
        court_data = []
        for file_path in court_files:
            content = file_path.read_text()
            court_data.append(self._parse_court_markdown(content, file_path.stem))
        
        results = {
            'jurisdiction': jurisdiction,
            'location': location,
            'court_count': len(court_data),
            'indexed': False,
            'webpage': None,
            'markdown_file': None
        }
        
        # Index in Chronicle
        combined = "\n".join([c['name'] for c in court_data])
        if self.indexer.index_court(jurisdiction, location, combined, court_files[0]):
            results['indexed'] = True
        
        # Generate webpage
        html_file = self.web.generate_court_page(jurisdiction, location, court_data)
        results['webpage'] = str(html_file)
        
        # Export markdown
        md_file = self.file_exporter.export_court_info(jurisdiction, location, court_data)
        results['markdown_file'] = str(md_file)
        
        return results
    
    def _parse_court_markdown(self, content: str, filename: str) -> dict:
        """Parse court information from markdown content"""
        court = {
            'name': filename.replace('_', ' ').title(),
            'phone': 'N/A',
            'address': 'N/A',
            'hours': 'N/A',
            'jurisdiction': 'N/A',
            'website': 'N/A',
            'judge': 'N/A'
        }
        
        # Look for patterns like "- **Phone**: (303) 679-2330"
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            
            # Phone number
            if '- **Phone**:' in line or '- Phone:' in line:
                parts = line.split(':', 1)
                if len(parts) > 1:
                    court['phone'] = parts[1].strip()
            
            # Address
            elif '- **Address**:' in line or '- Address:' in line:
                parts = line.split(':', 1)
                if len(parts) > 1:
                    court['address'] = parts[1].strip()
            
            # Hours
            elif '- **Hours**:' in line or '- Hours:' in line:
                parts = line.split(':', 1)
                if len(parts) > 1:
                    court['hours'] = parts[1].strip()
            
            # Website
            elif '- **Website**:' in line or '- Website:' in line:
                parts = line.split(':', 1)
                if len(parts) > 1:
                    url = parts[1].strip()
                    # Extract URL from markdown link format [text](url)
                    url_match = re.search(r'\[([^\]]+)\]\(([^\)]+)\)', url)
                    if url_match:
                        court['website'] = url_match.group(2)
                    else:
                        court['website'] = url
            
            # Judge
            elif '- **Presiding Judge**:' in line or '- Judge:' in line or '- Presiding Judge:' in line:
                parts = line.split(':', 1)
                if len(parts) > 1:
                    court['judge'] = parts[1].strip()
            
            # Jurisdiction (list items after "## Jurisdiction")
            elif line.startswith('- ') and not court['jurisdiction']:
                if court['jurisdiction'] == 'N/A':
                    court['jurisdiction'] = line[2:]
                else:
                    court['jurisdiction'] += f"\n    • {line[2:]}"
        
        return court
    
    def display_results(self, results: dict) -> str:
        # Open webpage in browser
        import webbrowser
        if results['webpage']:
            webbrowser.open(f'file://{results["webpage"]}')
        
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  COURT: {results['jurisdiction']} - {results['location']}
╚══════════════════════════════════════════════════════════════════╝

📊 {results['court_count']} courts found
✅ Indexed in Chronicle: {'Yes' if results['indexed'] else 'No'}
🌐 Webpage opened in browser
📁 Markdown saved: {results['markdown_file']}

💡 The webpage should now display real court information!
"""

court_orchestrator = CourtOrchestrator()
