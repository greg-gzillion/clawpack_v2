"""Rate limiting and robots.txt handling"""

import time
import re
import requests
from urllib.parse import urlparse
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Optional

class RateLimiter:
    """Rate limiter for web requests"""
    
    def __init__(self):
        self.last_request: Dict[str, float] = {}
        self.delay_seconds = 1.0  # Default 1 second between requests to same domain
        
    def can_request(self, url: str) -> bool:
        """Check if we can make a request to this domain"""
        domain = urlparse(url).netloc
        last = self.last_request.get(domain, 0)
        now = time.time()
        
        if now - last >= self.delay_seconds:
            self.last_request[domain] = now
            return True
        return False
    
    def wait_if_needed(self, url: str):
        """Wait if needed before making request"""
        domain = urlparse(url).netloc
        last = self.last_request.get(domain, 0)
        now = time.time()
        elapsed = now - last
        
        if elapsed < self.delay_seconds:
            wait_time = self.delay_seconds - elapsed
            time.sleep(wait_time)
        
        self.last_request[domain] = time.time()

class RobotsTxtParser:
    """Parse and respect robots.txt"""
    
    def __init__(self, user_agent: str = "WebClaw"):
        self.user_agent = user_agent
        self.cache: Dict[str, dict] = {}
    
    def get_rules(self, domain: str) -> dict:
        """Get rules for a domain"""
        if domain in self.cache:
            return self.cache[domain]
        
        rules = {"allow": [], "disallow": [], "crawl_delay": 1.0}
        
        try:
            robots_url = f"https://{domain}/robots.txt"
            response = requests.get(robots_url, timeout=10, headers={'User-Agent': self.user_agent})
            
            if response.status_code == 200:
                content = response.text
                current_agent = None
                
                for line in content.split('\n'):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    if line.lower().startswith('user-agent:'):
                        agent = line.split(':', 1)[1].strip()
                        current_agent = agent
                    
                    elif current_agent == self.user_agent or current_agent == '*':
                        if line.lower().startswith('disallow:'):
                            path = line.split(':', 1)[1].strip()
                            if path:
                                rules["disallow"].append(path)
                        elif line.lower().startswith('allow:'):
                            path = line.split(':', 1)[1].strip()
                            if path:
                                rules["allow"].append(path)
                        elif line.lower().startswith('crawl-delay:'):
                            try:
                                rules["crawl_delay"] = float(line.split(':', 1)[1].strip())
                            except:
                                pass
        except:
            pass
        
        self.cache[domain] = rules
        return rules
    
    def is_allowed(self, url: str) -> bool:
        """Check if URL is allowed to be crawled"""
        parsed = urlparse(url)
        domain = parsed.netloc
        path = parsed.path or "/"
        
        rules = self.get_rules(domain)
        
        # Check disallow first
        for disallow in rules["disallow"]:
            if path.startswith(disallow):
                # Check if there's an allow override
                for allow in rules["allow"]:
                    if path.startswith(allow):
                        return True
                return False
        
        return True
    
    def get_crawl_delay(self, url: str) -> float:
        """Get crawl delay for domain"""
        domain = urlparse(url).netloc
        rules = self.get_rules(domain)
        return rules.get("crawl_delay", 1.0)

# Singleton
_rate_limiter = None
_robots_parser = None

def get_rate_limiter():
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter

def get_robots_parser():
    global _robots_parser
    if _robots_parser is None:
        _robots_parser = RobotsTxtParser()
    return _robots_parser
