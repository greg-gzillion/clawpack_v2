"""list command - List jurisdictions"""
from pathlib import Path

name = "/list"

def run(args):
    LEGAL_REFS = Path("C:/Users/greg/dev/clawpack_v2/agents/webclaw/references/lawclaw")
    juris_path = LEGAL_REFS / "jurisdictions"
    
    output = []
    output.append("\n" + "="*50)
    output.append("??? AVAILABLE JURISDICTIONS")
    output.append("="*50)
    
    if juris_path.exists():
        states = sorted([d.name for d in juris_path.iterdir() if d.is_dir()])
        output.append(f"\nFound {len(states)} states/territories:\n")
        line = ""
        for i, state in enumerate(states, 1):
            line += f"  {state:<4}"
            if i % 8 == 0:
                output.append(line)
                line = ""
        if line:
            output.append(line)
        output.append("\n?? Use /browse STATE to explore a state")
    else:
        output.append("No jurisdictions found")
    
    return "\n".join(output)
