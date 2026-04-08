"""Medical search command for MedicLaw - IMPROVED"""

from core.data import get_data_path
from utils.helpers import format_result
import re

def search_command(query):
    if not query:
        print("Usage: /search [condition or symptom]")
        print("Example: /search hypertension")
        return
    
    data_path = get_data_path()
    print(f"\n🔍 Searching for: {query}")
    print(f"📁 Searching in: {data_path}")
    print("-"*50)
    
    if not data_path.exists():
        print(f"❌ Data path not found: {data_path}")
        return
    
    # Search through all medical reference files
    found = False
    md_files = list(data_path.glob("**/*.md"))
    print(f"📚 Found {len(md_files)} medical files to search...")
    
    for md_file in md_files:
        try:
            content = md_file.read_text(encoding='utf-8', errors='ignore')
            if query.lower() in content.lower():
                print(f"\n✅ Found in: {md_file.parent.name}/{md_file.name}")
                print("="*40)
                # Find the section containing the query
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if query.lower() in line.lower():
                        # Show context (2 lines before, 2 after)
                        start = max(0, i-2)
                        end = min(len(lines), i+3)
                        context = '\n'.join(lines[start:end])
                        print(context)
                        print("-"*40)
                        found = True
                        break
                if found:
                    break
        except Exception as e:
            pass
    
    if not found:
        print(f"❌ No results found for: '{query}'")
        print("\n💡 Try these search terms:")
        # Show some example conditions from file names
        examples = set()
        for md_file in md_files[:10]:
            name = md_file.stem.replace('_', ' ').replace('-', ' ')
            examples.add(name.lower())
        for ex in list(examples)[:5]:
            print(f"   • /search {ex}")

def symptoms_command(query):
    if not query:
        print("Usage: /symptoms [condition]")
        return
    search_command(query)

def conditions_command(query):
    if not query:
        print("Usage: /conditions [symptom]")
        return
    search_command(query)