"""Production Error Handling with Exponential Backoff"""

import asyncio
import random
from typing import TypeVar, Callable, Any, Dict, List
from dataclasses import dataclass
from datetime import datetime
from functools import wraps

T = TypeVar('T')

class RetryableError(Exception):
    """Error that can be retried"""
    pass

class PermanentError(Exception):
    """Error that should NOT be retried"""
    pass

@dataclass
class RetryConfig:
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True

class RetryHandler:
    """Exponential backoff with jitter"""
    
    def __init__(self, config: RetryConfig = None):
        self.config = config or RetryConfig()
        self.attempts = 0
        self.errors: List[Exception] = []
    
    async def execute(self, func: Callable[..., T], *args, **kwargs) -> T:
        """Execute function with retry logic"""
        delay = self.config.base_delay
        
        for attempt in range(self.config.max_retries + 1):
            try:
                self.attempts = attempt + 1
                return await func(*args, **kwargs)
                
            except PermanentError as e:
                self.errors.append(e)
                raise
                
            except Exception as e:
                self.errors.append(e)
                
                if attempt == self.config.max_retries:
                    raise Exception(f"Max retries ({self.config.max_retries}) exceeded. Last error: {e}")
                
                # Calculate backoff
                if self.config.jitter:
                    delay = delay * self.config.exponential_base + random.uniform(0, 0.1)
                else:
                    delay = delay * self.config.exponential_base
                
                delay = min(delay, self.config.max_delay)
                
                print(f"⚠️ Attempt {attempt + 1} failed: {str(e)[:100]}. Retrying in {delay:.1f}s...")
                await asyncio.sleep(delay)
        
        raise Exception("Unreachable")
    
    def get_stats(self) -> dict:
        return {
            "attempts": self.attempts,
            "errors": [str(e)[:100] for e in self.errors],
            "success": self.attempts <= self.config.max_retries
        }

def retryable(func):
    """Decorator for retryable functions"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        handler = RetryHandler()
        return await handler.execute(func, *args, **kwargs)
    return wrapper

class ErrorHandler:
    """Centralized error handling"""
    
    @staticmethod
    def classify(error: Exception) -> str:
        """Classify error for appropriate handling"""
        error_str = str(error).lower()
        
        if "rate limit" in error_str or "429" in error_str:
            return "rate_limit"
        elif "timeout" in error_str:
            return "timeout"
        elif "connection" in error_str:
            return "connection"
        elif "auth" in error_str or "401" in error_str or "403" in error_str:
            return "auth"
        elif "not found" in error_str or "404" in error_str:
            return "not_found"
        else:
            return "unknown"
    
    @staticmethod
    def is_retryable(error: Exception) -> bool:
        """Check if error should be retried"""
        classification = ErrorHandler.classify(error)
        return classification in ["rate_limit", "timeout", "connection"]
    
    @staticmethod
    def handle(error: Exception, context: dict = None) -> dict:
        """Handle error and return standardized response"""
        classification = ErrorHandler.classify(error)
        context = context or {}
        
        response = {
            "success": False,
            "error": str(error),
            "error_type": classification,
            "retryable": ErrorHandler.is_retryable(error),
            "timestamp": datetime.now().isoformat(),
            "context": context
        }
        
        # Log error (would go to structured logging)
        print(f"❌ [{classification.upper()}] {str(error)[:200]}")
        
        return response
"""Complete Error Handling with Circuit Breaker & Dead Letter Queue"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum

class CircuitState(str, Enum):
    CLOSED = "closed"       # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    recovery_timeout: int = 60  # seconds
    half_open_max_calls: int = 3

class CircuitBreaker:
    """Circuit breaker pattern for fault tolerance"""
    
    def __init__(self, name: str, config: CircuitBreakerConfig = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.half_open_calls = 0
    
    def call(self, func, *args, **kwargs):
        """Call function with circuit breaker protection"""
        if self.state == CircuitState.OPEN:
            if self._should_try_recovery():
                self.state = CircuitState.HALF_OPEN
                self.half_open_calls = 0
            else:
                raise Exception(f"Circuit {self.name} is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.half_open_calls += 1
            if self.half_open_calls >= self.config.half_open_max_calls:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
        else:
            self.failure_count = 0
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
        elif self.failure_count >= self.config.failure_threshold:
            self.state = CircuitState.OPEN
    
    def _should_try_recovery(self) -> bool:
        if not self.last_failure_time:
            return True
        elapsed = (datetime.now() - self.last_failure_time).total_seconds()
        return elapsed >= self.config.recovery_timeout
    
    def get_state(self) -> dict:
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "last_failure": self.last_failure_time.isoformat() if self.last_failure_time else None
        }

@dataclass
class DeadLetter:
    """Failed message stored for later processing"""
    id: str
    original_request: Dict[str, Any]
    error: str
    failed_at: datetime
    retry_count: int = 0
    max_retries: int = 3

class DeadLetterQueue:
    """Store failed requests for later retry"""
    
    def __init__(self, storage_path: Path = None):
        self.storage_path = storage_path or Path.home() / ".clawpack" / "dead_letters"
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._queue: List[DeadLetter] = []
        self._load()
    
    def add(self, request: Dict[str, Any], error: str):
        import uuid
        letter = DeadLetter(
            id=str(uuid.uuid4())[:8],
            original_request=request,
            error=error,
            failed_at=datetime.now()
        )
        self._queue.append(letter)
        self._save()
        return letter.id
    
    def get_pending(self) -> List[DeadLetter]:
        return [l for l in self._queue if l.retry_count < l.max_retries]
    
    def mark_retried(self, letter_id: str):
        for letter in self._queue:
            if letter.id == letter_id:
                letter.retry_count += 1
                self._save()
                return
    
    def remove(self, letter_id: str):
        self._queue = [l for l in self._queue if l.id != letter_id]
        self._save()
    
    def _save(self):
        data = []
        for letter in self._queue:
            data.append({
                "id": letter.id,
                "request": letter.original_request,
                "error": letter.error,
                "failed_at": letter.failed_at.isoformat(),
                "retry_count": letter.retry_count
            })
        (self.storage_path / "queue.json").write_text(json.dumps(data, indent=2))
    
    def _load(self):
        path = self.storage_path / "queue.json"
        if path.exists():
            data = json.loads(path.read_text())
            for item in data:
                self._queue.append(DeadLetter(
                    id=item["id"],
                    original_request=item["request"],
                    error=item["error"],
                    failed_at=datetime.fromisoformat(item["failed_at"]),
                    retry_count=item["retry_count"]
                ))
    
    def stats(self) -> dict:
        pending = len(self.get_pending())
        total = len(self._queue)
        return {
            "total": total,
            "pending": pending,
            "completed": total - pending
        }

# Global circuit breakers
_circuit_breakers: Dict[str, CircuitBreaker] = {}

def get_circuit_breaker(name: str) -> CircuitBreaker:
    if name not in _circuit_breakers:
        _circuit_breakers[name] = CircuitBreaker(name)
    return _circuit_breakers[name]

# Global dead letter queue
_dlq = None

def get_dead_letter_queue() -> DeadLetterQueue:
    global _dlq
    if _dlq is None:
        _dlq = DeadLetterQueue()
    return _dlq
