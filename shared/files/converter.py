'''File Converter — format conversion operations.'''
import json
import csv
from pathlib import Path
from typing import Dict

def convert_file(input_path: str, target_format: str) -> Dict:
    '''Convert file between formats.'''
    input_path = Path(input_path)
    if not input_path.exists():
        return {'error': f'File not found: {input_path}'}

    source_format = input_path.suffix[1:].lower()
    output_path = input_path.with_suffix(f'.{target_format}')

    try:
        if source_format == 'csv' and target_format == 'json':
            with open(input_path, 'r') as f:
                data = list(csv.DictReader(f))
            output_path.write_text(json.dumps(data, indent=2))
            return {'success': True, 'output': str(output_path), 'rows': len(data)}
        elif source_format == 'json' and target_format == 'csv':
            data = json.loads(input_path.read_text())
            if isinstance(data, list) and data:
                with open(output_path, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
                return {'success': True, 'output': str(output_path), 'rows': len(data)}
        elif source_format == 'md' and target_format == 'txt':
            output_path.write_text(input_path.read_text())
            return {'success': True, 'output': str(output_path)}
        elif source_format == 'txt' and target_format == 'md':
            output_path.write_text(input_path.read_text())
            return {'success': True, 'output': str(output_path)}
        elif source_format == 'json' and target_format in ('yaml', 'yml'):
            try:
                import yaml
                data = json.loads(input_path.read_text())
                output_path.write_text(yaml.dump(data, default_flow_style=False))
                return {'success': True, 'output': str(output_path)}
            except ImportError:
                return {'error': 'PyYAML not installed'}
        elif source_format in ('yaml', 'yml') and target_format == 'json':
            try:
                import yaml
                data = yaml.safe_load(input_path.read_text())
                output_path.write_text(json.dumps(data, indent=2))
                return {'success': True, 'output': str(output_path)}
            except ImportError:
                return {'error': 'PyYAML not installed'}
        elif source_format in ('txt', 'md', 'json', 'xml', 'html', 'csv', 'yaml', 'yml', 'toml', 'ini', 'cfg') and target_format in ('txt', 'md', 'json', 'xml', 'html'):
            output_path.write_text(input_path.read_text())
            return {'success': True, 'output': str(output_path), 'note': 'Content preserved, extension changed'}
        else:
            return {'error': f'Conversion from {source_format} to {target_format} not yet supported'}
    except Exception as e:
        return {'error': str(e)}

__all__ = ['convert_file']
