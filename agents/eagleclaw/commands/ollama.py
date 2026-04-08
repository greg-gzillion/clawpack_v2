"""Ollama command for EagleClaw - uses local LLMs"""

import subprocess
import sys

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def ollama_command(prompt):
    """Send a prompt to local Ollama LLM"""
    if not prompt:
        print("Usage: /ollama [model] [prompt]")
        print("Example: /ollama deepseek-coder:6.7b Write a Python function")
        print("Example: /ollama list")
        print("\n📋 Available models:")
        print("  • qwen3-coder:30b - Best for code & legal reasoning (18GB)")
        print("  • gemma3:12b - General purpose (8GB)")
        print("  • deepseek-r1:8b - Reasoning (5GB)")
        print("  • llama3.2:3b - Fast responses (2GB)")
        return
    
    parts = prompt.strip().split(' ', 1)
    
    # Handle list command
    if parts[0] == 'list':
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, encoding='utf-8', errors='replace')
        print("\n📋 Available Ollama Models:")
        print(result.stdout)
        return
    
    # Check if first part is a model name (contains colon)
    if ':' in parts[0]:
        model = parts[0]
        query = parts[1] if len(parts) > 1 else ""
    else:
        # Default to qwen3-coder (best for reasoning)
        model = "qwen3-coder:30b"
        query = prompt
    
    if not query:
        print(f"Usage: /ollama {model} [your prompt]")
        return
    
    print(f"\n🤖 Running: {model}")
    print(f"📝 Question: {query[:100]}...")
    print("-"*50)
    
    # Run ollama with proper encoding
    try:
        result = subprocess.run(
            ['ollama', 'run', model, query], 
            capture_output=True, 
            text=True, 
            encoding='utf-8',
            errors='replace',
            timeout=120
        )
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"Error: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("❌ Request timed out after 120 seconds")
    except Exception as e:
        print(f"Error: {e}")

def models_command(args=None):
    """List available models"""
    result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, encoding='utf-8', errors='replace')
    print("\n📋 Available Ollama Models:")
    print(result.stdout)

def ask_legal(question):
    """Ask a legal question using qwen3-coder (best for reasoning)"""
    if not question:
        print("Usage: /asklegal [your legal question]")
        return
    ollama_command(f"qwen3-coder:30b {question}")