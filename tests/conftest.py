"""Pytest configuration and shared fixtures"""

import pytest
import asyncio
import tempfile
from pathlib import Path
from typing import Generator, AsyncGenerator
from datetime import datetime


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests"""
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)


@pytest.fixture
def mock_agent():
    """Create a mock agent for testing"""
    class MockAgent:
        def __init__(self):
            self.agent_name = "TestAgent"
            self.session_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.tools = {}
            self.memory = None
            self.hooks = None
            self.skills = None
            self.forks = None
    
    return MockAgent()


@pytest.fixture
def sample_memory_content():
    """Sample memory content for testing"""
    return {
        "name": "Test Memory",
        "description": "A test memory",
        "type": "feedback",
        "content": "This is test content for memory system."
    }


@pytest.fixture
def sample_tool_definitions():
    """Sample tool definitions for testing"""
    return [
        {"name": "translate", "description": "Translate text", "safety": "read_only"},
        {"name": "calculate", "description": "Calculate expression", "safety": "read_only"},
        {"name": "send_transaction", "description": "Send blockchain transaction", "safety": "destructive"}
    ]


@pytest.fixture
def event_loop():
    """Create an event loop for async tests"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
