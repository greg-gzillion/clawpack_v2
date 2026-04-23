"""Complete Security with Input Sanitization & Audit Logging"""

import re
import hashlib
import secrets
from pathlib import Path
from typing import Optional, List
from datetime import datetime

class InputSanitizer:
    """Sanitize user inputs"""
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Remove path traversal characters"""
        # Remove any path separators
        filename = re.sub(r'[/\\:\*\?"<>\|]', '_', filename)
        # Remove dot segments
        filename = re.sub(r'\.\.', '_', filename)
        # Limit length
        return filename
    
    @staticmethod
    def sanitize_sql_like(text: str) -> str:
        """Escape SQL-like patterns"""
        return text.replace("'", "''").replace(";", "")
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """Escape HTML tags"""
        return text.replace("<", "&lt;").replace(">", "&gt;")
    
    @staticmethod
    def validate_path(path: str, base_dir: Path) -> Optional[Path]:
        """Ensure path is within base directory"""
        try:
            resolved = (base_dir / path).resolve()
            if str(resolved).startswith(str(base_dir.resolve())):
                return resolved
        except:
            pass
        return None

class AuditLogger:
    """Security audit logging"""
    
    def __init__(self, log_dir: Path = None):
        self.log_dir = log_dir or Path.home() / ".clawpack" / "audit"
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def _write(self, event_type: str, **details):
        log_file = self.log_dir / f"audit_{datetime.now().strftime('%Y%m%d')}.jsonl"
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            **details
        }
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(str(entry).replace("'", '"') + "\n")
    
    def log_auth(self, user: str, success: bool, **details):
        self._write("auth", user=user, success=success, **details)
    
    def log_tool_call(self, tool: str, args: dict, user: str = "system"):
        # Redact sensitive args
        safe_args = {k: ("***" if any(s in k.lower() for s in ["key", "token", "password", "secret"]) else v) 
                     for k, v in args.items()}
        self._write("tool_call", tool=tool, args=safe_args, user=user)
    
    def log_file_access(self, path: str, operation: str, user: str = "system"):
        self._write("file_access", path=path, operation=operation, user=user)
    
    def log_permission_denied(self, resource: str, reason: str, user: str = "system"):
        self._write("permission_denied", resource=resource, reason=reason, user=user)

class SecretManager:
    """Secure secret handling"""
    
    @staticmethod
    def mask_secret(secret: str, visible_chars: int = 4) -> str:
        if len(secret) <= visible_chars * 2:
            return "*" * len(secret)
        return secret[:visible_chars] + "*" * (len(secret) - visible_chars * 2) + secret[-visible_chars:]
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def hash_secret(secret: str) -> str:
        return hashlib.sha256(secret.encode()).hexdigest()

class RateLimitByIP:
    """IP-based rate limiting"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self._requests: dict = {}
    
    def is_allowed(self, ip: str) -> bool:
        now = datetime.now().timestamp()
        window_start = now - self.window
        
        # Clean old entries
        self._requests = {k: v for k, v in self._requests.items() if v["timestamp"] > window_start}
        
        if ip not in self._requests:
            self._requests[ip] = {"count": 1, "timestamp": now}
            return True
        
        if self._requests[ip]["count"] >= self.max_requests:
            return False
        
        self._requests[ip]["count"] += 1
        return True

# Global instances
_sanitizer = InputSanitizer()
_audit_logger = AuditLogger()
_secret_manager = SecretManager()
_ip_rate_limiter = RateLimitByIP()

def get_sanitizer() -> InputSanitizer:
    return _sanitizer

def get_audit_logger() -> AuditLogger:
    return _audit_logger

def get_secret_manager() -> SecretManager:
    return _secret_manager

def get_ip_rate_limiter() -> RateLimitByIP:
    return _ip_rate_limiter
