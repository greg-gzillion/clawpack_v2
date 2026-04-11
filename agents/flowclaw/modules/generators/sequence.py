"""Sequence diagram generator module"""
class SequenceGenerator:
    @staticmethod
    def generate(description):
        return f"""sequenceDiagram
    participant User
    participant System
    User->>System: {description}
    System-->>User: Response"""
