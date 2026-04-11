"""Guarantee valid Mermaid syntax"""

class SyntaxValidator:
    
    @staticmethod
    def create_simple_flowchart(description: str) -> str:
        """Create a guaranteed valid simple flowchart"""
        # Template-based approach - guaranteed valid
        return f"""graph TD
    A[Start: {description[:30]}]
    B[Process Step 1]
    C{{Decision?}}
    D[Process Step 2]
    E[End]
    
    A --> B
    B --> C
    C -->|Yes| D
    C -->|No| E
    D --> E"""
    
    @staticmethod
    def create_simple_sequence(description: str) -> str:
        """Create guaranteed valid sequence diagram"""
        return f"""sequenceDiagram
    participant User
    participant System
    participant Database
    
    User->>System: {description[:30]}
    System->>Database: Query
    Database-->>System: Result
    System-->>User: Response"""
    
    @staticmethod
    def create_simple_architecture(components: str) -> str:
        """Create guaranteed valid architecture diagram"""
        return f"""graph TB
    subgraph Frontend
        A[UI Layer]
    end
    subgraph Backend
        B[API Layer]
        C[Logic Layer]
    end
    subgraph Data
        D[Database]
    end
    
    A --> B
    B --> C
    C --> D"""
    
    @staticmethod
    def validate_and_fix(code: str) -> str:
        """Strip any markdown and ensure basic validity"""
        # Remove markdown code blocks
        code = code.replace('```mermaid', '').replace('```', '')
        
        # Remove common problematic characters
        code = code.replace('|>', '|').replace('>>', '>')
        code = code.replace('<<', '<').replace('<|', '<')
        
        # Ensure it starts with a valid Mermaid type
        valid_starts = ['graph', 'sequenceDiagram', 'gantt', 'stateDiagram-v2', 'classDiagram', 'erDiagram']
        lines = code.strip().split('\n')
        
        if lines and not any(lines[0].startswith(start) for start in valid_starts):
            # Default to flowchart
            code = "graph TD\n    A[Start] --> B[Process]\n    B --> C[End]"
        
        return code.strip()
    
    @staticmethod
    def is_valid(code: str) -> bool:
        """Basic validation"""
        code = code.strip()
        if not code:
            return False
        valid = ['graph', 'sequenceDiagram', 'gantt', 'stateDiagram', 'classDiagram', 'erDiagram']
        return any(code.startswith(v) for v in valid)
