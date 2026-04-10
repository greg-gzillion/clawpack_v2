"""dreamclaw Core Logic"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class dreamclawCore:
    """Core processing logic for dreamclaw"""
    
    def process(self, query: str) -> str:
        """Process a query"""
        # Original logic from the simple agent
        #!/usr/bin/env python3
"""Dreamclaw - AI Vision & Generation Agent"""
import sys
import os
import asyncio
import aiohttp
import json
import base64
from pathlib import Path

class Dreamclaw:
    def __init__(self):
        self.key = self._load_key()
        self.exports_dir = Path("exports")
        self.exports_dir.mkdir(exist_ok=True)
        self.vision_model = "qwen3-vl:30b"
    
    def _load_key(self):
        env = Path(".env").read_text() if Path(".env").exists() else ""
        for line in env.split('\n'):
            if 'OPENROUTER_API_KEY=' in line:
                return line.split('=', 1)[1].strip().strip('"').strip("'")
        return None
    
    async def analyze_image(self, image_path: str, question: str = "Describe this image in detail") -> str:
        """Use local qwen3-vl to analyze an image"""
        if not Path(image_path).exists():
            return f"Image not found: {image_path}"
        
        try:
            import base64
            image_data = base64.b64encode(Path(image_path).read_bytes()).decode()
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": self.vision_model,
                        "prompt": question,
                        "images": [image_data],
                        "stream": False
                    },
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as resp:
                    result = await resp.json()
                    return result.get("response", "Analysis failed").strip()
        except Exception as e:
            return f"Vision model error: {e}"
    
    async def generate_prompt(self, idea: str) -> str:
        """Use LLM to create a detailed image prompt"""
        headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "google/gemma-4-26b-a4b-it:free",
            "messages": [{"role": "user", "content": f"Create a detailed image generation prompt for: {idea}. Describe the scene, style, lighting, and colors in 2-3 sentences."}],
            "max_tokens": 150
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                result = await resp.json()
                if "choices" in result:
                    return result["choices"][0]["message"]["content"].strip()
        return idea
    
    def create_visualization(self, prompt: str, original: str) -> str:
        """Create a visual representation"""
        try:
            from PIL import Image, ImageDraw
            
            img = Image.new('RGB', (1024, 768), color='#0a0a1a')
            draw = ImageDraw.Draw(img)
            
            draw.rectangle([0, 0, 1024, 80], fill='#1a1a3a')
            draw.text((512, 40), f"Dream: {original[:50]}", fill='#e94560', anchor='mm')
            
            y = 120
            words = prompt.split()
            line = ""
            for word in words:
                if len(line + word) < 70:
                    line += word + " "
                else:
                    draw.text((40, y), line, fill='#ccccff')
                    y += 30
                    line = word + " "
            if line:
                draw.text((40, y), line, fill='#ccccff')
            
            draw.rectangle([10, 10, 1014, 758], outline='#4a9eff', width=2)
            
            path = self.exports_dir / f"dream_{hash(original)%10000}.png"
            img.save(str(path))
            os.startfile(str(path))
            
            return f"Visualization saved: {path}\n\nPrompt: {prompt}"
        except:
            return f"Prompt generated:\n\n{prompt}"
    
    async def dream(self, idea: str) -> str:
        print("Generating prompt...")
        detailed_prompt = await self.generate_prompt(idea)
        print("Creating visualization...")
        return self.create_visualization(detailed_prompt, idea)
    
    def run(self):
        if len(sys.argv) > 1:
            cmd = ' '.join(sys.argv[1:])
            
            if cmd.startswith("analyze "):
                parts = cmd[8:].strip().split(" ", 1)
                image_path = parts[0]
                question = parts[1] if len(parts) > 1 else "Describe this image in detail"
                result = asyncio.run(self.analyze_image(image_path, question))
                print(result)
            elif cmd.startswith("dream "):
                idea = cmd[6:].strip()
                result = asyncio.run(self.dream(idea))
                print(result)
            return
        
        print("\n" + "="*50)
        print("DREAMCLAW - AI Vision & Generation")
        print("="*50)
        print(f"Vision: {self.vision_model}")
        print("Commands:")
        print("  dream <idea>           - Generate image prompt")
        print("  analyze <image> [question] - Analyze image with vision model")
        print("  /quit                  - Exit")
        
        while True:
            try:
                cmd = input("> ").strip()
                if cmd == "/quit":
                    break
                if cmd.startswith("dream "):
                    idea = cmd[6:].strip()
                    result = asyncio.run(self.dream(idea))
                    print(f"\n{result}\n")
                elif cmd.startswith("analyze "):
                    parts = cmd[8:].strip().split(" ", 1)
                    image_path = parts[0]
                    question = parts[1] if len(parts) > 1 else "Describe this image in detail"
                    print("Analyzing...")
                    result = asyncio.run(self.analyze_image(image_path, question))
                    print(f"\n{result}\n")
                else:
                    print("Usage: dream <idea>  OR  analyze <image> [question]")
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    Dreamclaw().run()

        return f"[dreamclaw] Processing: {query}"

    def _help(self) -> str:
        return "dreamclaw Commands: /help, /stats, /quit"
