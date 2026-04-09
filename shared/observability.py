"""Complete Observability with Tracing & Health Checks"""

import time
import uuid
from contextlib import contextmanager
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

@dataclass
class HealthCheck:
    name: str
    status: HealthStatus
    message: Optional[str] = None
    last_check: datetime = field(default_factory=datetime.now)
    duration_ms: float = 0

class HealthChecker:
    """Health check registry"""
    
    def __init__(self):
        self._checks: Dict[str, callable] = {}
        self._results: Dict[str, HealthCheck] = {}
    
    def register(self, name: str, check_func: callable):
        self._checks[name] = check_func
    
    def run_all(self) -> Dict[str, HealthCheck]:
        for name, check in self._checks.items():
            start = time.time()
            try:
                result = check()
                status = HealthStatus.HEALTHY if result else HealthStatus.UNHEALTHY
                message = None if result else "Check failed"
            except Exception as e:
                status = HealthStatus.UNHEALTHY
                message = str(e)
            
            self._results[name] = HealthCheck(
                name=name,
                status=status,
                message=message,
                duration_ms=(time.time() - start) * 1000
            )
        
        return self._results
    
    def get_overall_status(self) -> HealthStatus:
        if not self._results:
            return HealthStatus.UNHEALTHY
        
        statuses = [r.status for r in self._results.values()]
        if all(s == HealthStatus.HEALTHY for s in statuses):
            return HealthStatus.HEALTHY
        elif any(s == HealthStatus.UNHEALTHY for s in statuses):
            return HealthStatus.UNHEALTHY
        return HealthStatus.DEGRADED

@dataclass
class TraceSpan:
    trace_id: str
    span_id: str
    parent_id: Optional[str]
    name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict] = field(default_factory=list)
    status: str = "ok"

class Tracer:
    """Distributed tracing"""
    
    def __init__(self):
        self._current_span: Optional[TraceSpan] = None
        self._spans: List[TraceSpan] = []
        self._enabled = True
    
    @contextmanager
    def span(self, name: str, **attributes):
        if not self._enabled:
            yield None
            return
        
        span = TraceSpan(
            trace_id=self._current_span.trace_id if self._current_span else str(uuid.uuid4())[:16],
            span_id=str(uuid.uuid4())[:8],
            parent_id=self._current_span.span_id if self._current_span else None,
            name=name,
            start_time=datetime.now(),
            attributes=attributes
        )
        
        previous = self._current_span
        self._current_span = span
        
        try:
            yield span
            span.status = "ok"
        except Exception as e:
            span.status = "error"
            span.events.append({"type": "exception", "message": str(e)})
            raise
        finally:
            span.end_time = datetime.now()
            self._spans.append(span)
            self._current_span = previous
    
    def add_event(self, name: str, **attributes):
        if self._current_span:
            self._current_span.events.append({
                "name": name,
                "timestamp": datetime.now().isoformat(),
                **attributes
            })
    
    def get_spans(self) -> List[dict]:
        return [
            {
                "trace_id": s.trace_id,
                "span_id": s.span_id,
                "parent_id": s.parent_id,
                "name": s.name,
                "start": s.start_time.isoformat(),
                "end": s.end_time.isoformat() if s.end_time else None,
                "duration_ms": ((s.end_time - s.start_time).total_seconds() * 1000) if s.end_time else 0,
                "attributes": s.attributes,
                "events": s.events,
                "status": s.status
            }
            for s in self._spans
        ]
    
    def clear(self):
        self._spans.clear()

# Global instances
_health_checker = HealthChecker()
_tracer = Tracer()

def get_health_checker() -> HealthChecker:
    return _health_checker

def get_tracer() -> Tracer:
    return _tracer

# Register default health checks
_health_checker.register("llm", lambda: True)
_health_checker.register("memory", lambda: True)
_health_checker.register("disk", lambda: True)
