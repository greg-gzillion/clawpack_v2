"""Architecture diagram generator module"""
class ArchitectureGenerator:
    @staticmethod
    def generate(description):
        return """graph TB
    subgraph Frontend[Frontend]
        A[UI]
    end
    subgraph Backend[Backend]
        B[API]
        C[Logic]
    end
    subgraph Data[Data]
        D[(DB)]
    end
    A --> B --> C --> D"""
