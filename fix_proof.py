from pathlib import Path
f = Path(r'C:\Users\greg\dev\clawpack_v2\agents\mathematicaclaw\handlers\calculus\proof.py')
f.write_text('''"""Mathematical proof generation via LLM"""
def proof(statement=None):
    if not statement:
        return "Usage: /proof sqrt(2) is irrational"
    try:
        from shared.llm import get_llm_client
        client = get_llm_client()
        prompt = "Prove this mathematical statement rigorously with clear logical steps: " + statement
        response = client.call_sync(prompt=prompt, agent='mathematicaclaw', max_tokens=1024, temperature=0.3)
        return "PROOF: " + statement + chr(10)*2 + response.content
    except Exception as e:
        return "Proof generation failed (may time out on complex proofs): " + str(e)[:200]
''', encoding='utf-8')
print('Fixed')
