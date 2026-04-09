"""Structured JSON Logging"""

import json
import sys
from datetime import datetime
from typing import Any, Dict, Optional
from enum import Enum

class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class StructuredLogger:
    """JSON structured logger for production"""
    
    def __init__(self, service: str = "clawpack", level: LogLevel = LogLevel.INFO):
        self.service = service
        self.level = level
        self._extra_context: Dict[str, Any] = {}
    
    def with_context(self, **kwargs) -> 'StructuredLogger':
        """Create logger with additional context"""
        logger = StructuredLogger(self.service, self.level)
        logger._extra_context = {**self._extra_context, **kwargs}
        return logger
    
    def _log(self, level: LogLevel, message: str, **kwargs):
        """Internal log method"""
        if LogLevel[level.value] < LogLevel[self.level.value]:
            return
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level.value,
            "service": self.service,
            "message": message,
            **self._extra_context,
            **kwargs
        }
        
        # Remove None values
        log_entry = {k: v for k, v in log_entry.items() if v is not None}
        
        print(json.dumps(log_entry), file=sys.stderr if level in [LogLevel.ERROR, LogLevel.CRITICAL] else sys.stdout)
    
    def debug(self, message: str, **kwargs):
        self._log(LogLevel.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        self._log(LogLevel.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        self._log(LogLevel.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        self._log(LogLevel.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        self._log(LogLevel.CRITICAL, message, **kwargs)
    
    # Specialized loggers
    def tool_call(self, tool_name: str, args: dict = None, **kwargs):
        self.info(f"Tool called: {tool_name}", tool=tool_name, args=args, **kwargs)
    
    def tool_result(self, tool_name: str, duration_ms: float, success: bool, **kwargs):
        self.info(f"Tool completed: {tool_name}", tool=tool_name, duration_ms=duration_ms, success=success, **kwargs)
    
    def llm_request(self, provider: str, model: str, tokens: int, **kwargs):
        self.info(f"LLM request: {provider}/{model}", provider=provider, model=model, tokens=tokens, **kwargs)
    
    def llm_response(self, provider: str, tokens_used: int, duration_ms: float, cached: bool, **kwargs):
        self.info(f"LLM response: {provider}", provider=provider, tokens_used=tokens_used, duration_ms=duration_ms, cached=cached, **kwargs)
    
    def agent_start(self, agent_name: str, session_id: str, **kwargs):
        self.info(f"Agent started: {agent_name}", agent=agent_name, session_id=session_id, **kwargs)
    
    def agent_end(self, agent_name: str, session_id: str, turns: int, duration_ms: float, **kwargs):
        self.info(f"Agent ended: {agent_name}", agent=agent_name, session_id=session_id, turns=turns, duration_ms=duration_ms, **kwargs)

# Global logger
_logger = StructuredLogger(service="clawpack")

def get_logger(service: str = None) -> StructuredLogger:
    if service:
        return StructuredLogger(service=service)
    return _logger

# Convenience functions
def debug(msg, **kwargs): _logger.debug(msg, **kwargs)
def info(msg, **kwargs): _logger.info(msg, **kwargs)
def warning(msg, **kwargs): _logger.warning(msg, **kwargs)
def error(msg, **kwargs): _logger.error(msg, **kwargs)
def critical(msg, **kwargs): _logger.critical(msg, **kwargs)
