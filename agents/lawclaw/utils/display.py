"""
Display utilities for beautiful output - pure ASCII version
"""
from typing import List, Dict

class Display:
    """Handle beautiful console output with ASCII only"""
    
    @staticmethod
    def banner(title: str, icon: str = "[LAW]"):
        """Print a banner"""
        print("\n" + "="*80)
        print("=" + " "*78 + "=")
        print(f"={icon:^78}=")
        print(f"={title:^78}=")
        print("=" + " "*78 + "=")
        print("="*80)
    
    @staticmethod
    def header(text: str, char: str = "="):
        """Print a header"""
        print(f"\n{char*50}")
        print(f"{text}")
        print(f"{char*50}")
    
    @staticmethod
    def categories(categories: List[str], cols: int = 5):
        """Display categories in columns"""
        print("\nCATEGORIES\n" + "-"*50)
        for i, cat in enumerate(categories):
            if i % cols == 0 and i > 0:
                print()
            print(f"  * {cat:<20}", end="")
        print()
    
    @staticmethod
    def commands(commands: List[tuple], cols: int = 3):
        """Display commands in columns"""
        print("\nCOMMANDS\n" + "-"*50)
        for i, (cmd, desc) in enumerate(commands):
            if i % cols == 0 and i > 0:
                print()
            print(f"  {cmd:<15} - {desc:<25}", end="")
        print()
    
    @staticmethod
    def result(title: str, content: str, max_lines: int = 50):
        """Display a search result"""
        print(f"\n{'='*60}")
        print(f"[RESULT] {title}")
        print('='*60)
        
        lines = content.split('\n')
        for line in lines[:max_lines]:
            print(line)
        
        if len(lines) > max_lines:
            print(f"\n... ({len(lines) - max_lines} more lines)")
    
    @staticmethod
    def success(message: str):
        print(f"[OK] {message}")
    
    @staticmethod
    def error(message: str):
        print(f"[ERROR] {message}")
    
    @staticmethod
    def info(message: str):
        print(f"[INFO] {message}")

display = Display()
