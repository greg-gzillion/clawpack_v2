from pathlib import Path

def get_data_path():
    # Get the project root (clawpack_v2)
    root = Path(__file__).parent.parent.parent.parent
    # Return the agent's reference folder in webclaw
    return root / "agents" / "webclaw" / "references" / "webclaw"