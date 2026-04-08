import sys
from pathlib import Path
import importlib.util

sys.path.insert(0, '.')

languages_path = Path('languages')
print(f'Languages path: {languages_path.absolute()}')
print(f'Exists: {languages_path.exists()}')

for py_file in languages_path.glob('*.py'):
    if py_file.name.startswith('__'):
        continue
    print(f'\nChecking: {py_file.name}')
    
    try:
        spec = importlib.util.spec_from_file_location(f'test_{py_file.stem}', py_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if attr_name.endswith('Language'):
                print(f'  Found class: {attr_name}')
                try:
                    instance = attr()
                    print(f'    Instance created: {instance.name}')
                    print(f'    Generate: {instance.generate("test")[:50]}')
                except Exception as e:
                    print(f'    Error: {e}')
    except Exception as e:
        print(f'  Import error: {e}')
