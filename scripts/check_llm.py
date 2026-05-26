import requests

# Check active model
r = requests.post('http://127.0.0.1:8766/v1/message/llmclaw', json={'task': '/models'}, timeout=10)
print(r.json().get('result','')[:600])

# Test bare LLM
print('\n--- Bare LLM ---')
r = requests.post('http://127.0.0.1:8766/v1/message/llmclaw', json={'task': '/llm Say hello'}, timeout=60)
print('Status:', r.status_code)
print('Result:', r.json().get('result','')[:200])
