"""Advanced diagram processing engine"""
import re
from typing import Dict, List

class DiagramProcessor:
    """Process and validate diagrams"""
    
    @staticmethod
    def validate_mermaid(code: str) -> Dict:
        """Validate Mermaid syntax"""
        errors = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            if 'graph' in line and '-->' not in code:
                errors.append(f"Line {i}: Missing arrow syntax")
            if 'sequenceDiagram' in line and '->>' not in code:
                errors.append(f"Line {i}: Invalid sequence syntax")
        
        return {'valid': len(errors) == 0, 'errors': errors}
    
    @staticmethod
    def optimize_layout(code: str) -> str:
        """Optimize diagram layout"""
        # Add direction hints
        if 'graph TD' in code:
            code = code.replace('graph TD', 'graph TB')
        return code
    
    @staticmethod
    def add_styling(code: str) -> str:
        """Add professional styling"""
        style = """
    classDef process fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef decision fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef startEnd fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px
"""
        return code + style
