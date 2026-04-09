"""DocuClaw LLM Agent - Document generation and processing"""
from .. import get_llm

class DocuClawLLM:
    def __init__(self):
        self.llm = get_llm()
    
    def generate_document(self, doc_type: str, topic: str, audience: str = "general") -> str:
        """Generate a document based on type and topic"""
        prompt = f"Generate a {doc_type} document about '{topic}' for {audience} audience. Include proper structure and formatting."
        return self.llm.generate(prompt, task="general").text
    
    def improve_writing(self, text: str, style: str = "professional") -> str:
        """Improve writing quality and style"""
        prompt = f"Improve this writing to be more {style} while preserving meaning:\n\n{text}"
        return self.llm.generate(prompt, task="general").text
    
    def summarize_document(self, document: str, length: str = "medium") -> str:
        """Summarize a document"""
        prompt = f"Provide a {length} summary of this document:\n\n{document[:3000]}"
        return self.llm.generate(prompt, task="general").text
    
    def check_grammar(self, text: str) -> str:
        """Check grammar and suggest corrections"""
        prompt = f"Check this text for grammar, spelling, and style issues:\n\n{text}"
        return self.llm.generate(prompt, task="general").text
    
    def generate_template(self, doc_type: str, sections: list) -> str:
        """Generate a document template"""
        prompt = f"Generate a {doc_type} template with these sections: {', '.join(sections)}. Include placeholders and instructions."
        return self.llm.generate(prompt, task="general").text
    
    def convert_format(self, content: str, from_format: str, to_format: str) -> str:
        """Convert between document formats"""
        prompt = f"Convert this {from_format} content to {to_format} format:\n\n{content}"
        return self.llm.generate(prompt, task="general").text
