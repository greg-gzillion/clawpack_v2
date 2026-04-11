"""Template Library for common diagrams"""

class TemplateLibrary:
    TEMPLATES = {
        'business_process': '''graph TD
    A[Start Process] --> B{Approval?}
    B -->|Yes| C[Execute]
    B -->|No| D[Review]
    D --> B
    C --> E[End]''',
        
        'api_design': '''sequenceDiagram
    participant Client
    participant API
    participant DB
    Client->>API: Request
    API->>DB: Query
    DB-->>API: Result
    API-->>Client: Response''',
        
        'cloud_architecture': '''graph TB
    subgraph Cloud
        A[Load Balancer]
        B[App Server]
        C[Database]
    end
    User --> A --> B --> C''',
        
        'project_timeline': '''gantt
    title Project Timeline
    dateFormat YYYY-MM-DD
    section Phase 1
    Research :a1, 2024-01-01, 7d
    section Phase 2
    Development :after a1, 14d
    section Phase 3
    Testing :after a1, 21d''',
        
        'decision_tree': '''graph TD
    A[Start] --> B{Condition 1}
    B -->|Yes| C{Condition 2}
    B -->|No| D[Outcome B]
    C -->|Yes| E[Outcome A]
    C -->|No| F[Outcome C]''',
        
        'user_flow': '''graph LR
    A[Landing] --> B{Logged In?}
    B -->|Yes| C[Dashboard]
    B -->|No| D[Login]
    D --> E[Register]
    E --> C'''
    }
    
    @staticmethod
    def get(name):
        return TemplateLibrary.TEMPLATES.get(name, TemplateLibrary.TEMPLATES['business_process'])
    
    @staticmethod
    def list_all():
        return list(TemplateLibrary.TEMPLATES.keys())
