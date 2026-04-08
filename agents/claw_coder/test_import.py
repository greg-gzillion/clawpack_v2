import sys
import os
sys.path.insert(0, os.getcwd())

# Force clean import
import importlib
if 'core.base_language' in sys.modules:
    del sys.modules['core.base_language']

from core.base_language import BaseLanguage
print('BaseLanguage imported successfully')
print('Has abstractmethods:', hasattr(BaseLanguage, '__abstractmethods__'))

from languages.python import PythonLanguage
print('PythonLanguage imported')
lang = PythonLanguage()
print('Language name:', lang.name)
print('Generate method exists:', callable(lang.generate))
