"""Base Agent - All agents inherit from this"""
import sys
from pathlib import Path
from abc import ABC, abstractmethod

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.llm import LLMManager
from shared.input_handler import InputHandler
from shared.output_handler import OutputHandler

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.llm = LLMManager()
        self.input = InputHandler()
        self.output = OutputHandler()
    
    @abstractmethod
    def handle(self, query: str) -> str:
        pass
    
    def run_cli(self):
        print(f"\n🦞 {self.name}")
        while True:
            try:
                cmd = input("> ").strip()
                if cmd == "/quit":
                    break
                if cmd:
                    print(self.handle(cmd))
            except KeyboardInterrupt:
                break
