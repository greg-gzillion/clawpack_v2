import os
import sys
from pathlib import Path

def show_image(image_path):
    """Open image with default viewer"""
    if os.path.exists(image_path):
        os.startfile(image_path)
        return True
    return False

# Usage in commands:
# result = create_plot()
# show_image(result["path"])
