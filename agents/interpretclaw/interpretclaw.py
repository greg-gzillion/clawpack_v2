#!/usr/bin/env python3
"""Interpretclaw - Language Translation Agent"""
import sys
import asyncio
import aiohttp
import json
import subprocess
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
    
    def speak(self, text: str) -> str:
        """Use Windows TTS to speak text - completely hidden"""
        try:
            # Use CREATE_NO_WINDOW flag to prevent window minimization
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0  # SW_HIDE
            
            ps_script = f'Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.Speak("{text}")'
            subprocess.run(
                ['powershell', '-WindowStyle', 'Hidden', '-NoProfile', '-Command', ps_script],
                startupinfo=startupinfo,
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
            return f"Spoke: {text}"
        except Exception as e:
            return f"TTS error: {e}"
    
    async def translate(self, text: str, target: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"Translate '{text}' to {target}. Return ONLY the translation, no extra text."
        
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
                    translated = result["choices"][0]["message"]["content"].strip()
                    self.speak(translated)
                    return translated
                return "Translation failed"
    
    def run(self):
        if len(sys.argv) > 1:
            cmd = ' '.join(sys.argv[1:])
            
            if cmd.startswith("speak "):
                text = cmd[6:].strip()
                print(self.speak(text))
            elif " to " in cmd:
                parts = cmd.split(" to ")
                text = parts[0].replace("translate ", "").strip()
                target = parts[1].strip()
                result = asyncio.run(self.translate(text, target))
                print(result)
            return
        
        print("\n" + "="*50)
        print("INTERPRETCLAW - Translation Agent")
        print("="*50)
        print("Commands: translate <text> to <lang>, speak <text>, /quit")
        print("Example: translate Hello to Spanish\n")
        
        while True:
            try:
                cmd = input("> ").strip()
                if cmd == "/quit":
                    print("Goodbye!")
                    break
                if cmd.startswith("speak "):
                    text = cmd[6:].strip()
                    print(self.speak(text))
                elif " to " in cmd:
                    parts = cmd.split(" to ")
                    text = parts[0].replace("translate ", "").strip()
                    target = parts[1].strip()
                    print("Translating...")
                    result = asyncio.run(self.translate(text, target))
                    print(result)
                else:
                    print("Usage: translate <text> to <lang> OR speak <text>")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break

if __name__ == "__main__":
    Interpretclaw().run()
