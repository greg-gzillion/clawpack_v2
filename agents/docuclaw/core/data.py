from pathlib import Path

def get_data_path():
    # Point to central references in webclaw
    return Path(__file__).parent.parent.parent / "webclaw" / "references" / "docuclaw"