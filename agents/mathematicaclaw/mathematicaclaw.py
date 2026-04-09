#!/usr/bin/env python3
"""Mathematicaclaw - Math Computation Agent"""
import sys
import asyncio
import aiohttp
import json
from pathlib import Path

class Mathematicaclaw:
    def __init__(self):
        self.key = self._load_key()
        self.model = "google/gemma-4-26b-a4b-it:free"
    
    def _load_key(self):
        env = Path(".env").read_text() if Path(".env").exists() else ""
        for line in env.split('\n'):
            if 'OPENROUTER_API_KEY=' in line:
                return line.split('=', 1)[1].strip().strip('"').strip("'")
        return None
    
    async def solve(self, equation: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"Solve this equation: {equation}. Return ONLY the solution."
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                result = await resp.json()
                if "choices" in result:
                    return result["choices"][0]["message"]["content"].strip()
                return "Solution failed"
    
    def run(self):
        print("\n" + "="*50)
        print("MATHEMATICACLAW - Math Agent")
        print("="*50)
        print("Commands: solve <equation>, /quit")
        print("Example: solve x**2 - 4 = 0\n")
        
        while True:
            try:
                cmd = input("> ").strip()
                if cmd == "/quit":
                    break
                if cmd.startswith("solve "):
                    equation = cmd[6:].strip()
                    result = asyncio.run(self.solve(equation))
                    print(f"{result}\n")
                else:
                    print("Usage: solve <equation>")
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    Mathematicaclaw().run()