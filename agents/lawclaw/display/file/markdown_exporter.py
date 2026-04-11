"""Export court information as markdown files"""

from pathlib import Path
from datetime import datetime

class MarkdownExporter:
    def __init__(self):
        self.output_dir = Path.home() / ".clawpack" / "court_exports"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_court_info(self, jurisdiction: str, location: str, court_data: list) -> Path:
        md_content = f"""# Court Information: {jurisdiction} - {location}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        for court in court_data:
            md_content += f"""
## {court['name']}

- **Phone:** {court.get('phone', 'N/A')}
- **Address:** {court.get('address', 'N/A')}
- **Hours:** {court.get('hours', 'N/A')}
- **Jurisdiction:** {court.get('jurisdiction', 'N/A')}

"""
        
        md_file = self.output_dir / f"court_{jurisdiction}_{location.replace(' ', '_')}.md"
        md_file.write_text(md_content)
        return md_file

markdown_exporter = MarkdownExporter()
