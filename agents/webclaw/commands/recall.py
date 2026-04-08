"""Recall command - Recall from webclaw memory"""

def recall_command(args):
    if not args:
        print("Usage: /recall [query]")
        return
    
    from core import SharedMemory
    
    try:
        memory = SharedMemory("webclaw")
        results = memory.recall(args)
        
        if results:
            print(f"\n📖 RECALLED: '{args}'\n")
            for r in results:
                print(f"   📌 {r['query']}")
                print(f"      {r['response'][:300]}...")
                if 'timestamp' in r:
                    print(f"      📅 {r['timestamp'][:10]}\n")
        else:
            print(f"No saved knowledge found for: {args}")
    except Exception as e:
        print(f"Error recalling: {e}")
        print("Database may not be initialized yet. Save something first with /llm")
