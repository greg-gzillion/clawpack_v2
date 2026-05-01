"""Dreamclaw - AI Vision & Generation Agent

   CONSTITUTIONAL UPDATE: All model access now routes through 
   shared/llm/client.py — the sovereign gateway.
   
   No direct Ollama vision calls. No direct OpenRouter API calls.
   Every dream, every image analysis, every prompt generation is
   audited, budgeted, and governed through the throne.
"""
import sys
import os
import asyncio
import json
import base64
import warnings
from pathlib import Path

# Project root
_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

warnings.warn(
    "dreamclaw/core/agent.py had direct model access. "
    "All calls now route through shared/llm/client.py. "
    "This adapter preserves backward compatibility during transition.",
    DeprecationWarning,
    stacklevel=2
)


class Dreamclaw:
    """ADAPTER ONLY — All vision and generation calls route through sovereign gateway.
    
    No direct Ollama calls. No direct OpenRouter calls.
    Every dream is governed. Every vision is audited.
    """
    
    def __init__(self):
        self._client = None
        self.exports_dir = Path("exports")
        self.exports_dir.mkdir(exist_ok=True)
        # Vision model selection now handled by sovereign — not hardcoded
        print("✅ DreamClaw initialized — routing through sovereign gateway")
    
    @property
    def client(self):
        """THE SOVEREIGN GATEWAY — All model access passes through here."""
        if self._client is None:
            from shared.llm import get_llm_client
            self._client = get_llm_client()
        return self._client
    
    async def analyze_image(self, image_path: str, question: str = "Describe this image in detail") -> str:
        """Analyze an image through the sovereign gateway.
        
        Vision model selection is handled by the throne, not hardcoded.
        llmclaw /use controls which vision model is active.
        """
        if not Path(image_path).exists():
            return f"Image not found: {image_path}"
        
        try:
            # Encode image for sovereign vision call
            image_data = base64.b64encode(Path(image_path).read_bytes()).decode()
            
            # Route through sovereign gateway — the throne handles provider selection
            response = self.client.call_sync(
                prompt=question,
                agent="dreamclaw",
                capability="vision_analysis",
            )
            
            return (
                f"Model: {response.model} | Provider: {response.provider.value}\n"
                f"Audit: {response.request_hash}\n\n"
                f"{response.content}"
            )
        except Exception as e:
            raise RuntimeError(
                f"SOVEREIGN GATEWAY FAILURE in dreamclaw vision: "
                f"The throne is unreachable. Image analysis cannot proceed "
                f"without constitutional authority. Error: {e}"
            ) from e
    
    async def generate_prompt(self, idea: str) -> str:
        """Generate an image prompt through the sovereign gateway.
        
        No direct OpenRouter calls. The throne handles provider selection,
        API key management, budget enforcement, and audit logging.
        """
        prompt = (
            f"Create a detailed image generation prompt for: {idea}. "
            f"Describe the scene, style, lighting, and colors in 2-3 sentences."
        )
        
        try:
            response = self.client.call_sync(
                prompt=prompt,
                agent="dreamclaw",
                capability="prompt_generation",
            )
            return response.content
        except Exception as e:
            raise RuntimeError(
                f"SOVEREIGN GATEWAY FAILURE in dreamclaw prompt generation: "
                f"The throne is unreachable. Error: {e}"
            ) from e
    
    def create_visualization(self, prompt: str, original: str) -> str:
        """Create a visual representation — no model access, just rendering."""
        try:
            from PIL import Image, ImageDraw
            
            img = Image.new('RGB', (1024, 768), color='#0a0a1a')
            draw = ImageDraw.Draw(img)
            
            draw.rectangle([0, 0, 1024, 80], fill='#1a1a3a')
            draw.text((512, 40), f"Dream: {original}", fill='#e94560', anchor='mm')
            
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
        """Generate a dream through the sovereign gateway.
        
        Every dream is audited, budgeted, and governed.
        """
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
        print("Routing through sovereign gateway — all calls governed")
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