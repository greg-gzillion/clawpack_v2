"""Token Bucket Rate Limiter"""

import asyncio
import time
from typing import Optional
from dataclasses import dataclass
from collections import deque
from datetime import datetime

@dataclass
class RateLimitConfig:
    requests_per_minute: int = 60
    requests_per_day: int = 10000
    tokens_per_minute: int = 100000
    burst_size: int = 10

class TokenBucket:
    """Token bucket algorithm for rate limiting"""
    
    def __init__(self, rate: float, capacity: int):
        self.rate = rate  # Tokens per second
        self.capacity = capacity
        self.tokens = capacity
        self.last_refill = time.monotonic()
    
    def _refill(self):
        now = time.monotonic()
        elapsed = now - self.last_refill
        new_tokens = elapsed * self.rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill = now
    
    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens. Returns True if allowed."""
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
    
    async def wait_and_consume(self, tokens: int = 1, timeout: float = 60.0) -> bool:
        """Wait until tokens are available and consume them."""
        start = time.monotonic()
        
        while not self.consume(tokens):
            if time.monotonic() - start > timeout:
                return False
            await asyncio.sleep(0.1)
        
        return True

class RateLimiter:
    """Production rate limiter with multiple buckets"""
    
    def __init__(self, config: RateLimitConfig = None):
        self.config = config or RateLimitConfig()
        
        # Token buckets
        self.request_bucket = TokenBucket(
            rate=self.config.requests_per_minute / 60.0,
            capacity=self.config.burst_size
        )
        self.token_bucket = TokenBucket(
            rate=self.config.tokens_per_minute / 60.0,
            capacity=self.config.tokens_per_minute
        )
        
        # Daily tracking
        self.daily_requests: deque = deque()
        self.daily_tokens: deque = deque()
        
        # Stats
        self.total_requests = 0
        self.throttled_requests = 0
    
    def _clean_daily(self):
        """Remove entries older than 24 hours"""
        now = time.time()
        day_ago = now - 86400
        
        while self.daily_requests and self.daily_requests[0] < day_ago:
            self.daily_requests.popleft()
        
        while self.daily_tokens and self.daily_tokens[0] < day_ago:
            self.daily_tokens.popleft()
    
    def check_daily_limits(self, tokens: int = 0) -> bool:
        """Check if within daily limits"""
        self._clean_daily()
        
        if len(self.daily_requests) >= self.config.requests_per_day:
            return False
        
        if tokens > 0:
            current_tokens = sum(t for _, t in self.daily_tokens)
            if current_tokens + tokens > self.config.tokens_per_minute * 60 * 24:
                return False
        
        return True
    
    async def acquire(self, tokens: int = 1, timeout: float = 60.0) -> bool:
        """Acquire permission to make a request"""
        self.total_requests += 1
        
        # Check daily limits
        if not self.check_daily_limits(tokens):
            self.throttled_requests += 1
            return False
        
        # Check request rate
        if not await self.request_bucket.wait_and_consume(1, timeout):
            self.throttled_requests += 1
            return False
        
        # Check token rate
        if tokens > 0:
            if not await self.token_bucket.wait_and_consume(tokens, timeout):
                self.throttled_requests += 1
                return False
        
        # Record for daily tracking
        now = time.time()
        self.daily_requests.append(now)
        if tokens > 0:
            self.daily_tokens.append((now, tokens))
        
        return True
    
    def get_stats(self) -> dict:
        self._clean_daily()
        return {
            "total_requests": self.total_requests,
            "throttled_requests": self.throttled_requests,
            "throttle_rate": f"{(self.throttled_requests / max(1, self.total_requests)) * 100:.1f}%",
            "daily_requests_used": len(self.daily_requests),
            "daily_requests_limit": self.config.requests_per_day,
            "current_tokens": self.request_bucket.tokens,
            "daily_tokens_used": sum(t for _, t in self.daily_tokens)
        }

# Global instance
_rate_limiter = RateLimiter()

def get_rate_limiter() -> RateLimiter:
    return _rate_limiter
