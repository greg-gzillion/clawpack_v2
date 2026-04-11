"""Input Handler - Interactive design input collection"""
import sys
from typing import Optional, Dict, List

class InputHandler:
    """Collects structured input for design generation"""
    
    def prompt(self, question: str, default: str = "") -> str:
        """Simple prompt"""
        if default:
            response = input(f"{question} [{default}]: ").strip()
            return response if response else default
        return input(f"{question}: ").strip()
    
    def select(self, question: str, options: List[str], default: int = 0) -> str:
        """Select from options"""
        print(f"\n{question}")
        for i, opt in enumerate(options, 1):
            marker = "→" if i == default + 1 else " "
            print(f"  {marker} {i}. {opt}")
        
        while True:
            try:
                choice = input(f"\nChoose (1-{len(options)}) [{default+1}]: ").strip()
                if not choice:
                    return options[default]
                idx = int(choice) - 1
                if 0 <= idx < len(options):
                    return options[idx]
            except:
                pass
            print(f"Please enter 1-{len(options)}")
    
    def multiselect(self, question: str, options: List[str]) -> List[str]:
        """Select multiple options"""
        print(f"\n{question}")
        for i, opt in enumerate(options, 1):
            print(f"  [ ] {i}. {opt}")
        print("\nEnter numbers separated by commas (e.g., 1,3,5)")
        
        while True:
            try:
                choice = input("> ").strip()
                if not choice:
                    return []
                indices = [int(x.strip()) - 1 for x in choice.split(',')]
                return [options[i] for i in indices if 0 <= i < len(options)]
            except:
                pass
            print("Please enter numbers separated by commas")
    
    def collect_brand_brief(self) -> Dict:
        """Interactive brand brief collection"""
        print("\n" + "="*50)
        print("🎨 BRAND IDENTITY BRIEF")
        print("="*50)
        
        brief = {
            "name": self.prompt("Brand/Company name"),
            "industry": self.select("Industry", 
                ["Tech/Software", "Healthcare", "Luxury", "Creative Agency", "Corporate", "Startup"]),
            "tone": self.select("Brand tone",
                ["Professional", "Friendly", "Innovative", "Luxurious", "Playful", "Minimal"]),
            "values": self.multiselect("Core values (select 2-4)",
                ["Trust", "Innovation", "Quality", "Simplicity", "Community", "Sustainability", "Speed", "Craftsmanship"]),
            "target_audience": self.prompt("Target audience"),
            "competitors": self.prompt("Key competitors (optional)", "none"),
            "unique_value": self.prompt("What makes you different?")
        }
        
        return brief
    
    def collect_mood_brief(self) -> Dict:
        """Interactive mood board brief"""
        print("\n" + "="*50)
        print("🎭 MOOD BOARD BRIEF")
        print("="*50)
        
        brief = {
            "name": self.prompt("Project name"),
            "aesthetic": self.select("Aesthetic direction",
                ["Minimal", "Brutalist", "Organic", "Retro/Vintage", "Futuristic", "Dark Mode", "Light/Airy", "Bold/Maximalist"]),
            "color_mood": self.select("Color mood",
                ["Warm", "Cool", "Neutral", "Vibrant", "Muted", "High Contrast"]),
            "inspiration": self.prompt("What inspires this? (images, places, feelings)"),
            "avoid": self.prompt("What to avoid? (optional)", "nothing specific")
        }
        
        return brief
    
    def confirm(self, message: str) -> bool:
        """Confirm action"""
        response = input(f"{message} [Y/n]: ").strip().lower()
        return response in ['', 'y', 'yes']
