# Fix for line 94 - Remove sensitive data logging
# Change from:
#     print(f"API Key: {api_key}, Request: {request_data}")
# To:
#     print(f"API Request: {request_data}")  # Don't log API key
#     logger.debug("API key present: %s", bool(api_key))

import logging
import os
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class LLMAPI:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("LLM_API_KEY")
        # Sanitize logging - never log the actual key
        if self.api_key:
            logger.debug("LLM API initialized with key (length: %d)", len(self.api_key))
    
    def make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict:
        """Make API request without logging sensitive data"""
        # Sanitized logging - no API key exposure
        logger.info("Making LLM API request to: %s", endpoint)
        logger.debug("Request payload size: %d bytes", len(str(data)))
        
        # Actual API call
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        
        # ... rest of implementation
        return {}
