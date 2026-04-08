"""PDF importer"""
from pathlib import Path
from importers.base import BaseImporter

class PDFImporter(BaseImporter):
    name = "pdf"
    extensions = [".pdf"]
    
    def import_file(self, file_path):
        p = Path(file_path)
        try:
            # Try to use PyPDF2 if available
            import PyPDF2
            text = ""
            with open(p, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text()
            return {
                "text": text,
                "format": "pdf",
                "pages": len(reader.pages)
            }
        except ImportError:
            return {
                "text": f"PDF file: {p.name}\nInstall PyPDF2 for text extraction: pip install PyPDF2",
                "format": "pdf",
                "warning": "PyPDF2 not installed"
            }
        except Exception as e:
            return {"text": f"Error reading PDF: {e}", "format": "pdf"}
