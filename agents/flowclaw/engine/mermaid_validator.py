"""Validate and fix Mermaid syntax"""

class MermaidValidator:
    @staticmethod
    def validate_and_fix(code: str) -> str:
        """Fix common Mermaid syntax errors"""
        
        # Remove markdown code blocks
        if code.startswith('```'):
            lines = code.split('\n')
            code = '\n'.join(lines[1:-1])
        
        # Fix common issues
        fixes = [
            ('|>', '|'),           # Remove extra angle
            ('--|>', '-->'),       # Fix arrows
            ('-|>', '-->'),        # Fix arrows
            ('graph LR', 'graph TD'),  # Use top-down by default
            ('graph RL', 'graph TD'),
            ('>>', '>'),           # Fix angle brackets
            ('<<', '<'),
            ('participant "', 'participant '),  # Fix quotes
            ('" as "', ' as '),
        ]
        
        for old, new in fixes:
            code = code.replace(old, new)
        
        # Ensure flowchart has proper structure
        if 'graph' in code and '-->' not in code:
            code += '\n    A[Start] --> B[End]'
        
        # Ensure sequence diagram has participants
        if 'sequenceDiagram' in code and 'participant' not in code:
            code = 'sequenceDiagram\n    participant A\n    participant B\n' + code
        
        return code.strip()
    
    @staticmethod
    def is_valid(code: str) -> bool:
        """Basic validation"""
        if 'graph' in code or 'sequenceDiagram' in code or 'gantt' in code:
            return True
        return False
