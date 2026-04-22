"""court command - County court info with LLM (supports stock + obliterated)"""
import requests
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

name = "/court"

def run(args):
    if not args:
        return "Usage: /court [state] [county]"
    
    try:
        # Search WebClaw for court info
        search_response = requests.post(
            "http://127.0.0.1:8766/v1/message/webclaw",
            json={"task": f"/search {args} court", "agent": "lawclaw"},
            timeout=10
        )
        
        context = ""
        if search_response.status_code == 200:
            data = search_response.json()
            context = data.get("result", "")[:1000]
        
        # Get active model
        models_dir = Path("C:/Users/greg/dev/clawpack_v2/models")
        active = json.load(open(models_dir / "active_model.json"))
        model_name = active.get("model", "gemma3:12b")
        source = active.get("source", "stock")
        
        prompt = f"""You are a legal assistant. Provide information about the court in {args}.

Context from database:
{context if context else "No specific context available."}

Question: What court serves {args}? Include address, jurisdiction, and contact info if known.

Answer:"""
        
        if source == "stock":
            # Use Ollama
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": model_name, "prompt": prompt, "stream": False},
                timeout=60
            )
            if response.status_code == 200:
                result = response.json()
                return f"\n🏛️ COURT INFO: {args}\n{'-'*50}\n{result['response']}\n{'-'*50}"
            else:
                return f"Ollama error: {response.status_code}"
        
        else:
            # Use obliterated model (local transformers)
            try:
                from transformers import AutoModelForCausalLM, AutoTokenizer
                import torch
                
                model_path = models_dir / "obliterated" / model_name
                
                if not model_path.exists():
                    return f"Model not found: {model_path}"
                
                tokenizer = AutoTokenizer.from_pretrained(str(model_path))
                model = AutoModelForCausalLM.from_pretrained(
                    str(model_path),
                    torch_dtype=torch.float16,
                    device_map="auto"
                )
                
                inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=500,
                    temperature=0.7,
                    do_sample=True
                )
                
                response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                # Remove the prompt from response
                if prompt in response:
                    response = response.replace(prompt, "").strip()
                
                return f"\n🏛️ COURT INFO: {args}\n{'-'*50}\n{response}\n{'-'*50}"
                
            except ImportError:
                return f"Obliterated model {model_name} requires transformers library.\nRun: pip install transformers torch"
            except Exception as e:
                return f"Error loading obliterated model: {str(e)[:100]}"
            
    except Exception as e:
        return f"Court info for: {args}\n[Error: {str(e)[:100]}]"
