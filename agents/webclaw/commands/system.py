"""System command - System information"""

import sys
from pathlib import Path

def system_command(args=None):
    """Show system information"""
    print("\n" + "="*50)
    print("🖥️  SYSTEM INFORMATION")
    print("="*50)
    print(f"Python: {sys.version}")
    print(f"Path: {Path(__file__).parent.parent}")
    print("="*50)

name = "/system"
run = system_command
