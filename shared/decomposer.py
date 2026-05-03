"""Task decomposition for complex commands"""

from typing import List, Tuple, Dict
from dataclasses import dataclass
from enum import Enum

class TaskType(Enum):
    BUILD = "build"
    CREATE = "create"
    ANALYZE = "analyze"
    REFACTOR = "refactor"
    TEST = "test"
    DEPLOY = "deploy"

@dataclass
class SubTask:
    name: str
    description: str
    estimated_time: int  # minutes
    dependencies: List[str]
    agent: str

class TaskDecomposer:
    """Break complex tasks into manageable sub-tasks"""
    
    def __init__(self):
        self.task_patterns = {
            TaskType.BUILD: ['build', 'construct', 'create', 'develop'],
            TaskType.CREATE: ['create', 'generate', 'make', 'write'],
            TaskType.ANALYZE: ['analyze', 'review', 'check', 'inspect'],
            TaskType.REFACTOR: ['refactor', 'restructure', 'optimize'],
            TaskType.TEST: ['test', 'validate', 'verify', 'check'],
            TaskType.DEPLOY: ['deploy', 'release', 'publish', 'launch'],
        }
    
    def identify_task_type(self, task: str) -> TaskType:
        """Identify the type of task"""
        task_lower = task.lower()
        for task_type, keywords in self.task_patterns.items():
            if any(kw in task_lower for kw in keywords):
                return task_type
        return TaskType.BUILD
    
    def decompose(self, task: str) -> List[SubTask]:
        """Decompose task into sub-tasks"""
        task_type = self.identify_task_type(task)
        
        decompositions = {
            TaskType.BUILD: [
                SubTask("design", f"Design architecture for {task}", 30, [], "architect"),
                SubTask("implement", f"Implement core functionality for {task}", 60, ["design"], "developer"),
                SubTask("test", f"Test {task} implementation", 30, ["implement"], "qa"),
                SubTask("document", f"Document {task}", 20, ["implement"], "writer"),
            ],
            TaskType.CREATE: [
                SubTask("plan", f"Plan {task} structure", 15, [], "planner"),
                SubTask("generate", f"Generate {task} code", 30, ["plan"], "coder"),
                SubTask("review", f"Review generated {task}", 15, ["generate"], "reviewer"),
            ],
            TaskType.ANALYZE: [
                SubTask("scan", f"Scan {task} for issues", 10, [], "scanner"),
                SubTask("analyze", f"Deep analysis of {task}", 20, ["scan"], "analyst"),
                SubTask("report", f"Generate analysis report", 10, ["analyze"], "reporter"),
            ],
            TaskType.REFACTOR: [
                SubTask("audit", f"Audit current {task} state", 15, [], "auditor"),
                SubTask("plan", f"Plan refactoring strategy", 20, ["audit"], "architect"),
                SubTask("execute", f"Execute refactoring", 45, ["plan"], "developer"),
                SubTask("validate", f"Validate refactoring", 15, ["execute"], "qa"),
            ],
        }
        
        return decompositions.get(task_type, decompositions[TaskType.BUILD])
    
    def estimate_time(self, subtasks: List[SubTask]) -> int:
        """Estimate total time for all subtasks"""
        return sum(st.estimated_time for st in subtasks)

# Global instance
task_decomposer = TaskDecomposer()
