"""stats command - System statistics"""
import os
import subprocess
from pathlib import Path

name = "/stats"

def run(args):
    LEGAL_REFS = Path("str(PROJECT_ROOT)/agents/webclaw/references/lawclaw")
    
    output = []
    output.append("\n" + "="*50)
    output.append("?? LAWCLAW STATISTICS")
    output.append("="*50)
    output.append(f"API: {'? Configured' if os.environ.get('OPENROUTER_API_KEY') else '? Not configured'}")
    
    if LEGAL_REFS.exists():
        file_count = len(list(LEGAL_REFS.rglob("*.md")))
        output.append(f"Reference Files: {file_count}")
    
    juris_path = LEGAL_REFS / "jurisdictions"
    if juris_path.exists():
        states = len([d for d in juris_path.iterdir() if d.is_dir()])
        output.append(f"Jurisdictions: {states} states")
    
    # Check Ollama
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            models = len([l for l in result.stdout.split('\n')[1:] if l.strip()])
            output.append(f"Local LLMs: {models} models available")
    except:
        pass
    
    output.append("="*50)
    return "\n".join(output)
