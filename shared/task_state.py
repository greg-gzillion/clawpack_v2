"""Task State Machine — track every cross-agent call.

Constitutional requirement: every call_agent() creates a task with:
  - Unique ID
  - Status: pending -> running -> completed | failed | killed
  - Timing (start, end, duration)
  - Result reference
  - Calling agent + target agent

Pattern from Claude Code Ch8-10: state machine + disk persistence.
"""
import json
import time
import uuid
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, List

TASK_STORE = Path(__file__).parent.parent / "data" / "task_store.json"


class TaskStatus:
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    KILLED = "killed"


class Task:
    def __init__(self, caller: str, target: str, task_text: str, timeout: int = 120):
        self.id = f"task-{uuid.uuid4().hex[:8]}"
        self.caller = caller
        self.target = target
        self.task_text = task_text[:500]
        self.timeout = timeout
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.started_at = None
        self.completed_at = None
        self.duration_ms = 0
        self.result = None
        self.error = None

    def start(self):
        self.status = TaskStatus.RUNNING
        self.started_at = datetime.now(timezone.utc).isoformat()

    def complete(self, result: str):
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now(timezone.utc).isoformat()
        self.result = result[:1000]
        if self.started_at:
            start = datetime.fromisoformat(self.started_at)
            end = datetime.fromisoformat(self.completed_at)
            self.duration_ms = int((end - start).total_seconds() * 1000)

    def fail(self, error: str):
        self.status = TaskStatus.FAILED
        self.completed_at = datetime.now(timezone.utc).isoformat()
        self.error = error[:500]

    def kill(self):
        self.status = TaskStatus.KILLED
        self.completed_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "caller": self.caller,
            "target": self.target,
            "task": self.task_text,
            "timeout": self.timeout,
            "status": self.status,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration_ms": self.duration_ms,
            "result": self.result,
            "error": self.error,
        }


class TaskStore:
    """Persistent task tracking across sessions."""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self._load()

    def _load(self):
        if TASK_STORE.exists():
            try:
                data = json.loads(TASK_STORE.read_text())
                for t in data.get("tasks", []):
                    task = Task(t["caller"], t["target"], t.get("task", ""))
                    task.id = t["id"]
                    task.status = t.get("status", "unknown")
                    task.created_at = t.get("created_at", "")
                    task.started_at = t.get("started_at", "")
                    task.completed_at = t.get("completed_at", "")
                    task.duration_ms = t.get("duration_ms", 0)
                    task.result = t.get("result", "")
                    task.error = t.get("error", "")
                    self.tasks[task.id] = task
            except Exception:
                pass

    def _save(self):
        TASK_STORE.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "tasks": [t.to_dict() for t in self.tasks.values()],
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        TASK_STORE.write_text(json.dumps(data, indent=2, default=str))

    def create(self, caller: str, target: str, task_text: str, timeout: int = 120) -> Task:
        task = Task(caller, target, task_text, timeout)
        self.tasks[task.id] = task
        self._save()
        return task

    def get(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)

    def get_active(self) -> List[Task]:
        return [t for t in self.tasks.values() if t.status in (TaskStatus.PENDING, TaskStatus.RUNNING)]

    def get_recent(self, limit: int = 10) -> List[Task]:
        tasks = sorted(self.tasks.values(), key=lambda t: t.created_at, reverse=True)
        return tasks[:limit]

    def get_by_caller(self, caller: str, limit: int = 20) -> List[Task]:
        return [t for t in self.tasks.values() if t.caller == caller][:limit]

    def get_stats(self) -> dict:
        tasks = list(self.tasks.values())
        return {
            "total": len(tasks),
            "completed": sum(1 for t in tasks if t.status == TaskStatus.COMPLETED),
            "failed": sum(1 for t in tasks if t.status == TaskStatus.FAILED),
            "running": sum(1 for t in tasks if t.status == TaskStatus.RUNNING),
            "pending": sum(1 for t in tasks if t.status == TaskStatus.PENDING),
            "killed": sum(1 for t in tasks if t.status == TaskStatus.KILLED),
            "avg_duration_ms": int(sum(t.duration_ms for t in tasks if t.duration_ms) / max(1, sum(1 for t in tasks if t.duration_ms))),
        }


# Singleton
_store = None

def get_task_store() -> TaskStore:
    global _store
    if _store is None:
        _store = TaskStore()
    return _store
