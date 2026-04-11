"""Output formatters for different formats"""
import json

class OutputFormatter:
    @staticmethod
    def to_mermaid(diagram_data: Dict) -> str:
        """Convert to Mermaid format"""
        return diagram_data.get('code', '')
    
    @staticmethod
    def to_plantuml(diagram_data: Dict) -> str:
        """Convert to PlantUML format"""
        # Basic conversion
        mermaid = diagram_data.get('code', '')
        plantuml = mermaid.replace('graph TD', '@startuml\n').replace('-->', '->')
        return plantuml + '\n@enduml'
    
    @staticmethod
    def to_json(diagram_data: Dict) -> str:
        """Export as JSON"""
        return json.dumps(diagram_data, indent=2)
