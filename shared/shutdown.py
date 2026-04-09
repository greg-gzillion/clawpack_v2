"""Graceful Shutdown with Signal Handlers"""

import signal
import asyncio
import threading
import sys
from typing import Callable, List, Optional, Dict
from dataclasses import dataclass, field
from datetime import datetime
import time

@dataclass
class ShutdownContext:
    """Context for shutdown operations"""
    reason: str
    signal_name: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    cleanup_tasks: List[str] = field(default_factory=list)

class GracefulShutdown:
    """Manage graceful shutdown with cleanup handlers"""
    
    def __init__(self, timeout_seconds: float = 30.0):
        self.timeout = timeout_seconds
        self._handlers: List[Callable] = []
        self._async_handlers: List[Callable] = []
        self._shutdown_requested = False
        self._shutdown_context: Optional[ShutdownContext] = None
        self._lock = threading.Lock()
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Windows-specific
        if hasattr(signal, 'SIGBREAK'):
            signal.signal(signal.SIGBREAK, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        signal_names = {
            signal.SIGINT: "SIGINT",
            signal.SIGTERM: "SIGTERM",
        }
        if hasattr(signal, 'SIGBREAK'):
            signal_names[signal.SIGBREAK] = "SIGBREAK"
        
        signal_name = signal_names.get(signum, f"Signal({signum})")
        self.shutdown(f"Received {signal_name}")
    
    def register_handler(self, handler: Callable, is_async: bool = False):
        """Register a cleanup handler"""
        with self._lock:
            if is_async:
                self._async_handlers.append(handler)
            else:
                self._handlers.append(handler)
    
    def register_cleanup(self, name: str, cleanup_func: Callable):
        """Register a named cleanup function"""
        def handler():
            print(f"🧹 Cleaning up: {name}...")
            try:
                cleanup_func()
                print(f"   ✅ {name} cleaned up")
            except Exception as e:
                print(f"   ❌ {name} cleanup failed: {e}")
            return name
        
        self.register_handler(handler)
    
    def shutdown(self, reason: str = "Manual shutdown"):
        """Initiate graceful shutdown"""
        with self._lock:
            if self._shutdown_requested:
                return
            self._shutdown_requested = True
            self._shutdown_context = ShutdownContext(
                reason=reason,
                signal_name=reason,
                started_at=datetime.now()
            )
        
        print(f"\n🛑 Graceful shutdown initiated: {reason}")
        self._execute_shutdown()
    
    def _execute_shutdown(self):
        """Execute all cleanup handlers"""
        print(f"⏳ Shutting down (timeout: {self.timeout}s)...")
        
        # Run sync handlers
        for handler in self._handlers:
            try:
                name = handler()
                if name:
                    self._shutdown_context.cleanup_tasks.append(name)
            except Exception as e:
                print(f"   ❌ Handler failed: {e}")
        
        # Run async handlers
        if self._async_handlers:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    for handler in self._async_handlers:
                        asyncio.create_task(self._run_async_handler(handler))
                else:
                    for handler in self._async_handlers:
                        loop.run_until_complete(handler())
            except Exception as e:
                print(f"   ❌ Async handlers failed: {e}")
        
        self._shutdown_context.completed_at = datetime.now()
        duration = (self._shutdown_context.completed_at - self._shutdown_context.started_at).total_seconds()
        
        print(f"\n✅ Shutdown complete in {duration:.2f}s")
        print(f"   Cleaned up: {', '.join(self._shutdown_context.cleanup_tasks) if self._shutdown_context.cleanup_tasks else 'nothing'}")
    
    async def _run_async_handler(self, handler):
        try:
            await handler()
        except Exception as e:
            print(f"   ❌ Async handler failed: {e}")
    
    @property
    def is_shutting_down(self) -> bool:
        return self._shutdown_requested
    
    def wait(self):
        """Wait for shutdown to complete"""
        while not self._shutdown_requested:
            time.sleep(0.1)

class ShutdownManager:
    """Singleton shutdown manager"""
    
    _instance: Optional['ShutdownManager'] = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.shutdown = GracefulShutdown()
    
    def register(self, name: str, cleanup_func: Callable):
        """Register a cleanup function"""
        self.shutdown.register_cleanup(name, cleanup_func)
    
    def register_async(self, name: str, cleanup_func: Callable):
        """Register an async cleanup function"""
        async def handler():
            print(f"🧹 Cleaning up (async): {name}...")
            try:
                await cleanup_func()
                print(f"   ✅ {name} cleaned up")
            except Exception as e:
                print(f"   ❌ {name} cleanup failed: {e}")
            return name
        self.shutdown.register_handler(handler, is_async=True)

# Global instance
def get_shutdown_manager() -> ShutdownManager:
    return ShutdownManager()

# Convenience decorator
def on_shutdown(name: str):
    """Decorator to register a function for shutdown cleanup"""
    def decorator(func):
        get_shutdown_manager().register(name, func)
        return func
    return decorator
