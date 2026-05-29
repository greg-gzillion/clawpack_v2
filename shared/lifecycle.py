"""
Agent Lifecycle Supervisor - guaranteed cleanup for every agent invocation.

Claude Code's runAgent() has a 15-step finally block that cleans up every
resource an agent touched. This is the distributed equivalent - called
from a2a_server.py around every process_task() invocation.

Usage in a2a_server.py:
    from shared.lifecycle import wrap_with_lifecycle
    result = wrap_with_lifecycle("lawclaw", task, lawclaw_process, task)
"""
import gc
import time


def agent_cleanup(agent_name: str, task: str = "", duration_ms: float = 0):
    """Called after every agent invocation. Guaranteed to run."""
    errors = []
    try:
        gc.collect()
    except Exception as e:
        errors.append(f"gc: {e}")
    try:
        from agents.webclaw.core.chronicle_ledger import log_event
        log_event(
            agent=agent_name,
            event="agent_invocation_complete",
            detail=f"task={str(task)[:100]} duration_ms={duration_ms:.0f}"
        )
    except Exception as e:
        errors.append(f"log: {e}")
    try:
        from shared.decision_ledger import get_ledger
        get_ledger().record(
            agent=agent_name,
            action="invocation_complete",
            query=str(task)[:200],
            result=f"duration_ms={duration_ms:.0f}"
        )
    except Exception as e:
        errors.append(f"ledger: {e}")
    if errors:
        try:
            print(f"[lifecycle] {agent_name} cleanup errors: {errors}", flush=True)
        except Exception:
            pass


def wrap_with_lifecycle(agent_name: str, task: str, fn, *args, **kwargs):
    """Wrap an agent invocation with lifecycle management."""
    start = time.time()
    try:
        result = fn(*args, **kwargs)
        return result
    except Exception as e:
        try:
            from shared._agent_helpers import log_err
            log_err(agent_name, "lifecycle_error", str(e)[:200])
        except Exception:
            pass
        raise
    finally:
        duration_ms = (time.time() - start) * 1000
        agent_cleanup(agent_name, task, duration_ms)
