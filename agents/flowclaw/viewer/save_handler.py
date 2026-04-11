"""Save diagrams in multiple formats"""
from pathlib import Path
import json
from typing import Dict

class SaveHandler:
    """Handle saving diagrams in various formats"""
    
    @staticmethod
    def save_as_mermaid(code: str, filepath: Path) -> bool:
        """Save as Mermaid file"""
        filepath.write_text(code)
        return True
    
    @staticmethod
    def save_as_json(code: str, metadata: Dict, filepath: Path) -> bool:
        """Save as JSON with metadata"""
        data = {
            'code': code,
            'metadata': metadata,
            'format': 'mermaid'
        }
        filepath.write_text(json.dumps(data, indent=2))
        return True
    
    @staticmethod
    def save_multiple_formats(code: str, base_name: str, output_dir: Path) -> Dict:
        """Save in multiple formats"""
        saved = {}
        
        # Save as .mmd
        mmd_path = output_dir / f"{base_name}.mmd"
        SaveHandler.save_as_mermaid(code, mmd_path)
        saved['mmd'] = str(mmd_path)
        
        # Save as .json
        json_path = output_dir / f"{base_name}.json"
        SaveHandler.save_as_json(code, {'timestamp': str(Path.cwd())}, json_path)
        saved['json'] = str(json_path)
        
        return saved
