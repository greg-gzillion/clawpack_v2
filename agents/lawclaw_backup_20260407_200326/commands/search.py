from core.data import get_data_path
from utils.helpers import format_result

def search_command(query):
    if not query:
        print("Provide a search term")
        return
    
    data_path = get_data_path()
    print(f"\nSearching for: {query}")
    print("-"*50)
    
    for folder in data_path.iterdir():
        if folder.is_dir() and folder.name != "jurisdictions":
            for md_file in folder.glob("*.md"):
                try:
                    content = md_file.read_text(encoding='utf-8', errors='ignore')
                    if query.lower() in content.lower():
                        print(f"\n{folder.name}/")
                        print(f"{md_file.name}")
                        print("-"*40)
                        print(format_result(content))
                        return
                except:
                    pass
    
    print(f"No results found for: {query}")
