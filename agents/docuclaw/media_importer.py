"""Media import handler for images, charts, graphs, and pictures"""

import base64
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class MediaImporter:
    """Handle importing images, charts, graphs, and pictures"""
    
    SUPPORTED_IMAGES = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg']
    SUPPORTED_CHARTS = ['.csv', '.xlsx', '.xls', '.json', '.xml']
    SUPPORTED_GRAPHS = ['.dot', '.gv', '.graphml', '.gml']
    
    @staticmethod
    def import_image(file_path: str, output_dir: Path) -> Dict:
        """Import an image file"""
        path = Path(file_path)
        if not path.exists():
            return {'error': f'File not found: {file_path}'}
        
        if path.suffix.lower() not in MediaImporter.SUPPORTED_IMAGES:
            return {'error': f'Unsupported image format: {path.suffix}. Supported: {", ".join(MediaImporter.SUPPORTED_IMAGES)}'}
        
        # Copy image to media directory
        media_dir = output_dir / "media"
        media_dir.mkdir(exist_ok=True)
        
        import shutil
        dest_path = media_dir / f"img_{datetime.now().strftime('%Y%m%d_%H%M%S')}{path.suffix}"
        shutil.copy2(path, dest_path)
        
        # Generate markdown embed code
        markdown_embed = f"![{path.stem}]({dest_path.relative_to(output_dir.parent)})"
        html_embed = f'<img src="{dest_path.relative_to(output_dir.parent)}" alt="{path.stem}" style="max-width:100%">'
        
        return {
            'type': 'image',
            'original': str(path),
            'saved': str(dest_path),
            'markdown': markdown_embed,
            'html': html_embed,
            'size': path.stat().st_size,
            'format': path.suffix[1:].upper()
        }
    
    @staticmethod
    def import_chart_data(file_path: str) -> Dict:
        """Import chart data from CSV/Excel/JSON"""
        path = Path(file_path)
        if not path.exists():
            return {'error': f'File not found: {file_path}'}
        
        data = {'type': 'chart', 'original': str(path), 'data': []}
        
        if path.suffix.lower() == '.csv':
            import csv
            with open(path, 'r') as f:
                reader = csv.DictReader(f)
                data['data'] = list(reader)
                data['headers'] = reader.fieldnames
        
        elif path.suffix.lower() in ['.xlsx', '.xls']:
            try:
                import pandas as pd
                df = pd.read_excel(path)
                data['data'] = df.to_dict('records')
                data['headers'] = list(df.columns)
                data['shape'] = df.shape
            except ImportError:
                data['error'] = 'pandas not installed. Install with: pip install pandas openpyxl'
        
        elif path.suffix.lower() == '.json':
            import json
            with open(path, 'r') as f:
                data['data'] = json.load(f)
        
        return data
    
    @staticmethod
    def generate_chart_html(data: List[Dict], chart_type: str = "bar") -> str:
        """Generate HTML for chart visualization"""
        import json
        
        # Prepare data for Chart.js
        if not data:
            return "<p>No data available</p>"
        
        labels = list(data[0].keys()) if data else []
        values = [list(row.values()) for row in data]
        
        html = f'''<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        .chart-container {{
            width: 100%;
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        canvas {{
            max-height: 400px;
        }}
    </style>
</head>
<body>
    <div class="chart-container">
        <canvas id="myChart"></canvas>
    </div>
    <script>
        const ctx = document.getElementById('myChart').getContext('2d');
        const chart = new Chart(ctx, {{
            type: '{chart_type}',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{
                    label: 'Dataset',
                    data: {json.dumps([v[0] if v else 0 for v in values])},
                    backgroundColor: 'rgba(102, 126, 234, 0.5)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>'''
        return html
    
    @staticmethod
    def import_graph(file_path: str) -> Dict:
        """Import graph definition (DOT, GraphML)"""
        path = Path(file_path)
        if not path.exists():
            return {'error': f'File not found: {file_path}'}
        
        content = path.read_text()
        
        return {
            'type': 'graph',
            'original': str(path),
            'content': content,
            'format': path.suffix[1:].upper()
        }
    
    @staticmethod
    def embed_in_document(content: str, media: List[Dict]) -> str:
        """Embed imported media into document"""
        doc_content = content
        
        for item in media:
            if item.get('type') == 'image':
                doc_content += f"\n\n## Image: {Path(item['original']).stem}\n\n{item['markdown']}\n"
            elif item.get('type') == 'chart' and item.get('data'):
                doc_content += f"\n\n## Chart: {Path(item['original']).stem}\n\n```json\n{str(item['data'][:3])}\n```\n"
            elif item.get('type') == 'graph':
                doc_content += f"\n\n## Graph: {Path(item['original']).stem}\n\n```{item['format'].lower()}\n{item['content'][:500]}\n```\n"
        
        return doc_content

class ChartGenerator:
    """Generate charts from data"""
    
    @staticmethod
    def create_chart(data: List[Dict], chart_type: str, title: str) -> str:
        """Create a chart visualization"""
        import json
        
        html = f'''<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        body {{ font-family: Arial; margin: 40px; }}
        .chart {{ max-width: 800px; margin: 0 auto; }}
        h1 {{ color: #667eea; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="chart">
        <canvas id="chartCanvas"></canvas>
    </div>
    <script>
        const data = {json.dumps(data)};
        const ctx = document.getElementById('chartCanvas').getContext('2d');
        new Chart(ctx, {{
            type: '{chart_type}',
            data: {{
                labels: data.map((_, i) => `Item ${{i+1}}`),
                datasets: [{{
                    label: 'Values',
                    data: data.map(row => Object.values(row)[0] || 0),
                    backgroundColor: '#667eea',
                    borderColor: '#764ba2',
                    borderWidth: 1
                }}]
            }}
        }});
    </script>
</body>
</html>'''
        return html
