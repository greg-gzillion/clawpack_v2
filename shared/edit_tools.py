"""Shared Edit Tools - Crop, resize, enhance, filters for all agents"""

import os
from pathlib import Path
from typing import Optional, Tuple
from .input_handler import InputHandler
from .output_handler import OutputHandler

class EditTools:
    """Image editing tools available to all agents"""
    
    @classmethod
    def _load_image(cls, file_path: str):
        """Load image with PIL"""
        try:
            from PIL import Image
            path = InputHandler.find_file(file_path)
            if path:
                return Image.open(path), path
        except ImportError:
            print("❌ PIL not installed. Run: pip install pillow")
        except Exception as e:
            print(f"❌ Error loading image: {e}")
        return None, None
    
    @classmethod
    def crop(cls, file_path: str, width: int, height: int) -> Optional[Path]:
        """Crop image to dimensions (center crop)"""
        img, original_path = cls._load_image(file_path)
        if not img:
            return None
        
        orig_w, orig_h = img.size
        left = (orig_w - width) // 2
        top = (orig_h - height) // 2
        right = left + width
        bottom = top + height
        
        if left >= 0 and top >= 0:
            img = img.crop((left, top, right, bottom))
        else:
            img = img.resize((width, height))
        
        filename = f"cropped_{original_path.name}"
        return OutputHandler.save_image(img, filename)
    
    @classmethod
    def resize(cls, file_path: str, width: int, height: int) -> Optional[Path]:
        """Resize image to dimensions"""
        img, original_path = cls._load_image(file_path)
        if not img:
            return None
        
        from PIL import Image
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        
        filename = f"resized_{original_path.name}"
        return OutputHandler.save_image(img, filename)
    
    @classmethod
    def enhance(cls, file_path: str, 
                sharpen: float = 1.0,
                contrast: float = 1.2,
                color: float = 1.1,
                brightness: float = 1.0) -> Optional[Path]:
        """AI-style enhancement"""
        img, original_path = cls._load_image(file_path)
        if not img:
            return None
        
        from PIL import ImageEnhance, ImageFilter
        
        if sharpen > 0:
            img = img.filter(ImageFilter.SHARPEN)
        
        if contrast != 1.0:
            img = ImageEnhance.Contrast(img).enhance(contrast)
        
        if color != 1.0:
            img = ImageEnhance.Color(img).enhance(color)
        
        if brightness != 1.0:
            img = ImageEnhance.Brightness(img).enhance(brightness)
        
        filename = f"enhanced_{original_path.name}"
        return OutputHandler.save_image(img, filename)
    
    @classmethod
    def rotate(cls, file_path: str, degrees: float) -> Optional[Path]:
        """Rotate image"""
        img, original_path = cls._load_image(file_path)
        if not img:
            return None
        
        img = img.rotate(degrees, expand=True)
        
        filename = f"rotated_{original_path.name}"
        return OutputHandler.save_image(img, filename)
    
    @classmethod
    def grayscale(cls, file_path: str) -> Optional[Path]:
        """Convert to grayscale"""
        img, original_path = cls._load_image(file_path)
        if not img:
            return None
        
        img = img.convert('L')
        
        filename = f"grayscale_{original_path.name}"
        return OutputHandler.save_image(img, filename)
    
    @classmethod
    def flip(cls, file_path: str, direction: str = 'horizontal') -> Optional[Path]:
        """Flip image horizontally or vertically"""
        img, original_path = cls._load_image(file_path)
        if not img:
            return None
        
        from PIL import Image
        if direction == 'horizontal':
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        elif direction == 'vertical':
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
        
        filename = f"flipped_{original_path.name}"
        return OutputHandler.save_image(img, filename)
    
    @classmethod
    def thumbnail(cls, file_path: str, size: int = 200) -> Optional[Path]:
        """Create thumbnail"""
        img, original_path = cls._load_image(file_path)
        if not img:
            return None
        
        img.thumbnail((size, size))
        
        filename = f"thumb_{original_path.name}"
        return OutputHandler.save_image(img, filename)


# Convenience functions
def crop(file_path: str, width: int, height: int) -> Optional[Path]:
    return EditTools.crop(file_path, width, height)

def enhance(file_path: str) -> Optional[Path]:
    return EditTools.enhance(file_path)

def resize(file_path: str, width: int, height: int) -> Optional[Path]:
    return EditTools.resize(file_path, width, height)
