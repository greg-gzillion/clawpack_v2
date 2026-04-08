"""Routes code requests to appropriate language modules"""

from pathlib import Path
import importlib.util
from typing import Optional

class LanguageOrchestrator:
    """Manages all language modules and routes requests"""
    
    def __init__(self):
        self.languages = {}
        self._discover_languages()
    
    def _discover_languages(self):
        """Auto-discover all language modules in languages/ folder"""
        languages_path = Path(__file__).parent.parent / "languages"
        
        if not languages_path.exists():
            print(f"⚠️ Languages folder not found: {languages_path}")
            return
        
        for py_file in languages_path.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
            
            module_name = py_file.stem
            try:
                # Import the module dynamically
                spec = importlib.util.spec_from_file_location(
                    f"languages.{module_name}", py_file
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Look for language class (ends with 'Language' and is not BaseLanguage)
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (attr_name.endswith('Language') and 
                        attr_name != 'BaseLanguage' and
                        hasattr(attr, 'name') and 
                        hasattr(attr, 'generate')):
                        # Instantiate the class
                        instance = attr()
                        self.languages[instance.name.lower()] = instance
                        print(f"  ✅ Loaded language: {instance.name}")
                        break
            except Exception as e:
                print(f"  ❌ Failed to load {module_name}: {e}")
        
        if not self.languages:
            print("  ⚠️ No languages loaded - creating default Python module")
            self._create_default_language()
    
    def _create_default_language(self):
        """Create a default Python language module if none exist"""
        class DefaultPython:
            name = "python"
            extensions = [".py"]
            compilers = ["python"]
            
            def generate(self, prompt: str, context: str = "") -> str:
                return f'# Generated Python code for: {prompt}\n\ndef solution():\n    pass\n'
            
            def analyze(self, code: str) -> dict:
                return {"issues": [], "suggestions": []}
            
            def refactor(self, code: str, suggestion: str) -> str:
                return code
        
        self.languages["python"] = DefaultPython()
        print("  ✅ Created default Python module")
    
    def get_language(self, lang_name: str):
        """Get language module by name"""
        return self.languages.get(lang_name.lower())
    
    def generate(self, lang: str, prompt: str, context: str = "") -> str:
        """Generate code in specified language"""
        language = self.get_language(lang)
        if not language:
            available = ', '.join(sorted(self.languages.keys()))
            return f"❌ Language '{lang}' not supported.\n💡 Available: {available}"
        return language.generate(prompt, context)
    
    def analyze(self, lang: str, code: str) -> dict:
        """Analyze code in specified language"""
        language = self.get_language(lang)
        if not language:
            return {"error": f"Language '{lang}' not supported"}
        return language.analyze(code)
    
    def list_languages(self) -> list:
        """List all supported languages"""
        return sorted(self.languages.keys())
