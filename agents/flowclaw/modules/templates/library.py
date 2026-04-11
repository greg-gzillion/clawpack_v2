"""Template library module"""
class TemplateLibrary:
    TEMPLATES = {
        'login': """graph TD
    A[Enter Credentials] --> B{Valid?}
    B -->|Yes| C[Dashboard]
    B -->|No| D[Error]""",
        'api': """sequenceDiagram
    Client->>Server: Request
    Server-->>Client: Response""",
        'deploy': """graph LR
    Build --> Test --> Deploy --> Monitor"""
    }
    
    @staticmethod
    def get(name):
        return TemplateLibrary.TEMPLATES.get(name, "graph TD\n    A[Start] --> B[End]")
    
    @staticmethod
    def list_all():
        return list(TemplateLibrary.TEMPLATES.keys())
