# Fix for line 15 and 45 - Remove sensitive data exposure

import logging
import os
from flask import Flask, request, jsonify

logger = logging.getLogger(__name__)
app = Flask(__name__)

# Line 15 fix - Don't log sensitive config
# Before: print(f"Starting server with config: {config}")
# After:
def start_server(config: dict):
    """Start server with sanitized logging"""
    # Only log non-sensitive config values
    safe_config = {k: "***" if "key" in k.lower() or "secret" in k.lower() else v 
                   for k, v in config.items()}
    logger.info("Starting server with config: %s", safe_config)
    # ... rest of startup

# Line 45 fix - Don't expose internal exceptions
@app.errorhandler(Exception)
def handle_error(error):
    """Handle errors without exposing internals"""
    logger.error("Request error: %s", type(error).__name__)  # Don't log full traceback
    # Return generic message to client (no internal details)
    return jsonify({"error": "An internal error occurred", "code": 500}), 500

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})
