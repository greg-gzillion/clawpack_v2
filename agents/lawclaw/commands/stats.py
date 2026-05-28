"""stats command - System statistics"""
import os
import subprocess
from pathlib import Path

name = "/stats"


def run(args):
    LAW_REFS = Path(__file__).parent.parent.parent.parent / "agents" / "webclaw" / "references" / "lawclaw"
    
    output = []
    output.append("")
    output.append("=" * 60)
    output.append("LAWCLAW STATISTICS")
    output.append("=" * 60)
    output.append(f"  API: {'Configured' if os.environ.get('OPENROUTER_API_KEY') else 'Not configured'}")
    
    if LAW_REFS.exists():
        file_count = len(list(LAW_REFS.rglob("*.md")))
        output.append(f"  Reference Files: {file_count}")
    
    juris_path = LAW_REFS / "jurisdictions"
    if juris_path.exists():
        states = len([d for d in juris_path.iterdir() if d.is_dir()])
        output.append(f"  Jurisdictions: {states} states")
    
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            models = len([l for l in result.stdout.split('\n')[1:] if l.strip()])
            output.append(f"  Local LLMs: {models} models available")
    except:
        pass
    
    output.append("=" * 60)
    return "\n".join(output)