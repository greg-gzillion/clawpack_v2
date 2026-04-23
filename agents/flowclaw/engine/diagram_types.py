"""All supported diagram types"""
from enum import Enum

class DiagramType(Enum):
    FLOWCHART = "flowchart"
    SEQUENCE = "sequence"
    ARCHITECTURE = "architecture"
    GANTT = "gantt"
    STATE = "state"
    CLASS = "class"
    ER = "er"
    TIMELINE = "timeline"
    PIE = "pie"
    MINDMAP = "mindmap"
    USER_JOURNEY = "user_journey"
    GITGRAPH = "gitgraph"
    C4 = "c4"

class DiagramGenerator:
    @staticmethod
    def get_template(diagram_type: str, description: str) -> str:
        templates = {
            'timeline': f"""timeline
    title {description}
    section Phase 1
        Planning : 2024-01-01 : 2024-01-15
        Design : 2024-01-16 : 2024-02-15
    section Phase 2
        Development : 2024-02-16 : 2024-04-15
        Testing : 2024-04-16 : 2024-05-15
    section Phase 3
        Deployment : 2024-05-16 : 2024-06-01
        Review : after Deployment""",
            'pie': f"""pie title {description}
    "Completed" : 65
    "In Progress" : 25
    "Not Started" : 10""",
            'mindmap': f"""mindmap
    root(({description}))
        Main Topic 1
            Subtopic A
            Subtopic B
        Main Topic 2
            Subtopic C
            Subtopic D""",
            'user_journey': f"""journey
    title {description}
    section Research
        Visit website: 5: User
        Compare options: 3: User
    section Decision
        Select product: 5: User
        Add to cart: 4: User
    section Purchase
        Checkout: 5: User
        Complete: 5: User""",
            'gitgraph': 'gitGraph\n    commit id: "Initial"\n    branch feature\n    checkout feature\n    commit id: "Development"\n    checkout main\n    merge feature\n    commit id: "Release v1.0"',
            'c4': f"""C4Context
    title {description}
    Person(user, "End User", "System user")
    System(system, "Main System", "Core application")
    Rel(user, system, "Uses")"""
        }
        return templates.get(diagram_type, "")
