from flask import Flask, request, jsonify
import requests
from pathlib import Path

app = Flask(__name__)

# Load API key from .env
api_key = None
env_path = Path(r"C:\Users\greg\dev\clawpack_v2\.env")
if env_path.exists():
    with open(env_path, 'r') as f:
        for line in f:
            if 'OPENROUTER_API_KEY' in line and '=' in line:
                api_key = line.split('=', 1)[1].strip().strip('"').strip("'")
                print(f"✅ Loaded API key: {api_key[:20]}...")
                break

if not api_key:
    print("❌ No API key found")

@app.route('/llm', methods=['POST'])
def llm():
    global api_key
    try:
        data = request.get_json()
        question = data.get('question', '')
        print(f"Question: {question[:50]}...")
        
        if not api_key:
            return jsonify({"response": "No API key configured"}), 500
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": question}], "max_tokens": 500},
            timeout=30
        )
        
        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"]
            return jsonify({"response": answer})
        else:
            return jsonify({"response": f"API Error: {response.status_code}"}), 500
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "api_key_loaded": api_key is not None})

if __name__ == '__main__':
    print("WebClaw API Server on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
