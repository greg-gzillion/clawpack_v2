"""Models command - List available models"""

import subprocess

def list_models() -> str:
    """List available models from Ollama"""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            output = "📋 Available Ollama Models:\n"
            output += "─" * 40 + "\n"
            output += result.stdout
            return output
        else:
            return "⚠️  Could not fetch Ollama models. Is Ollama running?"

    except FileNotFoundError:
        return "⚠️  Ollama not found. Install Ollama from https://ollama.ai"
    except Exception as e:
        return f"❌ Error: {e}"
