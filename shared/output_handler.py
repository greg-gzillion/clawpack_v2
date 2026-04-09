"""Shared Output Handler - Pop-ups, save, export for all agents"""

import os
import json
import csv
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

class OutputHandler:
    """Universal output handling for all Clawpack agents"""
    
    DEFAULT_EXPORT_DIR = Path.cwd() / "exports"
    
    @classmethod
    def show_popup(cls, file_path: str) -> bool:
        """Open file in default system viewer"""
        path = Path(file_path)
        if path.exists():
            os.startfile(str(path))
            return True
        return False
    
    @classmethod
    def save_image(cls, img, filename: str, directory: str = None) -> Path:
        """Save PIL image to exports folder"""
        export_dir = Path(directory) if directory else cls.DEFAULT_EXPORT_DIR
        export_dir.mkdir(exist_ok=True)
        
        if not filename.endswith(('.png', '.jpg', '.jpeg')):
            filename += '.png'
        
        output_path = export_dir / filename
        img.save(str(output_path))
        return output_path
    
    @classmethod
    def save_text(cls, content: str, filename: str, directory: str = None) -> Path:
        """Save text to file"""
        export_dir = Path(directory) if directory else cls.DEFAULT_EXPORT_DIR
        export_dir.mkdir(exist_ok=True)
        
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        output_path = export_dir / filename
        output_path.write_text(content, encoding='utf-8')
        return output_path
    
    @classmethod
    def save_json(cls, data: Dict, filename: str, directory: str = None) -> Path:
        """Save data as JSON"""
        export_dir = Path(directory) if directory else cls.DEFAULT_EXPORT_DIR
        export_dir.mkdir(exist_ok=True)
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        output_path = export_dir / filename
        output_path.write_text(json.dumps(data, indent=2, default=str))
        return output_path
    
    @classmethod
    def save_csv(cls, data: List[Dict], filename: str, directory: str = None) -> Path:
        """Save data as CSV"""
        export_dir = Path(directory) if directory else cls.DEFAULT_EXPORT_DIR
        export_dir.mkdir(exist_ok=True)
        
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        output_path = export_dir / filename
        if data:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        return output_path
    
    @classmethod
    def generate_filename(cls, prefix: str = "output", ext: str = "png") -> str:
        """Generate unique filename with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.{ext}"
    
    @classmethod
    def open_exports_folder(cls) -> bool:
        """Open the exports folder"""
        cls.DEFAULT_EXPORT_DIR.mkdir(exist_ok=True)
        os.startfile(str(cls.DEFAULT_EXPORT_DIR))
        return True


# Convenience functions
def show_popup(file_path: str) -> bool:
    return OutputHandler.show_popup(file_path)

def save_image(img, filename: str) -> Path:
    return OutputHandler.save_image(img, filename)

def save_text(content: str, filename: str) -> Path:
    return OutputHandler.save_text(content, filename)
