"""LLM command - AI with shared memory"""

def llm_command(question):
    if not question:
        print("Usage: /llm [your web/cloud/security question]")
        return
    
    from core import get_api, SharedMemory, WEB_REFS
    
    print(f"\n🤔 Question: {question}\n")
    
    # Check shared memory first
    memory = SharedMemory("webclaw")
    existing = memory.recall(question)
    
    if existing:
        print("📚 Found in shared memory:")
        print("="*60)
        print(existing[0]['response'])
        print("="*60)
        return
    
    # Search local references
    context = ""
    if WEB_REFS.exists():
        for category in WEB_REFS.iterdir():
            if category.is_dir():
                for md_file in category.rglob("*.md"):
                    try:
                        content = md_file.read_text(encoding='utf-8', errors='ignore')
                        if question.lower() in content.lower():
                            context += f"\n[Source: {category.name}/{md_file.name}]\n{content[:500]}\n"
                            if len(context) > 2000:
                                break
                    except:
                        pass
            if len(context) > 2000:
                break
    
    # Ask AI
    api = get_api()
    response = api.ask(question, context)
    
    # Save to shared memory
    memory.save(question, response, "web_question")
    
    print("="*60)
    print("🤖 RESPONSE:")
    print("="*60)
    print(response)
    print("="*60)
