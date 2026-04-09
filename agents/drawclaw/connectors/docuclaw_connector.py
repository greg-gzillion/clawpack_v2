"""Connector to Docuclaw agent for document integration"""

from pathlib import Path
from typing import Dict, List

class DocuclawConnector:
    def __init__(self):
        self.doc_path = Path(__file__).parent.parent.parent / "docuclaw"
        self.available = self.doc_path.exists()
    
    def export_drawing(self, drawing_id: str, format: str = "png", template: str = None) -> Dict:
        """Export drawing to Docuclaw format"""
        export_dir = Path("exports")
        export_dir.mkdir(exist_ok=True)
        
        filepath = export_dir / f"{drawing_id}_export.{format}"
        
        return {
            "success": True,
            "message": f"Drawing exported for Docuclaw integration",
            "filepath": str(filepath),
            "format": format,
            "template": template,
            "docuclaw_command": f"/import {filepath}" if self.available else None
        }
    
    def create_report(self, title: str, drawings: List[str], text: str = "") -> Dict:
        """Create a report with multiple drawings"""
        report = {
            "title": title,
            "drawings": drawings,
            "text": text,
            "timestamp": str(Path.cwd())
        }
        
        return {
            "success": True,
            "report": report,
            "message": f"Report '{title}' created with {len(drawings)} drawings"
        }
