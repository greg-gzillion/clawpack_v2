"""Ask command for EagleClaw - OpenRouter API primary, Ollama fallback"""

import os
import requests
import subprocess
from pathlib import Path

# Load API key from .env
def get_api_key():
    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith("OPENROUTER_API_KEY"):
                    return line.split("=", 1)[1].strip()
    return os.environ.get("OPENROUTER_API_KEY", "")

API_KEY = get_api_key()
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Available models (fastest to most capable)
API_MODELS = {
    "fast": "google/gemma-3-4b-it:free",      # Fast, decent
    "balanced": "deepseek/deepseek-chat:free", # Good balance
    "powerful": "anthropic/claude-3.5-sonnet", # Best quality (needs paid key)
    "legal": "meta-llama/llama-3.3-70b-instruct" # Good for legal
}

# Local fallback models
LOCAL_MODELS = {
    "fast": "llama3.2:3b",
    "balanced": "gemma3:4b",
    "reasoning": "deepseek-coder:6.7b"
}

def ask_command(question):
    """Ask a question - uses API primary, local fallback"""
    if not question:
        print("Usage: /ask [your question]")
        print("       /ask --legal [question] - use legal-optimized model")
        print("       /ask --fast [question] - use fast model")
        print("       /ask --local [question] - force local LLM only")
        return
    
    # Parse flags
    force_local = False
    model_type = "balanced"
    query = question
    
    if question.startswith("--legal"):
        model_type = "legal"
        query = question[7:].strip()
    elif question.startswith("--fast"):
        model_type = "fast"
        query = question[6:].strip()
    elif question.startswith("--local"):
        force_local = True
        query = question[7:].strip()
    
    print(f"\n🤔 Question: {query[:100]}...")
    print("-"*50)
    
    # Try API first (unless force_local)
    if not force_local and API_KEY:
        try:
            response = call_api(query, model_type)
            if response:
                print(f"\n✅ [API - {API_MODELS[model_type]}]")
                print("="*50)
                print(response)
                return
        except Exception as e:
            print(f"⚠️ API error: {e}")
            print("🔄 Falling back to local LLM...")
    
    # Fallback to local Ollama
    call_local(query, model_type)

def call_api(question, model_type="balanced"):
    """Call OpenRouter API"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    
    data = {
        "model": API_MODELS.get(model_type, API_MODELS["balanced"]),
        "messages": [{"role": "user", "content": question}],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    response = requests.post(API_URL, headers=headers, json=data, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        raise Exception(f"API returned {response.status_code}")

def call_local(question, model_type="balanced"):
    """Call local Ollama as fallback"""
    model = LOCAL_MODELS.get(model_type, LOCAL_MODELS["balanced"])
    
    print(f"\n🦙 [LOCAL - {model}]")
    print("="*50)
    
    try:
        result = subprocess.run(
            ['ollama', 'run', model, question],
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
        print("❌ Local LLM timed out")
    except Exception as e:
        print(f"Error: {e}")

def status_command(args=None):
    """Check API and local LLM status"""
    print("\n🔧 SYSTEM STATUS")
    print("="*50)
    
    # Check API
    if API_KEY:
        print("✅ OpenRouter API: Configured")
        print(f"   Key: {API_KEY[:8]}...")
    else:
        print("❌ OpenRouter API: No API key found")
    
    # Check local Ollama
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]
            models = [l.split()[0] for l in lines if l.strip()]
            print(f"✅ Ollama: Running with {len(models)} models")
            print(f"   Available: {', '.join(models[:5])}")
        else:
            print("❌ Ollama: Not responding")
    except:
        print("❌ Ollama: Not available")
    
    print("\n💡 COMMANDS:")
    print("   /ask What is the 1st amendment?")
    print("   /ask --legal Explain tort law")
    print("   /ask --fast Quick answer")
    print("   /ask --local Force local only")
    print("   /status Check API/local status")