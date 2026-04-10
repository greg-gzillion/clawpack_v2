#!/usr/bin/env python3
"""Fork Agent CLI"""
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.fork.fork_agent import ForkContext, ForkAgent

async def main():
    if len(sys.argv) < 2:
        print("Fork Agent - Parallel execution with cache sharing")
        print("\nUsage:")
        print("  python fork.py <task>")
        print("\nExamples:")
        print("  python fork.py 'calculate 2+2'")
        print("  python fork.py 'what is the capital of France'")
        return
    
    task = ' '.join(sys.argv[1:])
    
    context = ForkContext(
        system_prompt="You are a helpful assistant.",
        messages=[],
        tools=[],
        model="llama3.2:3b"
    )
    
    fork = ForkAgent(context, task)
    result = await fork.execute()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
