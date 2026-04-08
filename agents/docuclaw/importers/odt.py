"""ODT (OpenDocument) importer"""
from pathlib import Path
from importers.base import BaseImporter

class ODTImporter(BaseImporter):
    name = "odt"
    extensions = [".odt"]
    
    def import_file(self, file_path):
        p = Path(file_path)
        try:
            # Try to use odfpy if available
            from odf.opendocument import load
            from odf.text import P
            doc = load(p)
            text = "\n".join([para.firstChild.data for para in doc.getElementsByType(P) if para.firstChild])
            return {
                "text": text,
                "format": "odt"
            }
        except ImportError:
            return {
                "text": f"ODT file: {p.name}\nInstall odfpy for full support: pip install odfpy",
                "format": "odt",
                "warning": "odfpy not installed"
            }
        except Exception as e:
            return {"text": f"Error reading ODT: {e}", "format": "odt"}
