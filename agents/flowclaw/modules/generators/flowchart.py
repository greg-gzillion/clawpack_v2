"""Flowchart generator module"""
class FlowchartGenerator:
    @staticmethod
    def generate(description):
        return f"""graph TD
    A[Start: {description}]
    B[Process Step]
    C{{Decision?}}
    D[Action]
    E[End]
    A --> B --> C
    C -->|Yes| D --> E
    C -->|No| E"""
