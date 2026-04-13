"""Provider Factory"""

import subprocess
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
env_path = Path(__file__).parent.parent.parent.parent / ".env"
load_dotenv(env_path)

from .base import ProviderConfig
from .ollama import OllamaProvider
from .groq import GroqProvider

def discover_providers() -> list:
    providers = []
    
    # Discover Ollama models
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True, text=False, timeout=10
        )
        output = result.stdout.decode("utf-8", errors="replace")
        for line in output.split("\n")[1:]:
            if line.strip():
                model = line.split()[0]
                caps = _infer_capabilities(model)
                config = ProviderConfig(
                    name=f"ollama/{model}",
                    model=model,
                    capabilities=caps
                )
                providers.append(OllamaProvider(config))
    except Exception:
        pass
    
    # Add Groq if API key exists
    if os.getenv("GROQ_API_KEY"):
        config = ProviderConfig(
            name="groq",
            model="llama-3.3-70b-versatile",
            capabilities=["general", "code", "reasoning", "creative"],
            max_tokens=8192
        )
        providers.append(GroqProvider(config))
    
    return providers

def _infer_capabilities(model: str) -> list:
    caps = ["general"]
    m = model.lower()
    if any(w in m for w in ["coder", "code"]):
        caps.append("code")
    if any(w in m for w in ["deepseek", "r1"]):
        caps.append("reasoning")
    if any(w in m for w in ["gemma", "creative"]):
        caps.append("creative")
    return caps
