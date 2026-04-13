import sys
from pathlib import Path
sys.path.insert(0, r"C:\Users\greg\dev\clawpack_v2")

# Test hardcoded path
hardcoded = Path(r"C:\Users\greg\dev\clawpack_v2\models\obliterated")
print(f"Hardcoded path: {hardcoded}")
print(f"Exists: {hardcoded.exists()}")

if hardcoded.exists():
    print(f"\nContents of {hardcoded}:")
    for item in hardcoded.iterdir():
        print(f"  {item.name} (is_dir: {item.is_dir()})")
        if item.is_dir():
            config = item / "config.json"
            print(f"    config.json: {config.exists()}")
else:
    print("\n❌ Hardcoded path does NOT exist!")
    
# Now test what the provider is using
print("\n" + "="*50)
print("Testing provider function:")

try:
    from agents.llmclaw.providers.obliterated import get_obliterated_models
    models = get_obliterated_models()
    print(f"Provider found {len(models)} models")
    for m in models:
        print(f"  - {m['name']} ({m['size_gb']:.2f} GB)")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
