#!/usr/bin/env python3
"""Interpretclaw - Language Translation Agent"""
import sys
import asyncio
import aiohttp
import json
from pathlib import Path

class Interpretclaw:
    def __init__(self):
        self.key = self._load_key()
        self.model = "google/gemma-4-26b-a4b-it:free"
        
    def _load_key(self):
        env = Path(".env").read_text() if Path(".env").exists() else ""
        for line in env.split('\n'):
            if 'OPENROUTER_API_KEY=' in line:
                return line.split('=', 1)[1].strip().strip('"').strip("'")
        return None
    
    async def translate(self, text: str, target: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"Translate '{text}' to {target}. Return ONLY the translation."
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 50
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
                return "Translation failed"
    
    def run(self):
        if len(sys.argv) > 1:
            cmd = ' '.join(sys.argv[1:])
            if " to " in cmd:
                parts = cmd.split(" to ")
                text = parts[0].replace("translate ", "").strip()
                target = parts[1].strip()
                result = asyncio.run(self.translate(text, target))
                print(result)
            return
        
        print("\n" + "="*50)
        print("INTERPRETCLAW - Translation Agent")
        print("="*50)
        print("Commands: translate <text> to <lang>, /quit")
        
        while True:
            try:
                cmd = input("> ").strip()
                if cmd == "/quit":
                    break
                if " to " in cmd:
                    parts = cmd.split(" to ")
                    text = parts[0].replace("translate ", "").strip()
                    target = parts[1].strip()
                    result = asyncio.run(self.translate(text, target))
                    print(f"{result}\n")
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    Interpretclaw().run()
