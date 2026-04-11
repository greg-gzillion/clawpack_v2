"""Media Import Module"""
import shutil
from pathlib import Path
from datetime import datetime

MEDIA_DIR = Path(__file__).parent.parent.parent / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

class MediaHandler:
    @staticmethod
    def import_image(file_path):
        path = Path(file_path)
        if not path.exists():
            return None
        dest = MEDIA_DIR / f"img_{datetime.now().strftime('%Y%m%d_%H%M%S')}{path.suffix}"
        shutil.copy2(path, dest)
        return {'path': str(dest), 'embed': f'![{path.stem}]({dest.name})'}
    
    @staticmethod
    def import_csv(file_path):
        import csv
        path = Path(file_path)
        if not path.exists():
            return None
        with open(path, 'r') as f:
            data = list(csv.DictReader(f))
        return {'rows': len(data), 'columns': list(data[0].keys()) if data else []}
