"""Core diagram processing with guaranteed valid syntax"""
from engine.syntax_validator import SyntaxValidator

class DiagramEngine:
    
    def __init__(self):
        self.validator = SyntaxValidator()
    
    def generate(self, diagram_type: str, description: str, llm=None) -> str:
        """Generate diagram with guaranteed valid syntax"""
        
        # For now, use templates to guarantee valid output
        # (Will integrate LLM later for more complex diagrams)
        
        if diagram_type == "flowchart":
            code = self.validator.create_simple_flowchart(description)
        elif diagram_type == "sequence":
            code = self.validator.create_simple_sequence(description)
        elif diagram_type == "architecture":
            code = self.validator.create_simple_architecture(description)
        else:
            code = self.validator.create_simple_flowchart(description)
        
        # Validate and clean
        code = self.validator.validate_and_fix(code)
        
        return code
    
    def generate_with_llm(self, diagram_type: str, description: str, llm) -> str:
        """Generate using LLM with fallback to template"""
        try:
            prompts = {
                'flowchart': f"Create a valid Mermaid flowchart for: {description}. Use ONLY: graph TD, [] for processes, {{}} for decisions. Output ONLY valid Mermaid code:",
                'sequence': f"Create a valid Mermaid sequence diagram for: {description}. Use ONLY: sequenceDiagram, participant, ->> for arrows. Output ONLY valid Mermaid code:",
                'architecture': f"Create a valid Mermaid architecture diagram for: {description}. Use ONLY: graph TB, subgraph, square brackets. Output ONLY valid Mermaid code:",
            }
            
            prompt = prompts.get(diagram_type, prompts['flowchart'])
            code = llm.chat_sync(prompt, task_type="diagram")
            code = self.validator.validate_and_fix(code)
            
            if self.validator.is_valid(code):
                return code
        except:
            pass
        
        # Fallback to template
        return self.generate(diagram_type, description, None)
