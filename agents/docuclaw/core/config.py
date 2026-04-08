"""DocuClaw config"""
from pathlib import Path
ROOT = Path(__file__).parent.parent.parent.parent
TEMPLATES = ROOT / "docuclaw/templates"
OUTPUT = Path.home() / ".docuclaw_output"
OUTPUT.mkdir(exist_ok=True)
