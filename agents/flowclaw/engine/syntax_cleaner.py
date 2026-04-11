"""Clean and validate Mermaid syntax"""
import re

class MermaidCleaner:
    @staticmethod
    def clean_flowchart(code: str) -> str:
        """Clean flowchart syntax"""
        # Remove extra angle brackets
        code = re.sub(r'--+\|', '-->|', code)
        code = re.sub(r'\|>', '|', code)
        code = re.sub(r'>>', '>', code)
        
        # Fix common issues
        code = code.replace('graph LR', 'graph TD')
        code = code.replace('-->|>', '-->|')
        code = code.replace('|>', '|')
        
        return code
    
    @staticmethod
    def clean_sequence(code: str) -> str:
        """Clean sequence diagram syntax"""
        # Fix participant lines
        code = re.sub(r'participant\s+(\w+)\s+as\s+"([^"]+)"', r'participant \1 as \2', code)
        return code
    
    @staticmethod
    def validate_and_fix(code: str, diagram_type: str = "flowchart") -> str:
        """Validate and fix common syntax errors"""
        if diagram_type == "flowchart":
            return MermaidCleaner.clean_flowchart(code)
        elif diagram_type == "sequence":
            return MermaidCleaner.clean_sequence(code)
        return code
